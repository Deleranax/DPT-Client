import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Lava(pygame.sprite.Sprite):
    texture = "dpt.images.environment.liquids.Lava_Tile"
    textures = "dpt.images.environment.liquids.Lava_Tile_*"
    screen_width, screen_height = Game.surface.get_size()
    sounds = "dpt.sounds.sfx.sfx_snow"
    width = height = Game.TILESIZE
    offset_x = 0
    offset_y = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group,
                                      TileManager.deadly_object_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = [pygame.transform.scale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(
            self.textures)]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y

    def update(self):
        self.animation()

    def animation(self):
        self.image = self.frames[Game.anim_count_lava // 4]
