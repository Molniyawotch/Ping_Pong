import pygame as pg
from settings import *
import pygame.freetype as font


class Button:
    def __init__(self, text, pos, size):
        self.rect = pg.Rect(pos, size)
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.color = White
        self.message = font.SysFont("NFS", 78)
        self.text = text

    def __on_hover(self):
        if self.rect.left < self.mouse_x < self.rect.right and self.rect.top < self.mouse_y < self.rect.bottom:
            self.color = Silver
        else:
            self.color = White

    def update(self, surface):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.__on_hover()
        pg.draw.rect(surface, self.color, self.rect)
        self.message.render_to(surface, self.rect, self.text)
# (self.message.get_rect(self.text).width // 2)