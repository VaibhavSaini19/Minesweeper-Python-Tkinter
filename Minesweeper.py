import random
import turtle as myTurtle
myTurtle.speed(0)
myTurtle.shape("square")
myTurtle.color("yellow")


class cell:
    def __init__(self, pos, state=None):
        self.pos = pos                          # coordinates in terms of x, y
        self.is_bomb = False                       
        self.nearby = 0                      # number of bombs in adjacent 8 cells
        self.revealed = False                   
        self.stampId = None

class Grid:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.cellSize = 10
        self.locations = [[None for x in range(self.gridSize)] for y in range(self.gridSize)]
        self.total_bombs = self.gridSize**2 // 8
        #myTurtle.turtlesize(self.cellSize/20, self.cellSize/20)

    def setup(self):
        self.draw()
        self.set_bombs()
        myTurtle.ht()
    
    def draw(self):
        #myTurtle.dot(5, "blue")
        myTurtle.pu()
        x0 = -((20*self.gridSize/2) + (10*(self.gridSize-1)/2) - 10)
        y0 =  ((20*self.gridSize/2) + (10*(self.gridSize-1)/2) - 9)

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                x, y = x0 + i*(20+10), y0 - j*(20+10)
                myTurtle.goto(x, y)
                self.locations[i][j] = cell(myTurtle.pos())
                self.locations[i][j].stampId = myTurtle.stamp()
    
    def set_bombs(self):
        i = 0
        while i < self.total_bombs:
            bomb_x = random.randint(1, self.gridSize - 2)               # replace from (0, gridsize - 1) to avoid bombs
            bomb_y = random.randint(1, self.gridSize - 2)               # adjacent to walls (nearby count was getting messed up somehow)
            if not self.locations[bomb_x][bomb_y].is_bomb:  
                self.locations[bomb_x][bomb_y].is_bomb = True

                try:
                    self.locations[bomb_x-1][bomb_y-1].nearby += 1
                    self.locations[bomb_x][bomb_y-1].nearby += 1
                    self.locations[bomb_x+1][bomb_y-1].nearby += 1
                    self.locations[bomb_x-1][bomb_y].nearby += 1
                    self.locations[bomb_x+1][bomb_y].nearby += 1
                    self.locations[bomb_x-1][bomb_y+1].nearby += 1
                    self.locations[bomb_x][bomb_y+1].nearby += 1
                    self.locations[bomb_x+1][bomb_y+1].nearby += 1
                except:
                    continue

                i += 1
                #print("Bombs: ", bomb_x, bomb_y, i)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].is_bomb:
                    print("b", end=" ")
                else:
                    print(self.locations[i][j].nearby, end=" ")
            print()


    def explore(self, cell_x, cell_y):
        l = [(0, 0), (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        exp_x = cell_x
        exp_y = cell_y
        exp_cell = self.locations[exp_x][exp_y]
        if not exp_cell.revealed:
            exp_cell.revealed = True
            if exp_cell.nearby == 0:
                myTurtle.goto(exp_cell.pos)
                myTurtle.color("green")
                myTurtle.stamp()
                myTurtle.color("yellow")
                for pair in l:
                    try:
                        exp_x = cell_x + pair[0]
                        exp_y = cell_y + pair[1]
                        exp_cell = self.locations[exp_x][exp_y]
                        self.explore(exp_x, exp_y)
                    except:
                        pass
            else:
                        myTurtle.goto(exp_cell.pos[0]-2, exp_cell.pos[1]-7)
                        myTurtle.pencolor("black")
                        myTurtle.write(exp_cell.nearby)

        self.won()

    def end_game(self):
        print("BOMB encountered!!!")
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].is_bomb:
                    myTurtle.goto(self.locations[i][j].pos)
                    myTurtle.pd()
                    myTurtle.color("red")
                    myTurtle.stamp()
                    myTurtle.pu()
        myTurtle.exitonclick()

    def won(self):
        count = False
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.locations[i][j].revealed == False:
                    count += 1
        if count == self.total_bombs:
            print("You won!!!")
            myTurtle.exitonclick()


def get(x, y):
    #print("x, y: ", x, y)
    cell_x = None
    cell_y = None
    for i in range(g.gridSize):
        for j in range(g.gridSize):
            if (cell_x is None) and g.locations[i][j].pos[0]-10 <= x <= g.locations[i][j].pos[0]+10:
                cell_x = i
            if (cell_y is None) and g.locations[i][j].pos[1]-10 <= y <= g.locations[i][j].pos[1]+10:
                cell_y = j
    if g.locations[cell_x][cell_y].is_bomb:
        g.end_game()
    else:
        g.explore(cell_x, cell_y)

    

def main():
    global g
    g = Grid(10)
    g.setup()
    myTurtle.onscreenclick(get)
    myTurtle.mainloop()
    #myTurtle.exitonclick()

if __name__ == "__main__":
    main()
