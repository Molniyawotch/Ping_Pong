import pygame as pg
import pygame.freetype as font
import random
from settings import *
import pygame.mixer as mix


class Player:
    def __init__(self, x, y, color):
        self.speed = 0
        self.rect = pg.Rect(x, y, 20, 170)
        self.color = color
        self.score = 0
        self.sound = mix.Sound('media/score.wav')
        self.sound.set_volume(0.5)

    def move(self, key_up, key_down):
        keys = pg.key.get_just_pressed()
        keys_released = pg.key.get_just_released()
        if keys[key_up]:
            self.speed -= 3
        if keys[key_down]:
            self.speed += 3

        if keys_released[key_up] or keys_released[key_down]:
            self.speed = 0

        self.rect.y += self.speed
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT - 15:
            self.rect.bottom = HEIGHT - 15

    def increase_score(self, score=1):
        self.score += score
        self.sound.play()
        self.rect.y = HALF_HEIGHT - 75

    def start_pos(self):
        self.rect.y = HALF_HEIGHT - 75

    def draw(self, sc):
        pg.draw.rect(sc, self.color, self.rect)


class Ball:
    def __init__(self):
        d = (-2, 2)
        self.ball_speed_x = random.choice((-4, 4))
        self.ball_speed_y = random.choice(d)
        self.ball = pg.Rect(HALF_WIDTH, HALF_HEIGHT, 40, 40)
        self.ball_color = White
        self.sound = mix.Sound('media/pong.wav')

    def move(self, players: list[Player]):
        colors = (OrangeRed, RoyalBlue)

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        if self.ball.top < 0 or self.ball.bottom > HEIGHT - 20:
            self.sound.play(0, 0, 54)
            self.ball_speed_y = -self.ball_speed_y
        if self.ball.left <= -13:
            self.__goal(players[1])
            self.start_pos(players[0])
        elif self.ball.right >= WIDTH + 13:
            self.__goal(players[0])
            self.start_pos(players[1])

        index = self.ball.collidelist(players)

        if index >= 0:
            self.ball_color = colors[index]
            self.sound.play(0, 0, 54)
            if self.ball_speed_x < 0:
                if abs(self.ball.top - players[index].rect.bottom) < 10:
                    self.ball_speed_y = -self.ball_speed_y
                    self.ball_speed_x = 1
                elif abs(self.ball.bottom - players[index].rect.top) < 10:
                    self.ball_speed_y = -self.ball_speed_y
                    self.ball_speed_x = -self.ball_speed_x
                elif abs(self.ball.left - players[index].rect.right) < 130:
                    if self.ball_speed_y == 0:
                        self.ball_speed_y = random.choice((-1, 1))
                    self.ball_speed_x -= 2
                    self.ball_speed_x = -self.ball_speed_x
            elif self.ball_speed_x > 0:
                if abs(self.ball.top - players[index].rect.bottom) < 10:
                    self.ball_speed_y = -self.ball_speed_y
                    self.ball_speed_x = -1
                elif abs(self.ball.bottom - players[index].rect.top) < 10:
                    self.ball_speed_y = -self.ball_speed_y
                    self.ball_speed_x = -self.ball_speed_x
                elif abs(self.ball.right - players[index].rect.left) < 130:
                    if self.ball_speed_y == 0:
                        self.ball_speed_y = random.choice((-1, 1))
                    self.ball_speed_x += 2
                    self.ball_speed_x = -self.ball_speed_x

            # if self.ball.colliderect(walls[0]) or self.ball.colliderect(walls[1]):
            #     color = self.ball_color
            #     self.ball_color = White
            #     return color

    def draw(self, sc):
        pg.draw.ellipse(sc, self.ball_color, self.ball)

    def __goal(self, player):
        pg.time.wait(1500)
        self.ball.center = (HALF_WIDTH, HALF_HEIGHT)
        if self.ball_speed_x < 0:
            self.ball_speed_x = -5
        elif self.ball_speed_x > 0:
            self.ball_speed_x = 5
        self.ball_speed_y = 0
        self.ball_color = White
        player.increase_score()

    def start_pos(self, player):
        player.start_pos()


