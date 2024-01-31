import pygame
from config_file.config_game import *


class Shop:
    def __init__(self, pos):
        self.pos = pos
        self.font = ARIAL_24
        self.font_50 = ARIAL_50
        self.surface = pygame.display.get_surface()
        self.progressbar = pygame.Rect(340, 285, 37, 20)
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
        #if 460 <= ((player_pos[0] - self.pos[0]) ** 2 + (player_pos[1] - self.pos[0]) ** 2) ** 0.5 <= 505:
        if abs(self.pos[0] - 100 - player_pos[0]) < 250:
            return True
        else:
            return False

    def show_menu(self):
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(200, 200, 400, 200))
        text = self.font_50.render(f"Улучшения: ", True, (0, 0, 0))
        self.surface.blit(text, (230, 200))
        text = self.font.render(f"Здоровье: ", True, (0, 0, 0))
        self.surface.blit(text, (230, 280))
        self.progressbar.y = 285
        pygame.draw.rect(self.surface, (0, 255, 0), self.progressbar)
        text = self.font.render(f"Скорость: ", True, (0, 0, 0))
        self.surface.blit(text, (230, 340))
        self.progressbar.y = 345
        pygame.draw.rect(self.surface, (0, 255, 0), self.progressbar)
        pygame.display.flip()
