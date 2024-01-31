import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, skin, pos, group, screen_size, size_factor=1, restrict_vertical_movement=False):
        super().__init__(group)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"data/images/{skin}.png").convert_alpha()
        # Загружаем изображение игрока
        self.rect = self.image.get_rect(center=pos)
        self.z = 7
        self.direction = pygame.math.Vector2()
        # Определяем направление движения через задание вектора
        self.pos = pygame.math.Vector2(self.rect.center)

        # Устанавливаем скорость
        self.speed = 400

        # Увеличиваем размер спрайта
        self.set_size(size_factor)

        self.restrict_vertical_movement = restrict_vertical_movement

        self.screen_size = screen_size

    def movement(self):
        keys = pygame.key.get_pressed()
        # Изменяем направление вектора движения игрока, в зависимости от нажатой клавиши

        # TODO: arrows
        if not self.restrict_vertical_movement:
            if keys[pygame.K_UP]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, t):
        # Перемещение игрока по полю
        new_pos = self.pos + self.direction * self.speed * t
        x = new_pos[0] #+ self.image.get_size()[0] / 1.5
        y = new_pos[1] #+ self.image.get_size()[1] / 1.5
        if not (self.image.get_size()[0] / 4 <= x <= self.screen_size[0] - self.image.get_size()[0] / 1.5):
            return
        elif not (self.image.get_size()[1] / 4 <= y <= self.screen_size[1] - self.image.get_size()[1] / 1.5):
            return

        self.pos = new_pos#+= self.direction * self.speed * t
        self.rect.center = self.pos

    def update(self, t):
        self.movement()
        self.move(t)

    def set_size(self, k):
        size = self.image.get_size()
        bigger_img = pygame.transform.scale(self.image, (int(size[0] * k), int(size[1] * k)))
        self.image = bigger_img
