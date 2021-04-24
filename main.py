import pygame
import time
from pygame.locals import *

class Constants:
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    # Food and Snake Dimension
    SNAKE_SIZE = FOOD_SIZE = WALL_UNIT_SIZE = 15
    SNAKE_MID_DIST = FOOD_MID_DIST = 3
    CELL_SIZE = SNAKE_SIZE + SNAKE_MID_DIST
    SNAKE_SPEED = 2
    # Playground Dimensions based on Snake/Food Dimensions
    WIDHT_FACTOR = 50
    HEIGHT_FACTOR = 27
    WIDTH = CELL_SIZE*WIDHT_FACTOR
    HEIGHT = CELL_SIZE*HEIGHT_FACTOR

class Game:
    def __init__(self):
        pygame.init()
        self.playground = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.playground.fill(Constants.BLACK)
        # init Snake, Food and Wall Objects
        self.snake = Snake(self.playground)
        self.food = Food(self.playground)
        self.wall = Wall(self.playground)
        self.snake.draw()
        self.food.draw()
        self.wall.draw()

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
            self.play()
            time.sleep(0.18)
    
    def play(self):
        self.snake.walk()
        self.food.draw()
        self.wall.draw()

class Snake:
    def __init__(self, parent_playground, LENGTH=15):
        self.LENGTH = LENGTH
        self.X = [Constants.CELL_SIZE] * self.LENGTH
        self.Y = [Constants.CELL_SIZE] * self.LENGTH
        self.parent_playground = parent_playground
        self.DIRECTION = "RIGHT"
    
    def draw(self):
        self.parent_playground.fill(Constants.BLACK)
        for i in range(self.LENGTH):
            pygame.draw.rect(self.parent_playground, Constants.GREEN, [self.X[i], self.Y[i], Constants.SNAKE_SIZE, Constants.SNAKE_SIZE])
        # flip() => Called in Wall class draw method as it is better to call flip method once per event while loop execution to reduce flickering effect.
        # pygame.display.flip()

    def move_up(self):
        if self.DIRECTION != "DOWN":
            self.DIRECTION = "UP"

    def move_down(self):
        if self.DIRECTION != "UP":
            self.DIRECTION = "DOWN"

    def move_left(self):
        if self.DIRECTION != "RIGHT":
            self.DIRECTION = "LEFT"

    def move_right(self):
        if self.DIRECTION != "LEFT":
            self.DIRECTION = "RIGHT"
    
    def walk(self):
        for i in range(self.LENGTH-1, 0, -1):
            self.X[i] = self.X[i-1]
            self.Y[i] = self.Y[i-1]

        if self.DIRECTION == "UP":
            self.Y[0] -= Constants.SNAKE_SIZE + Constants.SNAKE_MID_DIST
        elif self.DIRECTION == "DOWN":
            self.Y[0] += Constants.SNAKE_SIZE + Constants.SNAKE_MID_DIST
        elif self.DIRECTION == "LEFT":
            self.X[0] -= Constants.SNAKE_SIZE + Constants.SNAKE_MID_DIST
        elif self.DIRECTION == "RIGHT":
            self.X[0] += Constants.SNAKE_SIZE + Constants.SNAKE_MID_DIST
        
        print(self.X,self.Y)
        self.draw()

class Food:
    def __init__(self, parent_playground):
        self.parent_playground = parent_playground
        self.X = Constants.CELL_SIZE*4
        self.Y = Constants.CELL_SIZE*4
    
    def draw(self):
        pygame.draw.circle(self.parent_playground, Constants.ORANGE, (self.X+Constants.FOOD_SIZE/2, self.Y+Constants.FOOD_SIZE/2), Constants.FOOD_SIZE/2)
        # pygame.display.flip() # Called in Wall class draw method

class Wall:
    def __init__(self, parent_playground):
        self.parent_playground = parent_playground
    
    def draw(self):
        # top border
        for i in range(Constants.WIDHT_FACTOR):
            x = i * Constants.CELL_SIZE
            y = 0
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # down border
        for i in range(Constants.WIDHT_FACTOR):
            x = i * Constants.CELL_SIZE
            y = Constants.HEIGHT - Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # left border
        for i in range(Constants.WIDHT_FACTOR):
            x = 0
            y = i * Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # right border
        for i in range(Constants.WIDHT_FACTOR):
            x = Constants.WIDTH - Constants.CELL_SIZE
            y = i * Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # refreshing the screen
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.start()