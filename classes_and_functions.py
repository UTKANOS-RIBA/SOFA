import pygame


class Card(pygame.Rect):
    def __init__(self, x, y, d, color):
        self.x = x
        self.y = y
        self.d = d
        self.click = 0
        self.color = color
        self.image = 0
        super().__init__(self.x, self.y, self.d, self.d)

    def set_image(self, image):
        self.image = image
