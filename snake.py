import pygame
from enum import Enum
import random

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

WIDTH, HEIGHT = 400, 500
BLOCK_WIDTH = WIDTH // 10
BLOCK_HEIGHT = HEIGHT // 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()


class Direction(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


class Snake:
    def __init__(self, direction=Direction.UP, color=GREEN, head_color=CYAN):
        self.score = 2
        self.pos_x = BLOCK_WIDTH // 2
        self.pos_y = BLOCK_HEIGHT // 2
        self.direction = direction
        self.color = color
        self.head_color = head_color
        # Time left for each block of snake body
        self.body = [[0 for _ in range(BLOCK_WIDTH)] for _ in range(BLOCK_HEIGHT)]
        self.body[self.pos_y][self.pos_x] = 2
        self.body[self.pos_y - 1][self.pos_x] = 1


    def update(self, direction):
        for i, row in enumerate(self.body):
            for k, block_val in enumerate(row):
                if block_val > 0:
                    self.body[i][k] = block_val - 1

        if direction == Direction.UP:
            self.pos_y -= 1
        elif direction == Direction.DOWN:
            self.pos_y += 1
        elif direction == Direction.RIGHT:
            self.pos_x += 1
        elif direction == Direction.LEFT:
            self.pos_x -= 1

        if (self.pos_x < 0) or (self.pos_x >= BLOCK_WIDTH) or (self.pos_y < 0) or (self.pos_y >= BLOCK_HEIGHT):
            return False
        elif (self.body[self.pos_y][self.pos_x] > 0):
            return False

        self.body[self.pos_y][self.pos_x] = self.score
        return True


    def display(self):
        for i, row in enumerate(self.body):
            for k, block_val in enumerate(row):
                if block_val > 0:
                    block_rect = pygame.Rect(k * 10, i * 10, 10, 10)
                    if (block_val == self.score):
                        pygame.draw.rect(screen, self.head_color, block_rect)
                    else:
                        pygame.draw.rect(screen, self.color, block_rect)


    def get_position(self):
        return (self.pos_x, self.pos_y)
    
    def has_block(self, pos_x, pos_y):
        return self.body[pos_y][pos_x] > 0
    
        

class Food:
    def __init__(self, pos_x, pos_y, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color

    def move(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def display(self):
        block_rect = pygame.Rect(self.pos_x * 10, self.pos_y * 10, 10, 10)
        pygame.draw.rect(screen, self.color, block_rect)

    def get_position(self):
        return (self.pos_x, self.pos_y)
        


def main():
    running = True
    FPS = 10
    pause = False

    snake = Snake()
    food = Food(30, 30, WHITE)
    direction = Direction.UP

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != Direction.DOWN:
                        direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if direction != Direction.UP:
                        direction = Direction.DOWN
                elif event.key == pygame.K_RIGHT:
                    if direction != Direction.LEFT:
                        direction = Direction.RIGHT
                elif event.key == pygame.K_LEFT:
                    if direction != Direction.RIGHT:
                        direction = Direction.LEFT

        if not pause:
            if snake.update(direction) is False:
                pause = True

        snake.display()

        if snake.get_position() == food.get_position():
            snake.score += 1
            while True:
                food_x, food_y = random.randint(0, BLOCK_WIDTH - 1), random.randint(0, BLOCK_HEIGHT - 1)
                if not snake.has_block(food_x, food_y):
                    food.move(food_x, food_y)
                    break
                
        food.display()

        text = font20.render(f'score: {snake.score - 2}', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (50, 30)
        screen.blit(text, textRect)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()