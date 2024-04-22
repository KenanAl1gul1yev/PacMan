from board import boards
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60  # frame per second
font = pygame.font.Font('freesansbold.ttf', 20)
active_level = 0
level = boards[active_level]
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

player_x = 450
player_y = 663

direction = 0
counter = 0
flicker = False
turns_allowed = [False, False, False, False]  # RIGHT, LEFT, UP, DOWN
direction_command = 0
player_speed = 2
score = 0


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))


def check_collision(scr, lvl):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if lvl[center_y // num1][center_x // num2] == 1:
            lvl[center_y // num1][center_x // num2] = 0
            scr += 10
        if lvl[center_y // num1][center_x // num2] == 2:
            lvl[center_y // num1][center_x // num2] = 0
            scr += 50

    return scr


def draw_board(lvl: list):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'yellow', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'yellow', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), (i * num1 + num1)), 3)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, (i * num1 + (0.5 * num1))), 3)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [(j * num2 - (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, 'blue', [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1],
                                PI / 2, PI, 3)
            if lvl[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j * num2 + (0.5 * num2)), (i * num1 - (0.5 * num1)), num2, num1],
                                PI, 3 * PI / 2, 3)
            if lvl[i][j] == 8:
                pygame.draw.arc(screen, 'blue', [(j * num2 - (0.5 * num2)), (i * num1 - (0.5 * num1)), num2, num1],
                                3 * PI / 2, 2 * PI, 3)
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, (i * num1 + (0.5 * num1))), 3)


def draw_player(lvl: list):
    # RIGHT, LEFT, UP, DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerX, centerY, lvl):
    turns = [False, False, False, False]  # RIGHT, LEFT, UP, DOWN

    num1 = (HEIGHT - 50) // 32  # y
    num2 = WIDTH // 30  # x
    num3 = 15
    # check collisions based on centerX and centerY of player +/- fudge number
    if centerX // 30 < 29:
        if direction == 0:
            if lvl[centerY // num1][(centerX - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if lvl[centerY // num1][(centerX + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if lvl[(centerY + num3) // num1][centerX // num2] < 3:
                turns[3] = True
        if direction == 3:
            if lvl[(centerY - num3) // num1][centerX // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerX % num2 <= 18:
                if lvl[(centerY + num3) // num1][centerX // num2] < 3:
                    turns[3] = True
                if lvl[(centerY - num3) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 12 <= centerY % num1 <= 18:
                if lvl[centerY // num1][(centerX + num2) // num2] < 3:
                    turns[0] = True
                if lvl[centerY // num1][(centerX - num2) // num2] < 3:
                    turns[1] = True

        if direction == 0 or direction == 1:
            if 12 <= centerX % num2 <= 18:
                if lvl[(centerY + num1) // num1][centerX // num2] < 3:
                    turns[3] = True
                if lvl[(centerY - num1) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 12 <= centerY % num1 <= 18:
                if lvl[centerY // num1][(centerX - num3) // num2] < 3:
                    turns[1] = True
                if lvl[centerY // num1][(centerX + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y, lvl):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed

    return play_x, play_y


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 6:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')
    draw_board(level)
    draw_player(level)
    draw_misc()
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y, level)
    player_x, player_y = move_player(player_x, player_y, level)
    score = check_collision(score, level)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()

pygame.quit()
