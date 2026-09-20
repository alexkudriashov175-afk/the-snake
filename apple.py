"""Яблоко — игровой объект размером в одну клетку."""

from random import randint

import pygame

from game_object import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GameObject,
)


# Размер одной клетки игрового поля.
GRID_SIZE = 20


class Apple(GameObject):
    """Яблоко: хранит координаты клетки и умеет появляться случайно."""

    def __init__(self):
        """Создаёт яблоко красного цвета в случайной клетке."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Ставит яблоко в случайную клетку в пределах поля."""
        max_x = (SCREEN_WIDTH // GRID_SIZE) - 1
        max_y = (SCREEN_HEIGHT // GRID_SIZE) - 1
        self.position = (
            randint(0, max_x) * GRID_SIZE,
            randint(0, max_y) * GRID_SIZE,
        )

    def draw(self, surface):
        """Рисует яблоко квадратом размером в одну клетку."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(surface, self.body_color, rect)
