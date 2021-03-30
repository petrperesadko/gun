import pygame
import random
import colors
import math as m
WIDTH = 800
HEIGHT = 650
FPS = 60
pygame.init()

# --------------------------
# Функция сложения векторов

font = pygame.font.Font( "arial.ttf" , 32)



def add_vectors(angle1, length1, angle2, length2):
    x = m.sin(angle1) * length1 + m.sin(angle2) * length2
    y = m.cos(angle1) * length1 + m.cos(angle2) * length2
    angle = 0.5 * m.pi - m.atan2(y, x)
    length = m.hypot(x, y)
    return angle, length

# --------------------------
# Функция столкновения объектов


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = m.hypot(dx, dy)

    if dist < p1.size + p2.size:
        tangent = m.atan2(dy, dx)
        angle = 0.5 * m.pi + tangent
        angle1 = 2 * tangent - p1.alpha
        speed1 = p1.speed * p1.elasticity
        (p1.alpha, p1.speed) = (angle1, speed1)
        p1.x += m.sin(angle)
        p1.y -= m.cos(angle)

        return True

# --------------------------


class Cannon(pygame.sprite.Sprite):

    def __init__(self, length, angle):
        super().__init__()
        self.x = 100
        self.y = 550
        self.length = length
        self.angle = angle
        self.time = 0

    def display(self):
        # surface = pygame.Surface((20, 20))
        pygame.draw.circle(screen, colors.BLACK, (self.x, self.y), 10)
        # surface.fill(colors.THISTLE)
        # a = pygame.draw.circle(screen, colors.MAROON, (10, 5), 5)
        # pygame.transform.rotate(screen, m.pi/2)
        # screen.blit(screen, (100, 500))

# --------------------------


class Target(pygame.sprite.Sprite):

    def __init__(self, x, y, size):
        super().__init__()
        self.size = size
        self.x = x
        self.y = y
        self.is_collided = False

    def display(self):
        pygame.draw.circle(screen, colors.BLACK, (self.x, self.y), self.size)

# --------------------------


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, alpha):
        super().__init__()
        self.x = x
        self.y = y
        self.alpha = alpha
        self.speed = speed
        self.top_speed = speed
        self.size = 10
        self.elasticity = 0.8
        self.drag = 0.995

    def display(self):
        pygame.draw.circle(screen, colors.BLACK, (self.x, self.y), self.size)

    def move(self):
        (self.alpha, self.speed) = add_vectors(self.alpha, self.speed, m.pi, 0.3)
        self.x += m.sin(self.alpha) * self.speed
        self.y -= m.cos(self.alpha) * self.speed
        self.speed *= self.drag
        # if self.speed <= self.top_speed:
        #     print("killed")
        #     self.kill()

    def bounce(self):

        if self.x >= WIDTH - self.size:
            self.x = 2 * (WIDTH - self.size) - self.x
            self.alpha = - self.alpha
            self.speed *= self.elasticity

        elif self.x <= self.size:
            self.x = 2 * self.size - self.x
            self.alpha = - self.alpha
            self.speed *= self.elasticity

        if self.y >= HEIGHT - self.size:
            self.y = 2 * (HEIGHT - self.size) - self.y
            self.alpha = m.pi - self.alpha
            self.speed *= self.elasticity
            self.speed *= self.elasticity

        elif self.y <= self.size:
            self.y = 2 * self.size - self.y
            self.alpha = m.pi - self.alpha
            self.speed *= self.elasticity

# --------------------------
# Создание игры

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# --------------------------

cannon = Cannon(20, m.pi/2)

# --------------------------
running = True
game = True
# --------------------------
# Цикл игры
while game:
    target = Target(random.randint(500, WIDTH - 50), random.randint(500, HEIGHT - 50), random.randint(20, 30))
    bullets = []
    # group = pygame.sprite.Group
    bullet1 = Bullet(100, 550, 0, 0)
    bullets.append(bullet1)
    counter = 0
    number_of_hits = 0
    moved = True
    started = False
    down = False
    start_time = 0
    end_time = 0
    sec = 0
    collided = False
    while running:
        clock.tick(FPS)
        SPEED = 0
        (mouseX, mouseY) = (0, 0)
        mouse = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_time = pygame.time.get_ticks()
                started = True
                down = False
            elif event.type == pygame.MOUSEBUTTONUP:
                end_time = pygame.time.get_ticks()
                (mouseX, mouseY) = pygame.mouse.get_pos()
                started = False
                down = True
                sec = 0
            if event.type == pygame.MOUSEMOTION:
                moved = True
            else:
                moved = False
            if down and not moved:
                sec = end_time - start_time

        if down and not started:
            started = True
            angle = m.atan((550 - mouseY) / (mouseX - 100))
            bullet = Bullet(100, 550, 5 + sec / 100, m.pi / 2 - angle)
            print(f"bullet {counter + 1} speed is {sec}")
            bullets.append(bullet)
            counter += 1
            number_of_hits += 1

        if down and counter > 0:
            bullets[counter].move()
            bullets[counter].bounce()
            bullets[counter].display()


        cannon.display()
        target.display()


        if counter > 0:
            if collide(bullets[counter], target):
                print("you killed the target in ", number_of_hits, " hits")
                running = False
                collided = True

        pygame.display.flip()
        screen.fill(colors.THISTLE)

    running = True

    text = font.render(f'You killed the target in {number_of_hits} hits!', colors.GREEN, colors.BLUE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, textRect)
    pygame.display.flip()
    pygame.time.delay(1000)

pygame.quit()
