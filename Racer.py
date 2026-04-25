import pygame
import random
import time

# --- INITIALIZATION ---
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Practice 11")
timer = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (218, 165, 32)

# Game variables
speed = 5
score = 0
coins_collected = 0

font_small = pygame.font.SysFont("Verdana", 20)

# --- CLASSES ---

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        # Random weight (1 or 5)
        self.weight = random.choice([1, 5])

        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey(BLACK)

        # Gold for heavy coin, yellow for normal
        color = GOLD if self.weight == 5 else YELLOW
        pygame.draw.circle(self.image, color, (15, 15), 15)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.reset()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -100)

    def move(self):
        global score
        self.rect.move_ip(0, speed)

        # Respawn enemy and increase score
        if self.rect.top > HEIGHT:
            score += 1
            self.rect.top = -100
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((44, 80))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()

        # Move left/right within screen bounds
        if self.rect.left > 0 and keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH and keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)


# --- CREATE OBJECTS ---
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
all_coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# --- GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(WHITE)

    # Draw score and coins
    screen.blit(font_small.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font_small.render(f"Coins: {coins_collected}", True, BLACK), (280, 10))

    # Update and draw all sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
        sprite.move()

    # --- COIN COLLECTION ---
    collected = pygame.sprite.spritecollide(P1, all_coins, False)
    for coin in collected:
        old_coins = coins_collected
        coins_collected += coin.weight

        # Increase speed every 10 coins
        if (coins_collected // 10) > (old_coins // 10):
            speed += 1

        coin.reset()

    # --- COLLISION WITH ENEMY ---
    if pygame.sprite.spritecollideany(P1, enemies):
        screen.fill(RED)

        msg = pygame.font.SysFont("Verdana", 60).render("GAME OVER", True, BLACK)
        screen.blit(msg, (30, 250))
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        exit()

    pygame.display.update()
    timer.tick(60)
