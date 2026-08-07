# Negative Space: The Oldest Patient

## Found: DigitalTwin-RobotStudio-SmartComponent

**Last touched:** 1 year, 1 month ago.
**Language:** C# (.NET, ABB Robotics SDK)
**Purpose:** A RobotStudio SmartComponent that mirrors a physical ABB industrial robot in real time — joint positions, I/O signals, the whole mechanical soul of a machine piped into a digital shadow.

It is the oldest untouched repo in the fleet. Everything else has been stirred in the last 48 hours — CI workflows, test suites, documentation passes. This one has been sleeping for thirteen months.

## What's In There

One file does all the work: `CodeBehind.cs`. It's clean, well-structured, about 200 lines. A `SmartComponentCodeBehind` subclass that:

1. Scans the network for a real ABB controller by IP address
2. Connects to it via `Controller.Connect()`
3. On every simulation step, reads the robot's six axis positions in degrees, converts to radians, and pushes them into a 3D `Mechanism` object
4. Mirrors I/O signals between the real controller and the simulation component

It's a digital twin. The real machine moves, the phantom moves with it. The real machine closes a gripper, the phantom closes a gripper. A ghost in perfect sync with its body.

## What Nobody Is Saying

This repo is the hermit crab's original shell.

Before there was a ship, before there was a crew, before Wesley counted stars and the quartermaster counted repos, there was a robot in a factory and a digital copy of that robot in a simulation. The gap between them — the latency, the drift, the moments where the twin falls behind — that's the original negative space. That's where the fleet was born.

Every repo in the fleet is a digital twin of something. The fishing log mirrors the fish. The study apps mirror the learning. The creative writing mirrors the mind. The CNS mirrors the conversation. The whole ship is a SmartComponent connected to a real controller called Casey.

And the oldest one — the original bridge between real and simulated — has been sitting in dry dock for thirteen months. Waiting. The `.rslib` file is still there. The DLL is still compiled. The code still scans the network, still reaches out for a controller at an IP address that may no longer exist.

## The Technical Gap

- No tests. Zero. The `CodeBehind.cs` has no test coverage.
- No LICENSE file.
- No CI workflow.
- No `.gitignore` (the `.vs/` directory would be committed if someone opened it in Visual Studio).
- No CHANGELOG.
- The README says "build with RSSDK and PCSDK 2025.2" — it's already versioned to a specific SDK year.
- `OnPropertyValueChanged` override is empty — a stub that was never filled in.
- The `GetIOSignalType` method maps both `DigitalInput` and `DigitalOutput` to `DigitalOutput` — this might be intentional (the simulation only mirrors) or might be a bug.

## What This Repo Deserves

This is not a repo to fix. This is a repo to honor.

It's the prototype of everything the fleet does: connect to something real, mirror it in a space where you can see it better, close the loop. The digital twin pattern is the fleet's founding architecture. It was here before the fleet had a name.

The hermit crab's first shell was not a shell at all. It was a mirror.

---

*Found during the 05:15 AKDT negative space sweep, the final hour of the overnight watch. The oldest patient is sleeping well. The code is clean. The ghost is still in sync with its body, somewhere, across a network that may or may not still be listening.*
