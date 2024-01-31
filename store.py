import pygame
import sqlite3
from config_file.config_game import *


class Shop:
    def __init__(self, pos):
        self.pos = pos
        self.font = ARIAL_24
        self.font_50 = ARIAL_50
        self.con = sqlite3.connect('data/game.sqlite3')
        self.cur = self.con.cursor()
        self.surface = pygame.display.get_surface()
        self.progressbar = pygame.Rect(390, 285, 37, 20)
        self.open_flag = False
        self.clock = pygame.time.Clock()

    def handle_collide(self, player_pos):
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_e]:
        #     if self.check_distance(player_pos):
        #         self.open_flag = True
        # if keys[pygame.K_q]:
        #     if self.check_distance(player_pos):
        #         self.open_flag = False

        self.open_flag = self.check_distance(player_pos)
        if self.open_flag:
            self.show_menu()

    def check_distance(self, player_pos):
        # if 460 <= ((player_pos[0] - self.pos[0]) ** 2 + (player_pos[1] - self.pos[0]) ** 2) ** 0.5 <= 505:
        if abs(self.pos[0] - 100 - player_pos[0]) < 250:
            return True
        else:
            return False

    def show_menu(self):
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(200, 200, 400, 200))
        speed, hp = self.get_upgrade_level()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if hp + 1 <= 5:
                        hp += 1
                        self.cur.execute(f"UPDATE player_stats SET hp_level={hp}")
                if event.key == pygame.K_2:
                    if speed + 1 <= 5:
                        speed += 1
                        self.cur.execute(f"UPDATE player_stats SET speed_level={speed}")
        text = self.font_50.render(f"Улучшения: ", True, (0, 0, 0))
        self.surface.blit(text, (230, 200))
        text = self.font.render(f"[1] Здоровье: {hp}/ 5 ", True, (0, 0, 0))
        self.surface.blit(text, (230, 280))
        self.progressbar.y = 285
        self.progressbar.width = 37 * hp
        pygame.draw.rect(self.surface, (0, 255, 0), self.progressbar)
        text = self.font.render(f"[2] Скорость: {speed}/5 ", True, (0, 0, 0))
        self.surface.blit(text, (230, 340))
        self.progressbar.y = 345
        self.progressbar.width = 37 * speed
        pygame.draw.rect(self.surface, (0, 255, 0), self.progressbar)
        pygame.display.flip()

    def get_upgrade_level(self):
        levels = self.cur.execute('SELECT speed_level, hp_level FROM player_stats').fetchone()
        return levels
