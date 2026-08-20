---
name: interactive-game-builder
description: Build interactive HTML5 Canvas browser games with React/Next.js integration. ALWAYS use this skill when the user mentions "game", "mini game", "arcade", "canvas game", "OIB Trail", "pelican", "Pelican Pooper", "parking", "Pier Parking", "interactive game", "browser game", "side-scroller", "text adventure", or "stealth game". This skill provides complete game loop patterns, sprite systems, collision detection, input handling, retro CRT monitor wrappers, and three ready-to-build OIB game templates.
---

# Interactive Game Builder

Browser games with HTML5 Canvas + React + TypeScript. All games wrap in the CRT monitor component. See `references/game-designs.md` for full OIB game design docs.

## 1. Canvas Game Loop

```typescript
function createGameLoop(
  canvas: HTMLCanvasElement,
  update: (state: any, dt: number) => any,
  render: (ctx: CanvasRenderingContext2D, state: any) => void,
  initialState: any
) {
  const ctx = canvas.getContext("2d")!;
  let state = initialState;
  let lastTime = 0;
  let frameId: number;

  function tick(timestamp: number) {
    const dt = Math.min((timestamp - lastTime) / 1000, 0.05);
    lastTime = timestamp;
    if (state.phase === "playing") state = update(state, dt);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    render(ctx, state);
    frameId = requestAnimationFrame(tick);
  }

  frameId = requestAnimationFrame((t) => { lastTime = t; tick(t); });
  return {
    getState: () => state,
    setState: (s: Partial<any>) => { state = { ...state, ...s }; },
    destroy: () => cancelAnimationFrame(frameId),
  };
}
```

## 2. React + Canvas Integration

```tsx
"use client";
import { useRef, useEffect } from "react";

interface GameCanvasProps {
  width: number;
  height: number;
  gameFactory: (canvas: HTMLCanvasElement) => { destroy: () => void };
}

export function GameCanvas({ width, height, gameFactory }: GameCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    const ctx = canvas.getContext("2d")!;
    ctx.scale(dpr, dpr);
    ctx.imageSmoothingEnabled = false;
    const game = gameFactory(canvas);
    return () => game.destroy();
  }, [width, height, gameFactory]);

  return <canvas ref={canvasRef} style={{ imageRendering: "pixelated", display: "block" }} tabIndex={0} />;
}
```

## 3. Sprite Animation

```typescript
class SpriteAnimator {
  private frame = 0;
  private elapsed = 0;

  constructor(
    private sheet: { image: HTMLImageElement; frameW: number; frameH: number; cols: number },
    private anim: { frames: number[]; duration: number; loop: boolean }
  ) {}

  update(dt: number) {
    this.elapsed += dt;
    if (this.elapsed >= this.anim.duration) {
      this.elapsed = 0;
      this.frame++;
      if (this.frame >= this.anim.frames.length)
        this.frame = this.anim.loop ? 0 : this.anim.frames.length - 1;
    }
  }

  draw(ctx: CanvasRenderingContext2D, x: number, y: number, scale = 1) {
    const idx = this.anim.frames[this.frame];
    const col = idx % this.sheet.cols, row = Math.floor(idx / this.sheet.cols);
    ctx.drawImage(this.sheet.image,
      col * this.sheet.frameW, row * this.sheet.frameH, this.sheet.frameW, this.sheet.frameH,
      x, y, this.sheet.frameW * scale, this.sheet.frameH * scale);
  }
}
```

## 4. Collision Detection

```typescript
// AABB (rectangles)
function aabb(a: {x:number,y:number,w:number,h:number}, b: typeof a): boolean {
  return a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.h && a.y+a.h > b.y;
}

// Circle
function circleHit(a: {x:number,y:number,r:number}, b: typeof a): boolean {
  const dx = a.x-b.x, dy = a.y-b.y;
  return Math.sqrt(dx*dx+dy*dy) < a.r+b.r;
}

// Point-in-cone (for stealth detection)
function pointInCone(px:number, py:number, cx:number, cy:number,
  angle:number, spread:number, range:number): boolean {
  const dx = px-cx, dy = py-cy;
  if (Math.sqrt(dx*dx+dy*dy) > range) return false;
  const diff = Math.atan2(Math.sin(Math.atan2(dy,dx)-angle), Math.cos(Math.atan2(dy,dx)-angle));
  return Math.abs(diff) < spread;
}
```

## 5. Input Handling

