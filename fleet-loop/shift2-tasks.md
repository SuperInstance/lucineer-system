## Subagent Task 1: Dialogue System with TALK TO Routing Through The Tap API

### 1. Task Name
Implement the Tap API, a dialogue tree runner, and a Phaser UI for NPC conversations, then route the `TALK TO` verb through the Tap API.

### 2. Exact Files to Create / Modify

**Create**
- `src/tap/TapAPI.ts`
- `src/tap/installTapAPI.ts`
- `src/dialogue/types.ts`
- `src/dialogue/DialogueSystem.ts`
- `src/dialogue/dialogues.ts`
- `src/dialogue/DialogueUI.ts`

**Modify**
- `src/systems/VerbEngine.ts`
- `src/main.ts`

### 3. Detailed Implementation Spec

#### 3.1 `src/tap/TapAPI.ts`
Create a central verb-dispatch event router named "The Tap API". This becomes the single choke point for all player-triggered verbs.

```ts
export type TapVerb =
  | 'LOOK'
  | 'TALK TO'
  | 'USE'
  | 'OPEN'
  | 'TAKE'
  | 'GO'
  | 'GIVE'
  | 'PUSH'
  | 'PULL'
  | 'CUSTOM';

export interface TapContext {
  scene: Phaser.Scene;
  targetId: string;
  target: any; // hotspot / NPC / item object from the current room
  roomId: string;
  store: SharedWorldStore;
  verb: string;
}

export interface TapHandlerResult {
  handled: boolean;
  blockVerbBar?: boolean;
}

export type TapHandler = (ctx: TapContext) => TapHandlerResult | Promise<TapHandlerResult>;

export class TapAPI {
  private handlers = new Map<TapVerb, TapHandler[]>();

  static getInstance(): TapAPI;

  register(verb: TapVerb, handler: TapHandler): void;

  unregister(verb: TapVerb, handler: TapHandler): void;

  dispatch(verb: string, ctx: TapContext): Promise<TapHandlerResult>;
}
```

Dispatch rules:
- Normalize verb input to uppercase.
- Try handlers in registration order.
- Stop at the first handler returning `{ handled: true }`.
- If all handlers return `handled: false`, return `{ handled: false }` so the existing `VerbEngine` fallback behavior can run.

#### 3.2 `src/dialogue/types.ts`
Define the dialogue tree data model:

```ts
export interface DialogueChoice {
  text: string;
  next: string;
  condition?: (store: SharedWorldStore) => boolean;
}

export interface DialogueNode {
  id: string;
  speaker: string;
  text: string;
  next?: string;
  choices?: DialogueChoice[];
  setFlags?: string[];
  pushEvent?: string; // optional MUD/terminal event message
}

export interface DialogueTree {
  id: string;
  startNode: string;
  nodes: Record<string, DialogueNode>;
  requiresFlag?: string;
}

export interface DialogueUIHandle {
  show(data: { speaker: string; text: string; choices?: string[] }): void;
  hide(): void;
  isVisible(): boolean;
}
```

#### 3.3 `src/dialogue/dialogues.ts`
Create at least two NPC dialogue trees:

1. `voss_greeting`
   - Bartender Voss in Bar-Rail.
   - First node welcomes the player.
   - Two choices: `Ask about the voyage` and `Ask about rumors`.
   - Both branches set flags:
     - `talked_about_voyage`
     - `talked_about_rumors`
   - A third choice `Leave` ends the dialogue.

2. `sable_route_greeting`
   - Navigator Sable in the navigation room.
   - `requiresFlag: 'talked_about_voyage'` gates the deeper branch.
   - If the flag is missing, only a short ambient conversation is available.
   - If the flag exists, a new choice `Ask about the safe route` opens.
   - That branch sets `got_safe_route_hint`.

Each dialogue node must support:
- Setting flags when entered.
- Pushing an optional event string via `pushEvent` so the MUD terminal can later display it.

#### 3.4 `src/dialogue/DialogueSystem.ts`
Implement the runtime:

- Constructor:
  ```ts
  constructor(api: TapAPI, store: SharedWorldStore, ui: DialogueUIHandle)
  ```
