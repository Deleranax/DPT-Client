import math

import pygame

from dpt.game import Game


class Button(pygame.sprite.Sprite):
    buttonsGroup = pygame.sprite.Group()
    text_sprite_buttonsGroup = pygame.sprite.Group()
    text_buttonsList = []

    def __init__(self, x, y, width, height, normal_image, **kwargs):
        pygame.sprite.Sprite.__init__(self, Button.buttonsGroup)  # Sprite's constructor called
        self.normal_image = normal_image
        try:
            self.pushed_image = kwargs["pushed_image"]
            del kwargs["pushed_image"]
        except KeyError:
            self.pushed_image = self.normal_image
        try:
            self.locked_image = kwargs["locked_image"]
            del kwargs["locked_image"]
        except KeyError:
            self.locked_image = self.normal_image
        try:
            self.hover_image = kwargs["hover_image"] or self.normal_image
            del kwargs["hover_image"]
        except KeyError:
            self.hover_image = self.normal_image
        try:
            self.font = kwargs["font"]
            del kwargs["font"]
        except KeyError:
            self.font = pygame.font.SysFont("arial", math.floor(15 * Game.DISPLAY_RATIO))
        try:
            self.font_color = kwargs["font_color"]
            del kwargs["font_color"]
        except KeyError:
            self.font_color = (0, 0, 0)
        try:
            self.text = kwargs["text"]
            del kwargs["text"]
        except KeyError:
            self.text = None
        try:
            self.text_sprite = kwargs["text_sprite"]
            del kwargs["text_sprite"]
        except KeyError:
            self.text_sprite = None
        self.eventargs = kwargs
        self.image = self.normal_image
        self.width = math.floor(width * Game.DISPLAY_RATIO)
        self.height = math.floor(height * Game.DISPLAY_RATIO)
        self.image = pygame.transform.smoothscale(self.image, (math.floor(width * Game.DISPLAY_RATIO),
                                                               math.floor(height * Game.DISPLAY_RATIO)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pushed = False
        self.locked = False
        Game.get_logger("Button").debug("Button created")

    def __bool__(self):
        return self.pushed

    def update(self):
        if self.text_sprite is not None:
            self.text_sprite.rect.centerx = self.rect.centerx
            self.text_sprite.rect.centery = self.rect.centery

        if self.text is not None:
            text = self.font.render(self.text, True, self.font_color)
            rect = text.get_rect()
            rect.centerx = self.rect.centerx
            rect.centery = self.rect.centery
            Button.text_buttonsList.append((text, rect))

        self.pushed = False
        if self.locked:
            self.image = self.locked_image
            return

        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.pushed = True

        if self.pushed:
            self.image = self.pushed_image
            if self.text_sprite is not None:
                self.text_sprite.rect.centery = self.rect.centery + math.floor(self.rect.height * 0.1)
                event = pygame.event.Event(Game.BUTTON_EVENT, **dict(button=self, **self.eventargs))
                pygame.event.post(event)
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
                Game.cursor_on_button = True
            else:
                self.image = self.normal_image

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    @classmethod
    def main_loop(cls):
        Button.text_buttonsList = []
        Button.buttonsGroup.update()
        Button.text_sprite_buttonsGroup.update()
        Button.buttonsGroup.draw(Game.surface)
        Button.text_sprite_buttonsGroup.draw(Game.surface)
        for i in Button.text_buttonsList:
            Game.surface.blit(i[0], i[1])
