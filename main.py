import pygame

pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True


class Player:
    def __init__(self):
        self.surf = pygame.Surface((20,20))
        self.surf.fill("black")
        self.rect = self.surf.get_rect(
            topleft = ((screen_width - self.surf.get_width()) / 2,
                        (screen_height - self.surf.get_height()) / 2)
            )
        self.position = pygame.Vector2(self.rect.topleft)
        self.speed = 350

    def get_movement(self):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_q],
            keys[pygame.K_s] - keys[pygame.K_z]
            )
        return movement.normalize() if movement else movement

    def update(self, movement, dt):
        self.position += movement * self.speed * dt

        self.position.x = max(0, min(self.position.x, screen_width - self.rect.width))
        self.position.y = max(0, min(self.position.y, screen_height - self.rect.height))

        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

class Missions:
    def __init__(self):
        self.goal_center = pygame.Vector2(1020, 520)
        self.goal_radius = 50
        self.goal_visible = True

    def update(self, player):
        closest_x = max(player.rect.left, min(self.goal_center.x, player.rect.right))
        closest_y = max(player.rect.top, min(self.goal_center.y, player.rect.bottom))

        distance = pygame.Vector2(
            closest_x - self.goal_center.x,
            closest_y - self.goal_center.y
        ).length()

        if distance <= self.goal_radius:
            self.goal_visible = False

    def draw(self):
        if self.goal_visible:
            pygame.draw.circle(
                screen, "white",
                (round(self.goal_center.x), round(self.goal_center.y)),
                self.goal_radius,
                width=2
            )

player = Player()
missions = Missions()

while running:
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill("salmon")

    missions.update(player)
    missions.draw()

    movement = player.get_movement()
    player.update(movement, dt)

    player.draw(screen)

    pygame.display.update()

pygame.quit()