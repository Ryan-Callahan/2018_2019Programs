"""
    Minesweeper_menu version 2.2.5 allows users to play a game of minesweeper
    in either easy, medium, or hard difficulty.
    Copyright (C) 2018  Ryan I Callahan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from tkinter import *
import random

root = Tk()
class Minesweeper:

    def __init__ (self, root):
        root.title("Minesweeper")
        self.button_dict = dict()

        self.label = Label(text="MINESWEEPER\n-------------\nInstructions: \nLeft click to reveal square\nRight click to flag/unflag\nFlag all mines to win\nNumbers = amount of mines touching square\n-------------\nChoose A Difficulty\n-------------")
        self.label.grid(columnspan=4, column=1, row=1, sticky='w')
        self.easystart = Button(text="Easy", command=self.easy)
        self.easystart.grid(column=1, row=2)
        self.mediumstart = Button(text="Medium", command=self.medium)
        self.mediumstart.grid(column=2, row=2)
        self.hardstart = Button(text="Hard", command=self.hard)
        self.hardstart.grid(column=3, row=2)
        self.customstart = Button(text="Custom", command=self.custom)
        self.customstart.grid(column=4, row=2)

        self.mine = 1
        self.size = 5
        self.mlist = []
        self.mines = []

    def easy(self):
        self.mine = 20
        self.size = 12
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.customstart.destroy()
        self.create()

    def medium(self):
        self.mine = 45
        self.size = 17
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.customstart.destroy()
        self.create()

    def hard(self):
        self.mine = 80
        self.size = 22
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.customstart.destroy()
        self.create()

    def custom(self):
        m=15
        s=10
        mc = []
        sc = []
        for x in range(0, 38):
            mc.append(m)
            m+=5
        for x in range(0, 11):
            sc.append(s)
            s+=2

        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.customstart.destroy()
        self.label.config(text="MINESWEEPER\n"
                                "-------------\n"
                                "Input Preference\n"
                                "-------------")
        self.mlabel = Label(text="Number of Mines: ")
        self.mlabel.grid(column=1, row=2)
        self.spinmines = Spinbox(values=mc, state='readonly')
        self.spinmines.grid(column=2, row=2)
        self.mslabel = Label(text="Size of Grid: ")
        self.mslabel.grid(column=1, row=3)
        self.spinsize = Spinbox(values=sc, state='readonly')
        self.spinsize.grid(column=2, row=3)
        self.begin = Button(text="Begin", command=self.custombegin)
        self.begin.grid(column=1, row=4)

    def custombegin(self):
        self.mine = int(self.spinmines.get())
        self.size = int(self.spinsize.get())
        #self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.customstart.destroy()
        self.mlabel.destroy()
        self.mslabel.destroy()
        self.spinmines.destroy()
        self.spinsize.destroy()
        self.begin.destroy()


        if (float((self.size**2))/float(self.mine)) > (8.0):
            self.custom()
            self.label.config(text="MINESWEEPER\n"
                                "-------------\n"
                                "Please add more mines, or make the size smaller.\n"
                                "Input Preference\n"
                                "-------------\n")
        elif (float((self.size**2)) <= float(self.mine)):
            self.custom()
            self.label.config(text="MINESWEEPER\n"
                                "-------------\n"
                                "Please use less mines, or make the size bigger.\n"
                                "Input Preference\n"
                                "-------------\n")

        elif (float((self.size ** 2)) / float(self.mine)) <= (8.0):
            self.label.destroy()
            self.create()


    def create(self):
        self.minecount = self.mine
        self.flagcount = self.mine
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.mlist.append([x, y])

        for x in range(0, self.size):
            for y in range(0, self.size):
                self.button_dict[f"{x}, {y}"] = Button(text="", height=1, width=2, background="gray95")
                self.button_dict[f"{x}, {y}"].bind("<ButtonPress-1>", self.minesweeperclick)
                self.button_dict[f"{x}, {y}"].bind("<ButtonRelease-3>", self.flag)
                self.button_dict[f"{x}, {y}"].grid(column=x, row=y)

        for x in range(0, self.mine):
            self.minegenerate()

        self.buttonlabel=Label(text=("Flags Remaining: %s" % self.flagcount))
        self.buttonlabel.grid(columnspan=10, column=1, row=999, sticky="ew")

    def minegenerate(self):
        x, y = random.choice(self.mlist)
        self.mines.append(self.button_dict[f"{x}, {y}"])
        self.button_dict[f"{x}, {y}"].unbind("<ButtonPress-1>")
        self.button_dict[f"{x}, {y}"].bind("<ButtonPress-1>", self.boom)
        self.mlist.remove([x, y])
        #self.button_dict[f"{x}, {y}"].config(text="m")

    def boom(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                button.config(text="*", relief="sunken")
                for x in range(0, self.size):
                    for y in range(0, self.size):
                        self.button_dict[f"{x}, {y}"].unbind("<ButtonPress-1>")
                        self.button_dict[f"{x}, {y}"].unbind("<ButtonRelease-3>")
                        self.button_dict[f"{x}, {y}"].config(state="disabled")
                root.update()
                self.losescreen()
                break

    def losescreen(self):
        lose = Toplevel()
        lose.geometry('50x60')
        lose.title("Minesweeper")
        msg = Message(lose, text="You Lose.")
        msg.pack()
        closebutton = Button(lose, text="Close", command=self.close)
        closebutton.pack()

    def flag(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                if button.cget("relief") == "raised":
                    if self.flagcount > 0:
                        button.config(relief="ridge", state="disabled", text="F", background="red")
                        self.flagcount -= 1
                        self.buttonlabel.config(text=("Flags Remaining: %s" % self.flagcount))
                    if button in self.mines:
                        self.minecount -= 1
                        if self.minecount == 0:
                            self.winscreen()
                            break
                    button.unbind("<ButtonPress-1>")
                    button.unbind("<ButtonRelease-3>")
                    button.bind("<ButtonRelease-3>", self.unflag)

    def winscreen(self):
        win = Toplevel()
        win.geometry('50x65')
        win.title("Minesweeper")
        msg = Message(win, text="You Win!")
        msg.pack()
        closebutton = Button(win, text="Close", command = self.close)
        closebutton.pack()

    def close(self):
        root.destroy()


    def unflag(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                self.flagcount += 1
                self.buttonlabel.config(text=("Flags Remaining: %s" % self.flagcount))
                button.config(relief="raised", state="disabled", text="", background='gray95')
                button.unbind("<ButtonRelease-3>")
                if button in self.mines:
                    button.bind("<ButtonPress-1>", self.boom)
                else:
                    button.bind("<ButtonPress-1>", self.minesweeperclick)
                button.bind("<ButtonRelease-3>", self.flag)



    def minesweeperclick(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                button.config(state="disabled", relief="sunken")
                button.unbind("<ButtonRelease-3>")
                self.numbertest(button)

    def numbertest(self, button):
        adjacentmines = 0
        for list in self.button_dict.items():
            if button in list:
                x, y = list[0].split(", ")
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {y}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {y}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                if adjacentmines == 0:
                    button.config(relief="sunken", text="", state="disabled", background='gray87')
                    self.blankspacecalculate(button)
                else:
                    button.config(relief="sunken", text=adjacentmines, state="disabled", background='gray87')

    def blankspacecalculate(self, button):
        for list in self.button_dict.items():
            if button in list:
                x, y = list[0].split(", ")
                try:
                    if self.button_dict[f"{int(x)-1}, {int(y)+1}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {int(y)+1}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{int(x)-1}, {y}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {y}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{int(x)-1}, {int(y)-1}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {int(y)-1}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)+1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{x}, {str(int(y)+1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)-1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{x}, {str(int(y)-1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {y}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {y}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"])
                except KeyError:
                    pass

Minesweeper(root)
root.mainloop()
