use crate::CnsError;
use serde::Serialize;
use std::fs::File;
use std::io::{BufRead, BufReader, Seek, SeekFrom, Write};
use std::path::{Path, PathBuf};

pub const DEAD_LETTER_FILE: &str = "dead-letter.jsonl";

/// A malformed line quarantined to `<spool_dir>/dead-letter.jsonl`.
#[derive(Debug, Serialize)]
pub struct DeadLetterRecord {
    pub spool_file: String,
    pub byte_offset: u64,
    pub timestamp: String,
    pub raw: String,
}

/// Per-file outcome of one drain pass.
#[derive(Debug, Default, Clone, Copy)]
pub struct FileOutcome {
    pub new_offset: u64,
    pub processed: u64,
    pub dead_lettered: u64,
}

/// List spool files in the directory: `*.jsonl`, regular files, sorted,
/// excluding the dead-letter file itself.
pub fn list_spool_files(spool_dir: &Path) -> Result<Vec<PathBuf>, CnsError> {
    let mut files = Vec::new();
    for entry in std::fs::read_dir(spool_dir)? {
        let entry = entry?;
        let path = entry.path();
        let is_jsonl = path.extension().and_then(|e| e.to_str()) == Some("jsonl");
        let is_dead_letter = path.file_name().and_then(|n| n.to_str()) == Some(DEAD_LETTER_FILE);
        let is_file = entry.file_type().map(|t| t.is_file()).unwrap_or(false);
        if is_jsonl && !is_dead_letter && is_file {
            files.push(path);
        }
    }
    files.sort();
    Ok(files)
}

/// Drain newline-terminated lines from `path` starting at `offset`.
///
/// Memory is O(line): a BufReader streams lines into a reused buffer; the
/// file is never slurped. A trailing partial line (no newline yet) is left
/// unconsumed so a later pass picks it up once the writer finishes it.
///
/// `on_event` receives valid JSON-object events; `on_poison` receives
/// (raw_line, byte_offset) for anything else and may fail (dead-letter I/O),
/// in which case the offset is NOT advanced past the bad line. `on_commit`
/// receives the new byte offset after every consumed line.
pub fn drain_file<F, G, H>(
    path: &Path,
    offset: u64,
    mut on_event: F,
    mut on_poison: G,
    mut on_commit: H,
) -> Result<FileOutcome, CnsError>
where
    F: FnMut(&serde_json::Value),
    G: FnMut(&str, u64) -> Result<(), CnsError>,
    H: FnMut(u64),
{
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    reader.seek(SeekFrom::Start(offset))?;

    let mut outcome = FileOutcome {
        new_offset: offset,
        ..FileOutcome::default()
    };
    let mut line = String::new();
    loop {
        line.clear();
        let n = reader.read_line(&mut line)?;
        if n == 0 {
            break; // EOF
        }
        if !line.ends_with('\n') {
            break; // partial line still being written; leave offset in place
        }
        let line_start = outcome.new_offset;
        let raw = line.trim_end_matches(['\n', '\r']);
        match serde_json::from_str::<serde_json::Value>(raw) {
            Ok(value) if value.is_object() => {
                on_event(&value);
                outcome.processed += 1;
            }
            // Valid JSON that isn't an object, or malformed JSON: poison.
            _ => {
                on_poison(raw, line_start)?;
                outcome.dead_lettered += 1;
            }
        }
        outcome.new_offset += n as u64;
        on_commit(outcome.new_offset);
    }
    Ok(outcome)
}

/// Append one dead-letter record to an already-open handle.
pub fn write_dead_letter(
    handle: &mut File,
    spool_file: &str,
    byte_offset: u64,
    raw: &str,
) -> Result<(), CnsError> {
    let record = DeadLetterRecord {
        spool_file: spool_file.to_string(),
        byte_offset,
        timestamp: chrono::Utc::now().to_rfc3339(),
        raw: raw.to_string(),
    };
    let line = serde_json::to_string(&record)?;
    writeln!(handle, "{}", line)?;
    Ok(())
}
