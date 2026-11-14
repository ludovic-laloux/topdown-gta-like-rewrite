import pygame

pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True


class World:
    def __init__(self, width=3000, height=2000):
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.offset = pygame.Vector2()   # top-left of the camera, in world coordinates

        self.surface.fill("salmon")
        # grid lines, only so you can SEE the camera moving (remove later)
        for x in range(0, width, 200):
            pygame.draw.line(self.surface, "white", (x, 0), (x, height))
        for y in range(0, height, 200):
            pygame.draw.line(self.surface, "white", (0, y), (width, y))

    def update_camera(self, target_rect):
        # center on the target, then stop at the world edges
        self.offset.x = target_rect.centerx - screen_width / 2
        self.offset.y = target_rect.centery - screen_height / 2

        self.offset.x = max(0, min(self.offset.x, self.rect.width - screen_width))
        self.offset.y = max(0, min(self.offset.y, self.rect.height - screen_height))

    def draw(self, surface):
        surface.blit(self.surface, (-round(self.offset.x), -round(self.offset.y)))


class Player:
    def __init__(self, world):
        self.surf = pygame.Surface((20, 20))
        self.surf.fill("black")
        self.rect = self.surf.get_rect(center=world.rect.center)
        self.position = pygame.Vector2(self.rect.topleft)
        self.speed = 250

    def get_movement(self):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_q],
            keys[pygame.K_s] - keys[pygame.K_z]
        )
        return movement.normalize() if movement else movement

    def update(self, movement, dt, world):
        self.position += movement * self.speed * dt

        # stay inside the WORLD, not the screen
        self.position.x = max(0, min(self.position.x, world.rect.width - self.rect.width))
        self.position.y = max(0, min(self.position.y, world.rect.height - self.rect.height))

        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def draw(self, surface, offset):
        surface.blit(self.surf, (self.rect.x - round(offset.x), self.rect.y - round(offset.y)))


class Missions:
    def __init__(self):
        self.goal_center = pygame.Vector2(2500, 1500)   # world coordinates
        self.goal_radius = 30
        self.goal_visible = True
        self.complete = False
        self.complete_timer = 0.0
        self.font = pygame.font.Font(None, 40)

    def update(self, player, dt):
        if self.complete:
            if self.complete_timer > 0:
                self.complete_timer -= dt
            return

        # collision test (circle vs rect), all in world coordinates
        closest_x = max(player.rect.left, min(self.goal_center.x, player.rect.right))
        closest_y = max(player.rect.top, min(self.goal_center.y, player.rect.bottom))

        distance = pygame.Vector2(
            closest_x - self.goal_center.x,
            closest_y - self.goal_center.y
        ).length()

        if distance <= self.goal_radius:
            self.goal_visible = False
            self.complete_timer = 2.0
            self.complete = True

    def draw(self, surface, offset):
        # the goal lives in the world, so it follows the camera
        if self.goal_visible:
            pygame.draw.circle(
                surface, "white",
                (round(self.goal_center.x - offset.x), round(self.goal_center.y - offset.y)),
                self.goal_radius,
                width=3
            )

    def draw_ui(self, surface):
        # the text lives on the screen, so no offset
        if self.complete_timer > 0:
            text = self.font.render("MISSION COMPLETE!", True, "white")
            surface.blit(text, (30, 30))
        elif not self.complete:
            text = self.font.render("WALK TO THE MARKED LOCATION", True, "white")
            surface.blit(text, (30, 30))


world = World()
player = Player(world)
missions = Missions()

while running:
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    movement = player.get_movement()
    player.update(movement, dt, world)
    world.update_camera(player.rect)      # after the player moved, so the camera never lags
    missions.update(player, dt)

    world.draw(screen)
    player.draw(screen, world.offset)
    missions.draw(screen, world.offset)
    missions.draw_ui(screen)

    pygame.display.update()

pygame.quit()