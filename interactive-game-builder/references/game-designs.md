# OIB Arcade - Game Design Documents

Three browser games set in the Ocean Isle Beach (OIB) universe. Each game is wrapped in the retro CRT monitor component and built with React + HTML5 Canvas (or React state for text adventures).

---

## 1. OIB Trail

**Genre**: Text Adventure / Resource Management
**Inspiration**: Oregon Trail
**Tagline**: "You have died of sunburn."

### Premise

It is summer at Ocean Isle Beach, NC. You are out of chicken tenders. The nearest Publix is a grueling drive through tourist-clogged roads, broken AC, and the unrelenting Carolina sun. Your mission: get to Publix and back with your sanity intact.

### Resources

| Resource | Starting Value | Max | What Drains It |
|----------|---------------|-----|----------------|
| Gas | 80% | 100% | Driving, idling in traffic, detours |
| Patience | 100% | 100% | Traffic, events, waiting, heat |
| Sunscreen | 5 applications | 10 | Sun exposure, open windows |
| Snacks | 4 | 10 | Eating to restore patience, seagull theft |
| Cash | $60 | $200 | Gas, supplies, bribes |

### Lose Conditions

- Gas hits 0: Stranded on Four Mile Road
- Patience hits 0: You turn around and go home empty-handed
- Sunscreen hits 0 while windows are down: Severe sunburn (game over)

### Win Condition

Reach Publix (0 miles remaining) with any resources above zero.

### Random Events

1. **Drawbridge Up** - Tourist boats passing through. Wait (patience drain), detour (gas drain), or honk (big patience drain).
2. **Seagull Attack** - A flock descends. Close windows and sweat, fight back with napkins, or offer tribute snacks.
3. **Tourist Traffic Jam** - Someone parallel parking a rented RV on Four Mile Road. Wait, cut through beach lot, or help them park.
4. **Gas Station Line** - 12 cars deep. Wait in line (patience + gas refill), skip it, or pay marina prices.
5. **AC Dies** - The sun is brutal. Windows down (sunscreen drain), stop to fix (gas drain), or buy ice (cash drain).
6. **Brunswick Man Crossing** - A man walking his alligator across the crosswalk. All options cost patience.
7. **Souvenir Shop Distraction** - Passenger wants to stop. Refuse (patience drain on them), allow it (time + cash), or compromise on a gas station souvenir.
8. **Beach Cruiser Cyclists** - A pack of 12 riding three-wide on the road. Honk, wait, or go off-road.
9. **Ice Cream Truck** - Kids are running into the street. Emergency stop (patience), buy ice cream (cash + patience boost), or take the long way around.
10. **Rain Squall** - Sudden Carolina downpour. Visibility drops, pull over (patience), keep driving slow (gas drain), or floor it (risk event).

### Route Choices

At key milestones, the player picks a route:
- **Four Mile Road (Scenic)**: More events, less gas usage
- **Highway 17 (Fast)**: Fewer events, more gas, tourist traps
- **Back Roads**: Unpredictable, chance of shortcuts or dead ends

### UI Design

- Green phosphor CRT display
- Resource bars at the top (ASCII-style progress bars)
- Scrolling text log in the center
- Choice buttons at the bottom
- Pixel art scene illustrations for major events

### Scoring

- Base: 1000 points for reaching Publix
- Bonus: Remaining resources x10
- Speed bonus: Miles per event encountered
- Style bonus: Funny choice combinations

---

## 2. Pelican Pooper

**Genre**: Side-Scroller / Arcade
**Inspiration**: Flappy Bird meets Angry Birds
**Tagline**: "Whitewash the tourists."

### Premise

You are a pelican. You have eaten too many fish. Below you, sunburnt tourists litter the beach with their umbrellas, coolers, and bad vibes. Nature calls. Repeatedly.

### Mechanics

**Player (Pelican)**:
- Flies horizontally at screen left, moves up/down
- UP arrow / W / Space: Flap upward
- DOWN arrow / S: Release a dropping
- Cannot go below the midpoint of the screen (stay airborne)
- Has a "fish meter" that depletes with each drop, refills by flying over the pier (fish pickup)

**Droppings (Projectiles)**:
- Affected by gravity (parabolic arc)
- Limited to 3 active at once
- Splash radius on impact
- Different sizes based on fish meter level

**Tourists (Targets)**:
- Scroll right to left at varying speeds
- Different types with different point values:
  - **Beach Chair Tourist** (50 pts): Stationary, easy target
  - **Jogger** (100 pts): Moving fast, narrow hitbox
  - **Selfie Tourist** (150 pts): Stops periodically to take photos (vulnerability window)
  - **Tourist Family** (200 pts): Large group, requires precision to hit the dad carrying the cooler
  - **Lifeguard** (-100 pts): Penalty target, do not hit

