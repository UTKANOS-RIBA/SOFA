import pygame
import arkanoid
import memory
import tetris


class Button(pygame.sprite.Sprite):
    def __init__(self, dir, left_top, game, *groups):
        super().__init__(*groups)
        self.reserve = pygame.image.load(dir)
        self.image = pygame.image.load(dir)
        self.rect = self.image.get_rect()
        self.rect.x = left_top[0]
        self.rect.y = left_top[1]
        self.game = game
        self.big = False
        self.small = True


    def become_bigger(self):
        if self.small:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() + 20, self.image.get_height() + 14))
            self.big = True
            self.small = False

    def become_smaller(self):
        if self.big:
            self.image = self.reserve
            self.small = True
            self.big = False

class Background(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('welcome_picture.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0


def main():
    running = True
    size = wigth, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('menu')
    background_sprite_group = pygame.sprite.Group()
    button_sprite_group = pygame.sprite.Group()
    Background(background_sprite_group)
    Button('1.png', [20, 20], 'arkanoid', button_sprite_group)
    Button('2.png', [100, 90], 'tetris', button_sprite_group)
    Button('3.png', [20, 160], 'memory', button_sprite_group)
    while running:
        try:
            screen.fill(pygame.Color('black'))
            background_sprite_group.draw(screen)
            button_sprite_group.draw(screen)
            pygame.display.flip()
            for elem in button_sprite_group:
                if elem.rect.collidepoint(pygame.mouse.get_pos()):
                    elem.become_bigger()
                else:
                    elem.become_smaller()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        for elem in button_sprite_group:
                            if elem.rect.collidepoint(pygame.mouse.get_pos()):
                                if elem.game == 'arkanoid':
                                    arkanoid.arkanoid()
                                elif elem.game == 'tetris':
                                    tetris.tetris()
                                else:
                                    memory.memory()
        except pygame.error:
            pygame.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
