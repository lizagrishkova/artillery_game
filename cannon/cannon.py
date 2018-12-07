from math import *
from tkinter import *
from random import *


screen_width = 800
screen_height = 600
shell_radius = 5
dt = 0.1  # физический шаг времени между кадрами обсчёта
g = -9.8

def screen(physical_x, physical_y):
    screen_x = physical_x
    screen_y = screen_height - physical_y
    return screen_x, screen_y


class Shell:
    def __init__(self, x, y, r, Vx, Vy, canvas):
        color = random.choice(['blue', 'green', 'red', 'cyan', 'pink', 'magenta', 'yellow'])
        self.x, self.y, self.r = x, y, r
        self.Vx, self.Vy = Vx, Vy
        self.canvas = canvas
        self.avatar = self.canvas.create_oval(screen(x - r, y - r),
                                         screen(x + r, y + r), fill=color)

    """ Метод move описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения 
           self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
               и стен по краям окна (размер окна 800х600).
    """
    def move(self):
        ax = 0
        ay = g
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt
        if self.x - self.r <= 0:
            self.Vx = -self.Vx
            self.x = self.r + 1
        if self.x + self.r >= screen_width:
            self.Vx = -self.Vx
            self.x = screen_width - self.r - 1

        x1, y1 = screen(self.x - self.r, self.y - self.r)
        x2, y2 = screen(self.x + self.r, self.y + self.r)
        self.canvas.coords(self.avatar, x1, y1, x2, y2)


class Cannon:
    max_cannon_length = 40

    def __init__(self, x, y, canvas):
        self.x, self.y = x, y
        self.length_x = 0
        self.length_y = 20
        self.canvas = canvas
        self.line = self.canvas.create_line(screen(self.x, self.y),
                                       screen(self.x + self.length_x, self.y + self.length_y),
                                       width=5, fill='red')

    def target(self, x, y):
        self.length_x = (x - self.x)
        self.length_y = (y - self.y)
        l = (self.length_x ** 2 + self.length_y ** 2) ** 0.5
        self.length_x = self.max_cannon_length * self.length_x / l
        self.length_y = self.max_cannon_length * self.length_y / l

        x1, y1 = screen(self.x, self.y)
        x2, y2 = screen(self.x + self.length_x, self.y + self.length_y)
        self.canvas.coords(self.line, x1, y1, x2, y2)

    def shoot(self, x, y):
        self.target(x, y)
        Vx = 1 * self.length_x
        Vy = 1 * self.length_y
        return Shell(self.x + self.length_x, self.y + self.length_y, shell_radius, Vx, Vy, self.canvas)
