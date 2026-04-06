Create a complete, playable 2D Top-Down Roguelike survival game in a single HTML5 file (using Vanilla JavaScript and Canvas API).

Core Gameplay:

Player survives for 10 minutes against endless waves of enemies spawning off-screen.

Simple controls: WASD or Arrow keys to move, Spacebar to Dash.

Automatic Combat: An "Explosion" attack triggers automatically around the player at a set interval.

Enemies: Simple AI that chases the player constantly.

Systems & Mechanics:

Procedural Map: Generate a grid-based infinite-feeling world with "Square Obstacles". Include a density parameter to control how many obstacles spawn.

XP & Leveling: Enemies drop XP. Collecting enough XP triggers a Level-Up pause menu where players choose 1 of 3 random upgrades:

Explosion: Increase Damage, Increase Radius, Add Enemy Knockback.

Dash: Decrease Cooldown, Increase Distance, Reduce Stamina/Mana cost.

Stats: Include Health (HP) and Mana/Stamina bars on a clean UI.

Screens & Flow:

Main Menu: Simple design with "Start Game" and "Highscore" buttons.

In-Game UI: 10-minute countdown timer, XP bar, Kill counter.

Game Over Screen: If HP reaches 0, show total kills/XP. Allow player to enter their name for the Highscore.

Win Screen: If the player survives 10 minutes, show a victory message and save to Highscore.

Highscore System: Use browser LocalStorage to save and display a persistent leaderboard.

Visuals:

Minimalist "Vibe": Use colored squares/shapes for player, enemies, and obstacles.

Ensure the code is self-contained, well-commented, and runs immediately when opened in a browser.
