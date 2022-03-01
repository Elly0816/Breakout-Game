from turtle import *


class Pad(Turtle):
    def __init__(self, posit):
        super().__init__()
        tracer(0, 0)
        self.penup()
        self.shape('square')
        self.color('green')
        self.setpos(posit)
        self.shapesize(stretch_wid=1, stretch_len=12)
