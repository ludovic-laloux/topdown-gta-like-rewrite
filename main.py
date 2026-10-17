import pygame

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True


class Player:
    def __init__(self):
        self.surf = pygame.Surface((20,20))
        self.surf.fill("black")
        self.rect = self.surf.get_rect(center = (screen_width / 2, screen_height / 2))
        self.position = pygame.Vector2(self.rect.center)
        self.speed = 250

    # update first then draw
    def update(self, dt):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_d] - keys[pygame.K_z])
        )

        if movement:
            movement = movement.normalize()

        self.position += movement * self.speed * dt

        half_w = self.rect.width / 2
        half_h = self.rect.height / 2
        self.position.x = max(half_w, min(self.position.x, screen_width - half_w))
        self.position.y = max(half_h, min(self.position.y, screen_height - half_h))

        self.rect.center = self.position

    def draw(self):
        screen.blit(self.surf, self.rect)


player = Player()

while running:
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill("salmon")
    player.update(dt)
    player.draw()

    pygame.display.update()

pygame.quit()