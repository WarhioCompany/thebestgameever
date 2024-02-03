from def_and_class import *
from player import Player
from store import Shop


class World:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.room_sprites = pygame.sprite.Group()
        self.setup()
        self.timer = 60

    def setup(self):
        self.player = Player("game_player",
                             (self.surface.get_size()[0] // 2, self.surface.get_size()[1] // 2),
                             self.all_sprites,
                             self.surface.get_size(),
                             5,
                             hp=3)
        self.player_in_room = Player("human/0",
                                     (self.surface.get_size()[0] // 2, self.surface.get_size()[1] // 2),
                                     self.room_sprites, self.surface.get_size(),
                                     8,
                                     True)
        self.shop = Shop((1270, 802.8))

    def create(self, t):
        self.surface.fill("black")
        self.all_sprites.draw(self.surface)
        self.all_sprites.update(t)
        self.update_timer()

    def update_timer(self):
        clock = pygame.time.Clock()
        self.timer -= clock.tick(60) / 1000
        font = pygame.font.SysFont(None, 100)
        text = font.render(str(int(self.timer)), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (300, 200)
        self.surface.blit(text, text_rect)




