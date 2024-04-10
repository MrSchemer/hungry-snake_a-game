import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return False

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def handle_collision(self, snack):
        if self.get_head_position() == snack.position:
            self.length += 1
            self.score += 1
            snack.randomize_position()


class Snack:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)


def starting_screen(window):
    font = pygame.font.SysFont(None, 64)
    title_text = font.render("Snake Game", True, GREEN)
    start_text = font.render("Press any key to start", True, BLACK)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height()))
    window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + title_text.get_height()))


def game_over_screen(window, score):
    font = pygame.font.SysFont(None, 64)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))


def main():
 
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')


    starting_screen(window)
    pygame.display.update()
    pygame.time.delay(2000)  

    snake = Snake()
    snack = Snack()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_over = False
        while not game_over and running:
            window.fill(WHITE)
            snake.handle_keys()
            game_over = snake.move()
            snake.handle_collision(snack)
            snake.draw(window)
            snack.draw(window)
            pygame.display.update()
            pygame.time.Clock().tick(15)

        if running:
            game_over_screen(window, snake.score)
            pygame.display.update()
            pygame.time.delay(3000)  

     
            snake.reset()
            snack.randomize_position()

    pygame.quit()  


if __name__ == "__main__":
    main()
