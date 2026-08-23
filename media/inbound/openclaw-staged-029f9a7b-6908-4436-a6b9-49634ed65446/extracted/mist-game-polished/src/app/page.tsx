'use client';

import { useEffect, useRef, useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMistStore } from '@/lib/mist/engine';
import { LEVELS, isLevelUnlocked, getLevelsForRank, getLevelById } from '@/lib/mist/levels';
import { SKILL_TREE, canUnlockSkill, getSkillsForRank } from '@/lib/mist/skills';
import { ALL_STICKERS, ALL_DISCOVERIES, BREED_INFO, ALL_FARM_UPGRADES, getCollectionProgress } from '@/lib/mist/collections';
import { generateDailyChallenge } from '@/lib/mist/daily';
import { RANK_ORDER, RANK_COLORS, RANK_LABELS, Rank, TileType, Weather, TILE_SIZE, DogAbility, StickerRarity, SeededRNG, SheepBreed } from '@/lib/mist/types';
import { spawnSheep, generateTerrain } from '@/lib/mist/procedural';
import { DEFAULT_FLOCKING, updateFlocking } from '@/lib/mist/flocking';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

// ============================================================
// TILE COLORS — Rich voxel-style palette
// ============================================================
const TILE_COLORS: Record<string, Record<string, string>> = {
  grass:       { a: '#7CB342', b: '#8BC34A', c: '#6DA832', d: '#9CCC65' },
  tall_grass:  { a: '#558B2F', b: '#689F38', c: '#4A7D28', d: '#7CB342' },
  dirt:        { a: '#A1887F', b: '#BCAAA4', c: '#8D6E63', d: '#D7CCC8' },
  stone:       { a: '#9E9E9E', b: '#BDBDBD', c: '#757575', d: '#E0E0E0' },
  water:       { a: '#42A5F5', b: '#64B5F6', c: '#1E88E5', d: '#90CAF9' },
  flowers:     { a: '#7CB342', b: '#8BC34A', c: '#F06292', d: '#FFD54F' },
  mud:         { a: '#795548', b: '#8D6E63', c: '#6D4C41', d: '#A1887F' },
  fence:       { a: '#8D6E63', b: '#A1887F', c: '#6D4C41', d: '#795548' },
  gate:        { a: '#A1887F', b: '#BCAAA4', c: '#8D6E63', d: '#D7CCC8' },
  pen_floor:   { a: '#D7CCC8', b: '#BCAAA4', c: '#A1887F', d: '#EFEBE9' },
  bush:        { a: '#388E3C', b: '#4CAF50', c: '#2E7D32', d: '#66BB6A' },
  tree:        { a: '#2E7D32', b: '#388E3C', c: '#1B5E20', d: '#4CAF50' },
  rock:        { a: '#616161', b: '#757575', c: '#424242', d: '#9E9E9E' },
  fog:         { a: '#CFD8DC', b: '#B0BEC5', c: '#ECEFF1', d: '#90A4AE' },
  ice:         { a: '#B3E5FC', b: '#E1F5FE', c: '#81D4FA', d: '#E0F7FA' },
  sand:        { a: '#FFE0B2', b: '#FFCC80', c: '#FFB74D', d: '#FFF3E0' },
  clover:      { a: '#66BB6A', b: '#81C784', c: '#4CAF50', d: '#A5D6A7' },
  path:        { a: '#BCAAA4', b: '#D7CCC8', c: '#A1887F', d: '#EFEBE9' },
};

// Weather overlays
const WEATHER_BG: Record<string, string> = {
  clear: 'bg-gradient-to-b from-sky-300 to-sky-100',
  cloudy: 'bg-gradient-to-b from-gray-400 to-gray-200',
  rainy: 'bg-gradient-to-b from-gray-500 to-gray-300',
  foggy: 'bg-gradient-to-b from-gray-300 to-gray-100',
  snowy: 'bg-gradient-to-b from-blue-100 to-white',
  windy: 'bg-gradient-to-b from-sky-200 to-sky-100',
  golden: 'bg-gradient-to-b from-amber-300 to-orange-100',
  starry: 'bg-gradient-to-b from-indigo-900 to-purple-900',
};

// ============================================================
// MAIN GAME COMPONENT
// ============================================================
export default function MistGame() {
  const store = useMistStore();
  const canvasRef = useRef<HTMLDivElement>(null);
  const animRef = useRef<number>(0);
  const lastTimeRef = useRef<number>(0);
  const [isClient, setIsClient] = useState(false);
  const [mobileDir, setMobileDir] = useState<string>('none');

  // Init on mount
  useEffect(() => {
    setIsClient(true);
    store.init();
  }, []);

  // Game loop
  useEffect(() => {
    if (store.screen !== 'game' || store.isPaused || store.isComplete) {
      if (animRef.current) cancelAnimationFrame(animRef.current);
      return;
    }

    const loop = (time: number) => {
      if (lastTimeRef.current === 0) lastTimeRef.current = time;
      const dt = Math.min((time - lastTimeRef.current) / 1000, 0.05); // Cap at 50ms
      lastTimeRef.current = time;

      // Combine keyboard + mobile input
      const state = useMistStore.getState();
      const dir = state.input.direction !== 'none' ? state.input.direction : (mobileDir !== 'none' ? mobileDir as any : 'none');
      if (dir !== 'none' && state.input.direction === 'none') {
        useMistStore.setState({ input: { ...state.input, direction: dir as any } });
      }

      state.updateGame(dt);
      animRef.current = requestAnimationFrame(loop);
    };

    lastTimeRef.current = 0;
    animRef.current = requestAnimationFrame(loop);
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [store.screen, store.isPaused, store.isComplete, mobileDir]);

  // Keyboard handlers
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'w', 'a', 's', 'd', 'W', 'A', 'S', 'D', ' ', 'Escape', 'e', 'E', 'q', 'Q'].includes(e.key)) {
        e.preventDefault();
      }
      store.handleKeyDown(e.key);
    };
    const up = (e: KeyboardEvent) => store.handleKeyUp(e.key);
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    return () => { window.removeEventListener('keydown', down); window.removeEventListener('keyup', up); };
  }, [store.screen]);

  if (!isClient) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-emerald-800 to-emerald-600">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center text-white"
        >
          <div className="text-6xl mb-4">🐕</div>
          <h1 className="text-4xl font-bold">MIST</h1>
          <p className="text-emerald-200 mt-2">Loading the meadow...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen flex flex-col bg-background select-none overflow-hidden">
        <AnimatePresence mode="wait">
          {store.screen === 'title' && <TitleScreen key="title" />}
          {store.screen === 'level_select' && <LevelSelectScreen key="levels" />}
          {store.screen === 'game' && <GameScreen key="game" canvasRef={canvasRef} mobileDir={mobileDir} setMobileDir={setMobileDir} />}
          {store.screen === 'level_complete' && <LevelCompleteScreen key="complete" />}
          {store.screen === 'skill_tree' && <SkillTreeScreen key="skills" />}
          {store.screen === 'collection_book' && <CollectionScreen key="collection" />}
          {store.screen === 'daily_challenge' && <DailyChallengeScreen key="daily" />}
          {store.screen === 'sandbox' && <SandboxScreen key="sandbox" />}
          {store.screen === 'settings' && <SettingsScreen key="settings" />}
          {store.screen === 'farm' && <FarmScreen key="farm" />}
        </AnimatePresence>
      </div>
    </TooltipProvider>
  );
}

