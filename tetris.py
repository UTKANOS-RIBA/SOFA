import pygame
import random
import main
from copy import deepcopy


def out_of_borders(fig, board, h, w):
    if fig.x < 0 or fig.x > w - 1:
        return False
    elif fig.y > h - 1 or board[fig.y][fig.x]:
        return False
    return True


count, speed, limit = 0, 60, 700


def tetris():
    pygame.init()
    pygame.display.set_caption('Tetris')
    w, h = 10, 20
    soc = 35  # size of cells
    size = width, height = w * soc, h * soc
    new_size = width + 400, height
    screen = pygame.display.set_mode(new_size)

    running = True
    fps = 20
    clock = pygame.time.Clock()

    figs_coords = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]  # coordinates of figures

    figs = []
    for i in range(len(figs_coords)):
        figs.append([])
        for coord in figs_coords[i]:
            figs[i].append(pygame.Rect(coord[0] + w // 2, coord[1], 1, 1))

    base_rect = pygame.Rect(0, 0, soc - 2, soc - 2)
    board = [[0 for i in range(w)] for j in range(h)]

    ind = random.randint(0, 6)
    fig = deepcopy(figs[ind])

    #  стартовые надписи
    font = pygame.font.Font(None, 100)
    start_text = font.render("START!", True, (0, 0, 0))
    go_text = font.render('GO!', True, (255, 0, 0))
    font_for_score = pygame.font.Font(None, 60)
    text_for_score = font_for_score.render('SCORE', True, 'white')
    game_over_text = font_for_score.render('GAME OVER', True, 'green')
    score_count = 0

    count, speed, limit = 0, 60, 700
    start = False
    game = True

    while running:
        diff_x, rotate = 0, False
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    diff_x = 1
                if event.key == pygame.K_LEFT:
                    diff_x = -1
                if event.key == pygame.K_DOWN:
                    limit = 100
                if event.key == pygame.K_UP:
                    rotate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= event.pos[0] <= width - 10 and 10 <= event.pos[1] <= 100:
                    start = True
        if not start:
            pygame.draw.rect(screen, 'white', (10, 10, width - 20, 100))
            screen.blit(start_text, (60, 30))
        if start:
            score = font.render(f'{score_count}', True, 'green')
            screen.blit(text_for_score, (490, 50))
            screen.blit(score, (540, 150))
            old_fig = deepcopy(fig)
            for i in range(4):
                fig[i].x += diff_x
                if not out_of_borders(fig[i], board, h, w):
                    fig = deepcopy(old_fig)
                    break
            count += speed
            if count > limit:
                count = 0
                for i in range(4):
                    fig[i].y += 1
                    if not out_of_borders(fig[i], board, h, w):
                        for k in range(4):
                            board[old_fig[k].y][old_fig[k].x] = pygame.Color('white')
                        ind = random.randint(0, 6)
                        fig = deepcopy(figs[ind])
                        limit = 700
                        break
            old_fig = deepcopy(fig)
            centre = fig[0]
            if rotate:
                for i in range(4):
                    x = fig[i].y - centre.y
                    y = fig[i].x - centre.x
                    fig[i].x = centre.x - x
                    fig[i].y = centre.y + y
                    fig[i].x += diff_x
                    if not out_of_borders(fig[i], board, h, w):
                        fig = deepcopy(old_fig)
                        break
            line = h - 1
            for row in range(h - 1, -1, -1):
                c = 0
                for i in range(w):
                    if board[row][i]:
                        c += 1
                    board[line][i] = board[row][i]
                if c < w:
                    line -= 1
                else:
                    score_count += 100
                    fps += 5
            for i in range(h):
                for j in range(w):
                    pygame.draw.rect(screen, 'gray', (j * soc, i * soc, soc, soc), 1)
            for i in range(4):
                base_rect.x = fig[i].x * soc
                base_rect.y = fig[i].y * soc
                pygame.draw.rect(screen, 'red', base_rect)

            for y, raw in enumerate(board):
                for x, color in enumerate(raw):
                    if color:
                        base_rect.x, base_rect.y = x * soc, y * soc
                        pygame.draw.rect(screen, color, base_rect)

            for i in range(w):
                if board[0][i]:
                    game = False

        if not game:
            screen.fill('black')
            screen.blit(game_over_text, (440, 50))
            for i in range(h):
                for j in range(w):
                    pygame.draw.rect(screen, 'blue', (j * soc, i * soc, soc, soc), 1)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    main.main()