```typescript
class InputManager {
  keys: Record<string, boolean> = {};
  private prev: Record<string, boolean> = {};

  constructor(target: HTMLElement | Window = window) {
    target.addEventListener("keydown", (e: any) => { this.keys[e.code] = true; e.preventDefault(); });
    target.addEventListener("keyup", (e: any) => { this.keys[e.code] = false; e.preventDefault(); });
  }

  update() { this.prev = { ...this.keys }; }
  isDown(code: string) { return !!this.keys[code]; }
  wasPressed(code: string) { return this.keys[code] && !this.prev[code]; }

  direction(): { x: number; y: number } {
    let x = 0, y = 0;
    if (this.isDown("ArrowLeft") || this.isDown("KeyA")) x--;
    if (this.isDown("ArrowRight") || this.isDown("KeyD")) x++;
    if (this.isDown("ArrowUp") || this.isDown("KeyW")) y--;
    if (this.isDown("ArrowDown") || this.isDown("KeyS")) y++;
    const len = Math.sqrt(x*x+y*y);
    return len > 0 ? { x: x/len, y: y/len } : { x: 0, y: 0 };
  }
}
```

## 6. Score & State

```typescript
class GameStateManager<T extends Record<string, any>> {
  private listeners: Array<(s: T) => void> = [];
  constructor(private state: T) {}

  get<K extends keyof T>(key: K): T[K] { return this.state[key]; }
  set<K extends keyof T>(key: K, val: T[K]) {
    this.state = { ...this.state, [key]: val };
    this.listeners.forEach(fn => fn(this.state));
  }
  subscribe(fn: (s: T) => void) {
    this.listeners.push(fn);
    return () => { this.listeners = this.listeners.filter(l => l !== fn); };
  }
}
```

## 7. Sound Effects (Web Audio API)

```typescript
class GameAudio {
  private ctx = new AudioContext();
  private buffers = new Map<string, AudioBuffer>();
  private gain: GainNode;

  constructor() { this.gain = this.ctx.createGain(); this.gain.connect(this.ctx.destination); }

  async load(name: string, url: string) {
    const buf = await (await fetch(url)).arrayBuffer();
    this.buffers.set(name, await this.ctx.decodeAudioData(buf));
  }

  play(name: string, vol = 1) {
    if (this.ctx.state === "suspended") this.ctx.resume();
    const src = this.ctx.createBufferSource();
    const g = this.ctx.createGain();
    g.gain.value = vol;
    src.buffer = this.buffers.get(name)!;
    src.connect(g).connect(this.gain);
    src.start();
  }

  blip(freq = 440, dur = 0.1, type: OscillatorType = "square") {
    if (this.ctx.state === "suspended") this.ctx.resume();
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type; o.frequency.value = freq;
    g.gain.setValueAtTime(0.3, this.ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + dur);
    o.connect(g).connect(this.gain);
    o.start(); o.stop(this.ctx.currentTime + dur);
  }
}
```

## 8. CRT Monitor Wrapper

The signature retro display. Every OIB game lives inside this. Uses Press Start 2P font, scanline overlay, phosphor glow, screen curvature.

```tsx
"use client";
import { ReactNode } from "react";

interface CRTMonitorProps {
  children: ReactNode;
  width?: number; height?: number;
  phosphor?: "green" | "amber" | "white";
  title?: string;
  onPowerToggle?: () => void;
  isPoweredOn?: boolean;
}

const GLOW = {
  green: { glow: "#00ff41", dim: "#003b00", text: "#00ff41" },
  amber: { glow: "#ffb000", dim: "#3b2800", text: "#ffb000" },
  white: { glow: "#ffffff", dim: "#1a1a2e", text: "#e0e0e0" },
};

export function CRTMonitor({ children, width=640, height=480,
  phosphor="green", title="OIB ARCADE", onPowerToggle, isPoweredOn=true }: CRTMonitorProps) {
  const c = GLOW[phosphor];
  return (
    <>
      <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet"/>
      <div style={{ display:"inline-flex", flexDirection:"column", alignItems:"center",
        background:"linear-gradient(180deg,#3a3a3a,#2a2a2a,#1a1a1a)", borderRadius:16,
        padding:"12px 16px 20px", boxShadow:"0 8px 32px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.1)" }}>
        <div style={{ fontFamily:"'Press Start 2P',monospace", fontSize:10, color:"#888",
          letterSpacing:4, marginBottom:8 }}>{title}</div>
        <div style={{ display:"flex", alignItems:"center", justifyContent:"center",
          background:"#1a1a1a", borderRadius:12, padding:24, border:"2px solid #0f0f0f",
          boxShadow:"inset 0 2px 8px rgba(0,0,0,0.8)" }}>
          <div style={{ position:"relative", width, height, borderRadius:8, overflow:"hidden",
            border:"1px solid #333", background: isPoweredOn ? c.dim : "#0a0a0a",
            boxShadow: isPoweredOn ? `inset 0 0 60px ${c.dim},0 0 20px ${c.glow}33` : "none" }}>
            {isPoweredOn && <div style={{ position:"absolute", inset:0, zIndex:2, pointerEvents:"none",
              background:"repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.15) 2px,rgba(0,0,0,0.15) 4px)" }}/>}
            {isPoweredOn && <div style={{ position:"absolute", inset:0, zIndex:3, pointerEvents:"none",
              background:"radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.03),transparent 60%)" }}/>}
            <div style={{ position:"relative", width:"100%", height:"100%", zIndex:1 }}>
              {isPoweredOn ? children : <div style={{ display:"flex", alignItems:"center",
                justifyContent:"center", height:"100%", color:"#333", fontSize:12,
                fontFamily:"'Press Start 2P',monospace" }}>SIGNAL LOST</div>}
            </div>
          </div>
        </div>
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", marginTop:12, gap:4 }}>
          <button onClick={onPowerToggle} style={{ width:16, height:16, borderRadius:"50%",
            border:"2px solid #555", cursor:"pointer",
            backgroundColor: isPoweredOn ? "#4ade80" : "#6b7280",
            boxShadow: isPoweredOn ? "0 0 8px #4ade80" : "none" }} aria-label="Power"/>
          <div style={{ fontFamily:"'Press Start 2P',monospace", fontSize:6, color:"#666",
            letterSpacing:2 }}>POWER</div>
        </div>
      </div>
    </>
  );
}
```

