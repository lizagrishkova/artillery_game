from tkinter import *
import random
import math


root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)

WIDTH = 800
HEIGHT = 600


class Shell:
    def __init__(self):
        self.x = 50
        self.y = 500
        self.r = 20


class Ground:

    def __init__(self):
        self.height = list()
        self.min_height = 400
        self.max_height = 500
        self.dx = int(WIDTH)
        self.generate()

    """
        Генерируется список высот на момент запуска
    """
    def generate(self):
        height = random.randint(self.min_height, self.max_height)
        for i in range(800):
            self.height.append(height)
            dh = random.randint(-2, 2)
            height += dh

    """
        Функция отрисовывает землю по списку высот
    """
    def draw(self):
        for i in range(800):
            canvas.create_line(i, HEIGHT, i+1, self.height[i], width=5, fill='red')
    """
        Функция проверяет столкновение снаяряда с землей
    """
    def check_collision(self, shell):
        return abs(shell.y - self.height[round(shell.x)]) <= shell.r

    """
        Функция уменьшает координаты столбиков земли в радиусе поражения снаряда
    """
    def explode(self, shell):
        damage = shell.r*2
        left_x = round(shell.x - damage)
        right_x = round(shell.x + damage)
        for i in range(left_x, right_x):
            dx = round(shell.x - i)  # расстояние от точки удара до i столбика земли
            dy = math.sqrt(damage * damage - dx * dx)
            self.height[i] = shell.x + dy
        self.draw()


gr = Ground()
gr.draw()
sh = Shell()
if gr.check_collision(sh):
    gr.explode()

mainloop()