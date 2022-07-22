import pygame
import random
from classes_and_functions import Card
import main


def memory():
    pygame.init()
    pygame.display.set_caption('Cards')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    font = pygame.font.Font(None, 100)
    start_text = font.render("START!", True, (0, 0, 0))
    font_for_score = pygame.font.Font(None, 20)
    score = font.render('0', True, 'green')
    start = False
    raws = 3
    columns = 10
    buttons = []
    size = 40
    c_x = 0
    c_y = 0
    v = open('values.txt')
    values = [i.strip() for i in v.readlines()]  # список с адресами картинок
    values += values
    images = []  # список для соответствия картинок и карточек
    # создание списка с карточками, пока без соответствующих картинок
    for i in range(raws):
        buttons.append([])
        for j in range(columns):
            buttons[i].append(Card(45 + j * size + c_x, 100 + i * size + c_y, size, 'white'))
            c_x += 1
        c_x = 0  # прибавления к икс для нормальной отрисовки карточек
        c_y += 1  # прибавления к игрек для нормальной отрисовки карточек

    running = True
    fps = 20
    clock = pygame.time.Clock()
    for i in range(raws):
        images.append([])
        for j in range(columns):
            image = random.choice(values)
            values.remove(image)
            images[i].append(image)

    cards_with_image = []
    pair = []
    score = 0
    win = False

    while running:
        if win:
            screen.fill('black')
            text_for_win = font.render('You Win!', True, 'red')
            screen.blit(text_for_win, (10, 10))
        if start:
            screen.fill('black')
            text_for_score = font.render(f'{score * 100}', True, 'green')
            text_score = font.render('SCORE:', True, 'green')
            screen.blit(text_score, (50, 400))
            screen.blit(text_for_score, (350, 400))
            # отрисовка карточек
            for i in range(len(buttons)):
                for j in range(len(buttons[i])):
                    pygame.draw.rect(screen, buttons[i][j].color, buttons[i][j])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверка нажатия на карточку
                if start:
                    for i in range(len(buttons)):
                        for j in range(len(buttons[i])):
                            if buttons[i][j].x <= event.pos[0] <= buttons[i][j].x + buttons[i][j].d and \
                                    buttons[i][j].y <= event.pos[1] <= buttons[i][j].y + buttons[i][j].d:
                                if buttons[i][j].click % 2 == 0:
                                    if buttons[i][j].image != '':
                                        buttons[i][j].set_image(images[i][j])
                                        cards_with_image.append(buttons[i][j])
                                        buttons[i][j].click += 1
                                        if buttons[i][j] not in pair:
                                            pair.append((buttons[i][j], i, j,))
                                else:
                                    try:
                                        buttons[i][j].click += 1
                                        cards_with_image.remove(buttons[i][j])
                                        pair.remove((buttons[i][j], i, j,))
                                    except ValueError:
                                        pass
                    count = 0
                    for i in range(len(buttons)):
                        for j in range(len(buttons[i])):
                            if buttons[i][j] == '':
                                count += 1
                    if count == len(buttons):
                        win = True

                # проверка нажатия на кнопку старта
                if 10 <= event.pos[0] <= width - 20 and 10 <= event.pos[1] <= 210:
                    start = True
                    fig_in_air = True
        if not start:
            # пока не нажата кнопка старта, она отрисовывается
            pygame.draw.rect(screen, 'white', (10, 10, width - 20, 200))
            screen.blit(start_text, (130, 80))

        for i in range(len(cards_with_image)):
            if cards_with_image[i].image:
                im = pygame.image.load(cards_with_image[i].image).convert()
                im = pygame.transform.scale(im, (40, 40))
                rect = im.get_rect()
                rect.center = (cards_with_image[i].x + 20, cards_with_image[i].y + 20)
                screen.blit(im, rect)

        pygame.time.delay(200)

        if len(pair) == 2:
            el_1 = pair[0][0]
            el_2 = pair[1][0]
            if el_1.image == el_2.image:
                cards_with_image = []
                buttons[pair[0][1]][pair[0][2]].color = 'black'
                buttons[pair[0][1]][pair[0][2]].image = ''
                buttons[pair[1][1]][pair[1][2]].color = 'black'
                buttons[pair[1][1]][pair[1][2]].image = ''
                score += 1
                pair = []
            else:
                cards_with_image = []
                el_1.click += 1
                el_2.click += 1
                pair = []

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    main.main()