## 9. Game Templates

### Side-Scroller: Pelican Pooper

Horizontal flight, gravity-based droppings, scrolling tourist targets. Key structure:

```typescript
// State shape
interface PelicanState {
  bird: { x: number; y: number; vy: number };
  droppings: { x: number; y: number; vy: number; active: boolean }[];
  tourists: { x: number; y: number; w: number; h: number; speed: number; hit: boolean }[];
  score: number; lives: number; scrollSpeed: number;
  phase: "menu" | "playing" | "gameover";
}

// Core update: bird flaps up, drops fall with gravity, tourists scroll left
// UP/Space = flap (bird.vy = -250), DOWN/S = drop projectile
// Gravity: vy += 600 * dt for droppings, 600 * 0.3 * dt for bird
// Collision: AABB between droppings and tourists
// Difficulty: scrollSpeed = 100 + score * 0.05
// Tourist types: Chair(50), Jogger(100), Selfie(150), Family(200), Lifeguard(-100)
```

### Text Adventure: OIB Trail

React state machine, no Canvas needed. Resources: gas, patience, sunscreen, snacks, cash.

```typescript
// State shape
type Scene = "start" | "driving" | "event" | "store" | "arrived" | "dead";
interface Resources { gas: number; patience: number; sunscreen: number; snacks: number; cash: number; }
interface GameEvent {
  text: string;
  choices: { label: string; effect: Partial<Resources> }[];
}

// Random events: drawbridge, seagull attack, tourist traffic, gas station line,
// AC failure, Florida Man crossing. See references/game-designs.md for full list.
// Lose: gas=0 or patience=0. Win: milesLeft=0.
// UI: green phosphor CRT, resource bars, scrolling log, choice buttons.
// Route choices at milestones: A1A (scenic), Highway 17 (fast), Back Roads (random).
```

### Top-Down Stealth: Pier Parking Panic

Player avoids golf-cart patrol enemies with vision cones. Park in highlighted spots.

```typescript
// State shape
interface PierState {
  player: { x: number; y: number; speed: number; hidden: boolean; parkedCount: number };
  enemies: {
    x: number; y: number; speed: number;
    patrolPath: { x: number; y: number }[];
    patrolIndex: number; angle: number;
    coneSpread: number; coneRange: number;
    alerted: boolean; alertTimer: number;
  }[];
  spots: { x: number; y: number; w: number; h: number; filled: boolean }[];
  detectionLevel: number; // 0-100, 100=caught
  phase: "playing" | "caught" | "won";
}

// Enemy AI: follow patrolPath waypoints, face movement direction
// Alert states: unaware (yellow), suspicious (orange, 1.5x speed), alert (red, 1.8x speed)
// Detection: pointInCone check each frame, fills meter proportionally
// Sprint (shift): faster but detection fills 2x as fast
// Hiding: behind cars/dumpsters reduces detection rate by 80%
// Draw cone: ctx arc from enemy position, colored by alert state
// Power-ups: sunglasses (invisible 5s), beach towel (distraction), flip flops (silent 10s)
```

## 10. Next.js Embedding

