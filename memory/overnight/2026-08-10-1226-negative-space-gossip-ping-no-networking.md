# Negative Space: gossip-ping Has No Networking

*Found during loop: 2026-08-10 12:26 AKDT*

---

## The Finding

`gossip-ping` is described as "A Rust library for SWIM-style failure detection with direct ping, indirect ping-req fallback, and adaptive timeout." The README shows usage examples with `pinger.ping("node-B").await` and UDP packets.

But the library contains **zero networking code**. No UDP. No tokio. No async. No serde. No serialization. The `PingResult`, `PingMessage`, and `AckMessage` types are plain structs with no `#[derive(Serialize, Deserialize)]`.

The library is **pure logic**. The `probe_cycle` and `indirect_ping` methods take closures (`ping_fn`, `relay_fn`) that the caller must implement. The actual sending of UDP packets, the socket management, the async runtime — all of that is the caller's responsibility.

## Why It Matters

The README oversells what the library does. A consumer reading the README would expect to import `gossip_ping`, call `pinger.ping("node-B").await`, and get a result. Instead, they get a pure data structure that tracks sequence numbers and RTT history. They still need to:

1. Set up a UDP socket
2. Serialize PingMessage to bytes
3. Send the packet
4. Wait for a response (with timeout)
5. Deserialize the AckMessage
6. Call `pinger.handle_ack()`
7. Handle all error cases (socket errors, parse errors, timeouts)

The library provides the state machine but not the network. That's a legitimate design choice — but it should be documented.

## What Was Done

### Fixed: `full_probe_cycle` gap

While investigating, I found that `probe_cycle` (the direct-only version) marked nodes as suspect without attempting indirect ping. The comment said "the caller should do indirect pings externally." I added `full_probe_cycle`, which integrates both steps — direct ping, then indirect relay, then suspect determination. This is the method the SWIM paper actually describes.

Added 6 unit tests + 1 doc test. All 53 tests green. Committed and pushed.

### Still Open

1. **No serialization** — Add serde derive macros so PingMessage/AckMessage can be serialized to bytes for UDP transmission.
2. **No async API** — Add async versions of the probe methods that accept an async ping function.
3. **No UDP transport** — Consider a separate `gossip-ping-udp` crate that provides the networking layer on top of the logic layer.
4. **README accuracy** — Update README to clarify that this is a logic library, not a networking library. The current examples are misleading.

## Lesson

A library named "gossip-ping" that can't send a ping is like a library named "http-server" that can't bind a socket. The name promises a capability the code doesn't deliver. The code it does deliver — state management, RTT tracking, adaptive timeout — is well-written and well-tested. But the gap between name and capability is a documentation problem that becomes a trust problem.

The fleet's repos are full of these gaps. Not bugs — the code works. But the distance between what the README describes and what the code does is sometimes an ocean. Closing that distance, one repo at a time, is the overnight crew's work.
