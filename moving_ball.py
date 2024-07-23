from math import floor

import pygame

pygame.init()

HEIGHT, WIDTH = 800, 800
WIN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("A Ball that moves around")

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
FONT = pygame.font.SysFont("Helvetica", 48)



class Ball:
    def __init__(self, x, y, radius=10, color=GREEN, x_vel=0, y_vel=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.x_vel = x_vel
        self.y_vel = y_vel

    def check_hit(self):

        if self.x + self.radius >= WIDTH:
            return False
            #self.x_vel = -self.x_vel

        if self.y -self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.y_vel = -self.y_vel
        
        if self.x - self.radius <= 0:
            return False
            #self.x_vel = -self.x_vel

        return True
        
    def bounce(self):
        self.x_vel = -self.x_vel 

    def get_coords(self):
        return (self.x - self.radius, self.x + self.radius, self.y)

    def player_move(self, x, y):
        self.x_vel = x
        self.y_vel = y
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.x = abs((self.radius + 5) - (WIDTH * (self.x + self.radius >= 800)))
        
        if self.y -self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.y = abs((self.radius + 5) - (HEIGHT * (self.y +self.radius >= 800))) 

        self.x += self.x_vel
        self.y += self.y_vel

    def auto_move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
class Paddle:

    def __init__(self, x, y, upper_bound=0, lower_bound=HEIGHT, width=20, color=BLUE):
        self.x = x
        self.y = y
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.color = color 
        self.width = width
        self.height = width * 6
        self.y_vel = 0
    
    def player_move(self, y):
        self.y_vel = y

        self.y += self.y_vel
        if self.y <= self.upper_bound or self.y >= (self.lower_bound - self.height):
            self.y = (self.upper_bound) + ((self.lower_bound - self.height - self.upper_bound) * (self.y + self.height >= self.lower_bound))
            """
            the self.y formula is fuck and anyone who askes me to explain why it works will get an explanation, and then be shot becuase it was so
            painfull and yet now I feel like an dumbass for not seeing as it was basic algebra
            """

    def return_coords(self):
        return (self.x + self.width, self.x, self.y, self.y + self.height)

    def check_hit(self, other, paddle_on_left=True):
        other_x_right, other_x_left, other_y = other.get_coords()

        if other_x_right <= self.x + self.width and paddle_on_left and other_y >= self.y and other_y <= self.y + self.height:
            other.bounce()

        if other_x_left >= self.x and not paddle_on_left and other_y >= self.y and other_y <= self.y + self.height:
            other.bounce()



    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        

    



def main(mode = 'keyboard', debug=False):
    run: bool = True
    clock = pygame.time.Clock()
    ball = Ball(400, 400, 10, GREEN, 2, 1.4)
    paddle = Paddle(50, 50)
    paddle2 = Paddle(WIDTH-70, 50, 0, HEIGHT, 20, RED)
    score: int = 0
    alive: bool = True
    alive2: bool = True
    motion: list = [0, 0]
    player_1_win = False
    plaery_2_win = False
    
    

    
    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if debug:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        paddle.player_move(-5)

                    if event.key == pygame.K_DOWN:
                        paddle.player_move(5)

        if mode == 'keyboard':
            if keys[pygame.K_w]:
                paddle.player_move(-5)

            if keys[pygame.K_s]:
                paddle.player_move(5)
            
            if keys[pygame.K_UP]:
                paddle2.player_move(-5)

            if keys[pygame.K_DOWN]:
                paddle2.player_move(5)

        if mode == 'gamepad':
            
            for joystick in joysticks:

                if joystick.get_instance_id() == 0:
                    if abs(joystick.get_hat(0)[1]) == 1:
                        motion[0] = -joystick.get_hat(0)[1] * 5
                
                if joystick.get_instance_id() == 1:
                    if abs(joystick.get_hat(0)[1]) == 1:
                        motion[1] = -joystick.get_hat(0)[1] * 5

                
                

            paddle.player_move(motion[0])
            #paddle2.player_move(motion[1])
            


        if alive and alive2:
            paddle.draw(WIN)
            paddle2.draw(WIN)
            ball.auto_move()
            alive = ball.check_hit()
            paddle.check_hit(ball)
            paddle2.check_hit(ball, False)
            #alive2 = ball.check_hit(paddle2.return_coords(), 'right')
            ball.draw(WIN)
            score += 0.05
        if not alive or not alive2:    
            score_text = FONT.render(f"Your score: {floor(score)} Points", 1, WHITE)
            WIN.blit(score_text, (WIDTH/2 - 0.5 * score_text.get_width(), HEIGHT/4 - score_text.get_height()/2))

        

        pygame.display.update()
    print(floor(score))    
    pygame.quit()            


main()