- Register a `TALK TO` handler on `api`.
- On `TALK TO`:
  - If a dialogue is already active, return `{ handled: true }`.
  - Determine dialogue ID from `ctx.target.dialogueId` OR `ctx.target.npcId`.
  - If no dialogue ID exists, return `{ handled: false }`.
  - Load tree from `dialogues.ts`.
  - If `tree.requiresFlag` is set and the flag is falsy in `store`, return `{ handled: true }`, and show a one-line "They seem unwilling to talk right now." via `ui`.
  - Otherwise start the tree.
- `advance(choiceIndex?: number)`:
  - Read current node.
  - If choices are present, pick `currentNode.choices[choiceIndex]`.
  - If condition exists, evaluate against `store`.
  - Move to `next` node or selected choice's `next`.
  - Apply `setFlags` to store.
  - If a `pushEvent` exists, call `store.pushEvent('dialogue', message)`.
  - If there is no next node, call `end()`.
- `end()`:
  - Hide UI.
  - Clear active tree/node.
  - Re-enable the verb bar immediately.

#### 3.5 `src/dialogue/DialogueUI.ts`
Create a Phaser UI overlay:

- Full-screen semi-transparent `Rectangle` with a centered dialogue panel.
- Speaker name text, dialogue body text, and optional choice buttons.
- If no choices are present, clicking/tapping anywhere advances the dialogue.
- If choices are present, only clicking a choice advances.
- UI is hidden initially.
- Use a simple typewriter effect if feasible; otherwise show full text instantly.
- Expose `show`, `hide`, `isVisible`.

#### 3.6 `src/tap/installTapAPI.ts`
Create a bootstrap installer:

```ts
export function installTapAPI(scene: Phaser.Scene, store: SharedWorldStore): TapAPI
```

- Get `TapAPI.getInstance()`.
- Instantiate `DialogueUI`.
- Instantiate `DialogueSystem` with the UI.
- Return the API instance.

This file prevents `main.ts` from becoming lumbered with system wiring.

#### 3.7 `src/systems/VerbEngine.ts` (Modify)

- Before executing a verb's default behavior, call:
  ```ts
  const tapResult = await TapAPI.getInstance().dispatch(verb, { ...context });
  if (tapResult.handled) return tapResult;
  ```
- Keep the existing fallback behavior for unhandled verbs, e.g., `LOOK` at a generic hotspot.

#### 3.8 `src/main.ts` (Modify)

- After the Phaser game is created and the shared store is available, call:
  ```ts
  installTapAPI(scene, store);
  ```
- This is the only line this task adds here.

### 4. Acceptance Criteria

- `npm run build` passes with TypeScript strict mode.
- `TALK TO` on Voss opens the dialogue UI with his name and welcome text.
- Clicking/tapping through a no-choice dialogue node advances the text without consuming extra clicks.
- Choosing `Ask about rumors` sets `store.flags.talked_about_rumors` to `true`.
- Starting a dialogue blocks the verb bar; ending it unblocks the verb bar.
- `TALK TO` on an NPC without a dialogue tree falls through to the existing default verb output.
- Navigating to Sable's tree respects `requiresFlag`; her special branch is invisible before `talked_about_voyage` and visible after.
- Dialogue lines that set `pushEvent` appear in `store.pastEvents`.

### 5. Dependencies

- Step 2: `VerbEngine` and `SharedWorldStore` must already exist.
- Step 4/5: Room hotspots and verb bar UI must be in place.
- No dependency on audio or MUD terminal for this task, but the `pushEvent` integration is written so later tasks can consume it.

---

## Subagent Task 2: Audio Backend with Room Ambients, Jukebox, and Crossfade

### 1. Task Name
Implement a centralized Phaser + SharedWorldStore audio backend supporting seamless room ambient crossfades and a jukebox interaction system.

### 2. Exact Files to Create / Modify

