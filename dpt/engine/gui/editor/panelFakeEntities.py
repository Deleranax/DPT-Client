import pygame
from dpt.engine.gui.editor.editorPanel import EditorPanel
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game


class PanelFakeEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, alpha, block):
        pygame.sprite.Sprite.__init__(self, EditorPanel.editorPanelGroup)
        try:
            self.block = RessourceLoader.get(block)
            self.image = RessourceLoader.get(self.block.texture)
        except UnreachableRessourceError:
            self.image = RessourceLoader.get("dpt.images.not_found")
        self.image = pygame.transform.scale(self.image, (self.block.width, self.block.height))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
