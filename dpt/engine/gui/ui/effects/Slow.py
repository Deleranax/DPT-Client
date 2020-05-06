import math
import pygame
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class Slow(pygame.sprite.Sprite):
    slow = "dpt.images.effects.slow"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, TileManager.effects_group)
        self.full_heart = pygame.transform.smoothscale(RessourceLoader.get(Slow.slow), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.image = self.full_heart
        self.rect = [0, 980 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO]

    def update(self):
        Game.surface.blit(self.image, self.rect)
