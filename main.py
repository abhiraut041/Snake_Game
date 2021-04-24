import pygame
import time
import random
from playsound import playsound
from pygame.locals import *

class Constants:
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    GRAY = (200, 200, 200)
    # Food and Snake Dimension
    SNAKE_SIZE = FOOD_SIZE = WALL_UNIT_SIZE = 15
    SNAKE_MID_DIST = FOOD_MID_DIST = 3
    CELL_SIZE = SNAKE_SIZE + SNAKE_MID_DIST
    SNAKE_SPEED = 2
    # Playground Dimensions based on Snake/Food Dimensions
    WIDHT_FACTOR = 25
    HEIGHT_FACTOR = 35
    WIDTH = CELL_SIZE * WIDHT_FACTOR
    HEIGHT = CELL_SIZE * HEIGHT_FACTOR
    # Last three rows will be used to display Game-info
    SNAKE_GROUND_FACTOR = HEIGHT_FACTOR-3
    # Scoreboard Coordinates
    SCOREBOARD_X = 1.5 * CELL_SIZE
    SCOREBOARD_Y = (HEIGHT_FACTOR - 3)*CELL_SIZE
    # Welcome Msg
    WELCOME_MSG = '\n\tWelcome to Snake Game \n \
        Rules : Use arrow keys or WASD to navigate \n \
                Press Esc to play/pause \n \
                Press Q to Quit \n \
        Enjoy..!\n'

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.playground = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        pygame.display.set_caption("Snake Game - by AbhiR")
        self.initialze_game()
    
    def initialze_game(self):
        self.playground.fill(Constants.BLACK)
        # init Snake, Food and Wall Objects
        self.snake = Snake(self.playground, 1)
        self.food = Food(self.playground, self.snake)
        self.wall = Wall(self.playground)
        # placing objects on playground
        self.snake.draw()
        self.food.draw()
        self.wall.draw()
        # Display Welcome msg
        print(Constants.WELCOME_MSG)

    def is_colloision(self, snake_x, snake_y, food_x, food_y):
        c = Constants.CELL_SIZE
        if food_x <= snake_x and (food_x + c) > snake_x:
            if food_y <= snake_y and (food_y + c) > snake_y:
                # Snake can eat food => Colloision Detected
                return True
        return False

    def display_scoreboard(self):
        # Score will be (length of snake - 1)
        score = self.snake.LENGTH - 1
        font = pygame.font.SysFont('arial', 30)
        scr_msg = font.render(f"Score : {score}", True, Constants.GREEN)
        self.playground.blit(scr_msg, (Constants.SCOREBOARD_X, Constants.SCOREBOARD_Y))
    
    def display_game_over(self):
        print(f'Game Over. Your Score is {self.snake.LENGTH-1}.  Colloision Detected..')
        self.playground.fill(Constants.BLACK)
        font = pygame.font.SysFont('arial', 15)
        msg1 = font.render(f"Game Over.. Your Score is {self.snake.LENGTH-1}.", True, Constants.ORANGE)
        msg2 = font.render("Press Enter to try again or Q to Quit.", True, Constants.GREEN)
        self.playground.blit(msg1, (Constants.CELL_SIZE, Constants.CELL_SIZE * Constants.SNAKE_GROUND_FACTOR/2))
        self.playground.blit(msg2, (Constants.CELL_SIZE, Constants.CELL_SIZE*(1.5 + Constants.SNAKE_GROUND_FACTOR/2 )))
        pygame.display.flip()
    
    def reset_game(self):
        print('Starting New Game => \n')
        self.initialze_game()

    def play_sound(self, name):
        try:
            if name == 'food':
                sound = pygame.mixer.Sound("./resources/ding.ogg")
            elif name == 'crash':
                sound = pygame.mixer.Sound("./resources/crash.ogg")
            pygame.mixer.Sound.play(sound)
        except Exception as e:
            print('Cannot Play Music..')

    def start(self):
        running = True
        paused = False
        game_over = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if game_over:
                        if event.key == K_RETURN:
                            paused = False
                            game_over = False
                            self.reset_game()
                        elif event.key == K_q:
                            running = False
                            print('Exiting. Have a Nice Day..!')
                    elif paused:
                        if event.key == K_ESCAPE:
                            paused = False
                            print('Game Resumed..')
                        elif event.key == K_q:
                            running = False
                            print('Exiting. Have a Nice Day..!')
                    elif not paused:
                        if event.key in (K_UP, K_w):
                            self.snake.move_up()
                        elif event.key in (K_DOWN, K_s):
                            self.snake.move_down()
                        elif event.key in (K_LEFT, K_a):
                            self.snake.move_left()
                        elif event.key in (K_RIGHT, K_d):
                            self.snake.move_right()
                        elif event.key == K_ESCAPE:
                            paused = True
                            print('Game Paused. Press Esc to resume..')
                        elif event.key == K_q:
                            running = False
                            print('Exiting. Have a Nice Day..!')
                elif event.type == QUIT:
                    running = False
            try:
                if not paused:
                    self.play()
            except Exception as e:
                print(e)
                self.display_game_over()
                game_over = True
                paused = True

            time.sleep(0.25)
    
    def play(self):
        self.playground.fill(Constants.BLACK)
        self.food.draw()
        self.snake.walk()
        self.wall.draw()
        self.display_scoreboard()
        pygame.display.flip()
        # Check if food can be eaten : Food Collision
        if self.is_colloision(self.snake.X[0], self.snake.Y[0], self.food.X, self.food.Y):
            # add food at new location and increase snake length
            self.food.change_location()
            self.snake.increase_length()
            # adding music
            self.play_sound('food')

        # Check for self-colloision
        for i in range(2, self.snake.LENGTH):
            if self.is_colloision(self.snake.X[0], self.snake.Y[0], self.snake.X[i], self.snake.Y[i]):
                # adding music and rasing Excetion
                self.play_sound('crash')
                raise "Game Over"

