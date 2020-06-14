import pygame
import gettext
import math
import random
import sys
from time import sleep
import menu2

import pygame
from pygame.locals import *

score = 0
abcount = 0


def game1():
    global score
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 750

    scurge_count = 0
    blackhole_count = 0  # 현재 나타나있는 블랙홀 개수

    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    YELLOW = (250, 250, 20)
    BLUE = (20, 20, 250)
    MINT = (170, 240, 209)

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pyspaceship: 우주 대전쟁')
    pygame.display.set_icon(pygame.image.load('warp.png'))
    fps_clock = pygame.time.Clock()
    FPS = 60

    default_font = pygame.font.Font('YiSunRegular.ttf', 36)
    background_img = pygame.image.load('background.jpg')
    explosion_sound = pygame.mixer.Sound("TDrDth00.wav")
    warp_sound = pygame.mixer.Sound('warp.wav')
    ship_sound = pygame.mixer.Sound('TDrYes00.wav')
    pygame.mixer.music.load("Terran-2.mp3")
    scurge_appear_sound = pygame.mixer.Sound('ZAvYes01.wav')
    scurge_dead_sound = pygame.mixer.Sound('ZAvDth00.wav')
    # Main_Menu_sound = pygame.mixer.Sound('MainMenu.wav')

    warning_img1 = pygame.image.load('warning1.gif')  # 워닝 이미지 4개
    warning_img2 = pygame.image.load('warning2.gif')
    warning_img3 = pygame.image.load('warning3.gif')
    warning_img4 = pygame.image.load('warning4.gif')

    warning_sound = pygame.mixer.Sound('warning_wav.wav')  # 워닝 사운드

    class Blackhole(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Blackhole, self).__init__()
            self.image = pygame.image.load('blackhole.png')
            self.rect = self.image.get_rect()
            self.rect.x = x - self.rect.centerx
            self.rect.y = y - self.rect.centery

        def collide(self, sprites):
            for sprite in sprites:
                if pygame.sprite.collide_rect(self, sprite):
                    return sprite

    class Spaceship(pygame.sprite.Sprite):
        def __init__(self):
            super(Spaceship, self).__init__()
            self.image = pygame.image.load('spaceship.png')
            self.rect = self.image.get_rect()
            self.centerx = self.rect.centerx
            self.centery = self.rect.centery

        def set_pos(self, x, y):
            self.rect.x = x - self.centerx
            self.rect.y = y - self.centery

        def collide(self, sprites):
            for sprite in sprites:
                if pygame.sprite.collide_rect(self, sprite):
                    return sprite

    class Rock(pygame.sprite.Sprite):
        def __init__(self, xpos, ypos, hspeed, vspeed):
            super(Rock, self).__init__()
            rocks = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png',
                     'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png',
                     'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png',
                     'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png',
                     'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png',
                     'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png')

            self.image = pygame.image.load(random.choice(rocks))
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = ypos
            self.hspeed = hspeed
            self.vspeed = vspeed
            self.set_direction()
            self.before_hspeed = hspeed  # 이전의 x축 방향 스피드를 임시로 가지고있을 변수
            self.before_vspeed = vspeed  # 이전의 y축 방향 스피드를 임시로 가지고있을 변수
            self.attractive_speed_x = 0  # 블랙홀의 중력장이 끌어당기는 힘에의해 돌들이 가지게 되는 x축 방향 스피드
            self.attractive_speed_y = 0  # 블랙홀의 중력장이 끌어당기는 힘에의해 돌들이 가지게 되는 y축 방향 스피드
            self.proportion = 0  # 블랙홀에 끌려갈 때, x좌표와 y좌표의 이동 비율

        def set_direction(self):
            if self.hspeed > 0:
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.hspeed < 0:
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.vspeed > 0:
                self.image = pygame.transform.rotate(self.image, 180)

        def update(self):
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed
            if self.collide():
                self.kill()

        def collide(self):
            if self.rect.x < 0 - self.rect.height or self.rect.x > WINDOW_WIDTH:
                return True
            elif self.rect.y < 0 - self.rect.height or self.rect.y > WINDOW_HEIGHT:
                return True

    class Scurge(pygame.sprite.Sprite):
        def __init__(self, xpos, ypos, hspeed, vspeed):
            super(Scurge, self).__init__()

            self.image = pygame.image.load('abc123.png')
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = ypos
            self.hspeed = hspeed
            self.vspeed = vspeed
            self.before_hspeed = hspeed  # 이전의 x축 방향 스피드를 임시로 가지고있을 변수
            self.before_vspeed = vspeed  # 이전의 y축 방향 스피드를 임시로 가지고있을 변수
            self.attractive_speed_x = 0  # 블랙홀의 중력장이 끌어당기는 힘에의해 돌들이 가지게 되는 x축 방향 스피드
            self.attractive_speed_y = 0  # 블랙홀의 중력장이 끌어당기는 힘에의해 돌들이 가지게 되는 y축 방향 스피드
            self.proportion = 0  # 블랙홀에 끌려갈 때, x좌표와 y좌표의 이동 비율

            self.set_direction()

        def set_direction(self):
            if self.hspeed > 0:
                self.image = pygame.transform.rotate(self.image, 225)
            elif self.hspeed < 0:
                self.image = pygame.transform.rotate(self.image, 45)

        def update(self):
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed
            if self.collide():
                self.kill()

        def collide(self):
            if self.rect.x < 0 - self.rect.height or self.rect.x > WINDOW_WIDTH:
                return True
            elif self.rect.y < 0 - self.rect.height or self.rect.y > WINDOW_HEIGHT:
                return True

    def random_rock(speed):
        random_direction = random.randint(1, 4)
        if random_direction == 1:
            return Rock(random.randint(0, WINDOW_WIDTH), 0, 0, speed)
        elif random_direction == 2:
            return Rock(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT), -speed, 0)
        elif random_direction == 3:
            return Rock(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT, 0, -speed)
        elif random_direction == 4:
            return Rock(0, random.randint(0, WINDOW_HEIGHT), speed, 0)

    def random_scurge(speed):
        random_direction = random.randint(1, 2)
        if random_direction == 1:
            return Scurge(0, random.randint(0, WINDOW_HEIGHT), speed, 0)
        elif random_direction == 2:
            return Scurge(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT), -speed, 0)

    class Warp(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Warp, self).__init__()
            self.image = pygame.image.load('warp.png')
            self.rect = self.image.get_rect()
            self.rect.x = x - self.rect.centerx
            self.rect.y = y - self.rect.centery

    def draw_repeating_background(background_img):
        background_rect = background_img.get_rect()
        for i in range(int(math.ceil(WINDOW_WIDTH / background_rect.width))):
            for j in range(int(math.ceil(WINDOW_HEIGHT / background_rect.height))):
                screen.blit(background_img, Rect(i * background_rect.width,
                                                 j * background_rect.height,
                                                 background_rect.width,
                                                 background_rect.height))

    def draw_text(text, font, surface, x, y, main_color):
        text_obj = font.render(text, True, main_color)
        text_rect = text_obj.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        surface.blit(text_obj, text_rect)

    def game_loop():
        global score
        global scurge_count
        global blackhole_count

        ship_sound.play()
        pygame.mixer.music.play(-1)
        pygame.mouse.set_visible(False)

        spaceship = Spaceship()
        spaceship.set_pos(*pygame.mouse.get_pos())
        rocks = pygame.sprite.Group()
        warps = pygame.sprite.Group()
        scurges = pygame.sprite.Group()
        blackholes = pygame.sprite.Group()  # 블랙홀 그룹화
        min_rock_speed = 1
        max_rock_speed = 1
        occur_of_rocks = 1
        occur_prob = 15  # 발생확률, 밑에서 15%를 나타냄
        score = 0
        scurge_count = 0
        blackhole_count = 0
        warp_count = 1
        paused = False
        angle = 0  # 블랙홀과 우주선의 각도를 구해서 담을 변수
        real_angle = 0  # angle을 케이스별로 적용한 실제 회전각을 담을 변수
        coordinate_x = 0  # 우주선의 회전각을 구하기 위해, 우주선의 위치를 원점으로 변환했을 때 블랙홀의 좌표
        coordinate_y = 0  # 우주선의 회전각을 구하기 위해, 우주선의 위치를 원점으로 변환했을 때 블랙홀의 좌표
        coordinate_rock_x = 0  # 블랙홀과 돌들의 관계에서, 돌들을 원점으로 이동시켰을 때 우주선의 x좌표
        coordinate_rock_y = 0  # 블랙홀과 돌들의 관계에서, 돌들을 원점으로 이동시켰을 때 우주선의 y좌표
        coordinate_scurge_x = 0  # 블랙홀과 스커지들의 관계에서, 스커지들을 원점으로 이동시켰을 때 우주선의 x좌표
        coordinate_scurge_y = 0  # 블랙홀과 스커지들의 관계에서, 스커지들을 원점으로 이동시켰을 때 우주선의 y좌표
        temp_blackhole_centerx = 0  # 블랙홀이 지역 객체로 선언되어 있어서 접근이 어려워서 만들어둔 블랙홀의 rect.centerx 좌표
        temp_blackhole_centery = 0  # 블랙홀이 지역 객체로 선언되어 있어서 접근이 어려워서 만들어둔 블랙홀의 rect.centery 좌표
        warning_sound_count = 0  # warning sound가 1번만 울릴 수 있게 카운트

        # 밑에서 변수 t가 if 문의 타이머 조건인 7000 (7초)를 함부로 넘지 못하도록 엄청 큰 값을 세팅
        ticks = 99999999999
        t = -99999999999

        while True:
            if(score == 300):         # clear 조건은 score 300점 달성!!!
                return 'game_screen'  # clear 조건으로, 다음 스테이지 넘어갈 준비!!!

            pygame.display.update()
            fps_clock.tick(FPS)

            if paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = not paused
                            pygame.mouse.set_visible(False)
                    if event.type == QUIT:
                        return 'quit'
            else:
                draw_repeating_background(background_img)

                occur_of_rocks = 1 + int(score / 200)
                min_rock_speed = 1 + int(score / 100)
                max_rock_speed = 1 + int(score / 100)
                # 점수에 비례해서 스커지의 속도 조절, 50점당 스커지의 속도가 3씩 빨라짐
                scurges_speed = 1 + (int(score / 50) * 2)

                if random.randint(1, occur_prob) == 1:
                    for i in range(occur_of_rocks):
                        rock = random_rock(random.randint(
                            min_rock_speed, max_rock_speed))
                        rocks.add(rock)
                        # rocks.add(random_rock(random.randint(
                        #     min_rock_speed, max_rock_speed)))
                        score += 1
                    if random.randint(1, occur_prob * 3) == 1:  # 일정 확률로 워프 생성
                        warp = Warp(random.randint(30, WINDOW_WIDTH - 30),
                                    random.randint(30, WINDOW_HEIGHT - 30))
                        warps.add(warp)
                    if random.randint(1, occur_prob * 3) == 1:  # 워프 발생주기와 똑같게 블랙홀 생성
                        if blackhole_count == 0:
                            blackhole_count += 1
                            ticks = pygame.time.get_ticks()  # 블랙홀 생성될 때를 기점으로 ticks에 타이머 가동

                t = pygame.time.get_ticks() - ticks  # 블랙홀 생성 시점과 현 시점의 시간 차이를 t에 저장

                if 0 < t < 2000:  # 블랙홀이 생성되기 전 2초까지 워닝을 표시
                    screen.fill(BLACK)  # 배경을 검정으로
                    if warning_sound_count == 0:
                        warning_sound.play()
                        warning_sound_count += 1
                    for i in range(0, 5):
                        if (400 * i) < t <= (100 + (400 * i)):
                            screen.blit(warning_img1, (120, 100))
                        if (100 + (400 * i)) < t <= (200 + (400 * i)):
                            screen.blit(warning_img2, (120, 100))
                        if (200 + (400 * i)) < t <= (300 + (400 * i)):
                            screen.blit(warning_img3, (120, 100))
                        if (300 + (400 * i)) < t <= (400 + (400 * i)):
                            screen.blit(warning_img4, (120, 100))

                if t >= 2000 and blackhole_count == 1:  # 블랙홀이 생성되기 시작함!
                    warning_sound_count = 0  # 워닝 사운드 카운트를 다시 0으로 초기화
                    blackhole_count += 1  # 이 함수는 1번만 실행되어야 하므로, blackhole_count를 하나 더 증가시켜줘서 구분!!!
                    blackhole = Blackhole(random.randint(
                        30, WINDOW_WIDTH - 30), random.randint(30, WINDOW_HEIGHT - 30))
                    temp_blackhole_centerx = blackhole.rect.centerx
                    temp_blackhole_centery = blackhole.rect.centery

                    mouse_pos = pygame.mouse.get_pos()
                    # 블랙홀의 좌표에서 우주선의 x좌표를 빼줘서 우주선이 원점에 있을 때 블랙홀의 상대 좌표를 구한다
                    coordinate_x = blackhole.rect.centerx - mouse_pos[0]
                    # 블랙홀의 좌표에서 우주선의 y좌표를 빼줘서 우주선이 원점에 있을 때 블랙홀의 상대 좌표를 구한다
                    coordinate_y = blackhole.rect.centery - mouse_pos[1]
                    # 라디안으로 표현된 각 쎄타이다. 밑에서 math.defrees를 활용하여 degree로 변환한다
                    angle = math.atan(
                        float(abs(coordinate_x)) / float(abs(coordinate_y)))
                    # 라디안으로 표현된 각 쎄타를 degree로 변환한다
                    angle = math.degrees(angle)
                    if coordinate_x > 0 and coordinate_y < 0:  # 우주선이 원점이 있을 때 블랙홀이 위치할 수 있는 총 4사분면에 대한 케이스 분류이다
                        real_angle = -angle
                        spaceship.image = pygame.transform.rotate(  # 여기서 매우 중요한 것이, rotate 메소드는 반시계방향의 회전이 +값이다!!!!!!!!
                            spaceship.image, real_angle)
                    elif coordinate_x > 0 and coordinate_y > 0:
                        real_angle = angle - 180.0
                        spaceship.image = pygame.transform.rotate(
                            spaceship.image, real_angle)
                    elif coordinate_x < 0 and coordinate_y > 0:
                        real_angle = -180.0 - angle
                        spaceship.image = pygame.transform.rotate(
                            spaceship.image, real_angle)
                    elif coordinate_x < 0 and coordinate_y < 0:
                        real_angle = angle
                        spaceship.image = pygame.transform.rotate(
                            spaceship.image, real_angle)
                    blackholes.add(blackhole)

                if blackhole_count == 2 and t < 7000:  # 블랙홀이 생성되어있고, 아직 워닝이 나타난지 7초가 지나지 않아서 살아있다면
                    for rock in rocks:  # 그룹화 되어있는 rocks에서 모든 rock에 개별 접근한다
                        coordinate_rock_x = temp_blackhole_centerx - \
                            rock.rect.centerx  # rock을 원점으로 이동시키는 좌표계 변환 과정이다
                        coordinate_rock_y = temp_blackhole_centery - rock.rect.centery
                        # 밑에서 rock.proportion을 구할 때 0으로 나누면 안되기 때문에 케이스 분류
                        if coordinate_rock_x == 0 and coordinate_rock_y != 0:
                            if coordinate_rock_y > 0:
                                rock.vspeed = random.randint(5, 8)
                            else:
                                rock.vspeed = -(random.randint(5, 8))
                        elif coordinate_rock_x != 0 and coordinate_rock_y == 0:
                            if coordinate_rock_x > 0:
                                rock.hspeed = random.randint(5, 8)
                            else:
                                rock.hspeed = -(random.randint(5, 8))
                        elif coordinate_rock_x == 0 and coordinate_rock_y == 0:
                            rock.kill()
                        else:
                            rock.proportion = float(abs(coordinate_rock_x)) / \
                                float(abs(coordinate_rock_y)
                                      )  # tan 값을 구해서, x좌표와 y좌표의 스피드 비율(이동 거리 비율)을 계산해준다
                            rock.attractive_speed_y = random.randint(
                                5, 8)  # y y축 speed 즉, vspeed를 랜덤으로 설정
                            # 위에서 구한 비율을 바탕으로 블랙홀을 향해 다가갈 수 있도록 비율대로 hspeed 계산
                            rock.attractive_speed_x = rock.proportion * rock.attractive_speed_y
                            # 좌표계 변환 후 총 4사분면에 블랙홀이 존재할 수 있으므로 4가지로 케이스 분류해준다
                            if coordinate_rock_x > 0 and coordinate_rock_y > 0:
                                rock.hspeed = rock.attractive_speed_x
                                rock.vspeed = rock.attractive_speed_y
                                if t >= 6500 and t < 7000:  # timer가 6.5초에서 7초 사이일 때, 각각의 rock들을 이전에 가지고 있던 속도로 초기화
                                    rock.hspeed = rock.before_hspeed
                                    rock.vspeed = rock.before_vspeed
                            elif coordinate_rock_x > 0 and coordinate_rock_y < 0:
                                rock.hspeed = rock.attractive_speed_x
                                rock.vspeed = -rock.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    rock.hspeed = rock.before_hspeed
                                    rock.vspeed = rock.before_vspeed
                            elif coordinate_rock_x < 0 and coordinate_rock_y > 0:
                                rock.hspeed = -rock.attractive_speed_x
                                rock.vspeed = rock.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    rock.hspeed = rock.before_hspeed
                                    rock.vspeed = rock.before_vspeed
                            elif coordinate_rock_x < 0 and coordinate_rock_y < 0:
                                rock.hspeed = -rock.attractive_speed_x
                                rock.vspeed = -rock.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    rock.hspeed = rock.before_hspeed
                                    rock.vspeed = rock.before_vspeed
                        # 위 과정은 각각의 rock들을 블랙홀로 빨려들어가고 , 블랙홀에 닿으면 사라지는 과정이다.
                    for scurge in scurges:  # 그룹화 되어있는 scurges에서 모든 scurge에 개별 접근한다
                        coordinate_scurge_x = temp_blackhole_centerx - \
                            scurge.rect.centerx  # scurge을 원점으로 이동시키는 좌표계 변환 과정이다
                        coordinate_scurge_y = temp_blackhole_centery - scurge.rect.centery
                        # 밑에서 scurge.proportion을 구할 때 0으로 나누면 안되기 때문에 케이스 분류
                        if coordinate_scurge_x == 0 and coordinate_scurge_y != 0:
                            if coordinate_scurge_y > 0:
                                scurge.vspeed = random.randint(5, 8)
                            else:
                                scurge.vspeed = -(random.randint(5, 8))
                        elif coordinate_scurge_x != 0 and coordinate_scurge_y == 0:
                            if coordinate_scurge_x > 0:
                                scurge.hspeed = random.randint(5, 8)
                            else:
                                scurge.hspeed = -(random.randint(5, 8))
                        elif coordinate_scurge_x == 0 and coordinate_scurge_y == 0:
                            scurge.kill()
                        else:
                            scurge.proportion = float(abs(coordinate_scurge_x)) / \
                                float(abs(coordinate_scurge_y)
                                      )  # tan 값을 구해서, x좌표와 y좌표의 스피드 비율(이동 거리 비율)을 계산해준다
                            scurge.attractive_speed_y = random.randint(
                                5, 8)  # y y축 speed 즉, vspeed를 랜덤으로 설정
                            # 위에서 구한 비율을 바탕으로 블랙홀을 향해 다가갈 수 있도록 비율대로 hspeed 계산
                            scurge.attractive_speed_x = scurge.proportion * scurge.attractive_speed_y
                            # 좌표계 변환 후 총 4사분면에 블랙홀이 존재할 수 있으므로 4가지로 케이스 분류해준다
                            if coordinate_scurge_x > 0 and coordinate_scurge_y > 0:
                                scurge.hspeed = scurge.attractive_speed_x
                                scurge.vspeed = scurge.attractive_speed_y
                                if t >= 6500 and t < 7000:  # timer가 6.5초에서 7초 사이일 때, 각각의 scurge들을 이전에 가지고 있던 속도로 초기화
                                    scurge.hspeed = scurge.before_hspeed
                                    scurge.vspeed = scurge.before_vspeed
                            elif coordinate_scurge_x > 0 and coordinate_scurge_y < 0:
                                scurge.hspeed = scurge.attractive_speed_x
                                scurge.vspeed = -scurge.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    scurge.hspeed = scurge.before_hspeed
                                    scurge.vspeed = scurge.before_vspeed
                            elif coordinate_scurge_x < 0 and coordinate_scurge_y > 0:
                                scurge.hspeed = -scurge.attractive_speed_x
                                scurge.vspeed = scurge.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    scurge.hspeed = scurge.before_hspeed
                                    scurge.vspeed = scurge.before_vspeed
                            elif coordinate_scurge_x < 0 and coordinate_scurge_y < 0:
                                scurge.hspeed = -scurge.attractive_speed_x
                                scurge.vspeed = -scurge.attractive_speed_y
                                if t >= 6500 and t < 7000:
                                    scurge.hspeed = scurge.before_hspeed
                                    scurge.vspeed = scurge.before_vspeed
                        # 위 과정은 각각의 scurge들을 블랙홀로 빨려들어가고 , 블랙홀에 닿으면 사라지는 과정이다.
                if 2000 <= t <= 7000:
                    draw_text('소멸 시간: {}'.format(round(7 - t / 1000, 1)),
                              default_font, screen, 510, 25, MINT)

                if t > 7000:  # 블랙홀 생성 워닝이 나타난지 7초 이상이되면
                    # 변수 t가 if 문의 타이머 조건인 7000 (7초)를 함부로 넘지 못하도록 엄청 큰 값을 세팅
                    blackhole_count = 0
                    spaceship.image = pygame.image.load('spaceship.png')
                    blackholes.empty()
                    ticks = 99999999999
                    t = -99999999999

                if(score > 0):
                    if int(score % 50) == 0:  # 점수 50점마다 5마리의 스커지가 나오게 구현
                        if(scurge_count == 0):
                            for i in range(5):
                                scurges.add(random_scurge(scurges_speed))
                                scurge_appear_sound.play()
                            scurge_count = 1
                            # if (scurge_count < 5):
                            #     scurges.add(random_scurge(scurges_speed))
                            #     scurge_count += 1
                    elif int(score % 50) == 1:
                        scurge_count = 0

                draw_text('점수: {}'.format(score),
                          default_font, screen, 100, 25, YELLOW)
                draw_text('워프: {}'.format(warp_count),
                          default_font, screen, 900, 25, BLUE)
                rocks.update()
                warps.update()
                scurges.update()
                blackholes.update()  # 블랙홀들 업데이트

                rocks.draw(screen)
                warps.draw(screen)
                scurges.draw(screen)
                blackholes.draw(screen)  # 블랙홀들 출력

                warp = spaceship.collide(warps)
                blackhole = spaceship.collide(blackholes)  # 우주선이 블랙홀과 충돌할 경우
                if spaceship.collide(rocks):
                    explosion_sound.play()
                    pygame.mixer.music.stop()
                    rocks.empty()
                    return 'game_screen'
                elif warp:
                    warp_count += 1
                    warp.kill()
                elif blackhole:  # 우주선이 블랙홀과 충돌할 경우 게임 종료
                    explosion_sound.play()
                    pygame.mixer.music.stop()
                    rocks.empty()
                    return 'game_screen'
                elif spaceship.collide(scurges):
                    scurge_dead_sound.play()  # 스커지 터지는 사운드로 수정
                    pygame.mixer.music.stop()
                    scurges.empty()
                    return 'game_screen'

                screen.blit(spaceship.image, spaceship.rect)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        mouse_pos = pygame.mouse.get_pos()
                        # 마우스의 x좌표가 왼쪽 10이내일 때, 10은 마진을 둔 것이다.
                        if mouse_pos[0] <= 10:
                            pygame.mouse.set_pos(
                                WINDOW_WIDTH - 10, mouse_pos[1])
                        # 마우스의 x좌표가 우측 창 기준 10에 근접했을 때
                        elif mouse_pos[0] >= WINDOW_WIDTH - 10:
                            pygame.mouse.set_pos(0 + 10, mouse_pos[1])
                        elif mouse_pos[1] <= 10:  # 마우스의 y좌표가 상단 10이내일 때
                            pygame.mouse.set_pos(
                                mouse_pos[0], WINDOW_HEIGHT - 10)
                        elif mouse_pos[1] >= WINDOW_HEIGHT - 10:  # 마우스의 y좌표가 하단 10이내일 때
                            pygame.mouse.set_pos(mouse_pos[0], 0 + 10)
                        spaceship.set_pos(*mouse_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if warp_count > 0:
                            warp_count -= 1
                            warp_sound.play()
                            sleep(1)
                            rocks.empty()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = not paused
                            if paused:
                                transp_surf = pygame.Surface(
                                    (WINDOW_WIDTH, WINDOW_HEIGHT))
                                transp_surf.set_alpha(150)
                                screen.blit(
                                    transp_surf, transp_surf.get_rect())
                                pygame.mouse.set_visible(True)
                                draw_text('일시정지',
                                          pygame.font.Font(
                                              'NanumGothic.ttf', 60),
                                          screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, YELLOW)
                    if event.type == QUIT:
                        return 'quit'
        return 'game_screen'

    def how_to_play():
        pygame.mouse.set_visible(True)
        start_image1 = pygame.image.load('explanation1.png')
        screen.blit(start_image1, [0, 0])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 'game_screen'

        return 'how_to_play'

    def game_screen():
        global score
        pygame.mouse.set_visible(True)
        start_image = pygame.image.load('game_screen.png')
        screen.blit(start_image, [0, 0])
        # Main_Menu_sound.play()
        draw_text('우주 대전쟁',
                  pygame.font.Font('YiSunRegular.ttf', 70), screen,
                  WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3.4, WHITE)
        draw_text('점수: {}'.format(score),
                  default_font, screen,
                  WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.4, YELLOW)
        draw_text('마우스버튼이나 "S"키를 누르면 게임이 시작됩니다.',
                  default_font, screen,
                  WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.0, WHITE)
        draw_text('게임을 종료하려면 "Q"키를 누르세요.',
                  default_font, screen,
                  WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8, WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 'quit'
                elif event.key == pygame.K_s:
                    return 'play'
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 'play'
            if event.type == QUIT:
                return 'quit'
        return 'game_screen'

    def main_loop():
        global abcount
        if abcount == 0:
            action = 'how_to_play'
            abcount += 1
        else:
            action = 'game_screen'
        while action != 'quit':
            if action == 'how_to_play':
                action = how_to_play()
            if action == 'game_screen':
                action = game_screen()
            elif action == 'play':
                action = game_loop()
                list = ['0', score]
                return list
                #action = game_loop()

        # pygame.quit()
        list = ['1', score]
        return list

    main_list = main_loop()
    return main_list
