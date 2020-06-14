import pygame as pg

screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()


def input_string(a, b, c, d):
    global screen
    global clock
    game_screen()
    font = pg.font.Font(None, 32)
    done = False
    pg.mouse.set_visible(True)
    while not done:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                done = True
        game_screen()
        draw_text(a, pg.font.Font('이순신Bold.ttf', 17), screen,
                  165, 298, (255, 255, 255))
        draw_text(b, pg.font.Font('이순신Bold.ttf', 18), screen,
                  165, 250, (255, 255, 255))
        draw_text(c, pg.font.Font('이순신Bold.ttf', 17), screen,
                  325, 298, (255, 255, 255))
        draw_text(d, pg.font.Font('이순신Bold.ttf', 18), screen,
                  325, 250, (255, 255, 255))
        draw_text("<명예의 전당>", pg.font.Font('이순신Bold.ttf', 30), screen,
                  250, 50, (255, 255, 255))
        draw_text("# 우주 대 전쟁", pg.font.Font('이순신Bold.ttf', 26), screen,
                  140, 200, (255, 0, 0))
        draw_text("# 텐가이", pg.font.Font('이순신Bold.ttf', 26), screen,
                  320, 200, (0, 0, 255))
        draw_text("이전으로 돌아가려면 화면을 클릭하세요.", pg.font.Font('이순신Bold.ttf', 20), screen,
                  250, 400, (151, 231, 201))

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
    start_image = pg.image.load('showglory.png')
    screen.blit(start_image, [0, 0])
    # Main_Menu_sound.play()