```tsx
// app/arcade/[game]/page.tsx — dynamic loading, no SSR for canvas games
import dynamic from "next/dynamic";

const games: Record<string, ReturnType<typeof dynamic>> = {
  "pelican-pooper": dynamic(() => import("@/games/pelican-pooper/PelicanGame").then(m => m.PelicanGame), { ssr: false }),
  "oib-trail": dynamic(() => import("@/games/oib-trail/OIBTrailGame").then(m => m.OIBTrailGame), { ssr: false }),
  "pier-parking": dynamic(() => import("@/games/pier-parking/PierParkingGame").then(m => m.PierParkingGame), { ssr: false }),
};

export default function GamePage({ params }: { params: { game: string } }) {
  const Game = games[params.game];
  if (!Game) return <div>Game not found</div>;
  return <div style={{ minHeight:"100vh", background:"#0a0a0a", display:"flex",
    alignItems:"center", justifyContent:"center" }}><Game /></div>;
}
```

## 11. Mobile Touch Controls

```tsx
"use client";
import { useRef, useEffect, useCallback } from "react";

export function TouchControls({ onDirection, onAction }: {
  onDirection: (d: {x:number,y:number}) => void; onAction: () => void;
}) {
  const originRef = useRef({ x: 0, y: 0 });

  const handleStart = useCallback((e: React.TouchEvent) => {
    const t = e.touches[0];
    originRef.current = { x: t.clientX, y: t.clientY };
  }, []);

  const handleMove = useCallback((e: React.TouchEvent) => {
    e.preventDefault();
    const t = e.touches[0];
    const dx = t.clientX - originRef.current.x, dy = t.clientY - originRef.current.y;
    const max = 40, dist = Math.min(Math.sqrt(dx*dx+dy*dy), max);
    const ang = Math.atan2(dy, dx);
    onDirection({ x: Math.cos(ang)*dist/max, y: Math.sin(ang)*dist/max });
  }, [onDirection]);

  return (
    <div style={{ position:"fixed", bottom:20, left:0, right:0, display:"flex",
      justifyContent:"space-between", padding:"0 24px", pointerEvents:"none" }}>
      <div onTouchStart={handleStart as any} onTouchMove={handleMove as any}
        onTouchEnd={() => onDirection({x:0,y:0})}
        style={{ width:100, height:100, borderRadius:"50%", background:"rgba(255,255,255,0.15)",
          border:"2px solid rgba(255,255,255,0.3)", display:"flex", alignItems:"center",
          justifyContent:"center", pointerEvents:"auto", touchAction:"none" }}>
        <div style={{ width:40, height:40, borderRadius:"50%", background:"rgba(255,255,255,0.3)" }}/>
      </div>
      <button onTouchStart={(e) => { e.preventDefault(); onAction(); }}
        style={{ width:70, height:70, borderRadius:"50%", background:"rgba(255,65,54,0.4)",
          border:"2px solid rgba(255,65,54,0.6)", color:"#fff", fontSize:20,
          fontFamily:"'Press Start 2P',monospace", pointerEvents:"auto", touchAction:"none" }}>A</button>
    </div>
  );
}
```

## 12. Leaderboard

### localStorage (offline)

```typescript
const KEY = "oib-arcade-leaderboard";

function getLeaderboard(game: string, max = 10) {
  const all = JSON.parse(localStorage.getItem(KEY) || "[]");
  return all.filter((e: any) => e.game === game).sort((a: any, b: any) => b.score - a.score).slice(0, max);
}

function addScore(game: string, name: string, score: number) {
  const all = JSON.parse(localStorage.getItem(KEY) || "[]");
  all.push({ name, score, date: new Date().toISOString(), game });
  localStorage.setItem(KEY, JSON.stringify(all));
  return getLeaderboard(game);
}

function isHighScore(game: string, score: number, max = 10) {
  const board = getLeaderboard(game, max);
  return board.length < max || score > (board[board.length - 1]?.score ?? 0);
}
```

### Supabase (online)

```sql
-- Setup
create table leaderboard (
  id uuid default gen_random_uuid() primary key,
  game text not null, player_name text not null, score integer not null,
  created_at timestamptz default now()
);
create index idx_lb on leaderboard(game, score desc);
alter table leaderboard enable row level security;
create policy "read" on leaderboard for select using (true);
create policy "insert" on leaderboard for insert with check (true);
```

```typescript
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

async function getLeaderboard(game: string, limit = 10) {
  const { data } = await sb.from("leaderboard").select("player_name,score,created_at")
    .eq("game", game).order("score", { ascending: false }).limit(limit);
  return data;
}

async function submitScore(game: string, name: string, score: number) {
  await sb.from("leaderboard").insert({ game, player_name: name, score });
}
```
