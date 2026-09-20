"""Базовый игровой объект."""

# Размеры игрового поля.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class GameObject:
    """Общие атрибуты игровых объектов: позиция и цвет."""

    def __init__(self):
        """Задаёт позицию в центре экрана и цвет по умолчанию."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (255, 255, 255)

    def draw(self, surface):
        """Отрисовка объекта. Переопределяется в дочерних классах."""
        pass
