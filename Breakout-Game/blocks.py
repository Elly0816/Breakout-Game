from turtle import *


class Block(Turtle):  # Block that inherits all the turtle properties

    def __init__(self, posit, col):
        super().__init__()
        tracer(0, 0)
        self.penup()
        self.setpos(posit)
        self.color(col)
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=4.5)

# screen = Screen()
# block = Block((0, 0), 'red')
# screen.mainloop()
