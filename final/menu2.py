import pygame
import random
from collections import deque

from database import Database
from load import load_image, load_sound, load_music

if not pygame.mixer:
    print('Warning, sound disabled')
if not pygame.font:
    print('Warning, fonts disabled')

BLUE = (0, 0, 255)
RED = (255, 0, 0)

direction = {None: (0, 0), pygame.K_w: (0, -2), pygame.K_s: (0, 2),
             pygame.K_a: (-2, 0), pygame.K_d: (2, 0)}


class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z'}


def main():
    pygame.mixer.pre_init(11025, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Shooting Game')
    pygame.mouse.set_visible(0)

    background = pygame.Surface((500, 2000))
    background = background.convert()
    background.fill((0, 0, 0))
    backgroundLoc = 1500
    finalStars = deque()
    for y in range(0, 1500, 30):
        size = random.randint(2, 5)
        x = random.randint(0, 500 - size)
        if y <= 500:
            finalStars.appendleft((x, y + 1500, size))
        pygame.draw.rect(
            background, (255, 255, 0), pygame.Rect(x, y, size, size))
    while finalStars:
        x, y, size = finalStars.pop()
        pygame.draw.rect(
            background, (255, 255, 0), pygame.Rect(x, y, size, size))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    speed = 1.5
    clockTime = 60  # FPS 설정
    clock = pygame.time.Clock()

    font = pygame.font.Font("이순신Bold.ttf", 30)

    inMenu = True

    title, titleRect = load_image('title.png')
    titleRect.midtop = screen.get_rect().inflate(0, -200).midtop

    war_start_Text = font.render('우주 대 전쟁 시작', 1, BLUE)
    war_start_Pos = war_start_Text.get_rect(
        midtop=titleRect.inflate(0, 100).midbottom)
    tegai_start_Text = font.render('텐가이 시작', 1, BLUE)
    tegai_start_Pos = tegai_start_Text.get_rect(
        topleft=war_start_Pos.bottomleft)
    rank_Text = font.render('명예의 전당', 1, BLUE)
    rank_Pos = rank_Text.get_rect(topleft=tegai_start_Pos.bottomleft)

    myscore_Text = font.render('나의 최고 기록', 1, BLUE)
    myscore_Pos = rank_Text.get_rect(topleft=rank_Pos.bottomleft)

    logout_Text = font.render('로그아웃', 1, BLUE)
    logout_Pos = logout_Text.get_rect(topleft=myscore_Pos.bottomleft)
    selectText = font.render('*', 1, BLUE)
    selectPos = selectText.get_rect(topright=war_start_Pos.topleft)
    menuDict = {1: war_start_Pos, 2: tegai_start_Pos,
                3: rank_Pos, 4: myscore_Pos, 5: logout_Pos}
    selection = 1
    show_menu2 = False
    soundFX = Database.getSound()
    music = Database.getSound(music=True)
    if music and pygame.mixer:
        pygame.mixer.music.play(loops=-1)

    while inMenu:
        clock.tick(clockTime)

        screen.blit(
            background, (0, 0), area=pygame.Rect(
                0, backgroundLoc, 500, 500))
        backgroundLoc -= speed
        if backgroundLoc - speed <= speed:
            backgroundLoc = 1500

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN):
                if show_menu2:
                    show_menu2 = False
                elif selection == 1:
                    inMenu = False
                    return 1
                elif selection == 2:
                    inMenu = False
                    return 2
                elif selection == 3:
                    return 3
                elif selection == 4:
                    return 4
                elif selection == 5:
                    return 5
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_w
                  and selection > 1
                  and not show_menu2):
                selection -= 1
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_s
                  and selection < len(menuDict)
                  and not show_menu2):
                selection += 1

        selectPos = selectText.get_rect(topright=menuDict[selection].topleft)

        if not show_menu2:
            textOverlays = zip([war_start_Text, tegai_start_Text, rank_Text,
                                myscore_Text, logout_Text, selectText],
                               [war_start_Pos, tegai_start_Pos, rank_Pos,
                                myscore_Pos, logout_Pos, selectPos])
            screen.blit(title, titleRect)
        for txt, pos in textOverlays:
            screen.blit(txt, pos)
        pygame.display.flip()

    while True:
        clock.tick(clockTime)

        screen.blit(
            background, (0, 0), area=pygame.Rect(
                0, backgroundLoc, 500, 500))
        backgroundLoc -= speed
        if backgroundLoc - speed <= 0:
            backgroundLoc = 1500
        pygame.display.flip()


if __name__ == '__main__':
    while(main()):
        pass
