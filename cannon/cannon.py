import math
from tkinter import *
from random import *

screen_width = 800
screen_height = 600
shell_radius = 10
cannon_radius = 20
dt = 0.3  # физический шаг времени между кадрами обсчёта
g = -9.8
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'black', 'cyan', 'pink', 'magenta']


def screen(x, y):
    return x, screen_height - y


class Ball:
    def __init__(self, x, y, r, Vx, Vy, canvas):
        self.color = choice(colors)
        self.x, self.y, self.r = x, y, r
        self.Vx, self.Vy = Vx, Vy
        self._canvas = canvas
        self.circle = canvas.create_oval(screen(x - r, y - r), screen(x + r, (y + r)), fill=self.color)
        self.damage_radius = 30
        self.damage = 10

    def move(self):
        """
            Движение снаряда за один кадр перерисовки и отражение от стенок
        """
        ax = 0
        ay = g
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += (ax * dt)*0.99
        self.Vy += ay * dt

        # отражение
        if self.x - self.r <= 0:
            self.Vx = -self.Vx
            self.x = self.r + 1
        if self.x + self.r >= screen_width:
            self.Vx = -self.Vx
            self.x = screen_width - self.r - 1
        if self.y + self.r <= 0:
            self.Vy = -self.Vy
            self.y = self.r + 1

        x1, y1 = screen(self.x - self.r, self.y - self.r)
        x2, y2 = screen(self.x + self.r, self.y + self.r)
        self._canvas.coords(self.circle, x1, y1, x2, y2)

    def check_collision(self, x, y):
        length = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return length <= self.r

    def destroy(self):
        """
            Удаление снаряда
        """
        self._canvas.delete(self.circle)


class Cannon:
    max_cannon_length = 30

    def __init__(self, x, y, canvas):
        self._canvas = canvas
        self.x, self.y = x, y
        self.r = cannon_radius
        self.length_x = 0
        self.length_y = -20
        self.hit_points = 0
        self.miss_points = 0
        self.health = 100
        self.cannon = canvas.create_line(screen(self.x, self.y,),
                                         screen(self.x + self.length_x, self.y + self.length_y),
                                         width=7, fill='black', tag='cannon')
        self.cannon_body = canvas.create_oval(screen(self.x - self.r, self.y - self.r),
                                              screen(self.x + self.r, self.y + self.r), fill='black', tag='cannon')

    def target(self, x, y):
        """
            Изменение направления дула пушки на точку x, y
        """
        self.length_x = (x - self.x)
        self.length_y = (y - self.y)
        length = (self.length_x ** 2 + self.length_y ** 2) ** 0.5
        self.length_x = self.max_cannon_length * self.length_x / length
        self.length_y = self.max_cannon_length * self.length_y / length

        x1, y1 = screen(self.x, self.y)
        x2, y2 = screen(self.x + self.length_x, self.y + self.length_y)
        self._canvas.coords(self.cannon, x1, y1, x2, y2)

    def shoot(self, x, y):
        """
            Выстрел пушки; Создается снаряд
        """
        self.target(x, y)
        Vx = self.length_x*2.3
        Vy = self.length_y*2.3
        return Ball(self.x + self.length_x, self.y + self.length_y, shell_radius, Vx, Vy, self._canvas)

    def hit_check(self, shell):
        """
            Проверка попадания снаряда в пушку
        """
        return (shell.x - self.x)**2 + (shell.y - self.y)**2 <= (self.r + shell.r)**2

    def redraw(self):
        """
            Отрисовка пушки
        """
        self.cannon = self._canvas.create_line(screen(self.x, self.y, ),
                                               screen(self.x + self.length_x, self.y + self.length_y),
                                               width=7, fill='black', tag='cannon')
        self.cannon_body = self._canvas.create_oval(screen(self.x - self.r, self.y - self.r),
                                                    screen(self.x + self.r, self.y + self.r),
                                                    fill='black', tag='cannon')