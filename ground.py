from tkinter import *
import random
import math

screen_width = 800
screen_height = 600
root = Tk()
frame = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)


class Background:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw()

    def draw(self):
        # Рисуем фон
        self.canvas.create_rectangle(0, 0, screen_width, screen_height, fill='skyblue')

        # Drawing mountains
        self.canvas.create_polygon((0, 600), (0, 350), (175, 50), (550, 600), fill='slate gray')
        self.canvas.create_polygon((300, 600), (175, 50), (550, 600), fill='light slate gray')

        # Drawing hill
        self.canvas.create_oval(-100, 800, 600, 350,  fill='forest green', outline='forest green')

        # Drawing mountains
        self.canvas.create_polygon((350, 600), (520, 280), (550, 500), (500, 600), fill='light slate gray')
        self.canvas.create_polygon((550, 500), (520, 280), (600, 400), fill='slate gray')

        self.canvas.create_polygon((500, 600), (700, 150), (750, 600), fill='light slate gray')
        self.canvas.create_polygon((750, 600), (700, 150), (800, 300), (800, 600), fill='slate gray')

        # Drawing snow
        self.canvas.create_polygon((115, 150), (175, 50), (185, 100), fill='white smoke')
        self.canvas.create_polygon((272, 190), (175, 50), (185, 100), fill='snow')

        self.canvas.create_polygon((632, 300), (700, 150), (710, 260), fill='snow')
        self.canvas.create_polygon((710, 260), (700, 150), (780, 270), fill='white smoke')

        self.canvas.create_polygon((465, 380), (520, 280), (530, 350), fill='snow')
        self.canvas.create_polygon((530, 350), (520, 280), (587, 380), fill='white smoke')

        # Drawing sun
        self.canvas.create_oval(550, 70, 600, 20, fill='yellow', outline='yellow')


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
            self.height.append(screen_height - height)
            dh = random.randint(-3, 3)
            height += dh

    """
        Функция отрисовывает землю по списку высот
    """
    def draw(self):
        # ыself.canvas.create_rectangle(0, 0, 800, 600, fill='white')
        self.canvas.delete('ground')
        for i in range(800):
            self.canvas.create_line(i, screen_height, i, self.height[i], width=5, fill='lime green', tag='ground')
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


a = Background(canv)
gr = Ground(canv)
gr.draw()

mainloop()
