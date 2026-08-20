use fleet_cns::Checkpointer;
use std::fs;
use std::time::Duration;
use tempfile::TempDir;

fn load(state: &TempDir, flush_every: u32, flush_interval: Duration) -> Checkpointer {
    Checkpointer::load(state.path(), flush_every, flush_interval).unwrap()
}

fn read_offsets(state: &TempDir) -> String {
    fs::read_to_string(state.path().join("offsets.json")).unwrap()
}

#[test]
fn flush_every_batch_threshold_triggers_write() {
    let state = TempDir::new().unwrap();
    // Huge interval so only the line-count threshold can fire.
    let mut cp = load(&state, 3, Duration::from_secs(3600));

    cp.advance("a.jsonl", 10);
    cp.advance("a.jsonl", 20);
    cp.maybe_flush().unwrap();
    assert!(
        !state.path().join("offsets.json").exists(),
        "below threshold: no write yet"
    );

    cp.advance("a.jsonl", 30);
    cp.maybe_flush().unwrap();
    assert!(state.path().join("offsets.json").exists());
    assert_eq!(cp.offset("a.jsonl"), 30);
}

#[test]
fn flush_interval_elapsed_triggers_write() {
    let state = TempDir::new().unwrap();
    // Huge line threshold, zero interval: time alone must fire the flush.
    let mut cp = load(&state, u32::MAX, Duration::ZERO);
    cp.advance("b.jsonl", 5);
    cp.maybe_flush().unwrap();
    assert!(state.path().join("offsets.json").exists());
    let on_disk: serde_json::Value = serde_json::from_str(&read_offsets(&state)).unwrap();
    assert_eq!(on_disk["b.jsonl"], 5);
}

#[test]
fn clean_state_never_writes() {
    let state = TempDir::new().unwrap();
    let mut cp = load(&state, 1, Duration::ZERO);
    cp.maybe_flush().unwrap();
    assert!(!state.path().join("offsets.json").exists());
}

#[test]
fn roundtrip_across_instances() {
    let state = TempDir::new().unwrap();
    {
        let mut cp = load(&state, 1, Duration::from_secs(3600));
        cp.advance("one", 100);
        cp.advance("two", 250);
        cp.flush().unwrap();
    }
    {
        let cp = load(&state, 1, Duration::from_secs(3600));
        assert_eq!(cp.offset("one"), 100);
        assert_eq!(cp.offset("two"), 250);
        assert_eq!(cp.offset("never-seen"), 0, "missing files start at 0");
    }
}

#[test]
fn corrupt_offsets_json_starts_from_zero() {
    let state = TempDir::new().unwrap();
    fs::write(state.path().join("offsets.json"), "{not json").unwrap();
    let cp = load(&state, 1, Duration::from_secs(3600));
    assert!(cp.offsets().is_empty(), "corrupt state is discarded, not fatal");
}

#[test]
fn reset_marks_dirty_and_flushes_to_zero() {
    let state = TempDir::new().unwrap();
    let mut cp = load(&state, 1, Duration::from_secs(3600));
    cp.advance("rotated", 999);
    cp.flush().unwrap();

    cp.reset("rotated");
    cp.flush().unwrap();
    let on_disk: serde_json::Value = serde_json::from_str(&read_offsets(&state)).unwrap();
    assert_eq!(on_disk["rotated"], 0);
}

#[test]
fn atomic_write_leaves_no_temp_file() {
    let state = TempDir::new().unwrap();
    let mut cp = load(&state, 1, Duration::from_secs(3600));
    cp.advance("x", 1);
    cp.flush().unwrap();
    let entries: Vec<_> = fs::read_dir(state.path()).unwrap().collect();
    assert_eq!(
        entries.len(),
        1,
        "only offsets.json survives the tmp+rename, got {entries:?}"
    );
}
