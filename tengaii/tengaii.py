import gettext
import sys
import os
import pygame
import random
import menu2


######################################################
# 기본 초기화 (반드시 해야 하는 것들)
def game2(screen):
    pygame.init()

    WHITE = (255, 255, 255)
    screen_width = 1024
    screen_height = 512
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.mixer.music.load("bgm.wav")
    pygame.mixer.music.play(-1)
    attack_sound = pygame.mixer.Sound("PhoHit00.wav")
    bd_sound = pygame.mixer.Sound("pabDth00.wav")

    # 화면 타이틀 설정
    pygame.display.set_caption("Tengai")

    # FPS
    clock = pygame.time.Clock()

    # 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
    current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
    image_path = os.path.join(current_path, "images")  # image 폴더 위치 반환

    # 폰트 정의
    game_font = pygame.font.Font('YiSunRegular.ttf', 40)  # 폰트 객체 생성 (폰트, 크기)
    # 시작시간정보
    total_time = 100
    # 시간 계산
    start_ticks = pygame.time.get_ticks()  # 시작 tick을 받아옴
    # 캐릭터 불러오기

    # 박쥐와 충돌
    game_result = "Game Over"

    isShotBat = False
    isShotDragon = False

    s_score = 0

    # 이벤트 루프
    def game_loop():
        battleship = pygame.image.load(os.path.join(image_path, "tradeship-removebg.png"))
        battleship_size = battleship.get_rect().size  # 이미지의 크기를 구해옴
        battleship_width = battleship_size[0]  # 캐릭터의 가로 크기
        battleship_height = battleship_size[1]  # 캐릭터의 세로 크기
        battleship_x_pos = 0
        battleship_y_pos = (screen_height / 2) - battleship_height

        # 캐릭터 이동위치
        battleship_to_x = 0
        battleship_to_y = 0

        # 캐릭터 이동속도
        battleship_speed = 3
        ###################################################################
        background = pygame.image.load(os.path.join(image_path, "SpaceBackground1.png"))
        background_width = 1024
        background2 = background.copy()
        background_x = 0
        background2_x = background_width

        # 적 박쥐
        ###################################################################
        bat = pygame.image.load(os.path.join(image_path, "bat.png"))
        bat_size = bat.get_rect().size
        bat_width = bat_size[0]
        bat_height = bat_size[1]
        bat_x = screen_width
        bat_y = random.randrange(0, screen_height)

        global s_score

        bat_speed = 10

        s_score = 0
        # 메인 적
        ###################################################################
        dragon = pygame.image.load(os.path.join(image_path, "spaceship.png"))
        dragon_size = dragon.get_rect().size
        dragon_width = dragon_size[0]
        dragon_height = dragon_size[1]
        dragon_x = screen_width - dragon_size[0]
        dragon_y = random.randrange(0, screen_height - dragon_height)
        dragon_speed = 10

        # 아군 무기
        ###################################################################
        bullet = pygame.image.load(os.path.join(image_path, "bullet1.png"))
        bullet_size = bullet.get_rect().size
        bullet_width = bullet_size[0]

        # 적군 무기
        ###################################################################
        shit = pygame.image.load(os.path.join(image_path, "shit.png"))
        shit_size = shit.get_rect().size
        shit_width = shit_size[0]
        shit_height = shit_size[1]
        shit_x = 0
        shit_y = 0

        boom = pygame.image.load(os.path.join(image_path, "boom.png"))
        boom_size = boom.get_rect().size
        boom_width = boom_size[0]
        boom_height = boom_size[1]
        boom_x = 0
        boom_y = 0  # 실행 안되면 88행부터 주석처리 하기

        bullet_speed = 10
        bullet_xy = []

        shit_speed = 25
        shit_xy = []

        bullet_to_remove = -1
        bat_to_remove = -1
        dragon_to_remove = -1
        dragon_remove_count = 0
        shit_to_remove = -1

        # 게임종료 메시지
        # 시간초과
        running = True  # 게임이 진행중인가?

        while running:
            clock.tick(60)  # 게임화면의 초당 프레임 수를 설정
            # 캐릭터가 1초 동안 60번 동작
            isShotBat = False
            isShotDragon = False
            '''if s_score>=300:
                running =False
                game_result = "Game Clear!"'''

            for event in pygame.event.get():  # 프로그램이 종료되지 않도록 이벤트는 계속 돌아야 함
                if event.type == pygame.QUIT:  # 여러 이벤트 중 quit이 있으면 종료
                    running = False  # 게임이 진행중이 아님

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        battleship_to_y -= battleship_speed  # 위쪽으로 4씩
                    elif event.key == pygame.K_DOWN:
                        battleship_to_y += battleship_speed  # 아래쪽으로 4씩
                    elif event.key == pygame.K_LEFT:
                        battleship_to_x -= battleship_speed  # 왼쪽으로 4씩
                    elif event.key == pygame.K_RIGHT:
                        battleship_to_x += battleship_speed  # 오른쪽으로 4씩
                    elif event.key == pygame.K_LSHIFT:
                        battleship_to_x = 0  # 제자리
                        battleship_to_y = 0
                    elif event.key == pygame.K_SPACE:
                        bullet_x = battleship_x_pos + battleship_width
                        bullet_y = battleship_y_pos + battleship_height / 2
                        bullet_xy.append([bullet_x, bullet_y])
                        attack_sound.play()

                if event.type == pygame.KEYUP:  # 키를 뗐을 때
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        battleship_to_x = 0
                    elif event.type == pygame.K_UP or event.type == pygame.K_DOWN:
                        battleship_to_y = 0

            bat_x -= bat_speed
            if bat_x <= 0:
                if (s_score - 5 <= 0):
                    s_score = 0
                elif (s_score - 5 > 0):
                    s_score = s_score - 5
                bat_x = screen_width
                bat_y = random.randrange(0, screen_height - bat_height)

            if dragon_x >= 0 and dragon_y >= 0:
                dragon_speed = 2
                dragon_x -= dragon_speed
                dragon_speed = 5
                dragon_y = random.randrange(dragon_y - 15, dragon_y + 15)
                if dragon_x >= 0:
                    rand = random.randrange(0, 50)
                    if rand == 1:
                        shit_x = dragon_x
                        shit_x -= shit_speed
                        shit_y = dragon_y + dragon_height / 2
                        shit_xy.append([shit_x, shit_y])

            if dragon_x < 0:
                dragon_x = 0
            elif dragon_x > screen_width - dragon_width:
                dragon_x = screen_width - dragon_width
            elif dragon_y < 0:
                dragon_y = 0
            elif dragon_y > screen_height - dragon_height:
                dragon_y = screen_height - dragon_height

            if (dragon_x <= 0):
                if (s_score - 10 <= 0):
                    s_score = 0
                elif (s_score - 10 > 0):
                    s_score = s_score - 10
                dragon_x = screen_width
                dragon_y = random.randrange(0, screen_height - dragon_height)

            battleship_x_pos += battleship_to_x
            battleship_y_pos += battleship_to_y

            # 가로, 세로 경계값 처리
            if battleship_x_pos < 0:
                battleship_x_pos = 0
            elif battleship_x_pos > screen_width - battleship_width:
                battleship_x_pos = screen_width - battleship_width
            elif battleship_y_pos < 0:
                battleship_y_pos = 0
            elif battleship_y_pos > screen_height - battleship_height:
                battleship_y_pos = screen_height - battleship_height

            # 충돌 처리를 위한 rect 정보 업데이트
            battleship_rect = battleship.get_rect()
            battleship_rect.left = battleship_x_pos
            battleship_rect.top = battleship_y_pos

            bat_rect = bat.get_rect()
            bat_rect.left = bat_x
            bat_rect.top = bat_y

            dragon_rect = dragon.get_rect()
            dragon_rect.left = dragon_x
            dragon_rect.top = dragon_y

            for shit_idx, shit_val in enumerate(shit_xy):
                shit_pos_x = shit_val[0]
                shit_pos_y = shit_val[1]

                shit_rect = shit.get_rect()
                shit_rect.left = shit_pos_x
                shit_rect.top = shit_pos_y

                if shit_rect.colliderect(battleship_rect):
                    shit_to_remove = shit_idx  # 해당 무기 없애기 위한 값 설정
                    battleship_to_remove = 1  # 박쥐 없애기 위한 값 설정
                    print("game over")
                    game_over()
                    pygame.time.delay(1000)
                    return 'game_screen'
                    break

                if shit_to_remove > -1:
                    del shit_xy[shit_to_remove]
                    shit_to_remove = -1  # 다시 초기화

            # 무기와 박쥐 충돌 설정
            for bullet_idx, bullet_val in enumerate(bullet_xy):
                bullet_pos_x = bullet_val[0]
                bullet_pos_y = bullet_val[1]

                bullet_rect = bullet.get_rect()
                bullet_rect.left = bullet_pos_x
                bullet_rect.top = bullet_pos_y

                '''boom_rect = boom.get_rect()
                boom_rect.left = boom_x
                boom_rect.top = boom_y'''

                if bullet_rect.colliderect(bat_rect):
                    isShotBat = True
                    bd_sound.play()
                    bullet_to_remove = bullet_idx  # 해당 무기   없애기 위한 값 설정
                    bat_to_remove = 1  # 박쥐 없애기 위한 값 설정
                    break

                if bullet_rect.colliderect(dragon_rect):
                    bullet_to_remove = bullet_idx
                    dragon_remove_count += 1
                    if (dragon_remove_count >= 5):
                        isShotDragon = True
                        bd_sound.play()
                        dragon_to_remove = 1
                        dragon_remove_count = 0
                        break

                if shit_to_remove > -1:
                    del shit_xy[shit_to_remove]
                    shit_to_remove = -1

                # 충돌된 무기 or 박쥐 없애기
                if bullet_to_remove > -1:
                    del bullet_xy[bullet_to_remove]
                    bullet_to_remove = -1  # 다시 초기화

                if bat_to_remove > -1:
                    s_score = s_score + 10
                    bat_x = screen_width  # 박쥐 다시 생성
                    bat_y = random.randrange(0, screen_height - bat_height)
                    bat_to_remove = -1  # 다시 초기화

                if dragon_to_remove > -1:
                    s_score += 50
                    dragon_x = screen_width  # 박쥐 다시 생성
                    dragon_y = random.randrange(0, screen_height - bat_height)
                    dragon_to_remove = -1  # 다시 초기화

            # 배틀쉽과 박쥐 충돌 체크
            if battleship_rect.colliderect(bat_rect):
                print("game over")
                game_over()
                pygame.time.delay(1000)
                return 'game_screen'

            if battleship_rect.colliderect(dragon_rect):
                print("game over")
                game_over()
                pygame.time.delay(1000)
                return 'game_screen'

            background_x -= 2
            background2_x -= 2

            if background_x == -background_width:
                background_x = background_width

            if background2_x == -background_width:
                background2_x = background_width

            if len(bullet_xy) != 0:
                for i, bxy in enumerate(bullet_xy):
                    bxy[0] += 15
                    bullet_xy[i][0] = bxy[0]
                    if bxy[0] >= screen_width:
                        bullet_xy.remove(bxy)

            if len(shit_xy) != 0:
                for j, axy in enumerate(shit_xy):
                    axy[0] -= 10
                    shit_xy[j][0] = axy[0]
                    if axy[0] <= 0:
                        shit_xy.remove(axy)

            # 타이머 집어 넣기
            # 경과 시간 계산
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시

            timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
            # 출력할 글자, True, 글자 색상
            score = game_font.render("Score : {}".format(int(s_score)), True, (255, 255, 255))
            screen.blit(background, (background_x, 0))  # 배경 그리기
            screen.blit(background2, (background2_x, 0))

            if len(bullet_xy) != 0:
                for bx, by in bullet_xy:
                    screen.blit(bullet, (bx, by))

            if len(shit_xy) != 0:
                for ax, ay in shit_xy:
                    screen.blit(shit, (ax, ay))

            screen.blit(battleship, (battleship_x_pos, battleship_y_pos))
            screen.blit(timer, (10, 10))
            screen.blit(score, (830, 10))
            screen.blit(bat, (bat_x, bat_y))
            screen.blit(dragon, (dragon_x, dragon_y))
            if (isShotBat == True):
                screen.blit(boom, (bat_x, bat_y))
            if (isShotDragon == True):
                screen.blit(boom, (dragon_x, dragon_y))

            # 만약 시간이 0이하이면 게임 종료
            if total_time - elapsed_time <= 0:
                game_result = "Time Over"
                return 'game_screen'

            pygame.display.update()  # 게임화면을 다시 그리기!

    def game_over():
        # 게임 오버 메시지
        msg = game_font.render(game_result, True, (255, 255, 0))
        msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
        screen.blit(msg, msg_rect)
        pygame.display.update()  # 게임화면을 다시 그리기!

    def game_screen():
        global s_score
        start_image = pygame.image.load(os.path.join(image_path, 'game_screen.png'))
        screen.blit(start_image, [0, 0])

        # Main_Menu_sound.play()
        title = game_font.render('텟카이', True, WHITE)
        screen.blit(title, (480, 50))
        sc = game_font.render("점수 : {}".format(int(s_score)), True, WHITE)
        screen.blit(sc, (455, 150))
        s = game_font.render('마우스버튼이나 "S"키를 누르면 게임이 시작됩니다.', True, WHITE)
        screen.blit(s, (120, 250))
        t = game_font.render('게임을 종료하려면 "Q"키를 누르세요.', True, WHITE)
        screen.blit(t, (210, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 'quit'
                elif event.key == pygame.K_s:
                    return 'play'
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 'play'
        return 'game_screen'

    def game_quit():
        pygame.quit()

    def main_loop():
        action = 'game_screen'

        while action != 'quit':
            if action == 'game_screen':
                action = game_screen()
            elif action == 'play':
                action = game_loop()
            elif action == 'quit':
                action = game_quit()

    main_loop()
    menu2.main()
