from pygame import * 
from random import randint as rnd
from time import sleep

init()
WIDTH = 700
HEIGHT = 500
sc = display.set_mode((WIDTH, HEIGHT))
display.set_caption('ping-pong')

ball_radius = 10

clock = time.Clock()
FPS = 75
score_pl1 = 0
score_pl2 = 0
qwerty = font.Font(None, 70)
qwertz = font.Font(None, 50)
pl1_wins = qwerty.render('PLAYER 1 WINS', True, (200, 200, 200))
pl2_wins = qwerty.render('PLAYER 2 WINS', True, (200, 200, 200))
score = qwertz.render(str(score_pl1)+':'+str(score_pl2), True, (200, 200, 200))
press_r = qwertz.render('press <r> to next round', True, (200, 200, 200))
class GameSprite(sprite.Sprite): 
    def __init__(self, width, height, p_x, p_y, speed, color): 
        super().__init__() 
        self.rect = Rect(p_x, p_y, width, height)
        self.speed = speed 
        self.color = color

class Paddle(GameSprite):
    def reset(self):
        draw.rect(sc, Color(self.color), self.rect)
    def update(self, up, down):
        keys = key.get_pressed()
        if keys[up] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom <= HEIGHT:
            self.rect.y += self.speed

q = [1, -1]
dx = q[rnd(0, 1)]
dy = q[rnd(0, 1)]

class Ball(GameSprite):
    def __init__(self, width, height, p_x, p_y, speed, color, radius):
        super().__init__(width, height, p_x, p_y, speed, color)
        self.ball_radius = radius
        self.ball_rect = int(radius * 2 ** 0.5)
        self.rect = Rect(p_x, p_y, self.ball_rect, self.ball_rect)
    def reset(self):
        draw.circle(sc, Color(self.color), self.rect.center, self.ball_radius)
    def collide(self, player1, player2):
        global dx, dy, game, finish, score_pl1, score_pl2
        if self.rect.x <= 0:
            finish = True
            score_pl2 += 1
            sc.blit(pl2_wins, (165, 170))
        if self.rect.right > WIDTH:
            finish = True
            score_pl1 += 1
            sc.blit(pl1_wins, (165, 170))
            sc.blit(press_r, (165, 210))
        if self.rect.y <= 0:
            dy = -dy
        if self.rect.bottom >= HEIGHT:
            dy = -dy
        if self.rect.colliderect(player1) and dx < 0:
            dx = -dx
        if self.rect.colliderect(player2) and dx > 0:
            dx = -dx
    def update(self, dx, dy):
        self.rect.x += self.speed * dx
        self.rect.y += self.speed * dy
        
player1 = Paddle(20, 100, 20, 200, 5, 'white')
player2 = Paddle(20, 100, (WIDTH - 40), 200, 5, 'white')
ball = Ball(1, 1, int(350-(ball_radius/2)), rnd(1, (HEIGHT- ball_radius-3)), 6, 'white', ball_radius)

game = True
finish = False
start = True
while game:
    for i in event.get(): 
        if i.type == QUIT or key.get_pressed()[K_ESCAPE]: 
            game = False
        elif i.type == KEYDOWN:
            if finish == True:
                if i.key == K_r:
                    player1.rect.y = 225
                    player2.rect.y = 225
                    ball.rect.x = int(350-(ball_radius/2))
                    ball.rect.y = rnd(1, (HEIGHT- ball_radius -3))
                    sc.fill(Color('black'))
                    dx = q[rnd(0, 1)]
                    dy = q[rnd(0, 1)]
                    start = True
                    finish = False

    player1.reset()
    player2.reset()
    ball.reset()
    sc.blit(score, (325, 10))
    display.update()

    if finish == False:
        sc.fill(Color('black'))
        if finish == False and start == True:
            sleep(1)
            start = False

        player1.update(K_w, K_s)
        player2.update(K_UP, K_DOWN)
        ball.collide(player1.rect, player2.rect)
        ball.update(dx, dy)
        player1.reset()
        player2.reset()
        ball.reset()

    score = qwertz.render(str(score_pl1)+':'+str(score_pl2), True, (200, 200, 200))
    sc.blit(score, (325, 10))
    clock.tick(FPS)
    display.update()