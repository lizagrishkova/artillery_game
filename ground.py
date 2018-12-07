from tkinter import *
import random
import math

screen_width = 800
screen_height = 600


class Ground:

    def __init__(self, canvas):
        self.height = list()
        self.min_height = screen_height - 500
        self.max_height = screen_height - 400
        self.dx = int(screen_width)
        self.canvas = canvas
        self.generate()

    """
        Генерируется список высот на момент запуска
    """
    def generate(self):
        height = random.randint(self.min_height, self.max_height)
        for i in range(800):
            self.height.append(screen_height - height)
            dh = random.randint(-3, 3)
            height += dh

    """
        Функция отрисовывает землю по списку высот
    """
    def draw(self):
        self.canvas.create_rectangle(0, 0, 800, 600, fill='white')
        for i in range(800):
            self.canvas.create_line(i, screen_height, i, self.height[i], width=5, fill='green')
    """
        Функция проверяет столкновение снаяряда с землей
    """
    def check_collision(self, shell):
        return (screen_height - (shell.y - shell.r)) <= self.height[round(shell.x)]

    """
        Функция уменьшает координаты столбиков земли в радиусе поражения снаряда
    """
    def explode(self, shell):
        damage = shell.r*1.5
        left_x = round(max(0, round(shell.x - damage)))
        right_x = round(min(screen_width, round(shell.x + damage)))
        for i in range(left_x, right_x):
            if i != round(shell.x):
                dx = abs(shell.x - i)  # расстояние от точки удара до i столбика земли
                dy = (damage**2 - dx**2)**0.5
                self.height[i] = round(self.height[round(shell.x)] + dy)
        self.height[round(shell.x)] += damage
        self.draw()
