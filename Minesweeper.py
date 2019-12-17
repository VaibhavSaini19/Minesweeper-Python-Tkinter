import random

from tkinter import *


class NButton(Button):
    def __init__(self, master, name=None, *args, **kwargs):
        Button.__init__(self, master, *args, **kwargs)
        self.master, self.name = master, name


master = Tk()
master.title("Main window")
master.geometry("500x450")
master.resizable(0, 0)


class cell:
    def __init__(self, pos, btn, state=None):
        self.pos = pos                          # coordinates in terms of x, y
        self.is_bomb = False
        self.nearby = 0                      # number of bombs in adjacent 8 cells
        self.revealed = False
        self.stampId = None
        self.btn = btn


class myGrid:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.locations = [[0 for x in range(
            self.gridSize)] for y in range(self.gridSize)]
        self.total_bombs = self.gridSize**2 // 8

    def setup(self):
        self.draw()
        self.set_bombs()

    def draw(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                btn = NButton(master, name=str(i)+"," +
                              str(j), text=None, bg="white", height=2, width=5)
                btn.bind('<Button-1>', get)
                btn.bind('<Button-3>', mark)
                btn.grid(row=i, column=j)
                self.locations[i][j] = cell((i, j), btn)

    def set_bombs(self):
        i = 0
        while i < self.total_bombs:
            bomb_x = random.randint(0, self.gridSize-1)
            bomb_y = random.randint(0, self.gridSize-1)
            if not self.locations[bomb_x][bomb_y].is_bomb:
                self.locations[bomb_x][bomb_y].is_bomb = True
                if bomb_x-1 >= 0 and bomb_y-1 >= 0:
                    self.locations[bomb_x-1][bomb_y-1].nearby += 1
                if bomb_y-1 >= 0:
                    self.locations[bomb_x][bomb_y-1].nearby += 1
                if bomb_x+1 <= self.gridSize-1 and bomb_y-1 >= 0:
                    self.locations[bomb_x+1][bomb_y-1].nearby += 1
                if bomb_x-1 >= 0:
                    self.locations[bomb_x-1][bomb_y].nearby += 1
                if bomb_x+1 <= self.gridSize-1:
                    self.locations[bomb_x+1][bomb_y].nearby += 1
                if bomb_x-1 >= 0 and bomb_y+1 <= self.gridSize-1:
                    self.locations[bomb_x-1][bomb_y+1].nearby += 1
                if bomb_y+1 <= self.gridSize-1:
                    self.locations[bomb_x][bomb_y+1].nearby += 1
                if bomb_x+1 <= self.gridSize-1 and bomb_y+1 <= self.gridSize-1:
                    self.locations[bomb_x+1][bomb_y+1].nearby += 1

                i += 1
        # printing bombs:
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].is_bomb:
                    print("b", end=" ")
                else:
                    print(self.locations[i][j].nearby, end=" ")
            print()

    def explore(self, cell_x, cell_y):
        l = [(0, 0), (-1, -1), (0, -1), (1, -1),
             (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        exp_x = cell_x
        exp_y = cell_y
        exp_cell = self.locations[exp_x][exp_y]
        if not exp_cell.revealed:
            exp_cell.revealed = True
            if exp_cell.nearby == 0:
                exp_cell.btn.config(bg="grey")
                for pair in l:
                    if 0 <= (cell_x + pair[0]) <= self.gridSize-1 and 0 <= (cell_y + pair[1]) <= self.gridSize-1:
                        exp_x = cell_x + pair[0]
                        exp_y = cell_y + pair[1]
                        exp_cell = self.locations[exp_x][exp_y]
                        self.explore(exp_x, exp_y)
            else:
                exp_cell.btn.config(text=exp_cell.nearby)
        self.won()

    def end_game(self):
        global finished
        finished = True
        print("BOMB encountered!!!")
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].is_bomb:
                    self.locations[i][j].btn.config(text='BOMB', bg="red")

    def won(self):
        count = False
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].revealed == False:
                    count += 1
        if count == self.total_bombs:
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if self.locations[i][j].is_bomb:
                        self.locations[i][j].btn.config(bg="green")
            print("You won!!!")


def get(event):
    global finished
    if finished:
        master.quit()
    #print("x, y: ", x, y)
    num = [x for x in str(event.widget.name) if x.isdigit()]
    x = int(''.join(num[:len(num)//2]))
    y = int(''.join(num[len(num)//2:]))

    cell_x = None
    cell_y = None
    for i in range(g.gridSize):
        for j in range(g.gridSize):
            if (cell_x is None) and g.locations[i][j].pos[0] <= x <= g.locations[i][j].pos[0]:
                cell_x = i
            if (cell_y is None) and g.locations[i][j].pos[1] <= y <= g.locations[i][j].pos[1]:
                cell_y = j
    if g.locations[cell_x][cell_y].is_bomb:
        g.end_game()
    else:
        g.explore(cell_x, cell_y)


def mark(event):
    num = [x for x in str(event.widget.name) if x.isdigit()]
    x = int(''.join(num[:len(num)//2]))
    y = int(''.join(num[len(num)//2:]))

    cell_x = None
    cell_y = None
    for i in range(g.gridSize):
        for j in range(g.gridSize):
            if (cell_x is None) and g.locations[i][j].pos[0] <= x <= g.locations[i][j].pos[0]:
                cell_x = i
            if (cell_y is None) and g.locations[i][j].pos[1] <= y <= g.locations[i][j].pos[1]:
                cell_y = j
    target = g.locations[cell_x][cell_y].btn
    if target['text'] == '':
        target.config(text="BOMB", bg="yellow")
    else:
        target.config(text='', bg="white")


def main():
    global g, finished
    finished = False
    g = myGrid(10)
    g.setup()

    master.mainloop()


if __name__ == "__main__":
    main()