**Create**
- `src/audio/AudioManager.ts`
- `src/audio/audioConfig.ts`
- `src/audio/JukeboxController.ts`
- `src/audio/installAudio.ts`
- `public/audio/ambients/bar_rail.ogg`
- `public/audio/ambients/galley.ogg`
- `public/audio/ambients/captains_quarters.ogg`
- `public/audio/ambients/cargo_hold.ogg`
- `public/audio/ambients/engine_room.ogg`
- `public/audio/ambients/crew_quarters.ogg`
- `public/audio/ambients/infirmary.ogg`
- `public/audio/jukebox/ballad_of_the_derelict.ogg`
- `public/audio/jukebox/portside_rum.ogg`

**Modify**
- `src/store/SharedWorldStore.ts`
- `src/main.ts`

Placeholder audio files are acceptable for the first pass. Generate 4–8 second seamless loops (sine wave, noise floor, or subtle tone variations) if no authored assets exist yet.

### 3. Detailed Implementation Spec

#### 3.1 `src/store/SharedWorldStore.ts` (Modify)

Add a light reactive subscription API if it does not already exist:

```ts
type StoreListener = (store: Readonly<SharedWorldStore>) => void;

subscribe(listener: StoreListener): () => void;
```

Also ensure the following are present:
- `store.currentRoomId: string`
- `store.setCurrentRoomId(roomId: string): void`
- `store.flags: Record<string, boolean>`
- `store.pastEvents: string[]`

Every mutation method must call all subscribed listeners after mutating state.

If `currentRoomId` already exists, do not duplicate it.

#### 3.2 `src/audio/audioConfig.ts`

```ts
export const ROOM_AMBIENT_KEYS: Record<string, string> = {
  bar_rail: 'amb_bar_rail',
  galley: 'amb_galley',
  captains_quarters: 'amb_captains_quarters',
  cargo_hold: 'amb_cargo_hold',
  engine_room: 'amb_engine_room',
  crew_quarters: 'amb_crew_quarters',
  infirmary: 'amb_infirmary',
};

export const AMBIENT_LOOP = true;
export const AMBIENT_VOLUME = 0.5;
export const FADE_SECONDS = 2.0;

export const JUKEBOX_TRACKS = [
  { key: 'jukebox_ballad', file: 'portside_rum.ogg', title: 'Portside Rum' },
  { key: 'jukebox_derelict', file: 'ballad_of_the_derelict.ogg', title: 'Ballad of the Derelict' },
];
```

#### 3.3 `src/audio/AudioManager.ts`

Create a class:

```ts
export class AudioManager {
  constructor(scene: Phaser.Scene, store: SharedWorldStore);
}
```

Responsibilities:

- Subscribe to `store` changes.
- When `store.currentRoomId` changes, call `crossfadeToAmbient(newRoomId)`.
- Load all ambient and jukebox audio keys once with `scene.load.audio`.
- Keep a reference to the active ambient sound and active jukebox sound.
- Maintain a list of active tweens so stale tweens can be cancelled on new transitions.

Crossfade behavior:

- If the new ambient key is the same as `currentAmbientKey`, no-op.
- If no ambient is playing, start the new ambient at volume `0`, tween up to `AMBIENT_VOLUME`.
- If an ambient is playing, start the new ambient at volume `0`, tween it up, and tween the old ambient down to `0`, then stop the old sound.
- All tweens use duration `FADE_SECONDS * 1000` milliseconds and `Phaser.Math.Easing.Linear` or `Sine.InOut`.

Jukebox methods:

- `playJukeboxTrack(index: number)`
- `stopJukebox()`
- `toggleJukebox()`

When a jukebox track starts, crossfade between the old track and the new one using the same volume tween pattern. While a jukebox is playing, keep ambients playing but lower their volume to `0.2`.

Mute/volume methods:

- `setMuted(muted: boolean)`
- `setMasterVolume(value: number)`

Debug methods:

- `getCurrentAmbientKey(): string | null`
- `getCurrentJukeboxKey(): string | null`

#### 3.4 `src/audio/JukeboxController.ts`

Register a `USE` handler with the Tap API:

```ts
api.register('USE', (ctx) => this.handleUse(ctx));
```

If `ctx.target.type === 'jukebox'`:
- If no jukebox track is playing, play first track.
- If a track is already playing, cycle to the next track.
- If the target has `data.jukeboxTrackIndex`, play that index.
- Return `{ handled: true }`.

If target is not a jukebox, return `{ handled: false }`.

