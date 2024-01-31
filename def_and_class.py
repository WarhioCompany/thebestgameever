import game
from config_file.config_game import *

from pynput.keyboard import Listener
import pygame
import os
import sys
import random
import sqlite3

con = sqlite3.connect('data/game.sqlite3')
cur = con.cursor()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
sprite = pygame.sprite.Sprite()
pygame.init()
screen.fill(pygame.Color("white"))
font = pygame.font.Font(None, 20)


def str_key(key):
    return str(key)[1]


def change_score(delta_score):
    score = list(cur.execute('SELECT * FROM player_stats').fetchone())
    score[0] += delta_score
    cur.execute("""Delete from player_stats""")
    cur.execute("""Insert into player_stats (
                                                score, 
                                                money, 
                                                night, 
                                                speed_level, 
                                                hp_level) 
                    values (?, ?, ?, ?, ?)""", score)


def change_money(delta_money):
    money = list(cur.execute('SELECT * FROM player_stats').fetchone())
    money[1] += delta_money
    cur.execute('Delete from player_stats')
    cur.execute("""Insert into player_stats (
                                                score, 
                                                money, 
                                                night, 
                                                speed_level, 
                                                hp_level) 
                    values (?, ?, ?, ?, ?)""", money)


class Keyboard:
    current_word = ()
    completed_length = 0
    active_words = []

    def __init__(self):
        self.reset_word()
        self.start_listener()

    def start_listener(self):
        listener = Listener(on_press=self.on_press)
        listener.start()

    def choose_active_word(self, key):
        for pair in self.active_words:
            word = pair[0]
            if word[0] == str_key(key):
                self.current_word = pair
                self.completed_length = 0
                print(f'{word} was chosen')
                return word

    def on_press(self, key):
        word = self.current_word[0]
        if not word:
            word = self.choose_active_word(key)
            if not word:
                return

        if str_key(key) == word[self.completed_length]:
            self.completed_length += 1
            print(f"{word[:self.completed_length]}")
            if self.completed_length == len(word):
                print("complete")
                self.current_word[-1](word)
                self.reset_word()

    def reset_word(self):
        if self.current_word:
            self.active_words.remove(self.current_word)
        self.current_word = ('', 0, None)
        self.completed_length = 0

    def set_active_words(self, words_and_distance):
        # (word, distance_from_player_to_enemy, event)
        self.active_words = sorted(words_and_distance, key=lambda a: a[1])


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
                 money,
                 tup,
                 *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(image_name), (76, 84))
        self.speed = speed
        self.name = name
        self.score = score
        self.money = money
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
                self.rect.y = random.randint(0, height)
            elif qwe == 2:
                self.rect.x = random.randint(0, width)
                self.rect.y = random.randint(height, height + 2000)
            elif qwe == 3:
                self.rect.x = random.randint(width, width + 2000)
                self.rect.y = random.randint(0, height)
            elif qwe == 4:
                self.rect.x = random.randint(0, width)
                self.rect.y = random.randint(-2000, 0)
        a = (self.rect.x - player_pos[0]) ** 2
        b = (self.rect.y - player_pos[0]) ** 2
        self.distance = (a + b) ** 0.5

    def update(self, player_pos, activ_word):
        if self.tup == 0:
            if abs(self.rect.x - player_pos[0]) > 50 or abs(self.rect.y - player_pos[1]) > 50:
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
                self.distance = ((self.rect.x - player_pos[0]) ** 2 + (self.rect.y - player_pos[0]) ** 2) ** 0.5
        elif self.tup == 1:
            self.rect.x += self.speed
        elif self.tup == 2:
            self.rect.y -= self.speed
        elif self.tup == 3:
            self.rect.x -= self.speed
        elif self.tup == 4:
            self.rect.y += self.speed
        if activ_word == self.name:
            print(self.name + "qwerty")
            self.kill()
            print(-1)
            change_score(self.score)
            change_money(self.money)
        a = (self.rect.x - player_pos[0]) ** 2
        b = (self.rect.y - player_pos[0]) ** 2
        self.distance = (a + b) ** 0.5
        if self.rect[0] == 0:
            print(self.tup)


def generate(n, tup):
    new_enemy = pygame.sprite.Group()
    if tup == 0:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 1,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    elif tup == 1:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 3,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    elif tup == 2:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 3,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    elif tup == 3:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 3,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    elif tup == 4:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 3,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    elif tup == 5:
        let = random.choices(letters, k=n)
        for i in range(n):
            Enemy((960, 540), let[i], 3,
                  f"enemy/{let[i]}/tile000.png", 30, 15, tup, new_enemy)
    return new_enemy
