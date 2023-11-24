import os
import time
import random
import pygame


# Initialize font in pygame
pygame.font.init()

# Set Global Parameters
WIDTH, HEIGHT = 650, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


## Load all off the Images
# Ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png")
)
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png")
)  # Player Ship
# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
# Background Image
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)
)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        # self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, "red", (self.x, self.y, 50, 50))


# Create Main Loop
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    ship = Ship((WIDTH / 2 - 25), (HEIGHT - 100))
    main_vel = 5

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, "red")
        WIN.blit(lives_label, (10, 10))

        level_label = main_font.render(f"Level: {level}", 1, "white")
        WIN.blit(level_label, ((WIDTH - level_label.get_width() - 10), 10))

        ship.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ship.x -= main_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ship.x += main_vel
        if keys[pygame.K_s] or keys[pygame.K_UP]:
            ship.y -= main_vel
        if keys[pygame.K_f] or keys[pygame.K_DOWN]:
            ship.y += main_vel


main()