After any jukebox interaction, push an event to the store:

```ts
store.pushEvent('audio', `The jukebox plays "${title}".`);
```

#### 3.5 `src/audio/installAudio.ts`

```ts
export function installAudio(scene: Phaser.Scene, store: SharedWorldStore): AudioManager
```

- Create `AudioManager`.
- Create `JukeboxController`.
- Wire both to the store.
- Return the `AudioManager`.

#### 3.6 `src/main.ts` (Modify)

After the game is initialized:

```ts
installAudio(scene, store);
```

Do not add audio-specific UI here; that belongs to later tasks.

### 4. Acceptance Criteria

- Walking from `bar_rail` to `galley` triggers a crossfade: Bar-Rail ambient fades out and stops, Galley ambient fades in.
- Calling `store.setCurrentRoomId('galley')` from the browser console triggers the same crossfade without requiring a scene transition.
- `USE` on a jukebox starts a jukebox track.
- Using the jukebox again cycles tracks with a crossfade.
- If the same room is entered twice, the ambient does not restart.
- If a stale fade is in progress when a new fade starts, old tweens are cancelled and no two ambients are left playing.
- `setMuted(true)` silences ambients and jukebox immediately.
- `setMasterVolume(0)` silences everything.
- No WebAudio autoplay errors appear: audio starts only after a user gesture (click, tap, or keyboard input).

### 5. Dependencies

- Task 1: `TapAPI` and its registration model.
- `SharedWorldStore.subscribe` addition made in this task is also required by Task 3.
- This task should land before Task 3 because Task 3 relies on `subscribe` and `pastEvents`.

---

## Subagent Task 3: Dual-Projection Sync, MUD Terminal Rendering, and Perception Deadband

### 1. Task Name
Implement the dual-projection bridge that keeps `SharedWorldStore`, Phaser room scenes, and the MUD terminal in sync, with a perception deadband to throttle redundant updates.

### 2. Exact Files to Create / Modify

**Create**
- `src/projection/perceptionDeadband.ts`
- `src/projection/MudFormatter.ts`
- `src/projection/ProjectionBridge.ts`
- `src/ui/MudTerminal.ts`
- `src/projection/installProjection.ts`

**Modify**
- `src/store/SharedWorldStore.ts`
- `src/main.ts`

### 3. Detailed Implementation Spec

#### 3.1 `src/store/SharedWorldStore.ts` (Modify)

Task 2 may have added `subscribe`. This task extends the store with:

```ts
pastEvents: string[];

pushEvent(type: string, message: string): void;
setObjectState(roomId: string, objectId: string, patch: Record<string, unknown>): void;
```

`pushEvent` behavior:
- Appends a formatted line to `pastEvents`.
- Caps `pastEvents` at 80 entries, dropping the oldest.
- Notifies all subscribers.

`setObjectState` behavior:
- Copies and merges `patch` into `store.roomObjects[roomId][objectId]`.
- Notifies all subscribers.

If `roomObjects` does not already exist, initialize it as:

```ts
roomObjects: Record<string, Record<string, any>>;
```

#### 3.2 `src/projection/perceptionDeadband.ts`

Create a helper:

```ts
export interface DeadbandOptions<T> {
  minDistance?: number;
  maxDelayMs?: number;
}

export function createDeadband<T>(
  applyFn: (latest: T, previous: T | null) => void,
  options: DeadbandOptions<T>
): (candidate: T) => void;
```

Rules:
- If no previous value exists, apply immediately.
- If `candidate` differs from `previous` by at least `minDistance`, apply.
- If `maxDelayMs` elapses since the last apply, always apply even if the change is tiny.
- Use `performance.now()` internally.

For room IDs, flags, and object structural changes, treat any difference as greater than deadband.
For numeric position values, use `minDistance = 0.5` pixels.
For repeated identical room changes, suppress projection completely.

#### 3.3 `src/projection/MudFormatter.ts`

Convert store state into MUD-style text.

```ts
formatRoom(store: SharedWorldStore): string;
formatObjectDelta(objectId: string, oldState: any, newState: any): string;
formatEvent(event: string): string;
```

Example room output:

