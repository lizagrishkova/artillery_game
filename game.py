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
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'cyan', 'pink', 'magenta', 'SeaGreen1', 'violet red']


class GameState(Enum):
    TANK_IS_AIMING = 1
    SHELL_IS_FLYING = 2


def screen(x, y):
    """
        Перевод координат в экранные
    """
    return x, screen_height - y


class Start_game():

    def __init__(self, root, canvas):

        self.canvas = canvas
        self.canvas["width"] = screen_width
        self.canvas["height"] = screen_height
        self.canvas.pack()
        self.root = root
        self.cannons = []
        Background(self.canvas)
        self.ground = Ground(self.canvas)
        self.ground.draw()

        # Создание первой пушки
        x = randint(70, 350)
        y = self.ground.height[round(x)]
        self.gamer1 = Cannon(x, y + cannon_radius, self.canvas)
        self.cannons.append(self.gamer1)

        # Создание второй пушки
        x = randint(400, 700)
        y = self.ground.height[round(x)]
        self.gamer2 = Cannon(x, y + cannon_radius, self.canvas)
        self.cannons.append(self.gamer2)

        self.current_player = 0
        self.shells = []

        self.canvas.create_text(55, 25, text="Попадания:", font='Arial 15')
        self.canvas.create_text(115, 25, text=self.cannons[0].hit_points, font='Arial 15', tag='hit_points')
        self.canvas.create_text(55, 50, text="Промахи:", font='Arial 15')
        self.canvas.create_text(115, 50, text=self.cannons[0].miss_points, font='Arial 15', tag='miss_points')
        self.canvas.create_text(50, 75, text="Здоровье:", font='Arial 15')
        self.canvas.create_text(120, 75, text=self.cannons[0].health, font='Arial 15', tag='health')

        self.canvas.create_text(710, 25, text="Попадания:", font='Arial 15')
        self.canvas.create_text(770, 25, text=self.cannons[1].hit_points, font='Arial 15', tag='hit_points')
        self.canvas.create_text(710, 50, text="Промахи:", font='Arial 15')
        self.canvas.create_text(770, 50, text=self.cannons[1].miss_points, font='Arial 15', tag='miss_points')
        self.canvas.create_text(710, 75, text="Здоровье:", font='Arial 15')
        self.canvas.create_text(775, 75, text=self.cannons[1].health, font='Arial 15', tag='health')

        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<Motion>", self.mouse_motion)
        root.bind('<Key>', self.key_move)
        self.game_state = GameState.TANK_IS_AIMING

    def mouse_motion(self, event):
        """
            Обработка движения мышки
        """
        if self.game_state != GameState.TANK_IS_AIMING:
            return
        cannon = self.cannons[self.current_player]
        cannon.target(event.x, screen_height - event.y)

    def mouse_click(self, event):
        """
           Обработка клика мышки
        """
        if self.game_state != GameState.TANK_IS_AIMING:
            return
        cannon = self.cannons[self.current_player]
        x, y = screen(event.x, event.y)
        cannon.target(x, y)
        shell = cannon.shoot(x, y)
        self.shells.append(shell)

        self.game_state = GameState.SHELL_IS_FLYING
        self.canvas.after(sleep_time, self.shell_flying)

        self.current_player = (self.current_player + 1) % 2

    def key_move(self, event):
        """
            Движение пушки кнопками клавиатуры
        """
        cannon = self.cannons[self.current_player]
        if event.keycode == 39:
            cannon.y = self.ground.height[round(cannon.x) + 1] + cannon.r
            cannon.x += 1
            self.fall_on_ground(cannon)
        elif event.keycode == 37:
            cannon.y = self.ground.height[round(cannon.x) - 1] + cannon.r
            cannon.x -= 1
            self.fall_on_ground(cannon)

    def change_hit_points(self, cannon_number):
        """
           Обработка изменения количества попаданий
        """
        self.canvas.delete('hit_points')
        cannon = self.cannons[cannon_number]
        cannon.hit_points += 1
        self.canvas.create_text(770, 25, text=self.cannons[1].hit_points, font='Arial 15', tag='hit_points')
        self.canvas.create_text(115, 25, text=self.cannons[0].hit_points, font='Arial 15', tag='hit_points')

    def change_miss_points(self, cannon_number):
        """
            Обработка изменения количества промахов
        """
        self.canvas.delete('miss_points')
        cannon = self.cannons[cannon_number]
        cannon.miss_points += 1
        self.canvas.create_text(770, 50, text=self.cannons[1].miss_points, font='Arial 15', tag='miss_points')
        self.canvas.create_text(115, 50, text=self.cannons[0].miss_points, font='Arial 15', tag='miss_points')

    def change_health(self, cannon_number):
        """
            Обработка изменения здоровья
        """
        self.canvas.delete('health')
        cannon = self.cannons[cannon_number]
        cannon.health -= 7*randint(2, 4)
        self.canvas.create_text(770, 75, text=self.cannons[1].health, font='Arial 15', tag='health')
        self.canvas.create_text(115, 75, text=self.cannons[0].health, font='Arial 15', tag='health')

    def fall_on_ground(self, cannon):
        """
            Перемещение пушку на землю при ее взрыве
        """
        if abs(self.ground.height[cannon.x] - cannon.y) >= cannon.r:
            cannon.y = self.ground.height[cannon.x] + cannon.r
            self.canvas.delete(cannon.cannon)
            self.canvas.delete(cannon.cannon_body)
            cannon.redraw()

    def end_game(self, cannon, player):
        """
            Выводится экран завершения игры
        """
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, 800, 600, fill='Powder blue')
        self.canvas.delete('ground')
        self.canvas.create_text(400, 250, text="Игра окончена", font='Arial 15')
        self.canvas.create_text(400, 300, text="Победил игрок "+str(player + 1), font='Arial 15')
        self.canvas.create_text(400, 350,
                                text="Другой игрок убит за "+str(cannon.hit_points)+" попаданий и " +
                                     str(cannon.miss_points)+" промахов", font='Arial 15')

    def shell_flying(self, *ignore):
        """
            Регулируется полет снаряда; Обрабатыватся соударение с земле и попадание в пушку другого игрока
        """
        if self.game_state != GameState.SHELL_IS_FLYING:
            return
        self.canvas.after(sleep_time, self.shell_flying)

        for shell in self.shells:
            shell.move()

        active_cannon = (self.current_player + 1) % 2
        inactive_cannon = self.current_player
        cannon = self.cannons[self.current_player]
        for shell in self.shells:
            if self.ground.check_collision(shell):
                self.ground.explode(shell)
                self.change_miss_points(active_cannon)
                self.game_state = GameState.TANK_IS_AIMING
                self.fall_on_ground(self.cannons[active_cannon])
                self.fall_on_ground(self.cannons[inactive_cannon])
                break
            if cannon.hit_check(shell):
                self.change_hit_points(active_cannon)
                self.change_health(inactive_cannon)
                self.game_state = GameState.TANK_IS_AIMING
                shell.destroy()
                if cannon.health <= 0:
                    self.end_game(self.cannons[active_cannon], active_cannon)
                break
        if self.game_state != GameState.SHELL_IS_FLYING:
            self.shells.clear()


root_window = Tk()
canvas = Canvas(root_window)
window = Start_game(root_window, canvas)
root_window.mainloop()