**Obstacles**:
- Seagulls flying across the screen (collision = lose a life)
- Beach umbrellas (block droppings)
- Kites (entanglement risk)

### Progression

- Speed increases over time
- More tourist types appear
- Obstacles become more frequent
- Every 1000 points: brief "Feeding Frenzy" bonus round over the pier

### Visual Style

- Amber phosphor CRT
- Pixel art sprites
- Parallax scrolling: ocean, beach, boardwalk
- Splat effects with white pixel explosions
- Chunky score counter in the corner

### Sound Design

- Retro blip for flapping
- Descending whistle for dropping
- Satisfying splat on hit
- Angry tourist sound bite on hit
- Warning buzz near seagulls

### Scoring

- Points per tourist type (see above)
- Combo multiplier for consecutive hits without missing
- "Perfect Drop" bonus for direct headshots
- End-of-game tally with funny stats ("Shirts ruined: 12")

---

## 3. Pier Parking Panic

**Genre**: Top-Down Stealth
**Inspiration**: Metal Gear Solid meets parking simulator
**Tagline**: "Avoid the Jersey guy in the golf cart."

### Premise

You need to park at the OIB pier, but every spot is being patrolled by an overzealous parking enforcer from New Jersey who drives a golf cart with a flashing light. One wrong move and you get a ticket (or worse, towed). Sneak to open parking spots while avoiding detection.

### Mechanics

**Player**:
- Top-down view, 8-directional movement (WASD or arrow keys)
- Walk speed (normal) or sprint (shift, but makes noise)
- Can hide behind parked cars, dumpsters, bushes
- Objective: reach and "park in" all highlighted spots

**Jersey Guy (Enemy AI)**:
- Patrols set routes in a golf cart
- Has a visible detection cone (like a flashlight beam)
- Detection states:
  - **Unaware** (yellow cone): Normal patrol
  - **Suspicious** (orange cone): Heard something, investigates nearby
  - **Alert** (red cone): Spotted you, chases at 1.8x speed
- Returns to patrol after losing sight for 5 seconds
- Multiple enemies on later levels

**Detection System**:
- Detection meter fills when in enemy cone of vision
- Fills faster when sprinting
- Fills slower when partially hidden
- At 100%: CAUGHT (lose a life)
- Drains slowly when out of sight

**Parking Spots**:
- Highlighted with dashed yellow outlines
- Walk into one and hold for 2 seconds to "park"
- Some spots are decoys (fire hydrant, handicap without permit)
- Filled spots turn green

**Power-ups**:
- **Sunglasses**: Temporarily invisible to detection
- **Beach Towel**: Drop to create a distraction
- **Ice Cream**: Lure enemy away from patrol route
- **Flip Flops**: Silent movement for 10 seconds

### Level Design

Each level is a different section of the pier/beach area:
1. **Tutorial**: One enemy, three spots, simple layout
2. **Pier Entrance**: Two enemies, tight corridors between cars
3. **Beach Lot**: Open area, multiple enemies, few hiding spots
4. **VIP Section**: Fast enemies, narrow paths, timed gates
5. **The Gauntlet**: All enemies, all mechanics, one last spot

### Visual Style

- White phosphor CRT (cleaner look for the top-down perspective)
- Simple geometric sprites (rectangles with detail accents)
- Detection cones rendered as semi-transparent colored triangles
- Mini-map in the corner showing enemy positions
- Parking lines and lot markings drawn with dashed strokes

### Sound Design

- Golf cart motor hum (louder when enemy is near)
- Footstep sounds (louder when sprinting)
- "Hey! You can't park there!" on detection
- Satisfying click when parking is complete
- Tension music that ramps with detection level

### Scoring

- Base: 500 points per spot parked
- Time bonus: Faster completion = more points
- Ghost bonus: Never detected = 2x multiplier
- No sprint bonus: Extra style points
- Level completion shows a "Parking Report Card"

---

## Shared Systems

All three games share:

1. **CRT Monitor Wrapper**: Retro display with scanlines, phosphor glow, power button
2. **Leaderboard**: localStorage for offline, Supabase for shared scores
3. **Sound Engine**: Web Audio API with retro blip synthesizer
4. **Mobile Controls**: Virtual joystick + action button overlay
5. **Next.js Integration**: Dynamic imports, `/arcade/[game]` routing

## Implementation Priority

1. OIB Trail (simplest, React state only, no Canvas needed)
2. Pelican Pooper (moderate, Canvas + basic physics)
3. Pier Parking Panic (most complex, AI pathfinding + stealth systems)
