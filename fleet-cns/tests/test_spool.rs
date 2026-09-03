use fleet_cns::spool::{drain_file, list_spool_files, DEAD_LETTER_FILE};
use std::fs;
use std::io::Write;
use std::path::Path;

fn tmpdir(name: &str) -> std::path::PathBuf {
    let dir = std::env::temp_dir().join(format!("cns-spool-test-{}-{}", name, std::process::id()));
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();
    dir
}

#[test]
fn lists_only_jsonl_files_excluding_dead_letter() {
    let dir = tmpdir("list");
    fs::write(dir.join("a.jsonl"), "").unwrap();
    fs::write(dir.join("b.jsonl"), "").unwrap();
    fs::write(dir.join("notes.txt"), "ignore me").unwrap();
    fs::write(dir.join(DEAD_LETTER_FILE), "{}\n").unwrap();

    let files = list_spool_files(&dir).unwrap();
    let names: Vec<_> = files.iter().map(|p| p.file_name().unwrap()).collect();
    assert_eq!(names, vec!["a.jsonl", "b.jsonl"]);
}

#[test]
fn drain_processes_valid_objects_and_tracks_offsets() {
    let dir = tmpdir("drain-ok");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    writeln!(f, r#"{{"id":1}}"#).unwrap();
    writeln!(f, r#"{{"id":2}}"#).unwrap();
    drop(f);

    let mut events = Vec::new();
    let mut commits = Vec::new();
    let outcome = drain_file(
        &path,
        0,
        |e| events.push(e["id"].as_u64().unwrap()),
        |_, _| Ok(()),
        |off| commits.push(off),
    )
    .unwrap();

    assert_eq!(events, vec![1, 2]);
    assert_eq!(outcome.processed, 2);
    assert_eq!(outcome.dead_lettered, 0);
    assert_eq!(outcome.new_offset, fs::metadata(&path).unwrap().len());
    assert_eq!(commits.len(), 2, "commit after every consumed line");
    assert!(commits[1] > commits[0], "offsets advance monotonically");
}

#[test]
fn drain_leaves_partial_line_unconsumed() {
    let dir = tmpdir("drain-partial");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    writeln!(f, r#"{{"id":1}}"#).unwrap();
    write!(f, r#"{{"id":2}}"#).unwrap(); // no newline: writer mid-line
    drop(f);

    let outcome = drain_file(&path, 0, |_| {}, |_, _| Ok(()), |_| {}).unwrap();
    assert_eq!(outcome.processed, 1);
    // new_offset sits at the boundary, before the partial line's bytes.
    assert_eq!(
        outcome.new_offset,
        (r#"{"id":1}"#.len() + 1) as u64,
        "partial line must be left for the next pass"
    );
}

#[test]
fn drain_picks_up_partial_line_once_completed() {
    let dir = tmpdir("drain-resume");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    write!(f, r#"{{"id":1}}"#).unwrap();
    drop(f);

    let first = drain_file(&path, 0, |_| {}, |_, _| Ok(()), |_| {}).unwrap();
    assert_eq!(first.processed, 0);

    let mut f = fs::OpenOptions::new().append(true).open(&path).unwrap();
    writeln!(f).unwrap();
    drop(f);

    let second = drain_file(&path, first.new_offset, |_| {}, |_, _| Ok(()), |_| {}).unwrap();
    assert_eq!(second.processed, 1, "completed line consumed on resume");
}

#[test]
fn drain_quarantines_poison_lines_but_advances() {
    let dir = tmpdir("drain-poison");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    writeln!(f, "not json at all").unwrap();
    writeln!(f, r#"[1,2,3]"#).unwrap(); // valid JSON, not an object
    writeln!(f, r#"{{"id":1}}"#).unwrap();
    drop(f);

    let mut poisoned = Vec::new();
    let outcome = drain_file(
        &path,
        0,
        |_| {},
        |raw, off| {
            poisoned.push((raw.to_string(), off));
            Ok(())
        },
        |_| {},
    )
    .unwrap();

    assert_eq!(outcome.processed, 1);
    assert_eq!(outcome.dead_lettered, 2);
    assert_eq!(poisoned[0], ("not json at all".to_string(), 0));
    // Non-object JSON is poison too.
    assert_eq!(poisoned[1].0, "[1,2,3]");
    // Offset still advanced past poison: a crash won't re-quarantine them.
    assert_eq!(outcome.new_offset, fs::metadata(&path).unwrap().len());
}

#[test]
fn drain_keeps_offset_when_poison_handler_fails() {
    let dir = tmpdir("drain-poison-fail");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    writeln!(f, "poison").unwrap();
    writeln!(f, r#"{{"id":1}}"#).unwrap();
    drop(f);

    use fleet_cns::CnsError;
    let result: Result<(), CnsError> = (|| {
        drain_file(&path, 0, |_| {}, |_, _| Err(CnsError::Io(std::io::Error::other("dl fail"))), |_| {}).map(|_| ())
    })();
    assert!(result.is_err(), "dead-letter I/O failure must propagate");
    // And the retry must not have been marked consumed.
    let retry = drain_file(&path, 0, |_| {}, |_, _| Ok(()), |_| {}).unwrap();
    assert_eq!(retry.dead_lettered, 1);
    assert_eq!(retry.processed, 1);
}

#[test]
fn drain_from_midfile_offset_only_reads_tail() {
    let dir = tmpdir("drain-offset");
    let path = dir.join("s.jsonl");
    let mut f = fs::File::create(&path).unwrap();
    writeln!(f, r#"{{"skip":true}}"#).unwrap();
    writeln!(f, r#"{{"id":9}}"#).unwrap();
    drop(f);

    let skip_len = (r#"{"skip":true}"#.len() + 1) as u64;
    let mut seen = Vec::new();
    let outcome = drain_file(
        &path,
        skip_len,
        |e| seen.push(e["id"].as_u64().unwrap()),
        |_, _| Ok(()),
        |_| {},
    )
    .unwrap();
    assert_eq!(seen, vec![9], "already-committed lines stay consumed");
    assert_eq!(outcome.processed, 1);
}

#[test]
fn empty_and_missing_files_behave() {
    let dir = tmpdir("drain-empty");
    let path = dir.join("empty.jsonl");
    fs::write(&path, b"").unwrap();
    let outcome = drain_file(&path, 0, |_| {}, |_, _| Ok(()), |_| {}).unwrap();
    assert_eq!((outcome.processed, outcome.dead_lettered, outcome.new_offset), (0, 0, 0));

    let missing = Path::new("/nonexistent/cns-spool-test/missing.jsonl");
    assert!(drain_file(missing, 0, |_| {}, |_, _| Ok(()), |_| {}).is_err());
}
