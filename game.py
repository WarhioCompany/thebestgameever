import sys

from def_and_class import generate

import pygame
from config_file.config_game import *
from world import World
from db_manager import get_night, reset_table, get_score, get_money

activ = True
act_word = ""


class Game:
    def __init__(self):
        pygame.init()
        self.font = ARIAL_24
        self.font_50 = ARIAL_50
        self.surface = pygame.display.get_surface()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                              pygame.RESIZABLE)
        # Задаём параметры экрана
        self.clock = pygame.time.Clock()
        self.enemy_sprites = pygame.sprite.Group()
        pygame.display.set_caption("Game")
        self.state = "menu"
        self.night = get_night()
        # Устанавливаем текущее состояние для показа нужной сцены
        self.world = World()

    def draw_start_menu(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 40)
        title = font.render('Игра', True, (255, 255, 255))

        start_button = font.render('Начать - [пробел]', True, (255, 255, 255))
        self.screen.blit(title,
                         (SCREEN_WIDTH / 2 - title.get_width() / 2,
                          SCREEN_HEIGHT / 2 - title.get_height() / 2))
        self.screen.blit(start_button,
                         (SCREEN_WIDTH / 2 - start_button.get_width() / 2,
                          SCREEN_HEIGHT / 2 + start_button.get_height() / 2))
        pygame.display.update()

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 40)
        title = font.render('GAME OVER', True, (255, 255, 255))

        start_button = font.render('Начать - [пробел]', True, (255, 255, 255))
        self.screen.blit(title,
                         (SCREEN_WIDTH / 2 - title.get_width() / 2,
                          SCREEN_HEIGHT / 2 - title.get_height() / 2))
        self.screen.blit(start_button,
                         (SCREEN_WIDTH / 2 - start_button.get_width() / 2,
                          SCREEN_HEIGHT / 2 + start_button.get_height() / 2))
        pygame.display.update()

    def draw_home(self):
        if self.settings:
            self.world.player_in_room.pos = (self.screen.get_size()[0] / 2, 615)
            self.settings = False
        self.screen.fill((0, 0, 0))

        background = pygame.image.load("data/images/room.jpg")
        self.screen.blit(background, (0, 0))
        self.world.room_sprites.draw(self.screen)
        keys = pygame.key.get_pressed()
        self.world.shop.handle_collide(self.world.player_in_room.pos)
        self.world.player.speed = 400 * self.world.shop.get_upgrade_level()[0]
        self.world.player.hp = self.world.shop.get_upgrade_level()[1]
        text = self.font_50.render(f"SCORE: {get_score()}", True, (255, 255, 255))
        self.surface.blit(text, (0, 0))
        text = self.font_50.render(f"MONEY: {get_money()}", True, (255, 255, 255))
        self.surface.blit(text, (300, 0))
        pygame.display.update()
        pygame.display.flip()

    def generate_enemies(self):
        if self.gen:
            for sprite in self.enemy_sprites:
                sprite.kill()
            self.enemy_sprites.add(generate(self.night * 8, 5))
            self.gen = False

    def start_game(self):
        global activ, act_word
        data = []
        activ = True
        act_word = ""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            # Изменение времени в цикле
            t = self.clock.tick() / 1000
            # Переключение сцен
            if self.state == "menu":
                self.draw_start_menu()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    reset_table()
                    self.state = "home"
                    self.settings = True

            elif self.state == "home":
                self.draw_home()
                self.world.player_in_room.update(t)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.gen = True
                    self.state = "game"
                    self.world.timer = 15
                    self.world.player.pos = (SCREEN_WIDTH // 2,
                                             SCREEN_HEIGHT // 2)
                    self.night += 1

                    print("Ночь номер:", self.night)

            elif self.state == "game":
                # Создание мира, отрисовка спрайтов и карты
                self.world.create(t)

                self.generate_enemies()

                if pygame.mouse.get_focused():
                    self.enemy_sprites.update(self.world.player, act_word)
                if activ:
                    activ = False
                    self.enemy_sprites.update(self.world.player, act_word)
                    act_word = ""
                self.enemy_sprites.draw(self.screen)
                for i in range(self.world.player.hp):
                    heart = pygame.image.load("data/images/hp.png")
                    self.screen.blit(heart, (400 + 50 * i, 170))

                if self.world.timer <= 0:
                    self.state = "home"
                elif self.world.player.hp <= 0:
                    print('game over')
                    self.state = "game over"

            elif self.state == "game over":
                self.game_over_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    reset_table()
                    self.state = "home"

            pygame.display.flip()
            pygame.display.update()

    def x(self, q):
        global activ, act_word
        activ = True
        act_word = q
