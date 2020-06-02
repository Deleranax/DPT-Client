#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class FlowerTulipeRed(pygame.sprite.Sprite):
    texture = "dpt.images.environment.plants.flowers.Flower_Tulipe_Red"
    sounds = "dpt.sounds.sfx.sfx_leaves"
    width = Game.TILESIZE // 3
    height = Game.TILESIZE
    offset_x = -(width // 2)
    offset_y = -(height // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
