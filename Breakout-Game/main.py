from turtle import *
from blocks import Block
from ball import Ball
from pad import Pad
import time
from scoreboard import ScoreBoard


class BreakOutGame:

    def __init__(self):
        self.colors = ['red', 'orange', 'green', 'yellow']
        self.win = Screen()
        self.win.setup(960, 800)
        self.win.title("Break Out")
        self.win.bgcolor("Black")
        win_width, win_height = self.win.window_width(), self.win.window_height()
        self.min_x, self.max_x = -win_width / 2, win_width / 2
        self.min_y, self.max_y = -win_height / 2, (win_height / 2) - 100
        self.blocks = []
        self.pad = None
        self.ball = None
        self.score = None
        self.sleep = 0.0001
        self.count = 0
        self.speed = 2

    def draw_margin(self):
        line = Turtle()
        tracer(0, 0)
        line.hideturtle()
        line.color('white')
        line.penup()
        line.setpos(self.min_x, self.max_y)
        line.right(90)
        line.pensize(3)
        line.pendown()
        line.goto(self.max_x, self.max_y)

    def draw_blocks(self):  # Draws the colored blocks
        x = self.min_x + 47.25
        y = self.max_y - 100
        for i in range(len(self.colors) * 2):
            if i < len(self.colors):
                col = self.colors[i]
            else:
                col = self.colors[i - 5]
            for j in range(10):
                self.blocks.append(Block((x, y), col))
                x += 95
            x = self.min_x + 47.25
            y -= 35

    def block_collision(self):
        for block in self.blocks:
            block_top = block.ycor() + 15.75
            block_bot = block.ycor() - 15.75
            block_right = block.xcor() + 47.25
            block_left = block.xcor() - 47.25
            if 15.75 <= self.ball.distance(block) <= 47.25:
                if block_left-10.5 <= self.ball.xcor() <= block_right+10.5:
                    self.ball.deflect_tb()
                    self.blocks.remove(block)
                    block.hideturtle()
                    self.score.add_score()
                    self.count += 1
                elif block_bot-10.5 <= self.ball.ycor() <= block_top+10.5:
                    self.ball.deflect_wall()
                    self.blocks.remove(block)
                    block.hideturtle()
                    self.score.add_score()
                    self.count += 1
            if self.count > 9:
                self.ball.x_move *= 1.05
                self.ball.x_move *= 1.05
                self.speed *= 1.05
                self.count = 0

    def draw_pad(self):  # Draws the pad
        self.pad = Pad((0, self.min_y+21))

    def pad_right(self):  # Function for moving the pad right
        if self.pad.xcor() + 127 < self.max_x:
            self.pad.setx(self.pad.xcor() + 30)

    def pad_left(self):  # Function for moving the pad left
        if self.pad.xcor() - 127 > self.min_x:
            self.pad.setx(self.pad.xcor() - 30)

    def draw_ball(self):  # Draws the ball
        self.ball = Ball((self.pad.xcor(), self.pad.ycor() + 21), speed=self.speed)

    def border_collision(self):
        if self.ball.xcor() + 10.5 >= self.max_x:  # Detects collision with right wall
            self.ball.deflect_wall()
        if self.ball.xcor() - 10.5 <= self.min_x:  # Detects collision with left wall
            self.ball.deflect_wall()
        if self.ball.ycor() + 10.5 >= self.max_y:  # Detects collision with roof
            self.ball.deflect_tb()
            # Detects collision with pad
        if (self.ball.ycor() - 10.5 <= self.pad.ycor() + 10.5) and (self.ball.distance(self.pad) <= 126):
            self.ball.deflect_tb()
            # Detects if ball has touched the floor
        if self.ball.ycor() - 10.5 <= self.min_y and (self.ball.distance(self.pad) >= 126):
            self.score.add_high_score()
            self.score.score = -1
            self.score.add_score()
            self.ball.hideturtle()
            self.speed = 2
            self.draw_ball()

    def draw_score(self):
        self.score = ScoreBoard((self.min_x+50, self.max_y+70), (self.max_x-250, self.max_y+70))

    def start_game(self):
        self.draw_margin()
        self.draw_blocks()
        self.draw_pad()
        self.win.listen()
        self.win.onkeypress(self.pad_right, 'Right')
        self.win.onkeypress(self.pad_left, 'Left')
        self.draw_ball()
        self.draw_score()
        game_on = True
        while game_on:  # Ball moves and detects collision while the game is on
            if len(self.blocks) == 0:
                self.draw_blocks()
                self.ball.hideturtle()
                self.draw_ball()
            time.sleep(self.sleep)
            self.ball.move()
            self.win.update()
            self.border_collision()
            self.block_collision()

        self.win.exitonclick()


game = BreakOutGame()
game.start_game()

block_x = 94.5
block_y = 31.5
pad_x = 252
pad_y = 21
ball_x = 21
ball_y = 21
