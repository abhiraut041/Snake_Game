import pygame
import time
from pygame.locals import *

class Snake:
    # Constants
    SNAKE_SIZE = 10
    SNAKE_SPEED = 15

    def __init__(self, parent_playground):
        self.X = 100
        self.Y = 100
        self.parent_playground = parent_playground
    
    def draw(self):
        self.parent_playground.fill(Game.BLACK)
        pygame.draw.rect(self.parent_playground, Game.WHITE, [self.X, self.Y, self.SNAKE_SIZE, self.SNAKE_SIZE])
        pygame.display.flip()
    
    def move_up(self):
        self.Y -= self.SNAKE_SIZE
        self.draw()

    def move_down(self):
        self.Y += self.SNAKE_SIZE
        self.draw()

    def move_left(self):
        self.X -= self.SNAKE_SIZE
        self.draw()

    def move_right(self):
        self.X += self.SNAKE_SIZE
        self.draw()


class Game:
    # Constants
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    WIDTH, HEIGHT = 600,400

    def __init__(self):
        pygame.init()
        self.playground = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.playground.fill(self.BLACK)
        # init Snake Object
        self.snake = Snake(self.playground)
        self.snake.draw()

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False


if __name__ == '__main__':
    game = Game()
    game.start()