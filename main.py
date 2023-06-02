import pygame
import pygame_menu
import random
import sys
from typing import Tuple, Any
from math import isclose


class Fruit:
    def __init__(self, display_width, display_height):
        self.snake_width = 25
        self.snake_height = 25
        self.display_width = display_width
        self.display_height = display_height
        self.food_position = [random.randrange(1, (self.display_width // 10)) * 10,
                              random.randrange(1, (self.display_height // 10)) * 10]

    def respawn(self):
        self.food_position = [random.randrange(1, (self.display_width // 10)) * 10,
                              random.randrange(1, (self.display_height // 10)) * 10]

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 255),
                         (self.food_position[0], self.food_position[1], self.snake_width / 2, self.snake_height / 2))


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display_width = 600
        self.display_height = 400
        self.green = (0, 255, 0)
        self.brown = (158, 25, 25)
        self.difficulty = 25
        self.win = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Snake Game by Ermin Lilaj')
        self.clock = pygame.time.Clock()
        self.player_name = ''
        self.default_player_name = True
        self.music = pygame.mixer.music.load('crunch.wav')

    def set_game_difficulty(self, selected: Tuple, value: Any):
        if value == 1:
            self.difficulty = 25
        elif value == 2:
            self.difficulty = 50
        elif value == 3:
            self.difficulty = 100
        else:
            self.difficulty = 25

    def set_player_name(self, name):
        self.player_name = name
        self.default_player_name = False

    def set_default_player_name(self):
        self.player_name = "Guest"
        self.default_player_name = False

    def show_start_screen(self):
        start_menu = pygame_menu.Menu(width=self.display_width, height=self.display_height,
                                      title='Welcome to Snake Game!', theme=pygame_menu.themes.THEME_ORANGE)
        start_menu.add.text_input("Your Name: ", default="Player", onchange=self.set_player_name)
        start_menu.add.selector("Difficulty: ", [("Easy", 1), ("Medium", 2), ("Hard", 3)], onchange=self.set_game_difficulty)
        start_menu.add.button("Play", self.game_loop)
        start_menu.add.button("Quit", pygame_menu.events.EXIT)
        if self.default_player_name:
            self.set_default_player_name()
        start_menu.mainloop(self.win)

    def replay_game(self):
        self.game_loop()

    def show_end_screen(self, game_score):
        end_menu = pygame_menu.Menu(width=self.display_width, height=self.display_height, title='Game Over',
                                    theme=pygame_menu.themes.THEME_ORANGE)
        end_menu.add.label("Your Score:" + str(game_score))
        end_menu.add.button("Replay Game", self.replay_game)
        end_menu.add.button("Quit Game", pygame_menu.events.EXIT)
        end_menu.mainloop(self.win)

    def game_loop(self):
        x = self.display_width / 2
        y = self.display_height / 2
        snake_position = [self.display_width / 2, self.display_height / 2]
        snake_body = [[self.display_width / 2, self.display_height / 2],
                      [(self.display_width / 2) - 10, self.display_height / 2],
                      [(self.display_width / 2) - (2 * 10), self.display_width / 2]]
        snake_width = 25
        snake_height = 25
        snake_speed = 5
        snake_direction = "UP"
        new_direction = snake_direction
        gameExit = False
        game_score = 0

        fruit = Fruit(self.display_width, self.display_height)

        while not gameExit:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
                break
            if keys[pygame.K_LEFT]:
                new_direction = "LEFT"
            if keys[pygame.K_RIGHT]:
                new_direction = "RIGHT"
            if keys[pygame.K_UP]:
                new_direction = "UP"
            if keys[pygame.K_DOWN]:
                new_direction = "DOWN"
            if snake_direction != "UP" and new_direction == "DOWN":
                snake_direction = new_direction
            if snake_direction != "DOWN" and new_direction == "UP":
                snake_direction = new_direction
            if snake_direction != "LEFT" and new_direction == "RIGHT":
                snake_direction = new_direction
            if snake_direction != "RIGHT" and new_direction == "LEFT":
                snake_direction = new_direction

            if snake_direction == "UP":
                snake_position[1] -= snake_speed
            if snake_direction == "DOWN":
                snake_position[1] += snake_speed
            if snake_direction == "LEFT":
                snake_position[0] -= snake_speed
            if snake_direction == "RIGHT":
                snake_position[0] += snake_speed

            snake_body.insert(0, list(snake_position))
            if isclose(snake_position[0], fruit.food_position[0], abs_tol=5) and \
                    isclose(snake_position[1], fruit.food_position[1], abs_tol=5):
                pygame.mixer.music.play(1)
                game_score += 10
                fruit.respawn()
            else:
                snake_body.pop()

            if snake_position in snake_body[1:]:
                self.show_end_screen(game_score)

            self.win.fill(self.green)
            for pos in snake_body:
                pygame.draw.rect(self.win, self.brown, pygame.Rect(pos[0], pos[1], snake_width / 2, snake_height / 2))

            fruit.draw(self.win)

            if snake_position[0] < 0 or snake_position[0] > (self.display_width - snake_width / 2):
                self.show_end_screen(game_score)
            if snake_position[1] < 0 or snake_position[1] > (self.display_height - snake_height / 2):
                self.show_end_screen(game_score)

            self.show_game_score('consolas', 20, game_score)
            pygame.display.update()

            self.clock.tick(self.difficulty)

    def show_game_score(self, font, size, game_score):
        game_score_font = pygame.font.SysFont(font, size)
        game_score_surface = game_score_font.render((self.player_name + "'s Game Score: " + str(game_score)),
                                                    True, self.brown)
        game_score_rect = game_score_surface.get_rect()
        game_score_rect.midtop = (self.display_width / 2, 15)
        self.win.blit(game_score_surface, game_score_rect)


game = SnakeGame()
game.show_start_screen()
