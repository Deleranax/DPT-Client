import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Lever(pygame.sprite.Sprite):
    texture = "dpt.images.environment.lever.Lever_Left"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = height = Game.TILESIZE
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group, TileManager.interactible_blocks_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.x = x
        self.y = y
        self.clicked = False
        self.clicked2 = False
        self.right = False
        self.left = True
        self.set = False
        if TileManager.is_loading_level:
            self.attributing = False
            TileEditor.attributing = False
        else:
            self.attributing = True
            TileEditor.attributing = True
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        if self.x + self.offset_x <= mousePos[0] - TileManager.camera.last_x <= self.x + self.offset_x + self.width and self.y + self.offset_y <= mousePos[1] <= self.y + self.offset_y + self.height:
            if mouse_buttons[0] == 1 and not self.clicked and self.rect.left - TileManager.camera.last_x - math.floor(50 * Game.DISPLAY_RATIO) <= Game.player_sprite.rect.right - TileManager.camera.last_x <= self.rect.left - TileManager.camera.last_x + math.floor(300 * Game.DISPLAY_RATIO):
                self.clicked = True
                if not TileEditor.is_editing:
                    if self.left:
                        self.left = False
                        self.right = True
                        texture = "dpt.images.environment.lever.Lever_Right"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                        data = TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]
                        if "assignement" in data:
                            for interact in TileManager.interactible_blocks_group:
                                positions = [tuple(map(int, i.split(", "))) for i in data["assignement"]]
                                for pos in positions:
                                    try:
                                        if hasattr(interact, "x") and hasattr(interact, "y"):
                                            if interact.x == pos[0] and interact.y == pos[1]:
                                                interact.activate()
                                        elif interact.rect.x - TileManager.camera.last_x == pos[0] and interact.rect.y == pos[1]:
                                            interact.activate()
                                        elif (interact.rect.x - TileManager.camera.last_x) // Game.TILESIZE == pos[0] and interact.rect.y // Game.TILESIZE == pos[1]:
                                            interact.activate()
                                    except AttributeError:
                                        continue
                    elif self.right:
                        self.right = False
                        self.left = True
                        texture = "dpt.images.environment.lever.Lever_Left"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                        data = TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]
                        if "assignement" in data:
                            for interact in TileManager.interactible_blocks_group:
                                positions = [tuple(map(int, i.split(", "))) for i in data["assignement"]]
                                for pos in positions:
                                    try:
                                        if hasattr(interact, "x") and hasattr(interact, "y"):
                                            if interact.x == pos[0] and interact.y == pos[1]:
                                                interact.deactivate()
                                        elif interact.rect.x - TileManager.camera.last_x == pos[0] and interact.rect.y == pos[1]:
                                            interact.deactivate()
                                        elif (interact.rect.x - TileManager.camera.last_x) // Game.TILESIZE == pos[0] and interact.rect.y // Game.TILESIZE == pos[1]:
                                            interact.deactivate()
                                    except AttributeError:
                                        continue
                elif TileEditor.is_editing:
                    self.attributing = True
                    TileEditor.attributing = True
            elif mouse_buttons[0] != 1 and self.clicked:
                self.clicked = False
        if TileEditor.is_editing and self.attributing:
            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y + 30), (mousePos[0], mousePos[1]), 1)
            if mouse_buttons[0] == 1 and not self.clicked2:
                self.clicked2 = True
                for sprites in TileManager.interactible_blocks_group:
                    if hasattr(sprites, "customPlacement"):
                        if sprites.rect.x <= mousePos[0] <= sprites.rect.x + sprites.width and sprites.rect.y <= mousePos[1] <= sprites.y:
                            if "assignement" not in TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]:
                                TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]["assignement"] = []
                            TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]["assignement"].append(str(sprites.rect.x - sprites.offset_x) + ", " + str(sprites.rect.y - sprites.offset_y))
                    else:
                        if sprites.rect.x - TileManager.camera.last_x <= mousePos[0] - TileManager.camera.last_x <= sprites.rect.x - TileManager.camera.last_x + sprites.width and sprites.rect.y <= mousePos[1] <= sprites.rect.y + sprites.width:
                            if "assignement" not in TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]:
                                TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]["assignement"] = []
                            TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]["assignement"].append(str((sprites.rect.x - TileManager.camera.last_x) // Game.TILESIZE) + ", " + str(sprites.rect.y // Game.TILESIZE))
            elif mouse_buttons[2] == 1:
                self.attributing = False
                TileEditor.attributing = False
            elif mouse_buttons[0] != 1 and self.clicked2:
                self.clicked2 = False

        if TileEditor.is_editing:
            if "assignement" in TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]:
                for sprite in TileEditor.created_level["tiles"][str(self.x) + ", " + str(self.y)]["assignement"]:
                    if sprite == str(self.x) + ", " + str(self.y):
                        continue
                    if "customPlace" in TileEditor.created_level["tiles"][sprite]:
                        x = int(sprite.split(", ")[0]) + Game.TILESIZE // 2
                        y = int(sprite.split(", ")[1])

                        pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y + 30), (x + TileManager.camera.last_x, y))
                    else:
                        x = (int(sprite.split(", ")[0]) * Game.TILESIZE) + (Game.TILESIZE // 2)
                        y = int(sprite.split(", ")[1]) * Game.TILESIZE

                        pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y + 30), (x + TileManager.camera.last_x, y))
