from math import *
from tkinter import *
from random import *


screen_width = 800
screen_height = 600
shell_radius = 5
dt = 0.1  # физический шаг времени между кадрами обсчёта
g = -9.8
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'black', 'cyan', 'pink', 'magenta']

def screen(physical_x, physical_y):
    screen_x = physical_x
    screen_y = screen_height - physical_y
    return screen_x, screen_y


class Ball:
    def __init__(self, x, y, r, Vx, Vy, canvas):
        self.color = choice(colors)
        self.x, self.y, self.r = x, y, r
        self.Vx, self.Vy = Vx, Vy
        self.canvas = canvas
        self.avatar = self.canvas.create_oval(screen(x - r, y - r), screen(x + r, y + r), fill=self.color)

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

    def collision(self, ball):
        if abs(ball.x - self.x) <= (self.r + ball.r) and abs(ball.y - self.y) <= (self.r + ball.r):
            return True
        else:
            return False


class Cannon:
    max_cannon_length = 40

    def __init__(self, x, y, canvas):
        self.x, self.y = x, y
        self.power = 10
        self.on = 0
        self.angle = 1
        self.length_x = 0
        self.length_y = 20
        self.canvas = canvas
        self.gun = self.canvas.create_line(screen(self.x, self.y), screen(self.x + self.length_x,
                                                                           self.y + self.length_y), width=7)

    def begin_shoot(self, event):
        self.on = 1

    def end_shoot(self, event):
        global balls
        new_ball = Shell()
        new_ball.r += 3
        self.angle = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.dx = self.power * math.cos(self.angle)
        new_ball.dy = -self.power * math.sin(self.angle)
        balls.append(new_ball)
        self.on = 0
        self.power = 10
        
    def target(self, event=0):
        if event:
            self.angle = math.atan((event.y - screen(self.y)) / (event.x - screen(self.x)))
        if self.on:
            canv.itemconfig(self.cannon, fill='orange')
        else:
            canv.itemconfig(self.cannon, fill='black')
        canv.coords(self.cannon, screen(self.x), screen(self.y), screen(self.x) + max(self.power, screen(self.x)) * math.cos(self.angle),
                    screen(self.y) + max(self.power, self.x) * math.sin(self.angle))

    def power_up(self):
        if self.on:
            if self.power < 100:
                self.power += 1
            canv.itemconfig(self.cannon, fill='orange')
        else:
            canv.itemconfig(self.cannon, fill='black')
    
    def shoot(self, x, y):
        self.target(x, y)
        Vx = 1 * self.length_x
        Vy = 1 * self.length_y
        return Shell(self.x + self.length_x, self.y + self.length_y, shell_radius, Vx, Vy, self.canvas)
"""

def new_game(event=''):
    balls = []
    canv.bind('<Button-1>', gn.begin_shoot)
    canv.bind('<ButtonRelease-1>', gn.end_shoot)
    canv.bind('<Motion>', gn.target)

""" 
