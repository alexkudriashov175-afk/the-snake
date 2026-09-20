"""Основной игровой цикл."""

import pygame

from apple import GRID_SIZE, Apple
from game_object import SCREEN_HEIGHT, SCREEN_WIDTH
from snake import BOARD_BACKGROUND_COLOR, Snake


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и задаёт новое направление."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction != (0, GRID_SIZE):
                    snake.next_direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN:
                if snake.direction != (0, -GRID_SIZE):
                    snake.next_direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT:
                if snake.direction != (GRID_SIZE, 0):
                    snake.next_direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                if snake.direction != (-GRID_SIZE, 0):
                    snake.next_direction = (GRID_SIZE, 0)


def check_apple_collision(snake, apple):
    """Растит змейку, если она съела яблоко."""
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()


def check_self_collision(snake):
    """Проверяет столкновение змейки с собой."""
    head = snake.get_head_position()
    if head in snake.positions[1:]:
        snake.reset()
        return True
    return False


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
    )
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(20)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        check_apple_collision(snake, apple)

        if check_self_collision(snake):
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
