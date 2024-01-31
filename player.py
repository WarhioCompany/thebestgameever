import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, skin, pos, group, screen_size, size_factor=1, restrict_vertical_movement=False):
        super().__init__(group)
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(f"data/images/{skin}.png").convert_alpha()
        self.image = self.original_image
        # Загружаем изображение игрока
        self.rect = self.image.get_rect(center=pos)
        self.z = 7
        self.direction = pygame.math.Vector2()
        # Определяем направление движения через задание вектора
        self.pos = pygame.math.Vector2(self.rect.center)

        # Устанавливаем скорость
        self.speed = 400

        # Увеличиваем размер спрайта
        self.size_factor = size_factor
        self.set_size()

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

        self.update_image()

    def update_image(self):
        if self.direction.x == -1:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction.x == 1:
            self.image = self.original_image
        else:
            return
        self.set_size()

    def move(self, t):
        # Перемещение игрока по полю
        new_pos = self.pos + self.direction * self.speed * t

        x = new_pos[0]
        y = new_pos[1]

        min_x = self.image.get_size()[0] / 4
        min_y = self.image.get_size()[1] / 4
        max_x = self.screen_size[0] - self.image.get_size()[0] / 1.5
        max_y = self.screen_size[1] - self.image.get_size()[1] / 1.5

        if not (min_x <= x <= max_x):
            return
        elif not (min_y <= y <= max_y):
            return

        self.pos = new_pos
        self.rect.center = self.pos

    def update(self, t):
        self.movement()
        self.move(t)

    def set_size(self):
        size = self.image.get_size()
        bigger_img = pygame.transform.scale(self.image,
                                            (int(size[0] * self.size_factor),
                                             int(size[1] * self.size_factor)))
        self.image = bigger_img
