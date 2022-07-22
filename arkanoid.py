import random
import main
from Classes import *
from Constants import *


def arkanoid():
    all_sprites = pygame.sprite.Group()
    platform_sprite_group = pygame.sprite.Group()
    bullet_sprite_group = pygame.sprite.Group()
    vertical_field_boundary_sprite_group = pygame.sprite.Group()
    horizontal_field_boundary_sprite_group = pygame.sprite.Group()
    points_sprite_group = pygame.sprite.Group()
    result_sprite_group = pygame.sprite.Group()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    screen.fill(GENERAL_COLOR)
    pygame.display.set_caption('arkanoid')
    clock = pygame.time.Clock()
    running = True
    platform = Platform(100, screen, 500, THEME_COLOR, (all_sprites, vertical_field_boundary_sprite_group),
                        all_sprites, platform_sprite_group)
    Bullet(5, screen, platform, -100, 100, THEME_COLOR, all_sprites, bullet_sprite_group)
    Bullet(5, screen, platform, 100, 100, THEME_COLOR, all_sprites, bullet_sprite_group)
    Border([0, 0], (1, height), GENERAL_COLOR, all_sprites, vertical_field_boundary_sprite_group)
    Border([width - 1, 0], (1, height), GENERAL_COLOR, all_sprites, vertical_field_boundary_sprite_group)
    Border([0, 0], (width, 1), GENERAL_COLOR, all_sprites, horizontal_field_boundary_sprite_group)
    Level('level_' + str(random.randrange(1, 4)), all_sprites, points_sprite_group, horizontal_field_boundary_sprite_group,
          vertical_field_boundary_sprite_group).build()
    all_sprites.draw(screen)
    check = True
    while running:
        timer = clock.tick()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and check:
            for elem in bullet_sprite_group:
                elem.moving = True
            check = False
        platform.move(keys, timer)
        game_over_check = 0
        for elem in bullet_sprite_group:
            game_over_check += 1
            if elem.moving:
                if pygame.sprite.spritecollideany(elem, vertical_field_boundary_sprite_group):
                    elem.speed[0] = -elem.speed[0]
                if pygame.sprite.spritecollideany(elem, horizontal_field_boundary_sprite_group) or \
                        pygame.sprite.spritecollideany(elem, platform_sprite_group):
                    elem.speed[1] = -elem.speed[1]
                if pygame.sprite.spritecollideany(elem, points_sprite_group):
                    elem.speed[0] = -elem.speed[0]
                    elem.speed[1] = -elem.speed[1]
                    sprite_to_kill = pygame.sprite.spritecollideany(elem, points_sprite_group)
                    sprite_to_kill.kill()
            if keys[pygame.K_UP] and check:
                elem.moving = True
                check = False
            elem.move(len(bullet_sprite_group))
            elem.game_over()
        if not game_over_check:
            res = Result(result_sprite_group)
            res.image = res.lose
            result_sprite_group.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            screen.fill(GENERAL_COLOR)
            running = False
        win_check = 0
        for _ in points_sprite_group:
            win_check += 1
        if not win_check:
            res = Result(result_sprite_group)
            res.image = res.win
            pygame.time.delay(500)
            result_sprite_group.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            screen.fill(GENERAL_COLOR)
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.fill(GENERAL_COLOR)
                running = False
        screen.fill(GENERAL_COLOR)
        platform_sprite_group.draw(screen)
        bullet_sprite_group.draw(screen)
        vertical_field_boundary_sprite_group.draw(screen)
        horizontal_field_boundary_sprite_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    screen.fill(GENERAL_COLOR)
    pygame.quit()
    main.main()
