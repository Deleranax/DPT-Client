import pygame
import math
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class Reverse(pygame.sprite.Sprite):
    """Effet reverse"""
    reverse = "dpt.images.effects.star"

    def __init__(self):
        """Crée l'effet reverse"""
        pygame.sprite.Sprite.__init__(self, TileManager.effects_group)
        self.full_heart = pygame.transform.smoothscale(RessourceLoader.get(Reverse.reverse), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.image = self.full_heart
        self.rect = [0, 970 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO]

    def update(self):
        """Affiche l'effet"""
        Game.surface.blit(self.image, self.rect)
