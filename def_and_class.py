import game
from config_file.config_game import *

from pynput.keyboard import Listener
import pygame
import os
import sys
import random
from db_manager import update_score_and_money, get_money


screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
sprite = pygame.sprite.Sprite()
pygame.init()
screen.fill(pygame.Color("white"))
font = pygame.font.Font(None, 20)


def str_key(key):
    return str(key)[1]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Enemy(pygame.sprite.Sprite):
    def __init__(self,
                 player_pos,
                 name,
                 speed,
                 image_name,
                 score,
                 tup,
                 *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(image_name), (76, 84))
        self.speed = speed
        self.name = name
        self.score = score
        self.tup = tup
        self.rect = self.image.get_rect()
        if self.tup == 0:
            top = random.randint(0, 2)
            if top:
                self.rect.x = random.choice([random.randint(-200, 0),
                                             random.randint(width, width + 200)])
                self.rect.y = random.randint(-200, height + 200)
            else:
                self.rect.x = random.randint(-200, width + 200)
                self.rect.y = random.choice([random.randint(-200, 0),
                                             random.randint(height, height + 200)])
        elif self.tup == 1:
            self.rect.x = random.randint(-2000, 0)
            self.rect.y = random.randint(0, height)
        elif self.tup == 2:
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(height, height + 2000)
        elif self.tup == 3:
            self.rect.x = random.randint(width, width + 2000)
            self.rect.y = random.randint(0, height)
        elif self.tup == 4:
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(-2000, 0)
        elif self.tup == 5:
            qwe = random.randint(1, 4)
            self.tup = qwe
            if qwe == 1:
                self.rect.x = random.randint(-2000, 0)
                self.rect.y = random.randint(100, height - 100)
            elif qwe == 2:
                self.rect.x = random.randint(100, width - 100)
                self.rect.y = random.randint(height, height + 2000)
            elif qwe == 3:
                self.rect.x = random.randint(width, width + 2000)
                self.rect.y = random.randint(100, height - 100)
            elif qwe == 4:
                self.rect.x = random.randint(100, width - 100)
                self.rect.y = random.randint(-2000, 0)
        a = (self.rect.x - player_pos[0]) ** 2
        b = (self.rect.y - player_pos[0]) ** 2
        self.distance = (a + b) ** 0.5

    def update(self, player, activ_word):
        """
        ⠄⠄⠄⠄⠄⠄⠄⠄⣀⣤⡴⠶⠟⠛⠛⠛⠛⠻⠶⢦⣤⣀⠄⠄⠄⠄⠄⠄⠄⠄
        ⠄⠄⠄⠄⠄⣠⣴⡟⠋⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠙⢻⣦⣄⠄⠄⠄⠄⠄
        ⠄⠄⠄⣠⡾⠋⠈⣿⣶⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣠⣶⣿⠁⠙⢷⣄⠄⠄⠄
        ⠄⠄⣴⠏⠄⠄⠄⠸⣇⠉⠻⣦⣀⠄⠄⠄⠄⣀⣴⠟⠉⣸⠇⠄⠄⠄⠹⣦⠄⠄
        ⠄⣼⠏⠄⠄⠄⠄⠄⢻⡆⠄⠄⠙⠷⣦⣴⠾⠋⠄⠄⢰⡟⠄⠄⠄⠄⠄⠹⣧⠄
        ⢰⡏⠄⠄⠄⠄⠄⠄⠈⣷⠄⢀⣤⡾⠋⠙⢷⣤⡀⠄⣾⠁⠄⠄⠄⠄⠄⠄⢹⡆
        ⣿⠁⠄⠄⠄⠄⠄⠄⠄⣸⣷⠛⠁⠄⠄⠄⠄⠈⠛⣾⣇⠄⠄⠄⠄⠄⠄⠄⠄⣿
        ⣿⠄⠄⠄⠄⠄⣠⣴⠟⠉⢻⡄⠄ AYAYA ⠄⣾⡟⠉⠻⣦⣄⠄⠄⠄⠄⠄⣿
        ⣿⡀⠄⢀⣴⠞⠋⠄⠄⠄⠈⣷⠄⠄⠄⠄⠄⠄⣾⠁⠄⠄⠄⠙⠳⣦⡀⠄⠄⣿
        ⠸⣧⠾⠿⠷⠶⠶⠶⠶⠶⠶⢾⣷⠶⠶⠶⠶⣾⡷⠶⠶⠶⠶⠶⠶⠾⠿⠷⣼⠇
        ⠄⢻⣆⠄⠄⠄⠄⠄⠄⠄⠄⠄⢿⡄⠄⠄⢠⡿⠄⠄⠄⠄⠄⠄⠄⠄⠄⣰⡟⠄
        ⠄⠄⠻⣆⠄⠄⠄⠄⠄⠄⠄⠄⠘⣷⠄⠄⣾⠃⠄⠄⠄⠄⠄⠄⠄⠄⣰⠟⠄⠄
        ⠄⠄⠄⠙⢷⣄⠄⠄⠄⠄⠄⠄⠄⢹⣇⣸⡏⠄⠄⠄⠄⠄⠄⠄⣠⡾⠋⠄⠄⠄
        ⠄⠄⠄⠄⠄⠙⠳⣦⣄⡀⠄⠄⠄⠄⢿⡿⠄⠄⠄⠄⢀⣠⣴⠞⠋⠄⠄⠄⠄⠄
        ⠄⠄⠄⠄⠄⠄⠄⠄⠉⠛⠳⠶⣦⣤⣼⣧⣤⣴⠶⠞⠛⠉⠄⠄⠄⠄⠄⠄⠄⠄
        """
        player_pos = player.pos
        player_size = player.image.get_size()
        if abs(self.rect.x - player_pos[0]) > player_size[0] - 50 or \
                abs(self.rect.y - player_pos[1]) > player_size[0] - 50:
            if self.tup == 0:
                k_x = (abs(self.rect.x - player_pos[0]) /
                       ((abs(self.rect.x - player_pos[0]) + abs(self.rect.y - player_pos[1])) / 2))
                k_y = (abs(self.rect.y - player_pos[1]) /
                       ((abs(self.rect.x - player_pos[0]) + abs(self.rect.y - player_pos[1])) / 2))
                if self.rect.x > player_pos[0] and self.rect.y > player_pos[1]:
                    self.rect.x -= self.speed * k_x
                    self.rect.y -= self.speed * k_y
                elif self.rect.x > player_pos[0] and self.rect.y < player_pos[1]:
                    self.rect.x -= self.speed * k_x
                    self.rect.y += self.speed * k_y
                elif self.rect.x < player_pos[0] and self.rect.y > player_pos[1]:
                    self.rect.x += self.speed * k_x
                    self.rect.y -= self.speed * k_y
                else:
                    self.rect.x += self.speed * k_x
                    self.rect.y += self.speed * k_y
            elif self.tup == 1:
                self.rect.x += self.speed
            elif self.tup == 2:
                self.rect.y -= self.speed
            elif self.tup == 3:
                self.rect.x -= self.speed
            elif self.tup == 4:
                self.rect.y += self.speed
            elif self.tup == 6:
                self.rect.x = 200
                self.rect.y = 200
        else:
            print('hit')
            player.hp -= 1
            print(player.hp)
            self.kill()
        keys = pygame.key.get_pressed()

        if keys[pygame.key.key_code(self.name)]:
            self.kill()
            update_score_and_money(self.score)
        self.distance = ((self.rect.x - player_pos[0]) ** 2 + (self.rect.y - player_pos[0]) ** 2) ** 0.5


def generate(n, tup):
    new_enemy = pygame.sprite.Group()
    if tup == 0:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    elif tup == 1:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    elif tup == 2:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    elif tup == 3:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    elif tup == 4:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    elif tup == 5:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], random.randint(1, 5),
                  f"enemy/{let[i]}/tile000.png", 10, tup, new_enemy)
    return new_enemy
