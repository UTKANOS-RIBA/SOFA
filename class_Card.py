import pygame


class Card(pygame.Rect):
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d
        super().__init__(self.x, self.y, self.d, self.d)

    def set_image(self, image):
        self.image = image

    def turning(self, side):
        pass
