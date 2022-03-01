from turtle import *


class ScoreBoard(Turtle):

    def __init__(self, score_position, hscore_position):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.score = 0
        self.high_score = 0
        self.position = score_position
        self.pos = hscore_position
        self.add = 1
        self.update_score()
        self.update_high_score()

    def update_score(self):
        self.goto(self.position)
        self.write(f"Score: {self.score}", font=("Arial", 15, "normal"))

    def update_high_score(self):
        self.goto(self.pos)
        self.write(f"High Score: {self.high_score}", font=("Arial", 15, "normal"))

    def add_high_score(self):
        if self.score > self.high_score:
            self.high_score += self.score
            self.clear()
            self.update_high_score()
            self.update_score()

    def add_score(self):
        self.score += self.add
        self.clear()
        self.update_score()
        self.update_high_score()

