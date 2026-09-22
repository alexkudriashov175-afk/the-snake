"""Игра «Змейка»."""

import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Начальная позиция объектов:
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Палитра цветоы:
COLORS = {
    'background': (0, 0, 0),
    'border': (93, 216, 228),
    'apple': (255, 0, 0),
    'snake': (0, 255, 0),
    'default': (255, 255, 255),
}

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый игровой объект."""

    def __init__(
        self,
        position=START_POSITION,
        body_color=COLORS['default'],
    ):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта. Переопределяется в дочерних классах."""
        raise NotImplementedError(
            f'Метод draw не переопределён в классе '
            f'{self.__class__.__name__}'
        )

    def draw_cell(self, position, border_color=COLORS['border']):
        """Рисует одну клетку с границей по указанной позиции."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Яблоко — игровой объект размером в одну клетку."""

    def __init__(
        self,
        occupied_cells=None,
        body_color=COLORS['apple'],
    ):
        """Создаёт яблоко в случайной свободной клетке."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """Ставит яблоко в случайную клетку, не занятую змейкой."""
        occupied_cells = occupied_cells or []
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_cells:
                return

    def draw(self):
        """Рисует яблоко квадратом размером в одну клетку."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка — основной игровой объект."""

    def __init__(self, body_color=COLORS['snake']):
        """Инициализирует змейку из одного сегмента."""
        super().__init__(body_color=body_color)
        self.reset()

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
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Рисует голову и хвост змейки, стирая след."""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, COLORS['background'], last_rect)

        self.draw_cell(self.positions[0])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и задаёт новое направление."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    screen.fill(COLORS['background'])

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Столкновение с собой или поедание яблока.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(COLORS['background'])
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()