class Application:
    def __init__(self):
        pg.init()
        # C:\\WINDOWS\\FONTS\\NFS.TTF
        self.font = font.Font(None, 78)
        self.clock = pg.time.Clock()
        self.sc = pg.display.set_mode(WINDOW)
        self.surf = pg.Surface(WINDOW)
        pg.display.set_caption('Ping Pong')
        self.running = True

        self.player1 = Player(15, HALF_HEIGHT - 75, Red)
        self.player2 = Player(WIDTH - 35, HALF_HEIGHT - 75, Blue)
        self.ball = Ball()

        self.floor_color = 192, 192, 192
        self.floor = pg.Rect(HALF_WIDTH - 15, 0, 15, HEIGHT)
        self.wall2_color = 220, 220, 220
        self.wall2 = pg.Rect(0, HEIGHT - 20, WIDTH, 20)
        self.finish_color = 220, 20, 60
        self.finish1 = pg.Rect(0, 0, 3, HEIGHT)
        self.finish2 = pg.Rect(WIDTH - 3, 0, 3, HEIGHT)

    def __events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.K_ESCAPE:
                pass

    def _main_menu(self):
        self.font.render_to(self.sc, (HALF_WIDTH - self.font.get_rect("Main Menu").width / 2, HEIGHT / 12), 'Main Menu',
                            fgcolor=White)
        self.play_button = pg.Rect(HALF_WIDTH - 150, HALF_HEIGHT // 2 + 10, 300, 80)
        pg.draw.rect(self.sc, White, self.play_button)
        self.cosmetic_button = pg.Rect(HALF_WIDTH - 150, HALF_HEIGHT - 45, 300, 80)
        pg.draw.rect(self.sc, White, self.cosmetic_button)
        self.exit_button = pg.Rect(HALF_WIDTH - 150, HALF_HEIGHT + 70, 300, 80)
        pg.draw.rect(self.sc, White, self.exit_button)
        self.font.render_to(self.sc, (HALF_WIDTH - self.font.get_rect("Play").width / 2, HALF_HEIGHT // 2 + 15), 'Play')

    def _game_loop(self):
        pg.draw.rect(self.sc, self.floor_color, self.floor)
        self.ball.draw(self.sc)
        pg.draw.rect(self.sc, self.finish_color, self.finish1)
        pg.draw.rect(self.sc, self.finish_color, self.finish2)

        self.player1.move(pg.K_w, pg.K_s)
        self.player2.move(pg.K_UP, pg.K_DOWN)
        self.ball.move([self.player1, self.player2])
        self.player1.draw(self.sc)
        self.player2.draw(self.sc)
        pg.draw.rect(self.sc, self.wall2_color, self.wall2)

        self.font.render_to(self.sc, (HALF_WIDTH // 2, 50), str(self.player1.score), fgcolor=Green)
        self.font.render_to(self.sc, (HALF_WIDTH // 2 + HALF_WIDTH, 50), str(self.player2.score), fgcolor=Green)
        self.end_screen()
        if self.player1.score == Max_score or self.player2.score == Max_score:
            pg.display.update()
            pg.time.wait(3000)
            self.running = False

    pg.quit()

    def run(self):
        while self.running:
            self.__events()
            self.sc.fill("black")
            self._main_menu()
            # self._game_loop()

            pg.display.update()
            self.clock.tick(FPS) / 1000
        pg.quit()

    def end_screen(self):
        if self.player1.score == Max_score:
            self.surf.set_alpha(30)
            self.surf.fill(White)
            self.sc.blit(self.surf, (0, 0))
            self.font.render_to(self.sc,
                                (HALF_WIDTH - self.font.get_rect("Red player win!").width / 2, HALF_HEIGHT - 20),
                                str("Red player win!"),
                                fgcolor=Red)
        if self.player2.score == Max_score:
            self.surf.set_alpha(30)
            self.surf.fill(White)
            self.sc.blit(self.surf, (0, 0))
            self.font.render_to(self.sc,
                                (HALF_WIDTH - self.font.get_rect("Blue player win!").width / 2, HALF_HEIGHT - 20),
                                str("Blue player win!"),
                                fgcolor=Blue)


if __name__ == '__main__':
    app = Application()
    app.run()
