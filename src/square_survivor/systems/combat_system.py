import pygame
from typing import List
from ..entities.player import Player
from ..entities.enemy import Enemy
from ..entities.weapons.base_weapon import Weapon

class CombatSystem:
    """Managed handler for weapon lifecycle and collision logistics."""

    def process_weapons(self, player: Player, enemies: List[Enemy], dt: float):
        """Update weapons and handle collisions within the sprite group."""
        # Update all weapons in the player's weapon group
        # This will call update() on each weapon entity
        player.weapons.update(dt)

        # Handle collisions
        for weapon in player.weapons:
            if not weapon.active:
                continue
            
            # Use pygame's optimized collision check (sprite vs list/group)
            hit_enemies = pygame.sprite.spritecollide(weapon, enemies, False)
            
            for enemy in hit_enemies:
                if not enemy.active:
                    continue
                
                # Apply damage
                enemy.hp -= weapon.damage
                
                # If the weapon has health (like SaturnSquare), reduce it
                if hasattr(weapon, 'hp'):
                    weapon.hp -= enemy.damage
                    if weapon.hp <= 0:
                        weapon.active = False
                        weapon.kill()
                
                # Apply knockback
                if weapon.knockback > 0:
                    weapon.knockback_logic(enemy, player)

        # Remove inactive weapons (handled by pygame.sprite.Group if using kill())
        # but just as a safety check for non-sprite weapons if any exist
        for weapon in list(player.weapons):
            if not weapon.active:
                weapon.kill()
