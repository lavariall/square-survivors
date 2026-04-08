---
trigger: always_on
glob: src/square_survivor/**/*.py
description: Architecural guidelines for the Square Survivor game engine.
---

# 🏗️ Square Survivor Architecture Guidelines

This document outlines the architectural principles and patterns for the Square Survivor game engine. Use these guidelines when adding new features or refactoring existing code to ensure a modular and scalable codebase.

## 1. Core Engine & State Management

The game follows a **Finite State Machine (FSM)** pattern. All game states must inherit from `GameState` and be managed by the `Engine`. Concrete states and their base class are located in the `states/` package.

- **Engine**: The central controller responsible for the main loop, state transitions, and high-level pygame initialization (found in `core/engine.py`).
- **GameState**: Abstract base class defining `handle_event`, `update`, and `draw` (found in `states/base.py`).
    - `PlayState`: The main gameplay loop (found in `states/play.py`).
    - `LevelUpState`: Handles upgrade selection with a dynamic grid layout (found in `states/level_up.py`).
    - **MenuState** / **GameOverState**: Handle UI, difficulty selection, and highscore persistence.

**Guideline**: Never implement gameplay logic directly in `engine.py`. New screens or major modes must be implemented as new `GameState` subclasses within the `states/` package. Selection of game properties (like difficulty) should happen in `MenuState` and be passed into `PlayState`. Transitions to modal states (like LevelUp) should use a **pending queue** (e.g. `player.level_ups_pending`) at the end of the update loop to prevent state-clobbering when multiple events occur in one frame.

## 2. Entity System

Entities (Player, Enemy, XPOrb) should maintain a strict separation between **logic** and **presentation**.

- **Coordinate Systems**: Use **World Coordinates** for all physics and logic. Only convert to **Screen Coordinates** (using `camera_offset`) inside the `draw()` method.
- **Base Class**: All moving game objects must inherit from `Entity` (found in `entities/base_entity.py`).
- **Variants**: For enemy variations like **Elites**, use an `is_elite` flag rather than a new class if behavior remains primarily the same (e.g., just health/size/XP changes).
- **Composition over Inheritance**: Prefer adding stats/flags to entities rather than creating deep inheritance trees.

## 3. Modular Upgrade System

The upgrade system is the most decoupled part of the framework, using an **Automatic Registry Pattern**.

### 🛠️ Implementing New Upgrades
Decorate your upgrade class with `@UpgradeManager.register`. 

```python
@UpgradeManager.register
class MyNewUpgrade(Upgrade):
    name = "Fire Boost"
    description = "Increases something by 20%"
    likelihood = 100  # Default selection weight
    
    def apply(self, player: Player):
        # Implementation logic here
        pass
```

### ⚖️ Balancing & Control
- **Likelihood**: Use the `likelihood` attribute for rarity tuning (higher = more common).
- **Dynamic Pool**: Use `self.disable()` within an upgrade's `apply` method to permanently remove it from the pool (e.g., for tier-based upgrades or maximum levels).
- **Selection**: `UpgradeManager.get_random_choices` performs **weighted sampling without replacement**.

## 4. Systems & Utility Logic

Functionality like combat, spawning, and UI should be partitioned into standalone systems.

- **WaveManager**: Autonomous logic for spawning enemies outside the player's viewport. It scales **Elite Chance** and **Spawn Numbers** based on the current `DifficultySetting`.
- **CombatSystem**: Stateless processor for explosions and damage calculations.
- **MapGenerator**: Handles procedural generation and tile-based collision data, scaling **Obstacle Density** based on difficulty.
- **Entity Management**: To maintain performance, entities with high volume (like `XPOrb`) use a `timer` for lifespan and a `MAX_XP_ORBS` cap with fallback recycling (reusing the oldest active orb if the cap is reached).

## 5. UI & Presentation

- **Components**: Use `ui/components.py` for reusable UI elements (Buttons, ProgressBars, InputBoxes).
- **Layouts**: For complex menus (like LevelUp), implement dynamic centering and grid layout logic to support varied content counts (e.g., up to 7 upgrade choices).
- **Navigation**: All menus must support **hybrid mouse/keyboard/joystick controls**. 
    - Sync a `selected_index` with `MOUSEMOTION` hover states in `handle_event`. 
    - Handle discrete navigation (W, A, S, D, Arrow Keys, Analog Sticks) in the `update()` method rather than `handle_event`. This prevents "double-triggering" when multiple events (like `TEXTINPUT` or joystick noise) occur in a single frame.
    - Use code abstraction (e.g., `InputAction` enum) to separate physical keys from logic.
- **Colors & Constants**: Always reference `constants.py`. Never use hardcoded RGB/HEX values in logic or draw calls.
- **Semantic Coloring**: Use semantic constants (`PLAYER_COLOR`, `ENEMY_COLOR`, `XP_ORB_COLOR`) rather than generic theme labels. This ensures that gameplay entities remain visually decoupled from the global UI theme.

## 6. Persistence & Data

- **Highscores**: Stored as JSON in `highscores.json`.
- **Game Constants**: Configuration for map size, game time, and window settings reside in `constants.py`.

## 7. Packaging & Distribution

The game is designed for standalone distribution on both Windows and Linux.

- **Windows**: Use `PyInstaller` natively. Standard output is a `.exe` file in the `dist/` folder.
- **Linux**: To ensure compatibility across different distributions (like Linux Mint or Ubuntu), use the **Docker-based build pipeline** (`build_linux.ps1`). 
    - This compiles the game against a stable GLIBC version in a `python-slim` container.
    - The output is an extensionless standalone binary.
- **Asset Bundling**: If adding new binary assets (images, sounds), update the `SquareSurvivor.spec` file under the `datas` list to ensure they are bundled into the final executable.

---

## 8. Git Workflow & Branching

To ensure the stability of the public repository, the following branching strategy is strictly enforced.

- **Main Branch Protection**: The `main` branch is reserved for stable, tested code. **Never commit directly to `main`.**
- **Active Branch Verification**: Before performing any commit or push, you MUST verify your current active branch.
  ```powershell
  git branch
  ```
- **Feature Branches**: All implementation work must occur in dedicated feature or fix branches (e.g., `feat/new-upgrade` or `fix/collision-bug`).
- **Review Requirement**: Merging into `main` should ideally happen via Pull Requests (PRs) after a final verification pass.

---

> [!TIP]
> Always decouple your features. If a new mechanic can be implemented as an `Upgrade` or a standalone `System`, it should be!
