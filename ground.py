from tkinter import *
import random
from math import *

screen_width = 800
screen_height = 600


def screen(x, y):
    return x, screen_height - y


class Background:
    def __init__(self, canvas):
        self._canvas = canvas
        self.draw()

    def draw(self):
        """
            Рисуем фон
        """
        self._canvas.create_rectangle(0, 0, screen_width, screen_height, fill='skyblue')

        # Drawing mountains
        self._canvas.create_polygon((0, 600), (0, 350), (175, 50), (550, 600), fill='slate gray')
        self._canvas.create_polygon((300, 600), (175, 50), (550, 600), fill='light slate gray')

        # Drawing hill
        self._canvas.create_oval(-100, 800, 600, 350,  fill='green4', outline='green4')

        # Drawing mountains
        self._canvas.create_polygon((350, 600), (520, 280), (550, 500), (500, 600), fill='light slate gray')
        self._canvas.create_polygon((550, 500), (520, 280), (600, 400), fill='slate gray')

        self._canvas.create_polygon((500, 600), (700, 150), (750, 600), fill='light slate gray')
        self._canvas.create_polygon((750, 600), (700, 150), (800, 300), (800, 600), fill='slate gray')

        # Drawing snow
        self._canvas.create_polygon((115, 150), (175, 50), (185, 100), fill='white smoke')
        self._canvas.create_polygon((272, 190), (175, 50), (185, 100), fill='snow')

        self._canvas.create_polygon((632, 300), (700, 150), (710, 260), fill='snow')
        self._canvas.create_polygon((710, 260), (700, 150), (780, 270), fill='white smoke')

        self._canvas.create_polygon((465, 380), (520, 280), (530, 350), fill='snow')
        self._canvas.create_polygon((530, 350), (520, 280), (587, 380), fill='white smoke')

        # Drawing sun
        self._canvas.create_oval(550, 70, 600, 20, fill='yellow', outline='yellow')

        # Drawing trees
        x = 100
        y = 370
        for _ in range(3):
            self._canvas.create_line(x, y, x, y + 40, fill='brown', width=10)
            x += 90
            y -= 5

        x = 50
        y = 300

        for _ in range(3):
            for _ in range(3):
                self._canvas.create_polygon((x, y), ((2*x + 100)/2, y - 60), (x + 100, y),
                                           fill='dark green', outline='dark green')
                y += 45
            x += 90
            y -= 150


class Ground:

    def __init__(self, canvas):
        self.height = list()
        self.min_height = screen_height - 500
        self.max_height = screen_height - 450
        self.dx = int(screen_width)
        self.canvas = canvas
        self.generate()

    """
        Генерируется список высот на момент запуска
    """
    def generate(self):
        height = random.randint(self.min_height, self.max_height)
        for i in range(800):
            self.height.append(height)
            dh = random.randint(-3, 3)
            height += dh

    """
         Функция отрисовывает землю по списку высот
    """
    def draw(self):
        self.delete()
        for i in range(800):
            self.canvas.create_line(i, screen_height, screen(i, self.height[i]), width=5, fill='lime green', tag='ground')
    """
         Функция проверяет столкновение снаяряда с землей
    """
    def check_collision(self, shell):
        return (shell.y - shell.r) <= self.height[round(shell.x)]

    """
         Функция уменьшает координаты столбиков земли в радиусе поражения снаряда
    """
    def explode(self, shell):
        damage = shell.r*2
        left_x = round(max(0, round(shell.x - damage)))
        right_x = round(min(screen_width, round(shell.x + damage)))
        for i in range(left_x, right_x):
            if i != round(shell.x):
                dx = abs(round(shell.x) - i)  # расстояние от точки удара до i столбика земли
                dy = ((abs(damage*damage - dx*dx))**0.5)
                self.height[i] = min(round(self.height[round(shell.x)] - dy), round(self.height[i]))
        self.height[round(shell.x)] -= damage
        self.draw()
        shell.destroy()

    def delete(self):
    """"
        Функция удаляет землю с экрана
    """
        self.canvas.delete('ground')