// ============================================================
// TITLE SCREEN
// ============================================================
function TitleScreen() {
  const { setScreen, saveData } = useMistStore();
  const daily = generateDailyChallenge();
  const dailyDone = saveData.dailyChallenges[daily.date]?.completed;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex-1 flex flex-col items-center justify-center p-4 relative overflow-hidden"
      style={{ background: 'linear-gradient(180deg, #1a472a 0%, #2d5a3f 30%, #4a7c59 60%, #7CB342 100%)' }}
    >
      {/* Animated mist particles */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {Array.from({ length: 20 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full bg-white/10"
            style={{
              width: 60 + i * 15,
              height: 30 + i * 8,
              left: `${(i * 37) % 100}%`,
              top: `${20 + (i * 23) % 60}%`,
            }}
            animate={{
              x: [0, 30, -20, 10, 0],
              opacity: [0.1, 0.3, 0.15, 0.25, 0.1],
            }}
            transition={{ duration: 8 + i * 0.5, repeat: Infinity, ease: 'easeInOut' }}
          />
        ))}
      </div>

      {/* Title */}
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-center relative z-10"
      >
        <div className="text-7xl sm:text-8xl mb-2 drop-shadow-lg">🐕</div>
        <h1 className="text-5xl sm:text-7xl font-bold text-white drop-shadow-lg tracking-wider" style={{ textShadow: '3px 3px 6px rgba(0,0,0,0.3)' }}>
          MIST
        </h1>
        <p className="text-emerald-200 text-lg sm:text-xl mt-2 font-light italic">Tale of a Sheepdog Puppy</p>
      </motion.div>

      {/* Rank badge */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.5, type: 'spring' }}
        className="mt-6 relative z-10"
      >
        <Badge className="text-sm px-4 py-1" style={{ backgroundColor: RANK_COLORS[saveData.currentRank], color: 'white' }}>
          {RANK_LABELS[saveData.currentRank]}
        </Badge>
      </motion.div>

      {/* Menu buttons */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="mt-8 flex flex-col gap-3 w-full max-w-xs relative z-10"
      >
        <Button onClick={() => setScreen('level_select')} className="h-14 text-lg bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl shadow-lg">
          Continue Adventure
        </Button>
        <Button
          onClick={() => { useMistStore.getState().startDailyChallenge(); }}
          variant={dailyDone ? 'outline' : 'default'}
          className={`h-12 ${dailyDone ? 'border-amber-400 text-amber-400' : 'bg-amber-500 hover:bg-amber-400 text-white'} rounded-xl shadow-lg`}
        >
          {dailyDone ? 'Daily Challenge (Done)' : `Daily: ${daily.levelName}`}
        </Button>
        <Button onClick={() => setScreen('skill_tree')} variant="outline" className="h-12 rounded-xl border-emerald-400 text-emerald-300">
          Skill Tree ({saveData.skillPoints} pts)
        </Button>
        <Button onClick={() => setScreen('collection_book')} variant="outline" className="h-12 rounded-xl border-emerald-400 text-emerald-300">
          Collection Book
        </Button>
        <Button onClick={() => setScreen('sandbox')} variant="outline" className="h-12 rounded-xl border-emerald-400 text-emerald-300">
          Sandbox Lab
        </Button>
        <Button onClick={() => setScreen('farm')} variant="outline" className="h-12 rounded-xl border-emerald-400 text-emerald-300">
          Your Farm
        </Button>
        <Button onClick={() => setScreen('settings')} variant="outline" className="h-12 rounded-xl border-white/20 text-white/50">
          Settings
        </Button>
      </motion.div>

      {/* Stats footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="mt-8 text-emerald-300/70 text-xs text-center relative z-10"
      >
        <p>{saveData.totalSheepHerded} sheep herded | {saveData.discoveryCount} discoveries | {saveData.dailyStreak} day streak</p>
      </motion.div>
    </motion.div>
  );
}

// ============================================================
// LEVEL SELECT SCREEN
// ============================================================
function LevelSelectScreen() {
  const { setScreen, saveData } = useMistStore();

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 sm:p-6 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #1a472a 0%, #2d5a3f 100%)' }}
    >
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <Button variant="ghost" onClick={() => setScreen('title')} className="text-white hover:bg-white/10">
            ← Back
          </Button>
          <h2 className="text-2xl font-bold text-white flex-1">Select Level</h2>
          <Badge style={{ backgroundColor: RANK_COLORS[saveData.currentRank] }} className="text-white">
            {RANK_LABELS[saveData.currentRank]}
          </Badge>
        </div>

        {/* Rank sections */}
        {RANK_ORDER.map(rank => {
          const levels = getLevelsForRank(rank);
          return (
            <div key={rank} className="mb-6">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: RANK_COLORS[rank] }} />
                <h3 className="text-lg font-semibold text-white capitalize">{rank}</h3>
                <span className="text-emerald-300/60 text-sm">
                  {levels.filter(l => (saveData.levelResults[l.id]?.stars ?? 0) >= 1).length}/{levels.length} completed
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {levels.map(level => {
                  const result = saveData.levelResults[level.id];
                  const stars = result?.stars ?? 0;
                  const unlocked = isLevelUnlocked(level.id, saveData.levelResults);
                  const bestTime = result?.time;

                  return (
                    <motion.div key={level.id} whileHover={{ scale: unlocked ? 1.03 : 1 }} whileTap={{ scale: unlocked ? 0.97 : 1 }}>
                      <Card
                        className={`${unlocked ? 'cursor-pointer hover:shadow-lg hover:shadow-emerald-500/20' : 'opacity-50'} transition-all border-white/10`}
                        style={{ backgroundColor: unlocked ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.2)' }}
                        onClick={() => unlocked && useMistStore.getState().startLevel(level.id)}
                      >
                        <CardContent className="p-3">
                          <div className="flex justify-between items-start">
                            <div>
                              <p className="text-white font-semibold text-sm">{level.name}</p>
                              <p className="text-emerald-300/60 text-xs mt-0.5">{level.subtitle}</p>
                            </div>
                            {!unlocked && <span className="text-2xl">🔒</span>}
                          </div>
                          <div className="mt-2 flex items-center gap-2">
                            <div className="flex gap-0.5">
                              {[1, 2, 3].map(s => (
                                <span key={s} className={`text-sm ${s <= stars ? 'text-yellow-400' : 'text-white/20'}`}>★</span>
                              ))}
                            </div>
                            {bestTime != null && (
                              <span className="text-emerald-300/50 text-xs ml-auto">{bestTime.toFixed(1)}s</span>
                            )}
                          </div>
                          {result?.discoveriesFound > 0 && (
                            <p className="text-emerald-300/40 text-xs mt-1">{result.discoveriesFound} discoveries</p>
                          )}
                        </CardContent>
                      </Card>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

// ============================================================
// GAME SCREEN — The actual gameplay
// ============================================================
function GameScreen({ canvasRef, mobileDir, setMobileDir }: { canvasRef: React.RefObject<HTMLDivElement | null>; mobileDir: string; setMobileDir: (d: string) => void }) {
  const store = useMistStore();
  const { grid, gridWidth, gridHeight, dog, sheep, collectibles, obstacles, particles,
    timer, barksUsed, sheepInPen, totalSheep, sheepLost, isPaused, isComplete,
    currentLevel, currentDialog, weather, activeTutorial, discoveriesThisLevel } = store;

  if (!grid.length || !dog || !currentLevel) return <div className="flex-1 flex items-center justify-center text-white">Loading...</div>;

  const timeLimit = currentLevel.objective.timeLimit;
  const maxBarks = currentLevel.constraints.maxBarks;
  const allDiscovered = discoveriesThisLevel.length >= currentLevel.discoveries.length;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className={`flex-1 flex flex-col relative overflow-hidden ${WEATHER_BG[weather.current] ?? WEATHER_BG.clear}`}
    >
      {/* HUD */}
      <div className="absolute top-0 left-0 right-0 z-20 p-2 sm:p-3">
        <div className="flex items-center justify-between bg-black/50 backdrop-blur-sm rounded-xl px-3 py-2 text-white text-sm">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" className="text-white/80 hover:text-white h-8 w-8 p-0"
              onClick={() => store.setScreen('level_select')}>
              ✕
            </Button>
            <span className="font-bold">{currentLevel.name}</span>
          </div>
          <div className="flex items-center gap-3 text-xs">
            <span>🐑 {sheepInPen}/{totalSheep}</span>
            {timeLimit && (
              <span className={(timeLimit - timer) < timeLimit * 0.2 ? 'text-red-400 animate-pulse' : ''}>
                ⏱ {Math.max(0, timeLimit - timer).toFixed(0)}s
              </span>
            )}
            {!timeLimit && <span>⏱ {timer.toFixed(1)}s</span>}
            {maxBarks && <span className={barksUsed > maxBarks * 0.8 ? 'text-amber-400' : ''}>📢 {barksUsed}/{maxBarks}</span>}
            {sheepLost > 0 && <span className="text-red-400">💔 {sheepLost}</span>}
            {discoveriesThisLevel.length > 0 && (
              <span className="text-yellow-400">✨ {discoveriesThisLevel.length}/{currentLevel.discoveries.length}</span>
            )}
          </div>
        </div>
      </div>

      {/* Stamina bar */}
      <div className="absolute bottom-20 sm:bottom-4 left-3 z-20">
        <div className="bg-black/40 backdrop-blur-sm rounded-lg px-2 py-1.5 w-28">
          <div className="flex items-center gap-1.5">
            <span className="text-xs text-white/70">⚡</span>
            <div className="flex-1 h-2 bg-black/30 rounded-full overflow-hidden">
              <div className="h-full bg-emerald-400 rounded-full transition-all" style={{ width: `${dog.stamina}%` }} />
            </div>
          </div>
          {dog.activeAbility && (
            <p className="text-[10px] text-yellow-300 mt-1">{dog.activeAbility.replace(/_/g, ' ')}</p>
          )}
        </div>
      </div>

      {/* Ability indicator */}
      {dog.abilities.length > 0 && (
        <div className="absolute bottom-20 sm:bottom-4 right-3 z-20">
          <div className="bg-black/40 backdrop-blur-sm rounded-lg px-2 py-1.5">
            <p className="text-[10px] text-white/50">Q: Switch ability</p>
            <p className="text-xs text-yellow-300">{dog.activeAbility?.replace(/_/g, ' ') ?? 'none'}</p>
          </div>
        </div>
      )}

      {/* Game Canvas */}
      <div ref={canvasRef} className="flex-1 flex items-center justify-center relative">
        <div
          className="relative"
          style={{
            width: gridWidth * TILE_SIZE,
            height: gridHeight * TILE_SIZE,
            transform: `scale(${Math.min(1, typeof window !== 'undefined' ? window.innerWidth / (gridWidth * TILE_SIZE + 40) : 1, typeof window !== 'undefined' ? window.innerHeight / (gridHeight * TILE_SIZE + 120) : 1)})`,
            transformOrigin: 'center center',
          }}
        >
          {/* Terrain tiles */}
          {grid.map((row, y) => row.map((tile, x) => {
            const colors = TILE_COLORS[tile.type] ?? TILE_COLORS.grass;
            const color = colors[tile.variant] ?? colors.a;
            return (
              <div
                key={`${x}-${y}`}
                className="absolute border border-black/5"
                style={{
                  left: x * TILE_SIZE,
                  top: y * TILE_SIZE,
                  width: TILE_SIZE,
                  height: TILE_SIZE,
                  backgroundColor: color,
                  transform: `translateY(${-tile.elevation * 2}px)`,
                  zIndex: tile.elevation,
                }}
              >
                {/* Tile decorations */}
                {tile.type === TileType.Tree && (
                  <div className="absolute inset-0 flex items-center justify-center text-lg" style={{ zIndex: tile.elevation + 1 }}>🌲</div>
                )}
                {tile.type === TileType.Bush && (
                  <div className="absolute inset-0 flex items-center justify-center text-sm" style={{ zIndex: tile.elevation + 1 }}>🌿</div>
                )}
                {tile.type === TileType.Rock && (
                  <div className="absolute inset-0 flex items-center justify-center text-sm" style={{ zIndex: tile.elevation + 1 }}>🪨</div>
                )}
                {tile.type === TileType.Water && (
                  <div className="absolute inset-0 flex items-center justify-center animate-pulse text-xs" style={{ zIndex: tile.elevation + 1 }}>〰</div>
                )}
                {tile.type === TileType.Flowers && tile.variant === 'c' && (
                  <div className="absolute inset-0 flex items-center justify-center text-xs" style={{ zIndex: tile.elevation + 1 }}>🌸</div>
                )}
                {tile.type === TileType.Fence && (
                  <div className="absolute inset-0 border-2 border-amber-800/60 rounded-sm" />
                )}
                {tile.type === TileType.Gate && (
                  <div className="absolute inset-0 border-2 border-amber-600 rounded-sm flex items-center justify-center text-[8px] text-amber-800">GATE</div>
                )}
                {tile.type === TileType.Fog && (
                  <div className="absolute inset-0 bg-white/30 animate-pulse rounded" />
                )}
                {tile.type === TileType.Ice && (
                  <div className="absolute inset-0 bg-blue-200/40 rounded" />
                )}
              </div>
            );
          }))}

          {/* Collectibles */}
          {collectibles.filter(c => !c.discovered).map(c => (
            <motion.div
              key={c.id}
              className="absolute z-10"
              style={{ left: c.pos.x * TILE_SIZE, top: c.pos.y * TILE_SIZE, width: TILE_SIZE, height: TILE_SIZE }}
              animate={{ y: [0, -4, 0], scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <div className="w-full h-full flex items-center justify-center text-lg drop-shadow-lg">
                {c.collectibleType === 'concept_page' ? '📜' : c.collectibleType === 'sticker' ? '⭐' : c.collectibleType === 'sheep_catalog' ? '📋' : c.collectibleType === 'lore_page' ? '📖' : c.collectibleType === 'farm_upgrade' ? '🏠' : '🔮'}
              </div>
              {/* Sparkle effect */}
              <div className="absolute inset-0 flex items-center justify-center">
                <motion.div animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }} transition={{ duration: 1.5, repeat: Infinity }}>
                  <span className="text-yellow-300 text-xs">✦</span>
                </motion.div>
              </div>
            </motion.div>
          ))}

          {/* Sheep */}
          {sheep.filter(s => !s.isInPen && !s.isLost).map(s => (
            <div
              key={s.id}
              className="absolute z-20 transition-all duration-75"
              style={{
                left: s.pos.x * TILE_SIZE + 4,
                top: s.pos.y * TILE_SIZE + 4,
                width: TILE_SIZE - 8,
                height: TILE_SIZE - 8,
              }}
            >
              <div className="w-full h-full rounded-full relative" style={{ backgroundColor: s.color, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}>
                {/* Face direction indicator */}
                <div className={`absolute text-[10px] ${s.facing === 'down' ? 'bottom-0 left-1/2 -translate-x-1/2' : s.facing === 'up' ? 'top-0 left-1/2 -translate-x-1/2' : s.facing === 'left' ? 'left-0 top-1/2 -translate-y-1/2' : 'right-0 top-1/2 -translate-y-1/2'}`}>
                  👁
                </div>
                {/* Happiness indicator */}
                {s.happiness < 30 && (
                  <motion.div animate={{ y: [0, -3, 0] }} transition={{ duration: 1, repeat: Infinity }}
                    className="absolute -top-2 right-0 text-xs">😟</motion.div>
                )}
                {s.personality === 'stubborn' && (
                  <div className="absolute -top-1 left-0 text-[8px]">😤</div>
                )}
              </div>
            </div>
          ))}

          {/* Dog (player) */}
          <div
            className="absolute z-30 transition-all duration-75"
            style={{
              left: dog.pos.x * TILE_SIZE,
              top: dog.pos.y * TILE_SIZE,
              width: TILE_SIZE,
              height: TILE_SIZE,
            }}
          >
            <motion.div
              animate={dog.isBarking ? { scale: [1, 1.2, 1] } : {}}
              transition={{ duration: 0.15 }}
              className="w-full h-full relative flex items-center justify-center"
            >
              {/* Dog body */}
              <div className="w-10 h-10 rounded-full bg-amber-600 shadow-lg relative flex items-center justify-center">
                <span className="text-xl" style={{ transform: `scaleX(${dog.facing === 'left' ? -1 : 1})` }}>{dog.facing === 'up' ? '🐕' : dog.facing === 'down' ? '🐕' : '🐕'}</span>
                {/* Bark radius indicator when barking */}
                {dog.isBarking && (
                  <motion.div
                    initial={{ scale: 0.3, opacity: 0.8 }}
                    animate={{ scale: 1.5, opacity: 0 }}
                    transition={{ duration: 0.4 }}
                    className="absolute inset-0 rounded-full border-2 border-white/50"
                    style={{ width: dog.barkRadius * TILE_SIZE * 2, height: dog.barkRadius * TILE_SIZE * 2, left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }}
                  />
                )}
              </div>
            </motion.div>
          </div>

          {/* Particles */}
          {particles.map(p => (
            <div
              key={p.id}
              className="absolute rounded-full pointer-events-none z-40"
              style={{
                left: p.pos.x * TILE_SIZE,
                top: p.pos.y * TILE_SIZE,
                width: p.size,
                height: p.size,
                backgroundColor: p.color,
                opacity: p.life / p.maxLife,
              }}
            />
          ))}

          {/* Weather overlay */}
          {weather.current === Weather.Foggy && (
            <div className="absolute inset-0 bg-white/20 pointer-events-none z-50" />
          )}
          {weather.current === Weather.Rainy && (
            <div className="absolute inset-0 pointer-events-none z-50 overflow-hidden">
              {Array.from({ length: 30 }).map((_, i) => (
                <motion.div key={i} className="absolute w-0.5 h-3 bg-blue-300/40"
                  style={{ left: `${(i * 7 + 3) % 100}%` }}
                  animate={{ y: [-20, gridHeight * TILE_SIZE] }}
                  transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.1 }}
                />
              ))}
            </div>
          )}
          {weather.current === Weather.Snowy && (
            <div className="absolute inset-0 pointer-events-none z-50 overflow-hidden">
              {Array.from({ length: 20 }).map((_, i) => (
                <motion.div key={i} className="absolute w-2 h-2 bg-white/60 rounded-full"
                  style={{ left: `${(i * 11 + 5) % 100}%` }}
                  animate={{ y: [-10, gridHeight * TILE_SIZE], x: [-10, 10] }}
                  transition={{ duration: 3, repeat: Infinity, delay: i * 0.3 }}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Tutorial overlay */}
      {activeTutorial && !currentDialog && (
        <div className="absolute bottom-24 sm:bottom-16 left-1/2 -translate-x-1/2 z-30 max-w-sm">
          <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
            <Card className="bg-black/70 backdrop-blur text-white border-white/20">
              <CardContent className="p-3 text-center text-sm">
                <p>{activeTutorial.text}</p>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      )}

      {/* Dialog overlay */}
      {currentDialog && <DialogOverlay />}

      {/* Pause overlay */}
      {isPaused && (
        <div className="absolute inset-0 z-40 bg-black/60 flex items-center justify-center">
          <Card className="bg-gray-900/90 border-white/20 text-white w-64">
            <CardContent className="p-6 text-center">
              <h3 className="text-xl font-bold mb-4">Paused</h3>
              <div className="flex flex-col gap-2">
                <Button onClick={() => useMistStore.setState({ isPaused: false })} className="bg-emerald-600 hover:bg-emerald-500">Resume</Button>
                <Button variant="outline" onClick={() => store.setScreen('level_select')} className="border-white/30 text-white">Quit Level</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Mobile controls */}
      <div className="sm:hidden absolute bottom-2 left-0 right-0 z-30 px-4">
        <div className="flex justify-between items-end">
          <div className="grid grid-cols-3 gap-1 w-32">
            <div />
            <button className="bg-black/30 backdrop-blur rounded-lg p-2 text-white text-lg active:bg-black/50" onTouchStart={() => setMobileDir('up')} onTouchEnd={() => setMobileDir('none')} onTouchCancel={() => setMobileDir('none')}>↑</button>
            <div />
            <button className="bg-black/30 backdrop-blur rounded-lg p-2 text-white text-lg active:bg-black/50" onTouchStart={() => setMobileDir('left')} onTouchEnd={() => setMobileDir('none')} onTouchCancel={() => setMobileDir('none')}>←</button>
            <button className="bg-black/30 backdrop-blur rounded-lg p-2 text-white text-lg active:bg-black/50" onTouchStart={() => setMobileDir('down')} onTouchEnd={() => setMobileDir('none')} onTouchCancel={() => setMobileDir('none')}>↓</button>
            <button className="bg-black/30 backdrop-blur rounded-lg p-2 text-white text-lg active:bg-black/50" onTouchStart={() => setMobileDir('right')} onTouchEnd={() => setMobileDir('none')} onTouchCancel={() => setMobileDir('none')}>→</button>
          </div>
          <div className="flex flex-col gap-1.5">
            {dog.abilities.length > 0 && (
              <button className="bg-blue-500/80 backdrop-blur rounded-xl p-2.5 text-white text-sm font-bold active:bg-blue-400" onTouchStart={() => store.useAbility()}>
                Q: {dog.activeAbility?.replace(/_/g, ' ') ?? 'Ability'}
              </button>
            )}
            <button className="bg-amber-500/80 backdrop-blur rounded-xl p-3 text-white text-xl font-bold active:bg-amber-400" onTouchStart={() => store.bark()}>
              BARK!
            </button>
          </div>
        </div>
      </div>

      {/* Discovery notification */}
      {discoveriesThisLevel.length > 0 && !currentDialog && (
        <motion.div
          key={`disc-${discoveriesThisLevel.length}`}
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -20, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="absolute top-16 left-1/2 -translate-x-1/2 z-30"
        >
          <Badge className="bg-yellow-500 text-white px-3 py-1 text-xs shadow-lg">
            ✨ {discoveriesThisLevel.length} discovery{discoveriesThisLevel.length > 1 ? 'ies' : 'y'} found!
          </Badge>
        </motion.div>
      )}
    </motion.div>
  );
}

// ============================================================
// DIALOG OVERLAY
// ============================================================
function DialogOverlay() {
  const { currentDialog, advanceDialog, dialogHistory } = useMistStore();
  if (!currentDialog) return null;

  const emotionIcons: Record<string, string> = {
    wise: '🧙', playful: '😊', concerned: '😟', proud: '🥰',
    mysterious: '🌙', encouraging: '💪',
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="absolute inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 p-4"
      onClick={() => !currentDialog.choices?.length && advanceDialog()}
    >
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="w-full max-w-lg"
      >
        <Card className="bg-gradient-to-br from-amber-50 to-orange-50 border-amber-300 shadow-2xl">
          <CardContent className="p-4 sm:p-5">
            {/* Speaker */}
            <div className="flex items-center gap-2 mb-3">
              <span className="text-2xl">{currentDialog.speaker === 'elder_bark' ? '🐕' : '🐑'}</span>
              <div>
                <p className="font-bold text-amber-900 text-sm">{currentDialog.speaker === 'elder_bark' ? 'Elder Bark' : 'Narrator'}</p>
                {currentDialog.emotion && (
                  <span className="text-xs text-amber-600">{emotionIcons[currentDialog.emotion] ?? ''} {currentDialog.emotion}</span>
                )}
              </div>
            </div>

            {/* Text */}
            <p className="text-amber-950 text-sm sm:text-base leading-relaxed mb-4">
              {currentDialog.text}
            </p>

            {/* Choices */}
            {currentDialog.choices && currentDialog.choices.length > 0 && (
              <div className="flex flex-col gap-2">
                {currentDialog.choices.map((choice, i) => (
                  <Button key={i} variant="outline" className="border-amber-300 text-amber-900 hover:bg-amber-100 text-left justify-start text-sm"
                    onClick={(e) => { e.stopPropagation(); advanceDialog(choice.nextId); }}>
                    {choice.text}
                  </Button>
                ))}
              </div>
            )}

            {/* Continue hint */}
            {!currentDialog.choices?.length && (
              <p className="text-amber-400 text-xs text-right animate-pulse">Press E or tap to continue...</p>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  );
}

// ============================================================
// LEVEL COMPLETE SCREEN
// ============================================================
function LevelCompleteScreen() {
  const store = useMistStore();
  const { currentLevel, timer, sheepInPen, totalSheep, barksUsed, discoveriesThisLevel, currentDialog, saveData, isComplete } = store;

  if (!currentLevel) return null;

  const result = saveData.levelResults[currentLevel.id];
  const stars = result?.stars ?? 0;
  const isDaily = currentLevel.id === 'daily';

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex-1 flex items-center justify-center p-4"
      style={{ background: 'linear-gradient(180deg, #1a472a 0%, #2d5a3f 50%, #1a472a 100%)' }}
    >
      <div className="max-w-md w-full">
        {/* Dialog if present */}
        {currentDialog ? (
          <DialogOverlay />
        ) : (
          <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ type: 'spring' }}>
            <Card className="bg-gradient-to-br from-amber-50 to-orange-50 border-amber-300 shadow-2xl">
              <CardContent className="p-6 text-center">
                <motion.div animate={{ rotate: [0, -10, 10, 0] }} transition={{ delay: 0.3, duration: 0.5 }}>
                  <span className="text-5xl">🐕</span>
                </motion.div>

                <h2 className="text-2xl font-bold text-amber-900 mt-3">{stars > 0 ? 'Level Complete!' : 'Try Again!'}</h2>
                <p className="text-amber-700 text-sm mt-1">{currentLevel.name}</p>

                {/* Stars */}
                <div className="flex justify-center gap-2 mt-4">
                  {[1, 2, 3].map(s => (
                    <motion.span
                      key={s}
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ delay: 0.5 + s * 0.3, type: 'spring' }}
                      className={`text-3xl ${s <= stars ? 'text-yellow-400' : 'text-gray-300'}`}
                    >
                      ★
                    </motion.span>
                  ))}
                </div>

                {/* Stats */}
                <div className="mt-4 grid grid-cols-3 gap-2 text-center">
                  <div className="bg-white/50 rounded-lg p-2">
                    <p className="text-amber-900 font-bold">{sheepInPen}/{totalSheep}</p>
                    <p className="text-amber-600 text-xs">Sheep Herded</p>
                  </div>
                  <div className="bg-white/50 rounded-lg p-2">
                    <p className="text-amber-900 font-bold">{timer.toFixed(1)}s</p>
                    <p className="text-amber-600 text-xs">Time</p>
                  </div>
                  <div className="bg-white/50 rounded-lg p-2">
                    <p className="text-amber-900 font-bold">{discoveriesThisLevel.length}</p>
                    <p className="text-amber-600 text-xs">Discoveries</p>
                  </div>
                </div>

                {/* AI Concept (unlocked if 1+ star) */}
                {stars >= 1 && currentLevel.aiConcept && (
                  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.5 }} className="mt-4">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-left">
                      <p className="text-blue-900 font-semibold text-sm">AI Concept: {currentLevel.aiConcept.name}</p>
                      <p className="text-blue-700 text-xs mt-1">{currentLevel.aiConcept.metaphor}</p>
                    </div>
                  </motion.div>
                )}

                {/* Parent Layer hint */}
                {stars >= 1 && currentLevel.parentLayerContent && saveData.parentLayerEnabled && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2 }} className="mt-2">
                    <p className="text-blue-500 text-xs text-left cursor-pointer hover:underline">
                      👨‍👩‍👧 Parent: {currentLevel.parentLayerContent.aiConnection.slice(0, 80)}...
                    </p>
                  </motion.div>
                )}

                {/* Actions */}
                <div className="flex gap-2 mt-5">
                  <Button onClick={() => store.setScreen('level_select')} variant="outline" className="flex-1 border-amber-300">
                    Levels
                  </Button>
                  {!isDaily && (
                    <Button onClick={() => store.startLevel(currentLevel.id)} className="flex-1 bg-emerald-600 hover:bg-emerald-500">
                      {stars >= 3 ? 'Perfect!' : stars > 0 ? 'Replay' : 'Retry'}
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// ============================================================
// SKILL TREE SCREEN
// ============================================================
function SkillTreeScreen() {
  const { setScreen, saveData, unlockSkillAction } = useMistStore();

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 sm:p-6 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #1a3a2a 0%, #2d4a3f 100%)' }}
    >
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-4">
          <Button variant="ghost" onClick={() => setScreen('title')} className="text-white hover:bg-white/10">← Back</Button>
          <h2 className="text-2xl font-bold text-white flex-1">Skill Tree</h2>
          <Badge className="bg-yellow-500 text-white">{saveData.skillPoints} Skill Points</Badge>
        </div>

        {RANK_ORDER.map(rank => {
          const skills = getSkillsForRank(rank);
          if (skills.length === 0) return null;

          return (
            <div key={rank} className="mb-6">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: RANK_COLORS[rank] }} />
                <h3 className="text-lg font-semibold text-white capitalize">{rank}</h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {skills.map(skill => {
                  const isUnlocked = saveData.unlockedSkills.includes(skill.id);
                  const canUnlock = canUnlockSkill(skill.id, saveData.unlockedSkills, saveData.skillPoints);

                  return (
                    <motion.div key={skill.id} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                      <Card
                        className={`${canUnlock ? 'cursor-pointer hover:shadow-lg' : ''} border-white/10 transition-all`}
                        style={{
                          backgroundColor: isUnlocked ? 'rgba(76,175,80,0.2)' : canUnlock ? 'rgba(255,215,0,0.15)' : 'rgba(0,0,0,0.2)',
                        }}
                        onClick={() => canUnlock && unlockSkillAction(skill.id)}
                      >
                        <CardContent className="p-3 flex gap-3 items-start">
                          <span className="text-2xl">{skill.icon}</span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <p className={`font-semibold text-sm ${isUnlocked ? 'text-green-300' : canUnlock ? 'text-yellow-300' : 'text-white/40'}`}>
                                {skill.name}
                              </p>
                              {isUnlocked && <span className="text-green-400 text-xs">✓</span>}
                            </div>
                            <p className="text-white/50 text-xs mt-0.5">{skill.description}</p>
                            {!isUnlocked && (
                              <p className={`text-xs mt-1 ${canUnlock ? 'text-yellow-400' : 'text-white/30'}`}>
                                Cost: {skill.cost} pts{skill.requires?.length ? ` (requires ${skill.requires.length} skills)` : ''}
                              </p>
                            )}
                            {isUnlocked && (
                              <p className="text-green-400/70 text-xs mt-1">{skill.effect.description}</p>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}

// ============================================================
// COLLECTION SCREEN
// ============================================================
function CollectionScreen() {
  const { setScreen, saveData } = useMistStore();
  const progress = getCollectionProgress(saveData.stickers, saveData.discoveries, saveData.sheepCatalog);
  const [tab, setTab] = useState<'stickers' | 'discoveries' | 'breeds'>('stickers');

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 sm:p-6 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #2a1a3a 0%, #3f2d4a 100%)' }}
    >
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-4">
          <Button variant="ghost" onClick={() => setScreen('title')} className="text-white hover:bg-white/10">← Back</Button>
          <h2 className="text-2xl font-bold text-white flex-1">Collection Book</h2>
        </div>

        {/* Progress overview */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          {[
            { label: 'Stickers', found: progress.stickers.found, total: progress.stickers.total },
            { label: 'Discoveries', found: progress.discoveries.found, total: progress.discoveries.total },
            { label: 'Breeds', found: progress.breeds.found, total: progress.breeds.total },
          ].map(item => (
            <Card key={item.label} className="bg-white/10 border-white/10">
              <CardContent className="p-3 text-center">
                <p className="text-white font-bold">{item.found}/{item.total}</p>
                <p className="text-white/50 text-xs">{item.label}</p>
                <Progress value={(item.found / item.total) * 100} className="mt-1 h-1" />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(['stickers', 'discoveries', 'breeds'] as const).map(t => (
            <Button key={t} size="sm" variant={tab === t ? 'default' : 'outline'}
              className={tab === t ? 'bg-purple-600' : 'border-white/20 text-white/60'}
              onClick={() => setTab(t)}>
              {t === 'stickers' ? `Stickers (${progress.stickers.found})` : t === 'discoveries' ? `Discoveries (${progress.discoveries.found})` : `Breeds (${progress.breeds.found})`}
            </Button>
          ))}
        </div>

        {/* Content */}
        {tab === 'stickers' && (
          <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
            {ALL_STICKERS.map(sticker => {
              const found = saveData.stickers[sticker.id];
              return (
                <Card key={sticker.id} className={`${found ? 'bg-white/10' : 'bg-black/20'} border-white/10`}>
                  <CardContent className="p-2 text-center">
                    <span className={`text-2xl ${found ? '' : 'grayscale opacity-30'}`}>{sticker.icon}</span>
                    <p className={`text-xs mt-1 ${found ? 'text-white' : 'text-white/20'}`}>{sticker.name}</p>
                    <Badge variant="outline" className={`text-[9px] mt-0.5 ${
                      sticker.rarity === StickerRarity.Legendary ? 'border-yellow-400 text-yellow-400' :
                      sticker.rarity === StickerRarity.Rare ? 'border-purple-400 text-purple-400' :
                      sticker.rarity === StickerRarity.Uncommon ? 'border-blue-400 text-blue-400' :
                      'border-white/20 text-white/40'
                    }`}>
                      {sticker.rarity}
                    </Badge>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {tab === 'discoveries' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {Object.entries(ALL_DISCOVERIES).map(([key, disc]) => {
              const found = saveData.discoveries[key];
              return (
                <Card key={key} className={`${found ? 'bg-white/10' : 'bg-black/20'} border-white/10`}>
                  <CardContent className="p-3 flex gap-2">
                    <span className={`text-xl ${found ? '' : 'grayscale opacity-30'}`}>{disc.icon}</span>
                    <div>
                      <p className={`text-sm font-semibold ${found ? 'text-white' : 'text-white/20'}`}>{disc.name}</p>
                      <p className={`text-xs mt-0.5 ${found ? 'text-white/60' : 'text-white/10'}`}>{found ? disc.description : '???'}</p>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {tab === 'breeds' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {Object.entries(BREED_INFO).map(([breed, info]) => {
              const found = saveData.sheepCatalog[breed];
              return (
                <Card key={breed} className={`${found ? 'bg-white/10' : 'bg-black/20'} border-white/10`}>
                  <CardContent className="p-3 flex gap-3">
                    <div className={`w-10 h-10 rounded-full ${found ? '' : 'grayscale opacity-30'}`} style={{ backgroundColor: found ? info.color : '#333' }} />
                    <div>
                      <p className={`text-sm font-semibold ${found ? 'text-white' : 'text-white/20'}`}>{info.name}</p>
                      <p className={`text-xs mt-0.5 ${found ? 'text-white/60' : 'text-white/10'}`}>{found ? info.description : '???'}</p>
                      {found && <p className="text-purple-300 text-[10px] mt-1">AI Concept: {info.aiConcept}</p>}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </motion.div>
  );
}

// ============================================================
// DAILY CHALLENGE SCREEN
// ============================================================
function DailyChallengeScreen() {
  const { setScreen, saveData } = useMistStore();
  const daily = generateDailyChallenge();
  const completed = saveData.dailyChallenges[daily.date]?.completed;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex-1 flex items-center justify-center p-4"
      style={{ background: 'linear-gradient(180deg, #4a3000 0%, #6b4c00 50%, #4a3000 100%)' }}
    >
      <Card className="w-full max-w-md bg-gradient-to-br from-amber-50 to-yellow-50 border-amber-300 shadow-2xl">
        <CardContent className="p-6 text-center">
          <span className="text-4xl">🌅</span>
          <h2 className="text-2xl font-bold text-amber-900 mt-2">Daily Challenge</h2>
          <p className="text-amber-700 text-sm mt-1">{daily.levelName}</p>

          <p className="text-amber-800 text-sm mt-4">{daily.description}</p>

          {daily.specialRules.length > 0 && (
            <div className="mt-3 space-y-1">
              {daily.specialRules.map((rule, i) => (
                <Badge key={i} variant="outline" className="border-amber-400 text-amber-800 text-xs">
                  {rule.description}
                </Badge>
              ))}
            </div>
          )}

          <div className="mt-4 bg-amber-100 rounded-lg p-3">
            <p className="text-amber-900 font-semibold text-sm">Rewards</p>
            <p className="text-amber-700 text-xs">{daily.reward.stickers} sticker(s) + {daily.reward.skillPoints} skill points</p>
          </div>

          {completed ? (
            <div className="mt-4">
              <p className="text-green-600 font-semibold">Completed! ✓</p>
              <p className="text-amber-600 text-xs">Come back tomorrow for a new challenge!</p>
            </div>
          ) : (
            <Button onClick={() => useMistStore.getState().startDailyChallenge()} className="mt-4 w-full bg-amber-500 hover:bg-amber-400">
              Start Challenge
            </Button>
          )}

          <div className="mt-3 flex items-center justify-center gap-2">
            <span className="text-amber-600 text-xs">Streak:</span>
            <span className="text-amber-900 font-bold">{saveData.dailyStreak} days</span>
            {saveData.dailyStreak >= 7 && <span className="text-yellow-500">🔥</span>}
          </div>

          <Button variant="ghost" onClick={() => setScreen('title')} className="mt-3 text-amber-600">← Back</Button>
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ============================================================
// SANDBOX SCREEN
// ============================================================
function SandboxScreen() {
  const { setScreen, sandboxParams, setSandboxParam, saveData } = useMistStore();
  const [sheepEntities, setSheepEntities] = useState<any[]>([]);
  const [running, setRunning] = useState(false);
  const animRef = useRef<number>(0);

  const startSandbox = () => {
    const rng = new SeededRNG(999);
    const grid = generateTerrain(16, 12, 999, sandboxParams.weather);
    const s = spawnSheep({
      ...LEVELS[1],
      sheepCount: sandboxParams.sheepCount,
      sheepBreeds: Object.values(SheepBreed),
      terrainSeed: 999,
      weather: sandboxParams.weather,
      gridSize: { x: 16, y: 12 },
      obstacles: [],
      discoveries: [],
      objective: { type: 'herd_all', description: '' },
      dialogIntro: { id: 's', speaker: 'narrator' as any, text: '' },
      dialogOutro: { id: 's', speaker: 'narrator' as any, text: '' },
      parentLayerContent: { title: '', conceptName: '', whatHappened: '', aiConnection: '', tryAtHome: '', ageAppropriate: '' },
    }, grid, rng);

    setSheepEntities(s);
    setRunning(true);
  };

  useEffect(() => {
    if (!running || sheepEntities.length === 0) return;

    let lastT = performance.now();
    const loop = (time: number) => {
      const dt = Math.min((time - lastT) / 1000, 0.05);
      lastT = time;

      // Simple flocking update for sandbox using real boids
      setSheepEntities(prev => {
        const updated = [...prev];
        const flockParams = {
          ...DEFAULT_FLOCKING,
          separation: sandboxParams.separation,
          alignment: sandboxParams.alignment,
          cohesion: sandboxParams.cohesion,
        };
        // Build a fake grid (all walkable)
        const fakeGrid = Array.from({ length: 12 }, () =>
          Array.from({ length: 16 }, () => ({ type: TileType.Grass, variant: 'a' as any, walkable: true, swimable: false, elevation: 0 }))
        );
        updateFlocking(updated, null as any, fakeGrid, 16, 12, flockParams, dt);
        // Clamp positions
        for (const s of updated) {
          s.pos.x = Math.max(0.5, Math.min(15.5, s.pos.x + s.vel.x * dt));
          s.pos.y = Math.max(0.5, Math.min(11.5, s.pos.y + s.vel.y * dt));
          s.facing = Math.abs(s.vel.x) > Math.abs(s.vel.y) ? (s.vel.x > 0 ? 'right' : 'left') : (s.vel.y > 0 ? 'down' : 'up');
        }
        return updated;
      });

      animRef.current = requestAnimationFrame(loop);
    };
    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, [running, sheepEntities.length]);

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #1a2a3a 0%, #2d3f4a 100%)' }}
    >
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-3 mb-4">
          <Button variant="ghost" onClick={() => { setRunning(false); setScreen('title'); }} className="text-white hover:bg-white/10">← Back</Button>
          <h2 className="text-2xl font-bold text-white flex-1">Sandbox Lab</h2>
        </div>

        <p className="text-blue-200/70 text-sm mb-4">Experiment with flocking parameters! Adjust the sliders and watch how the sheep behavior changes. This is how AI researchers explore emergent behavior.</p>

        {/* Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <Card className="bg-white/5 border-white/10">
            <CardContent className="p-4">
              <label className="text-white text-sm font-semibold">Separation: {sandboxParams.separation.toFixed(1)}</label>
              <input type="range" min="0" max="5" step="0.1" value={sandboxParams.separation}
                onChange={e => setSandboxParam('separation', parseFloat(e.target.value))}
                className="w-full mt-1" />
              <p className="text-white/40 text-xs">How much sheep avoid each other</p>
            </CardContent>
          </Card>
          <Card className="bg-white/5 border-white/10">
            <CardContent className="p-4">
              <label className="text-white text-sm font-semibold">Alignment: {sandboxParams.alignment.toFixed(1)}</label>
              <input type="range" min="0" max="5" step="0.1" value={sandboxParams.alignment}
                onChange={e => setSandboxParam('alignment', parseFloat(e.target.value))}
                className="w-full mt-1" />
              <p className="text-white/40 text-xs">How much sheep match their neighbors' direction</p>
            </CardContent>
          </Card>
          <Card className="bg-white/5 border-white/10">
            <CardContent className="p-4">
              <label className="text-white text-sm font-semibold">Cohesion: {sandboxParams.cohesion.toFixed(1)}</label>
              <input type="range" min="0" max="5" step="0.1" value={sandboxParams.cohesion}
                onChange={e => setSandboxParam('cohesion', parseFloat(e.target.value))}
                className="w-full mt-1" />
              <p className="text-white/40 text-xs">How much sheep move toward the group center</p>
            </CardContent>
          </Card>
          <Card className="bg-white/5 border-white/10">
            <CardContent className="p-4">
              <label className="text-white text-sm font-semibold">Sheep Count: {sandboxParams.sheepCount}</label>
              <input type="range" min="2" max="30" step="1" value={sandboxParams.sheepCount}
                onChange={e => setSandboxParam('sheepCount', parseInt(e.target.value))}
                className="w-full mt-1" />
              <p className="text-white/40 text-xs">More sheep = more complex emergence</p>
            </CardContent>
          </Card>
        </div>

        <Button onClick={startSandbox} className="w-full bg-blue-600 hover:bg-blue-500 text-white mb-4">
          {running ? 'Restart Simulation' : 'Start Simulation'}
        </Button>

        {/* Sandbox canvas */}
        {sheepEntities.length > 0 && (
          <div className="relative w-full overflow-hidden rounded-xl border border-white/10" style={{ aspectRatio: '16/12', background: '#7CB342' }}>
            {sheepEntities.map((s: any, i: number) => (
              <motion.div
                key={i}
                className="absolute rounded-full"
                style={{
                  width: 20,
                  height: 20,
                  backgroundColor: s.color,
                  left: `${(s.pos.x / 16) * 100}%`,
                  top: `${(s.pos.y / 12) * 100}%`,
                  boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
                }}
                animate={{ left: `${(s.pos.x / 16) * 100}%`, top: `${(s.pos.y / 12) * 100}%` }}
                transition={{ type: 'tween', duration: 0.05 }}
              />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

// ============================================================
// SETTINGS SCREEN
// ============================================================
function SettingsScreen() {
  const { setScreen, saveData } = useMistStore();
  const store = useMistStore();

  const updateSetting = (key: string, value: any) => {
    const newSave = { ...store.saveData, [key]: value };
    if (typeof window !== 'undefined') localStorage.setItem('mist_save_data', JSON.stringify(newSave));
    useMistStore.setState({ saveData: newSave });
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 sm:p-6 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)' }}
    >
      <div className="max-w-md mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <Button variant="ghost" onClick={() => setScreen('title')} className="text-white hover:bg-white/10">← Back</Button>
          <h2 className="text-2xl font-bold text-white flex-1">Settings</h2>
        </div>

        <div className="space-y-4">
          <Card className="bg-white/10 border-white/10">
            <CardContent className="p-4">
              <h3 className="text-white font-semibold mb-3">Audio</h3>
              <div className="space-y-3">
                <div>
                  <label className="text-white/70 text-sm">Music Volume: {Math.round(saveData.musicVolume * 100)}%</label>
                  <input type="range" min="0" max="1" step="0.1" value={saveData.musicVolume}
                    onChange={e => updateSetting('musicVolume', parseFloat(e.target.value))}
                    className="w-full mt-1" />
                </div>
                <div>
                  <label className="text-white/70 text-sm">SFX Volume: {Math.round(saveData.sfxVolume * 100)}%</label>
                  <input type="range" min="0" max="1" step="0.1" value={saveData.sfxVolume}
                    onChange={e => updateSetting('sfxVolume', parseFloat(e.target.value))}
                    className="w-full mt-1" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/10 border-white/10">
            <CardContent className="p-4">
              <h3 className="text-white font-semibold mb-3">Gameplay</h3>
              <div className="space-y-3">
                <label className="flex items-center justify-between cursor-pointer">
                  <span className="text-white/70 text-sm">Parent Layer (AI Explanations)</span>
                  <input type="checkbox" checked={saveData.parentLayerEnabled}
                    onChange={e => updateSetting('parentLayerEnabled', e.target.checked)}
                    className="w-5 h-5 rounded" />
                </label>
                <label className="flex items-center justify-between cursor-pointer">
                  <span className="text-white/70 text-sm">Show Tutorials</span>
                  <input type="checkbox" checked={saveData.showTutorials}
                    onChange={e => updateSetting('showTutorials', e.target.checked)}
                    className="w-5 h-5 rounded" />
                </label>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/10 border-white/10">
            <CardContent className="p-4">
              <h3 className="text-white font-semibold mb-3">Your Stats</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="text-white/50">Sheep Herded</div><div className="text-white font-bold text-right">{saveData.totalSheepHerded}</div>
                <div className="text-white/50">Total Barks</div><div className="text-white font-bold text-right">{saveData.totalBarks}</div>
                <div className="text-white/50">Levels Done</div><div className="text-white font-bold text-right">{saveData.totalLevelsCompleted}</div>
                <div className="text-white/50">Perfect Herds</div><div className="text-white font-bold text-right">{saveData.perfectHerds}</div>
                <div className="text-white/50">Discoveries</div><div className="text-white font-bold text-right">{saveData.discoveryCount}</div>
                <div className="text-white/50">Daily Streak</div><div className="text-white font-bold text-right">{saveData.dailyStreak} days</div>
              </div>
            </CardContent>
          </Card>

          <Button variant="outline" onClick={() => {
            if (confirm('Reset all progress? This cannot be undone!')) store.resetSave();
          }} className="w-full border-red-500/50 text-red-400 hover:bg-red-500/10">
            Reset All Progress
          </Button>
        </div>
      </div>
    </motion.div>
  );
}

// ============================================================
// FARM SCREEN
// ============================================================
function FarmScreen() {
  const { setScreen, saveData } = useMistStore();

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="flex-1 p-4 sm:p-6 overflow-y-auto"
      style={{ background: 'linear-gradient(180deg, #2d1b00 0%, #4a3000 50%, #2d1b00 100%)' }}
    >
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <Button variant="ghost" onClick={() => setScreen('title')} className="text-white hover:bg-white/10">← Back</Button>
          <h2 className="text-2xl font-bold text-white flex-1">Your Farm</h2>
          <Badge className="bg-amber-700 text-white">{saveData.farmUpgrades.length} Upgrades</Badge>
        </div>

        <p className="text-amber-200/60 text-sm mb-4">As you complete levels and find discoveries, you unlock farm upgrades. Each one ties back to an AI concept you learned!</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {ALL_FARM_UPGRADES.map((upgrade: any) => {
            const owned = saveData.farmUpgrades.includes(upgrade.id);
            return (
              <Card key={upgrade.id} className={`${owned ? 'bg-amber-900/30 border-amber-500/30' : 'bg-black/20 border-white/10'}`}>
                <CardContent className="p-3 flex gap-3 items-start">
                  <span className={`text-2xl ${owned ? '' : 'grayscale opacity-30'}`}>{upgrade.icon}</span>
                  <div className="flex-1">
                    <p className={`text-sm font-semibold ${owned ? 'text-amber-200' : 'text-white/30'}`}>{upgrade.name}</p>
                    <p className={`text-xs mt-0.5 ${owned ? 'text-amber-300/60' : 'text-white/15'}`}>{owned ? upgrade.description : '???'}</p>
                    {owned && upgrade.aiConcept && (
                      <p className="text-amber-400/50 text-[10px] mt-1">AI: {upgrade.aiConcept}</p>
                    )}
                  </div>
                  {owned && <span className="text-green-400 text-xs">✓</span>}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}