```
The Bar-Rail Tavern
A low-ceilinged room smelling of salt and cheap rum.
Obvious exits: Galley, Officers' Mess
You see: Bartender Voss, Jukebox, Ship's Dice
```

Use room description text from existing room data when available. If a room has no description in the shared store, use a sensible default string from the room ID.

#### 3.4 `src/ui/MudTerminal.ts`

Create a Phaser UI container anchored to the right side of the screen.

- Width: `320px` on desktop; collapses to `220px` on mobile.
- Height: full viewport height.
- Background: dark panel with semi-transparent black fill.
- Text: monospace font, 12–14px.
- The terminal keeps a ring buffer of the last `50` lines.
- If more than 50 lines are pushed, drop the oldest silently.
- Provide `print(line: string): void`, `clear(): void`, and `toggle(): void`.
- Toggle binding: keyboard key `M`.
- When closed, the terminal is completely hidden and does not capture pointer events.

#### 3.5 `src/projection/ProjectionBridge.ts`

```ts
export class ProjectionBridge {
  constructor(scene: Phaser.Scene, store: SharedWorldStore, terminal: MudTerminal);
}
```

Responsibilities:

- Subscribe to `store.subscribe`.
- On every store change:
  - Call `scheduleProjection()`.
- `scheduleProjection()` uses the perception deadband and `requestAnimationFrame`-style coalescing:
  - If a projection is already scheduled this frame, do not schedule another.
  - If the store changed but no meaningful projected field changed, suppress the update.
- On meaningful change:
  - `projectRoom()`:
    - If `currentRoomId` changed, tell the active Phaser scene to show that room via `scene.events.emit('projection:room-changed', roomId)`.
    - Push `MudFormatter.formatRoom(store)` into the terminal.
  - `projectObjects()`:
    - For each changed object in `roomObjects`, emit `scene.events.emit('projection:object-changed', objectId, patch)`.
    - Push a line from `formatObjectDelta` into the terminal.
  - `projectEvents()`:
    - Drain any new `pastEvents` entries since the last projection.
    - Push each line into the terminal using `formatEvent`.
- Write-back from Phaser scenes:
  - Listen to Phaser scene events:
    ```ts
    scene.events.on('projection:object-moved', ({ roomId, objectId, x, y }) => { ... });
    ```
  - Write through to the store with `setObjectState`.
  - Apply deadband to `x/y` changes before writing back.
- `destroy()`:
  - Unsubscribe from store.
  - Off all Phaser events.

#### 3.6 `src/projection/installProjection.ts`

```ts
export function installProjection(scene: Phaser.Scene, store: SharedWorldStore): ProjectionBridge;
```

- Create `MudTerminal`.
- Create `ProjectionBridge`.
- Create `MudFormatter` instance or use a static API.
- Return the bridge.

#### 3.7 `src/main.ts` (Modify)

After the Phaser game is initialized:

```ts
installProjection(scene, store);
```

This is the final integration line added in this task.

### 4. Acceptance Criteria

- Loading into a room updates both the Phaser room scene and the MUD terminal with the same room name, description, and exit list.
- Moving an object in a Phaser scene writes through to `store.roomObjects` and appears in the MUD terminal as a delta line.
- Calling `store.pushEvent('test', 'hello from store')` from the console prints `hello from store` in the terminal within one frame.
- Running `store.setCurrentRoomId('galley')` twice in a row triggers only one room projection and one terminal room print.
- Rapidly mutating `store.flags` 100 times in one tick results in exactly one projected scene update and one terminal update in that frame.
- Pressing `M` toggles the terminal open/closed without breaking room input or verb bar interactions.
- Dialogue lines pushed by Task 1 appear in the terminal as `Voss says, "..."`.
- Audio events pushed by Task 2 appear in the terminal as `The jukebox plays "Portside Rum".`
- `npm run build` passes TypeScript strict mode.

### 5. Dependencies

- Task 1: `TapAPI`, dialogue `pushEvent` output, and room hotspot structure.
- Task 2: `SharedWorldStore.subscribe` and audio event lines.
- The `SharedWorldStore` changes from Task 2 must be merged before this task is started.
- This is the final integration task and should land last.