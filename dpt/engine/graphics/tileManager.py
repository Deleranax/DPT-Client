from dpt.engine.graphics.platforms.Block import *
import pygame

#          {"x, y": {"blockClass": Classe}}
levelTest ={"0, 32": {"blockClass": Block},
            "1, 32": {"blockClass": Block},
            "2, 32": {"blockClass": Block},
            "3, 32":{"blockClass": Block},
            "4, 32":{"blockClass": Block},
            "5, 32":{"blockClass": Block},
            "6, 32":{"blockClass": Block},
            "7, 32":{"blockClass": Block},
            "8, 32":{"blockClass": Block},
            "9, 32":{"blockClass": CeciEstUnBlock},
            "10, 32":{"blockClass": Block}}

class TileManager():
    def __init__(self):
        self.game = Game.get_instance()
        self.log = self.game.get_logger("TileManager")
        self.tileSize = 32
        self.userConfirm = True
        self.levelName = None
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        self.coords = None

    def enableGrid(self):
        if self.userConfirm:
            for x in range(0, self.game.surface.get_size()[0], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (x, 0), (x, self.game.surface.get_size()[1]))
            for y in range(0, self.game.surface.get_size()[1], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (0, y), (self.game.surface.get_size()[0], y))

    def disableGrid(self):
        pass

    def loadLevel(self, levelName):
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        if levelName == None:
            self.log.critical("The level can't be loaded")
        for keys in levelTest:
            coords = tuple(map(int, keys.split(", ")))
            if coords[0] > self.maxWidthSize:
                self.maxWidthSize = coords[0]
            elif coords[1] > self.maxHeightSize:
                self.maxHeightSize = coords[1]
            if coords[0] < 0 or coords[1] < 0:
                self.log.warning("The tile position can't be negative")
                continue
            for data in levelTest[keys].values():
                self.game.platforms.add(data((255, 0, 0), coords[0] * self.tileSize, coords[1] * self.tileSize, self.tileSize, self.tileSize))


class Camera():
    def __init__(self, width, height):
        self.game = Game.get_instance()
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.game.surface.get_size()[0] / 2)
        self.camera = pygame.Rect(x, 0, self.width, self.height)