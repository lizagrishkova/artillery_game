from ground import *
from tkinter import *
from math import *
from random import randrange as randint, choice
import time
from cannon import *
from enum import Enum

sleep_time = 50
screen_width = 800
screen_height = 600
shell_radius = 5
dt = 10  # физический шаг времени между кадрами обсчёта
g = -9.8
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'black', 'cyan', 'pink', 'magenta']


class GameState(Enum):
    TANK_IS_AIMING = 1
    SHELL_IS_FLYING = 2


def screen(x, y):
    return x, screen_height - y


class Start_game():
    def __init__(self, root):
        global canvas
        canvas = Canvas(root)
        canvas["width"] = screen_width
        canvas["height"] = screen_height
        canvas.pack()
        self.cannons = []
        Background(canvas)
        self.ground = Ground(canvas)
        self.ground.draw()

        x = randint(10, 385)
        y = self.ground.height[round(x)]
        self.gamer1 = Cannon(x, y, canvas)
        self.cannons.append(Cannon(x, y, canvas))

        x = randint(385, 770)
        y = self.ground.height[round(x)]
        self.gamer2 = Cannon(x, y, canvas)
        self.cannons.append(Cannon(x, y, canvas))

        self.current_player = 0
        self.shells = []

        canvas.bind("<Button-1>", self.mouse_click)
        canvas.bind("<Motion>", self.mouse_motion)
        # root.bind('<Key>', self.move)
        self.game_state = GameState.TANK_IS_AIMING

    def mouse_motion(self, event):
        if self.game_state != GameState.TANK_IS_AIMING:
            return
        cannon = self.cannons[self.current_player]
        cannon.target(event.x, screen_height - event.y)

    def mouse_click(self, event):
        if self.game_state != GameState.TANK_IS_AIMING:
            return
        cannon = self.cannons[self.current_player]
        x, y = screen(event.x, event.y)
        cannon.target(x, y)
        shell = cannon.shoot(x, y)
        self.shells.append(shell)

        self.game_state = GameState.SHELL_IS_FLYING
        canvas.after(sleep_time, self.shell_flying)

        self.current_player = (self.current_player + 1) % 2

    def shell_flying(self, *ignore):
        if self.game_state != GameState.SHELL_IS_FLYING:
            return
        canvas.after(sleep_time, self.shell_flying)

        for shell in self.shells:
            shell.move()

        for shell in self.shells:
            if self.ground.check_collision(shell):
                self.ground.explode(shell)
                self.game_state = GameState.TANK_IS_AIMING
        if self.game_state != GameState.SHELL_IS_FLYING:
            self.shells.clear()


root_window = Tk()
window = Start_game(root_window)
root_window.mainloop()
