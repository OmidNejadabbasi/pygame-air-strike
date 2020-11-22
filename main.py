import pygame
import random

pygame.init()
clock = pygame.time.Clock()

size = width, height = 800, 500
# font of current score
my_font = pygame.font.SysFont('Helvetica', 25)

my_screen = pygame.display.set_mode(size)
pygame.display.set_caption("Boooooooom !!!!")

# defining game variables
move_speed = 3
score = 0
last_strike = pygame.time.get_ticks()
alien_interval = 600

# load images
jet = pygame.image.load('res/jet.png')
alien = pygame.image.load('res/alien.png')
bullet = pygame.image.load('res/bullet.png')
bg = pygame.image.load('res/bg.png')


# A function for drawing score on the my_screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    my_screen.blit(img, (x, y))


class Jet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = jet
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [35, pygame.mouse.get_pos()[1]]
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += 20  # bullet speed
        if self.rect.x > width + 100:
            self.kill()
            pass


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = alien
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step_y = random.randrange(-5, 5)
        self.step_x = random.randrange(6, 10)

    def update(self):
        self.rect.x -= self.step_x
        if self.rect.bottomleft[1] > height or self.rect.topleft[1] < 0:
            self.step_y = - self.step_y

        self.rect.y -= self.step_y
        pass


# Sprite groups
alien_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
jet_group = pygame.sprite.Group()

jet_sprite = Jet(100, 100)
jet_group.add(jet_sprite)

# Game loop goes here
running = True
while running:
    clock.tick(50)  # This game is 50 fps
    my_screen.blit(bg, (0, 0))

    alien_group.draw(my_screen)
    jet_group.draw(my_screen)
    bullet_group.draw(my_screen)

    jet_group.update()
    bullet_group.update()
    alien_group.update()

    now = pygame.time.get_ticks()
    if now - last_strike > alien_interval:
        alien_group.add(Alien(width, random.randrange(50, height - 50)))
        last_strike = now

    # collisions
    for i in alien_group:
        for j in bullet_group:
            if pygame.sprite.collide_rect(i, j):
                i.kill()
                j.kill()
                score += 1
                pygame.mixer.music.load('res/explosion.mp3')
                pygame.mixer.music.play()

    for i in alien_group:
        if i.rect.x < -10:
            running = False
            print('---------------------    GAME OVER    --------------------------')
            print(f"Your score was : {score}")

    # displaying score

    your_score = my_font.render(f"Score : {score}", False, (20, 20, 20))
    my_screen.blit(your_score, (5, height-30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(Bullet(jet_sprite.rect.center[0] + 25, jet_sprite.rect.center[1] - 5))
            pygame.mixer.music.load('res/fire.mp3')
            pygame.mixer.music.play()

            print('shuttle is at x :  ', jet_sprite.rect.x)

    pygame.display.update()

pygame.quit()
