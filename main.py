import os
import time
import random
import pygame

# Initialize font in pygame
pygame.font.init()

# Set Global Parameters
WIDTH, HEIGHT = 800, 675
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load all off the Images #
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


class Laser:
    def __init__(self, x, y, img, diagonal):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.diagonal = diagonal[0]
        self.direction_diagonal = diagonal[1]

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
        if self.diagonal == 0:
            self.x += (vel*self.direction_diagonal)/2

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 5
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            d = random.randrange(0, 2)
            nop = random.choice([-1, 1])
            diagonal = [d, nop]

            laser = Laser(self.x, self.y, self.laser_image, diagonal)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SPACE_SHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(
            window,
            "red",
            (
                self.x,
                self.y + self.ship_image.get_height() + 10,
                self.ship_image.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            "green",
            (
                self.x,
                self.y + self.ship_image.get_height() + 10,
                self.ship_image.get_width() * (self.health / self.max_health),
                10,
            ),
        )


class EnemyShip(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, diagonal, diagonal_direction, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.diagonal = diagonal
        self.diagonal_direction = diagonal_direction

    def move(self, vel):
        if self.diagonal:
            if self.diagonal_direction == 0:
                self.x += 0.5
            else:
                self.x -= 0.5
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# Create Main Loop
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 100)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player = Player(
        WIDTH / 2 - YELLOW_SPACE_SHIP.get_width() / 2,
        HEIGHT - YELLOW_SPACE_SHIP.get_height() - 25,
    )
    player_vel = 3
    laser_vel = 4

    lost = False
    lost_count = 0

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, "red")
        WIN.blit(lives_label, (10, 10))

        level_label = main_font.render(f"Level: {level}", 1, "white")
        WIN.blit(level_label, ((WIDTH - level_label.get_width() - 10), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            lost_label = lost_font.render("You Lost:(", 1, "red")
            WIN.blit(
                lost_label,
                (
                    (WIDTH / 2 - lost_label.get_width() / 2),
                    (HEIGHT / 2 - lost_label.get_height() / 2),
                ),
            )
            pygame.display.update()

            if lost_count > FPS * 3:
                break
            else:
                continue

        if len(enemies) == 0:
            level += 1
            player.COOLDOWN -= 1
            wave_length += 2
            for i in range(wave_length):
                diagonal = random.choice([True, False*20])
                diagonal_direction = random.choice([0, 1])
                enemy = EnemyShip(
                    random.randrange(50, WIDTH - 50),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"]),
                    diagonal,
                    diagonal_direction
                )
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_a]
            or keys[pygame.K_LEFT]
            and player.x - player_vel > -player.ship_image.get_width() / 2
        ):
            player.x -= player_vel
        if (
            keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
            and player.x + player_vel < WIDTH - player.ship_image.get_width() / 2
        ):
            player.x += player_vel
        if keys[pygame.K_s] or keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if (
            keys[pygame.K_f]
            or keys[pygame.K_DOWN]
            and player.y + player_vel < HEIGHT - player.ship_image.get_height() - 20
        ):
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 4 * 60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            if enemy.y + enemy.ship_image.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            if enemy.x + enemy.ship_image.get_height() > WIDTH or enemy.x < 0:
                enemies.remove(enemy)
        player.move_lasers(-laser_vel, enemies)

        # Shoot Lasers from our main Ship
        player.shoot()


# Run Our main() function
main()
