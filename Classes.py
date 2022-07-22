from Constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, length, surface: pygame.Surface, speed, color: pygame.Color,
                 groups_for_l_r_plats: tuple, *groups):
        super().__init__(*groups)
        self.surface = surface
        self.x = surface.get_rect().width // 2
        self.y = surface.get_rect().height - 30
        self.size = length, 7
        self.speed = speed
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.left_platform = Border([self.x - 2, self.y], (2, self.size[1]), THEME_COLOR)
        self.right_platform = Border([self.x + self.size[0], self.y], (2, self.size[1]), THEME_COLOR)
        for elem in groups_for_l_r_plats:
            self.left_platform.add(elem)
            self.right_platform.add(elem)

    def move(self, keys, timer):
        if keys[pygame.K_LEFT] and self.check_borders() != 'l':
            self.x -= self.speed * timer / 1000
            self.left_platform.point[0] -= self.speed * timer / 1000
            self.right_platform.point[0] -= self.speed * timer / 1000
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            self.left_platform.rect = pygame.Rect(self.left_platform.point, self.left_platform.size)
            self.right_platform.rect = pygame.Rect(self.right_platform.point, self.right_platform.size)
        if keys[pygame.K_RIGHT] and self.check_borders() != 'r':
            self.x += self.speed * timer / 1000
            self.left_platform.point[0] += self.speed * timer / 1000
            self.right_platform.point[0] += self.speed * timer / 1000
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            self.left_platform.rect = pygame.Rect(self.left_platform.point, self.left_platform.size)
            self.right_platform.rect = pygame.Rect(self.right_platform.point, self.right_platform.size)

    def check_borders(self):
        if self.rect.x <= 0:
            return 'l'
        elif self.rect.x + self.size[0] >= self.surface.get_width():
            return 'r'


class Bullet(pygame.sprite.Sprite):
    def __init__(self, radius, surface: pygame.Surface, platform: Platform, speed_x, speed_y, color, *group):
        super().__init__(*group)
        self.radius = radius
        self.moving = False
        self.speed = [speed_x, speed_y]
        self.change_coefficient()
        self.color = color
        self.platform = platform
        self.time = int(((1000 / self.speed[0])**2 + (1000 / self.speed[1])**2)**0.5)
        self.surface = surface
        self.center = [self.platform.x + self.platform.size[0] / 2, self.platform.y - self.radius]
        self.image = pygame.Surface((self.radius * 2 + 2, self.radius * 2 + 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, self.color, (self.radius + 1, self.radius + 1), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.center[0] - self.radius, self.center[1] - self.radius - 2

    def move(self, amount):
        if self.moving:
            self.change_coefficient()
            self.center[0] += 1 * self.coefficient_x
            self.center[1] -= 1 * self.coefficient_y
            self.rect.x, self.rect.y = self.center[0] - self.radius, self.center[1] - self.radius
            pygame.time.delay(int(self.time / amount))
        else:
            self.center = [self.platform.x + self.platform.size[0] / 2, self.platform.y - self.radius - 2]
            self.rect.x, self.rect.y = self.center[0] - self.radius, self.center[1] - self.radius

    def game_over(self):
        if self.rect.y >= self.surface.get_height():
            self.kill()

    def change_coefficient(self):
        if self.speed[0] >= 0:
            self.coefficient_x = 1
        else:
            self.coefficient_x = -1
        if self.speed[1] >= 0:
            self.coefficient_y = 1
        else:
            self.coefficient_y = -1


class Border(pygame.sprite.Sprite):
    def __init__(self, left_top, size: tuple, color: pygame.Color, *groups):
        super().__init__(*groups)
        self.size = size
        self.point = left_top
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.point, self.size)


class Point(pygame.sprite.Sprite):
    def __init__(self, left_top: list, color: pygame.Color, *groups):
        super().__init__(*groups)
        self.point = left_top
        self.color = color
        self.width, self.height = 8, 8
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image.fill(THEME_POINTS_COLOR)
        self.rect = pygame.Rect(self.point, (self.width, self.height))


class Level:
    def __init__(self, instructions: str, all_s: pygame.sprite.Group,
                 points: pygame.sprite.Group, borders_h: pygame.sprite.Group, borders_v: pygame.sprite.Group):
        self.y = 0
        self.x = 0
        self.instructions = [elem.rstrip() for elem in open(instructions).readlines()]
        self.block_size = 10, 10
        self.groups = [all_s, points, borders_h, borders_v]

    def build(self):
        for elem in self.instructions:
            i = 0
            check_2 = False
            if check_2:
                break
            while i < len(elem):
                amount = 0
                check = True
                while elem[i] == '1':
                    if check:
                        Border([self.x - 1, self.y], (2, self.block_size[1]), GENERAL_COLOR, self.groups[0],
                               self.groups[3])
                        check = False
                    amount += 1
                    i += 1
                    if i == len(elem):
                        check_2 = True
                        break
                Border([self.x, self.y], (self.block_size[0] * amount, self.block_size[1]), THEME_COLOR, self.groups[0],
                       self.groups[2])
                self.x += self.block_size[0] * amount
                if not check:
                    Border([self.x, self.y], (1, self.block_size[1]), GENERAL_COLOR, self.groups[0],
                           self.groups[3])
                if check_2:
                    break
                while elem[i] == '2':
                    Point([self.x + 1, self.y + 1], THEME_POINTS_COLOR, self.groups[0], self.groups[1])
                    self.x += self.block_size[0]
                    i += 1
                    if i == len(elem):
                        check_2 = True
                        break
                if check_2:
                    break
                while elem[i] == '0':
                    i += 1
                    self.x += self.block_size[0]
                    if i == len(elem):
                        check_2 = True
                        break
            self.y += self.block_size[1]
            self.x = 0


class Result(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.win = pygame.transform.scale(pygame.image.load('you_win_picture.jpg'), (400, 400))
        self.lose = pygame.transform.scale(pygame.image.load('game_over_picture.jpg'), (400, 400))
        self.rect = pygame.Rect(0, 0, 400, 400)
