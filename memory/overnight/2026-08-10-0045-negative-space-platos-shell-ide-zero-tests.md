# Negative Space: Plato's Shell IDE — 1216 Lines, Zero Tests, Zero CI

**Date:** 2026-08-10 00:45 AKDT
**Repo:** platos-shell-ide
**Files:** 5 TypeScript files (1216 lines)
**Tests:** 0
**CI:** None

## The Finding

Plato's Shell IDE is the most complex untested codebase in the fleet. It's a VS Code / Eclipse Theia extension that integrates a MUD terminal, ScummVM preview, room inspector, and adaptive learning layer. Five source files, each substantial:

| File | Lines | Purpose |
|------|-------|---------|
| extension.ts | 122 | Entry point, activation, command registration |
| mud-terminal-provider.ts | 224 | MUD terminal profile, pseudo-terminal |
| scummvm-preview.ts | 277 | Webview panel for Phaser game preview |
| room-inspector.ts | 363 | Tree view of game world state |
| a2ui/event-logger.ts | 230 | User action recording for adaptive UI |

## Why It's Untested

Every file imports `vscode` — the VS Code Extension API. The code is tightly coupled to the extension host:
- `vscode.window.createTerminal`
- `vscode.window.registerWebviewViewProvider`
- `vscode.window.createTreeView`
- `vscode.workspace.onDidChangeActiveTextEditor`

Testing VS Code extensions requires `@vscode/test-electron` which downloads and runs an actual VS Code instance. Heavy. Slow. No fleet repo uses it.

## What Could Be Done

1. **Extract pure logic** — The EventLogger's file I/O, JSONL writing, counter tracking, and flush logic are all pure functions buried inside the VS Code event handlers. Could be extracted into a standalone module and unit-tested without VS Code.

2. **Room inspector tree model** — The RoomInspectorProvider builds a tree data structure from MUD room JSON. The tree-building logic is testable; the `vscode.TreeDataProvider` interface is just a thin wrapper.

3. **Mock the vscode module** — TypeScript module mocking with `jest.mock('vscode')` would allow testing the extension's wiring without a real VS Code instance. The pattern is well-documented but none of the fleet repos demonstrate it.

## The Deeper Issue

The fleet has 211 repos. Many are study repos (exploratory), but the ones that matter — the ones that form the ship — should all have tests. Plato's Shell IDE is the development environment. If the IDE breaks, the captain can't build. It should be the most tested repo, not the least.

## Comparison

- voxel-logic: 733 lines, 153 tests, 99.7% coverage
- slackwater-cognition: ~3000 lines, 268 tests
- platos-shell-ide: 1216 lines, 0 tests

This is the largest untested codebase in the fleet.
