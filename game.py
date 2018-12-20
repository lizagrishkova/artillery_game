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
cannon_radius = 20
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

        x = randint(30, 350)
        y = self.ground.height[round(x)]
        self.gamer1 = Cannon(x, y + cannon_radius, canvas)
        self.cannons.append(Cannon(x, y + cannon_radius, canvas))

        x = randint(400, 770)
        y = self.ground.height[round(x)]
        self.gamer2 = Cannon(x, y + cannon_radius, canvas)
        self.cannons.append(Cannon(x, y + cannon_radius, canvas))

        self.current_player = 0
        self.shells = []

        canvas.create_text(55, 25, text="Попадания", font='Arial 15')
        canvas.create_text(115, 25, text=self.cannons[0].score, font='Arial 15', tag='text')
        canvas.create_text(55, 50, text="Здоровье", font='Arial 15')
        canvas.create_text(115, 50, text=self.cannons[0].health, font='Arial 15', tag='text')

        canvas.create_text(710, 25, text="Попадания", font='Arial 15')
        canvas.create_text(770, 25, text=self.cannons[0].score, font='Arial 15', tag='text')
        canvas.create_text(710, 50, text="Здоровье", font='Arial 15')
        canvas.create_text(770, 50, text=self.cannons[0].health, font='Arial 15', tag='text')

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

    def change_text(self, cannon_number):
        canvas.delete('text')
        cannon = self.cannons[cannon_number]
        inactive_cannon = self.cannons[(cannon_number + 1) % 2]
        cannon.score += 1
        inactive_cannon.health -= 15
        canvas.create_text(770, 25, text=self.cannons[1].score, font='Arial 15', tag='text')
        canvas.create_text(770, 50, text=self.cannons[1].health, font='Arial 15', tag='text')

        canvas.create_text(115, 25, text=self.cannons[0].score, font='Arial 15', tag='text')
        canvas.create_text(115, 50, text=self.cannons[0].health, font='Arial 15', tag='text')

    # def fall_on_ground(self, cannon_number, x, y):
        # if abs(self.ground.height[x] - y) >= self.cannons[cannon_number].r:
            # self.cannons[cannon_number].y = self.ground.height[x] + self.cannons[cannon_number].r
            # self.cannons[cannon_number].redraw(x, self.ground.height[x])

    def shell_flying(self, *ignore):
        if self.game_state != GameState.SHELL_IS_FLYING:
            return
        canvas.after(sleep_time, self.shell_flying)

        for shell in self.shells:
            shell.move()

        inactive_cannon = (self.current_player + 1) % 2
        cannon = self.cannons[self.current_player]
        for shell in self.shells:
            if self.ground.check_collision(shell):
                self.ground.explode(shell)
                self.game_state = GameState.TANK_IS_AIMING
                # self.fall_on_ground(self.current_player, cannon.x, cannon.y)
                break
            if cannon.hit_check(shell):
                self.change_text(inactive_cannon)
                self.game_state = GameState.TANK_IS_AIMING
                shell.destroy()
                if cannon.health <= 0:
                    canvas.delete('all')
                    canvas.create_rectangle(0, 0, 800, 600, fill='Powder blue')
                    canvas.delete('ground')
                    canvas.create_text(100, 25, text="Игра окончена", font='Arial 15')
                break
        if self.game_state != GameState.SHELL_IS_FLYING:
            self.shells.clear()


root_window = Tk()
window = Start_game(root_window)
root_window.mainloop()
