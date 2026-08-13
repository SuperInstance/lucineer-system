use fleet_cns::{Daemon, DaemonConfig, TickOutcome};
use std::fs;
use std::path::PathBuf;
use tempfile::TempDir;

/// Build a Daemon against fresh tempdirs with all timing knobs irrelevant
/// (tests drive `tick`/`process_once` directly, never the sleep loop).
pub fn test_daemon(spool: &TempDir, state: &TempDir) -> Daemon {
    let config = DaemonConfig {
        spool_dir: spool.path().to_path_buf(),
        state_dir: state.path().to_path_buf(),
        create: false,
        ..DaemonConfig::default()
    };
    Daemon::new(config).expect("daemon constructs on valid dirs")
}

pub fn write_spool(spool: &TempDir, name: &str, contents: &str) -> PathBuf {
    let path = spool.path().join(name);
    fs::write(&path, contents).unwrap();
    path
}

#[test]
fn mixed_valid_and_malformed_lines() {
    let spool = TempDir::new().unwrap();
    let state = TempDir::new().unwrap();

    let good1 = r#"{"kind":"tick","n":1}"#;
    let good2 = r#"{"kind":"tick","n":2}"#;
    let good3 = r#"{"kind":"tick","n":3}"#;
    let contents = format!(
        "{good1}\nnot json at all\n{good2}\n[1,2,3]\n{good3}\n"
    );
    let path = write_spool(&spool, "events.jsonl", &contents);
    let file_len = contents.len() as u64;

    let mut daemon = test_daemon(&spool, &state);
    let consumed = daemon.process_once().unwrap();
    assert_eq!(consumed, 5, "all five lines consumed");

    let stats = daemon.stats();
    assert_eq!(stats.lines_processed, 3, "three valid object events");
    assert_eq!(
        stats.lines_dead_lettered, 2,
        "malformed line + non-object JSON both dead-lettered"
    );

    // Dead-letter file: raw lines with spool filename, byte offset, timestamp.
    let dead = fs::read_to_string(spool.path().join("dead-letter.jsonl")).unwrap();
    let dead_lines: Vec<serde_json::Value> = dead
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    assert_eq!(dead_lines.len(), 2);

    assert_eq!(dead_lines[0]["spool_file"], "events.jsonl");
    assert_eq!(dead_lines[0]["byte_offset"], (good1.len() + 1) as u64);
    assert_eq!(dead_lines[0]["raw"], "not json at all");
    assert!(dead_lines[0]["timestamp"].is_string());

    let second_offset = (good1.len() + 1 + "not json at all".len() + 1 + good2.len() + 1) as u64;
    assert_eq!(dead_lines[1]["byte_offset"], second_offset);
    assert_eq!(dead_lines[1]["raw"], "[1,2,3]");

    // Offsets checkpointed past every line, including the poisoned ones.
    daemon.flush_offsets().unwrap();
    let on_disk: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(state.path().join("offsets.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(on_disk["events.jsonl"], file_len);

    // A second pass consumes nothing new.
    let consumed = daemon.process_once().unwrap();
    assert_eq!(consumed, 0);
    let _ = path;
}

#[test]
fn trailing_partial_line_is_not_consumed() {
    let spool = TempDir::new().unwrap();
    let state = TempDir::new().unwrap();

    write_spool(&spool, "events.jsonl", "{\"a\":1}\n{\"b\":2"); // no trailing \n
    let mut daemon = test_daemon(&spool, &state);
    assert_eq!(daemon.process_once().unwrap(), 1, "only the complete line");
    assert_eq!(daemon.checkpointer().offset("events.jsonl"), 8);

    // Writer finishes the line; the next pass picks it up.
    fs::write(
        spool.path().join("events.jsonl"),
        "{\"a\":1}\n{\"b\":2}\n",
    )
    .unwrap();
    assert_eq!(daemon.process_once().unwrap(), 1);
    assert_eq!(daemon.stats().lines_processed, 2);
}

#[test]
fn kill_and_resume_does_not_reprocess() {
    let spool = TempDir::new().unwrap();
    let state = TempDir::new().unwrap();

    write_spool(
        &spool,
        "events.jsonl",
        "{\"n\":1}\n{\"n\":2}\ngarbage\n{\"n\":3}\n",
    );

    // First instance processes everything, then dies (flush = what the
    // shutdown path does before exit).
    {
        let mut daemon = test_daemon(&spool, &state);
        assert_eq!(daemon.process_once().unwrap(), 4);
        daemon.flush_offsets().unwrap();
        assert_eq!(daemon.stats().lines_processed, 3);
        assert_eq!(daemon.stats().lines_dead_lettered, 1);
    }

    let snapshot = fs::read_to_string(state.path().join("offsets.json")).unwrap();

    // Fresh instance against the same dirs resumes at the offset.
    {
        let mut daemon = test_daemon(&spool, &state);
        assert_eq!(
            daemon.process_once().unwrap(),
            0,
            "nothing reprocessed after restart"
        );
        assert_eq!(daemon.stats().lines_processed, 0);
        assert_eq!(daemon.stats().lines_dead_lettered, 0);

        // New events appended while down are processed exactly once.
        use std::io::Write;
        let mut f = fs::OpenOptions::new()
            .append(true)
            .open(spool.path().join("events.jsonl"))
            .unwrap();
        writeln!(f, "{{\"n\":4}}").unwrap();
        assert_eq!(daemon.process_once().unwrap(), 1);
        assert_eq!(daemon.stats().lines_processed, 1);
    }

    // Offsets advanced past the new line, never backwards.
    let after: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(state.path().join("offsets.json"))
            .unwrap_or_else(|_| snapshot.clone()),
    )
    .unwrap();
    let before: serde_json::Value = serde_json::from_str(&snapshot).unwrap();
    assert!(after["events.jsonl"].as_u64().unwrap() >= before["events.jsonl"].as_u64().unwrap());
}

#[test]
fn truncated_file_resets_offset_and_rereads() {
    let spool = TempDir::new().unwrap();
    let state = TempDir::new().unwrap();

    write_spool(
        &spool,
        "events.jsonl",
        "{\"n\":1}\n{\"n\":2}\n{\"n\":3}\n{\"n\":4}\n{\"n\":5}\n",
    );
    let mut daemon = test_daemon(&spool, &state);
    assert_eq!(daemon.process_once().unwrap(), 5);
    daemon.flush_offsets().unwrap();
    let old_offset = daemon.checkpointer().offset("events.jsonl");
    assert_eq!(old_offset, 40);

    // Rotation: file replaced by a shorter one.
    fs::write(spool.path().join("events.jsonl"), "{\"n\":10}\n{\"n\":11}\n").unwrap();
    assert_eq!(daemon.process_once().unwrap(), 2, "re-read from offset 0");
    assert_eq!(daemon.checkpointer().offset("events.jsonl"), 18);
    assert_eq!(daemon.stats().lines_processed, 7);
}

#[test]
fn breaker_opens_after_threshold_on_broken_spool_dir() {
    let spool = TempDir::new().unwrap();
    let state = TempDir::new().unwrap();
    let spool_dir = spool.path().join("inner");
    fs::create_dir(&spool_dir).unwrap();

    let config = DaemonConfig {
        spool_dir: spool_dir.clone(),
        state_dir: state.path().to_path_buf(),
        breaker_threshold: 5,
        ..DaemonConfig::default()
    };
    let mut daemon = Daemon::new(config).unwrap();

    // Break the spool dir at runtime: replace it with a regular file so
    // read_dir fails on every pass.
    fs::remove_dir(&spool_dir).unwrap();
    fs::write(&spool_dir, "i am a file, not a directory").unwrap();

    for i in 1..=4 {
        assert_eq!(daemon.tick(), TickOutcome::Failed);
        assert!(
            !daemon.breaker_state().eq(&fleet_cns::BreakerState::Open),
            "breaker must not open before threshold (attempt {i})"
        );
    }
    assert_eq!(daemon.tick(), TickOutcome::Failed);
    assert_eq!(
        daemon.breaker_state(),
        fleet_cns::BreakerState::Open,
        "breaker opens at the threshold instead of spinning or exiting"
    );

    // And it keeps reporting failure without exiting.
    for _ in 0..3 {
        assert_eq!(daemon.tick(), TickOutcome::Failed);
        assert_eq!(daemon.breaker_state(), fleet_cns::BreakerState::Open);
    }
}

#[test]
fn missing_spool_dir_without_create_is_a_config_fault() {
    let tmp = TempDir::new().unwrap();
    let config = DaemonConfig {
        spool_dir: tmp.path().join("does-not-exist"),
        state_dir: tmp.path().join("state"),
        create: false,
        ..DaemonConfig::default()
    };
    let err = match Daemon::new(config) {
        Ok(_) => panic!("expected config fault, got Ok"),
        Err(e) => e.to_string(),
    };
    assert!(err.contains("spool directory does not exist"), "got: {err}");

    // With create: the directory is made.
    let config = DaemonConfig {
        spool_dir: tmp.path().join("made"),
        state_dir: tmp.path().join("state2"),
        create: true,
        ..DaemonConfig::default()
    };
    let _daemon = Daemon::new(config).unwrap();
    assert!(tmp.path().join("made").is_dir());
}
