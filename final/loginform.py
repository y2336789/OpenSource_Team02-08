import pygame as pg

screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()

errortext = ''

input_box = pg.Rect(180, 165, 140, 32)
input_box2 = pg.Rect(180, 235, 140, 32)
login_box = pg.Rect(input_box2.right + 10, 290, 50, 30)
back_box = pg.Rect(input_box2.right - 60, 290, 50, 30)

count1 = False
count2 = False
space = ' '


def input_string():
    global screen
    global clock
    global input_box
    global input_box2
    global login_box
    global back_box
    global errortext
    global count1
    global count2
    global space
    font = pg.font.Font(None, 32)
    # input_box = pg.Rect(100, 100, 140, 32)
    # input_box2 = pg.Rect(190, 245, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_inactive2 = pg.Color('#7fffd4')
    color_active = pg.Color('dodgerblue2')
    color_active2 = pg.Color('#9af688')
    color = color_inactive
    color2 = color_inactive
    color3 = color_inactive2
    color4 = color_inactive2
    active = False
    active2 = False
    active3 = False
    active4 = False
    text = ''
    text2 = ''
    mask = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                if login_box.collidepoint(event.pos):
                    active3 = not active3
                    if count1 == False and count2 == False:
                        space = ' '*21
                        errortext = space+"아이디와 비밀번호를 입력하세요."
                    elif count1 == False:
                        space = ' '*1
                        errortext = space+"아이디를 입력하세요."
                    elif count2 == False:
                        space = ' '*5
                        errortext = space+"비밀번호를 입력하세요."
                    elif count1 == True and count2 == True:
                        Info = [text, text2]
                        return Info
                else:
                    active3 = False
                if back_box.collidepoint(event.pos):
                    active4 = not active4
                    print("이전입니다.")
                else:
                    active4 = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
                color2 = color_active if active2 else color_inactive
                color3 = color_active2 if active3 else color_inactive2
                color4 = color_active2 if active4 else color_inactive2
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                        if len(text) == 0:
                            count1 = False
                        pg.draw.rect(screen, (0, 0, 0),
                                     (input_box.x+5, input_box.y+5, input_box.width, input_box.height))
                    else:
                        text += event.unicode
                        count1 = True

                if active2:
                    if event.key == pg.K_RETURN:
                        print(text2)
                        text2 = ''
                        count += 1
                    elif event.key == pg.K_BACKSPACE:
                        text2 = text2[:-1]
                        if len(text2) == 0:
                            count2 = False
                        mask = mask[:-1]
                        pg.draw.rect(screen, (0, 0, 0),
                                     (input_box2.x+5, input_box2.y+5, input_box2.width, input_box2.height))
                    else:
                        text2 += event.unicode
                        mask += "*"
                        count2 = True

        game_screen()
        # screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # txt_surface2 = font.render(text2, True, color2)
        txt_surface2 = font.render(mask, True, color2)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        width2 = max(200, txt_surface2.get_width()+10)
        input_box.w = width
        input_box2.w = width2
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+10))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)
        pg.draw.rect(screen, color2, input_box2, 2)
        pg.draw.rect(screen, color3, login_box, 2)
        pg.draw.rect(screen, color4, back_box, 2)

        pg.display.flip()
        clock.tick(30)


def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def game_screen():
    global screen
    global errortext
    global input_box
    global input_box2
    start_image = pg.image.load('game_screen.png')
    screen.blit(start_image, [0, 0])
    # Main_Menu_sound.play()
    draw_text('ID   :',
              pg.font.Font('이순신Bold.ttf', 28), screen,
              140, 180, (255, 255, 255))
    draw_text('PW :',
              pg.font.Font('이순신Bold.ttf', 28), screen,
              140, 250, (255, 255, 255))
    draw_text(errortext, pg.font.Font('이순신Bold.ttf', 18), screen,
              input_box2.x, input_box2.centery+28, (255, 0, 0))
