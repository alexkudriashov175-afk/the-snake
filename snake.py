"""Змейка — основной игровой объект."""

from random import choice

import pygame

from game_object import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GameObject,
)


# Размер одной клетки игрового поля.
GRID_SIZE = 20

# Цвет фона игрового поля.
BOARD_BACKGROUND_COLOR = (0, 0, 0)


class Snake(GameObject):
    """Змейка: сегменты тела, движение и отрисовка."""

    def __init__(self):
        """Инициализирует змейку из одного сегмента."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применяет отложенное направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Смещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % SCREEN_WIDTH,
            (head_y + dy) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(
            [
                (GRID_SIZE, 0),
                (-GRID_SIZE, 0),
                (0, GRID_SIZE),
                (0, -GRID_SIZE),
            ]
        )
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Рисует все сегменты змейки, стирая след хвоста."""
        if self.last:
            last_rect = pygame.Rect(
                self.last[0],
                self.last[1],
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(
                surface,
                BOARD_BACKGROUND_COLOR,
                last_rect,
            )

        for segment in self.positions:
            rect = pygame.Rect(
                segment[0],
                segment[1],
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(surface, self.body_color, rect)
