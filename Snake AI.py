import pygame
import random
import math

# Board Colors
YELLOW = (255, 255, 0)
GREEN = (255, 0, 0)
GREEN = (255, 0, 0)
RED = (0, 0, 255)

# Board dimensions
BOARD_WIDTH = 900
BOARD_HEIGHT = 700
CELL_SIZE = 15

# Dimensions of snkae
SNAKE_SIZE = CELL_SIZE - 2

# Directions for the snake to move
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


pygame.init()

# Creating a new game window
window = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption("AI Snake Game")


clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        current_head = self.body[0]
        new_head = (current_head[0] + self.direction[0] * CELL_SIZE,
                    current_head[1] + self.direction[1] * CELL_SIZE)
        self.body.insert(0, new_head)

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow(self):
        self.body.append((0, 0))

    def collides_with_boundary(self):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= BOARD_WIDTH or
                head[1] < 0 or head[1] >= BOARD_HEIGHT)

    def collides_with_self(self):
        head = self.body[0]
        return head in self.body[1:]

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(window, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))


class Apple:
    def __init__(self):
        self.position = self.generate_random_position()

    def generate_random_position(self):
        x = random.randint(0, (BOARD_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (BOARD_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return x, y

    def draw(self):
        pygame.draw.rect(window, RED, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))


def heuristic(node, target):
    return math.sqrt((node[0] - target[0]) ** 2 + (node[1] - target[1]) ** 2)


def astar_search(start, target, obstacles):
    open_list = [start]
    closed_list = []
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, target)}
    parents = {}

    while open_list:
        current = min(open_list, key=f_scores.get)

        if current == target:
            path = []
            while current in parents:
                path.insert(0, current)
                current = parents[current]
            return path

        open_list.remove(current)
        closed_list.append(current)

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1,0)]]
        for neighbor in neighbors:
            if (neighbor[0] < 0 or neighbor[0] >= BOARD_WIDTH or
                    neighbor[1] < 0 or neighbor[1] >= BOARD_HEIGHT or
                    neighbor in closed_list or neighbor in obstacles):
                continue

            g_score = g_scores[current] + 1
            if neighbor not in open_list or g_score < g_scores[neighbor]:
                parents[neighbor] = current
                g_scores[neighbor] = g_score
                f_scores[neighbor] = g_score + heuristic(neighbor, target)

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None


def main():
    snake = Snake()
    apple = Apple()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        snake.move()

        if snake.collides_with_boundary() or snake.collides_with_self():
            game_over = True

        if snake.body[0] == apple.position:
            snake.grow()
            apple.position = apple.generate_random_position()

        window.fill(YELLOW)

        snake.draw()
        apple.draw()

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
