import tkinter as tk
import tkinter.messagebox as msb
import sys
import os

class ShootingGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.geometry("133x190")
        self.master.title("Shooting Game - ver 1.2.0")

        # self.pack()

        self.create_canvas()
        self.bg = self.pic(Path=ShootingGame.resource_path("Assets\\images\\bg.png"), x=0, y=0, tag="bg")
        self.fighter = self.pic(Path=ShootingGame.resource_path("Assets\\images\\fighter.png"), x=0, y=150, tag="fighter")
        self.enemy = self.pic(Path=ShootingGame.resource_path("Assets\\images\\ennemy.png"), x=0, y=0, tag="enemy")
        self.beam = self.pic(Path=ShootingGame.resource_path("Assets\\images\\beam.png"), x=0, y=-50, tag="beam")
        self.fighter_x = 0
        self.master.bind("<Key>", self.KeyEv)

        self.difference_x = 0
        self.difference_y = 0
        self.fighter_x = 0
        self.beam_x = 0
        self.beam_y = 0
        self.beam_tmp = 0
        self.canmove = True
        self.first = 0

        self.enemy_can_touch_area = [0, 0, 0, 0]

        self.status = 0
        self.enemy_x = 0
        self.enemy_y = 0

        self.move_enemy()

    @staticmethod
    def resource_path(relative_path):
        """PyInstallerの_onefile対応"""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        
        return os.path.join(os.path.abspath("."), relative_path)

    def create_canvas(self):
        self.frame_img = tk.Frame(self.master, width=133, height=190, bg="White")
        self.frame_img.place(x=0, y=0)

        self.canvas = tk.Canvas(self.frame_img, width=133, height=190, bg="White")
        self.canvas.place(x=0, y=0)

    def pic(self, Path, x, y, tag):
        img = tk.PhotoImage(file=Path)
        self.canvas.create_image(x, y, image=img, tag=tag)
        return img

    def KeyEv(self, event):
        if event.char == "c":
            self.move_fighter(Direction_of_movement="Right")

        elif event.char == "z":
            self.move_fighter(Direction_of_movement="Left")

        elif event.char == "x":
            self.create_beam()

    def move_fighter(self, Direction_of_movement):
        if Direction_of_movement == "Left":
            self.fighter_x -= 2
            self.canvas.move("fighter", -2, 0)

        elif Direction_of_movement == "Right":
            self.fighter_x += 2
            self.canvas.move("fighter", 2, 0)

    def create_beam(self):
        self.beam_tmp = self.canvas.bbox("beam")

        self.beam_x = self.beam_tmp[0] + 4
        self.beam_y = self.beam_tmp[1] + 16

        self.difference_x = self.fighter_x - self.beam_x
        self.difference_y = 150 - self.beam_y

        self.canvas.move("beam", self.difference_x, self.difference_y - 30)

        self.first += 1

        if self.first == 1:
            self.move_beam()

        if self.beam_x >= 0:
            self.canmove = False

        elif self.beam_x <= 0:
            self.canmove = True
            self.first = 0

        if self.canmove == True:
            self.move_beam()

    def move_beam(self):
        self.canvas.move("beam", 0, -2)

        self.enemy_can_touch_area = self.canvas.bbox("enemy")
        self.beam_tmp = self.canvas.bbox("beam")
        self.beam_x = self.beam_tmp[0] + 4
        self.beam_y = self.beam_tmp[1] + 16

        if (
            self.enemy_can_touch_area[0] <= self.beam_x
            and self.enemy_can_touch_area[2] >= self.beam_x
        ):
            if (
                self.enemy_can_touch_area[1] <= self.beam_y
                and self.enemy_can_touch_area[3] >= self.beam_y
            ):
                msb.showinfo("", "敵を撃退クリア")
                self.canvas.delete("enemy")

        self.canvas.after(30, self.move_beam)

    def move_enemy(self):
        if self.status == 0:
            self.enemy_x += 2
            self.canvas.move("enemy", 2, 0)

            if self.enemy_x >= 100:
                self.status = 1
                self.canvas.move("enemy", 0, 10)

                self.enemy_y += 10
                pass

        elif self.status == 1:
            self.enemy_x -= 2
            self.canvas.move("enemy", -2, 0)

            if self.enemy_x <= 0:
                self.status = 0
                self.canvas.move("enemy", 0, 10)

                self.enemy_y += 10
                pass

        self.fighter_can_touch_area = self.canvas.bbox("fighter")

        if (
            self.fighter_can_touch_area[0] <= self.enemy_x
            and self.fighter_can_touch_area[2] >= self.enemy_x
        ):
            if (
                self.fighter_can_touch_area[1] <= self.enemy_y
                and self.fighter_can_touch_area[3] >= self.enemy_y
            ):
                msb.showinfo("", "ゲームオーバー")

                self.canvas.delete("fighter")
                self.canvas.delete("beam")

        self.canvas.after(30, self.move_enemy)


def main():
    root = tk.Tk()
    app = ShootingGame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
