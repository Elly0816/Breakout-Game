from turtle import *
import random

class Ball(Turtle):

    def __init__(self, posit, *args, **kwargs):
        super().__init__()
        tracer(0, 0)
        self.penup()
        self.setpos(posit)
        self.color('white')
        self.shape('circle')
        move = kwargs['speed']
        self.x_move = random.choice([move, -move])
        self.y_move = move
        self.speed('slowest')

    def move(self):
        self.setpos(self.xcor()+self.x_move, self.ycor()+self.y_move)

    def deflect_wall(self):
        self.x_move *= -1

    def deflect_tb(self):
        self.y_move *= -1