class Snake:
    def __init__(self, parent_playground, LENGTH=15):
        self.LENGTH = LENGTH if LENGTH >= 1 else 1
        self.X = [Constants.CELL_SIZE] * self.LENGTH
        self.Y = [Constants.CELL_SIZE] * self.LENGTH
        self.parent_playground = parent_playground
        self.DIRECTION = "RIGHT"
    
    def draw(self):
        for i in range(self.LENGTH):
            pygame.draw.rect(self.parent_playground, Constants.GREEN, [self.X[i], self.Y[i], Constants.SNAKE_SIZE, Constants.SNAKE_SIZE])

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
        
        # print(self.X,self.Y)
        self.draw()
    
    def increase_length(self):
        self.LENGTH += 1
        # -1 is appended as the walk method will take care of adding
        # correct values duriing normal operation
        self.X.append(-1)
        self.Y.append(-1)

class Food:
    def __init__(self, parent_playground, snake):
        self.parent_playground = parent_playground
        self.snake = snake
        self.X, self.Y = self.get_valid_location()
    
    def draw(self):
        pygame.draw.circle(self.parent_playground, Constants.ORANGE, (self.X+Constants.FOOD_SIZE/2, self.Y+Constants.FOOD_SIZE/2), Constants.FOOD_SIZE/2)
    
    def change_location(self):
        self.X, self.Y = self.get_valid_location()
    
    def get_valid_location(self):
        # ignoring first and last cell as it is wall
        tmp_x = Constants.CELL_SIZE * random.randint(1,Constants.WIDHT_FACTOR-2)
        tmp_y = Constants.CELL_SIZE * random.randint(1,Constants.SNAKE_GROUND_FACTOR-2)
        # Food not on body
        snake_body = [(self.snake.X[i], self.snake.Y[i]) for i in range(self.snake.LENGTH)]
        while (tmp_x, tmp_y) in snake_body:
            tmp_x = Constants.CELL_SIZE * random.randint(1,Constants.WIDHT_FACTOR-2)
            tmp_y = Constants.CELL_SIZE * random.randint(1,Constants.SNAKE_GROUND_FACTOR-2)
        return tmp_x, tmp_y

class Wall:
    def __init__(self, parent_playground):
        self.parent_playground = parent_playground
    
    def draw(self):
        # top border
        for i in range(Constants.WIDHT_FACTOR):
            x = i * Constants.CELL_SIZE
            y = 0
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # first-down border
        for i in range(Constants.WIDHT_FACTOR):
            x = i * Constants.CELL_SIZE
            y = Constants.CELL_SIZE * (Constants.SNAKE_GROUND_FACTOR - 1)
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # second-last border
        for i in range(Constants.WIDHT_FACTOR):
            x = i * Constants.CELL_SIZE
            y = Constants.HEIGHT - Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # left border
        for i in range(Constants.HEIGHT_FACTOR):
            x = 0
            y = i * Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])
        # right border
        for i in range(Constants.HEIGHT_FACTOR):
            x = Constants.WIDTH - Constants.CELL_SIZE
            y = i * Constants.CELL_SIZE
            pygame.draw.rect(self.parent_playground, Constants.WHITE, [x, y, Constants.WALL_UNIT_SIZE, Constants.WALL_UNIT_SIZE])

if __name__ == '__main__':
    # Start the game..!
    game = Game()
    game.start()