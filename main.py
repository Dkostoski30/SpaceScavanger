import pygame
import random
import sys

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


RESOURCES = "./resources/"
SPACESHIP_IMG = pygame.image.load(RESOURCES + "spaceship.png")
ASTEROID_IMG = pygame.image.load(RESOURCES + "asteroid.png")
ENERGY_CRYSTAL_IMG = pygame.image.load(RESOURCES + "energy_crystal.png")
BACKGROUND_MUSIC = RESOURCES + "background_music.wav"
CLASH_SOUND = pygame.mixer.Sound(RESOURCES + "clash_sound.wav")


SPACESHIP = pygame.transform.scale(SPACESHIP_IMG, (50, 50))
ASTEROID = pygame.transform.scale(ASTEROID_IMG, (40, 40))
ENERGY_CRYSTAL = pygame.transform.scale(ENERGY_CRYSTAL_IMG, (30, 30))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()


pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)

class Spaceship:
    def __init__(self):
        self.image = SPACESHIP
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.hitbox = self.rect.inflate(-10, -10)
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        self.hitbox = self.rect.inflate(-10, -10)

    def draw(self):
        screen.blit(self.image, self.rect)


class Asteroid:
    def __init__(self):
        self.original_image = ASTEROID
        self.image = self.original_image
        self.rect = self.image.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        )
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(3, 6)
        self.update_orientation()

    def update_orientation(self):
        if self.speed_x > 0:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.speed_x < 0:
            self.image = self.original_image
        elif self.speed_x == 0 and self.speed_y > 0:
            self.image = pygame.transform.rotate(self.original_image, 45)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        screen.blit(self.image, self.rect)


class EnergyCrystal:
    def __init__(self):
        self.image = ENERGY_CRYSTAL
        self.rect = self.image.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        )
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)


def start_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    title_text = font.render("Space Scavenger", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

    font = pygame.font.SysFont(None, 36)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    start_screen()
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    crystals = [EnergyCrystal()]
    stars = [Star() for _ in range(120)]
    score = 0
    asteroid_speed_multiplier = 1
    star_speed_multiplier = 1
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if score % 50 == 0 and score != 0:
            asteroid_speed_multiplier += 0.002
            star_speed_multiplier += 0.002

        for star in stars:
            star.y += int(star.speed * star_speed_multiplier)
            if star.y > SCREEN_HEIGHT:
                star.y = 0
                star.x = random.randint(0, SCREEN_WIDTH)
            star.draw()

        keys = pygame.key.get_pressed()
        spaceship.move(keys)
        spaceship.draw()

        for asteroid in asteroids:
            asteroid.rect.x += int(asteroid.speed_x * asteroid_speed_multiplier)
            asteroid.rect.y += int(asteroid.speed_y * asteroid_speed_multiplier)
            asteroid.draw()

            if asteroid.rect.top > SCREEN_HEIGHT or asteroid.rect.right < 0:
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())

            if spaceship.hitbox.colliderect(asteroid.rect):
                pygame.mixer.Sound.play(CLASH_SOUND)
                running = False

        for crystal in crystals:
            crystal.move()
            crystal.draw()
            if crystal.rect.top > SCREEN_HEIGHT:
                crystals.remove(crystal)
                crystals.append(EnergyCrystal())

            if spaceship.hitbox.colliderect(crystal.rect):
                score += 10
                crystals.remove(crystal)
                crystals.append(EnergyCrystal())

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    game_over_screen(score)

if __name__ == "__main__":
    main()
