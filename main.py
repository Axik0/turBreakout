import turtle as t
from PIL import Image, ImageTk

import obstacles as o
from auxfunc import *

lifes = 3
PAD_LEVEL = -220
WALLX = 240
WALLY = [PAD_LEVEL + 10 + 5, 0]

COLORS6 = ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff", "#8ecae6"]
# Global color palette
main_color = '#f0f3f5'
focus_color = '#fff0fb'
text_color_a = '#262626'
text_color_ina = '#848484'

# # Global font
# main_font = ("Helvetica", 16)

w = t.Screen()
w.setup(width=500, height=500, startx=500, starty=100)
w.title('Breakout')
# loads an icon file, resizes it with a help of PIL and transfers to an tkinter object underneath Screen class
icon = Image.open("images/icon.png")
icon = icon.resize((35, 35), Image.Resampling.LANCZOS)
icon = ImageTk.PhotoImage(icon)
w._root.iconphoto(False, icon)
# w.textinput("Player setup", "Enter your name:")
w.bgcolor(focus_color)

ball = t.RawTurtle(w)
ball.shape("circle")
ball.penup()
ball.hideturtle()
ball.goto(0, PAD_LEVEL + 10 + 5)
ball.shapesize(0.5, 0.5)
ball.pendown()
ball.showturtle()
ball.seth(40)
ball.speed(0)


def igoto(point):
    # this function slows ball's movement but only when it travels inbetween 2 points
    ball.speed(2)
    ball.goto(point)
    ball.speed(0)


pad = t.RawTurtle(w)
pad.hideturtle()
pad.penup()
pad.goto(0, PAD_LEVEL)
pad.shape("square")
pad.shapesize(1, 4)
pad.showturtle()
w.onkeypress(lambda: pad.forward(20), 'Right')
w.onkeypress(lambda: pad.backward(20), 'Left')
w.listen()


def place_bars(hide=True, skip=True):
    """This function calls an Obstacle class object and draws all the bars according to those parameters"""
    obs = o.Obstacle(window_size=(498, 498), grid_size=(8, 6))
    obs.load()
    global WALLY
    WALLY[1] = obs.LL
    # obs.getlog(True)
    cid = 0
    if skip:
        w.tracer(0)
    for lev in obs.bars:
        for coord in obs.bars[lev]:
            bar = t.RawTurtle(w)
            if hide:
                bar.hideturtle()
                bar.speed(0)
            bar.penup()
            bar.shape('square')
            # no error, a stretch factor is perpendicular to the corresponding axis (depends of turtle's EAST heading!)
            bar.shapesize(obs.BAR_SEMI_HEIGHT / 10, obs.BAR_SEMI_WIDTH / 10)
            bar.goto(coord)
            bar.color(COLORS6[cid])
            if hide:
                bar.showturtle()
        cid += 1
        if skip:
            w.update()
    w.tracer(1)


place_bars()


for _ in range(10):
    tr = trajectory(ball.pos(), ball.heading())
    check_vw = line_intersection(tr, (1, 0, -WALLX)), line_intersection(tr, (1, 0, WALLX))
    check_hw = line_intersection(tr, (0, 1, -WALLY[1])), line_intersection(tr, (0, 1, -WALLY[0]))
    # we may reach one of 2 vertical walls, but have to if we haven't done that already
    if ball.pos()[0] != WALLX and WALLY[0] < check_vw[0][1] < WALLY[1]:
        igoto(check_vw[0])
        ball.seth(ver(ball.heading()))
    elif ball.pos()[0] != -WALLX and WALLY[0] < check_vw[1][1] < WALLY[1]:
        igoto(check_vw[1])
        ball.seth(ver(ball.heading()))
    # same for 2 horizontal walls
    elif ball.pos()[1] != WALLY[1] and abs(check_hw[0][0]) < WALLX:
        igoto(check_hw[0])
        ball.seth(hor(ball.heading()))
    elif ball.pos()[1] != WALLY[0] and abs(check_hw[1][0]) < WALLX:
        igoto(check_hw[1])
        ball.seth(hor(ball.heading()))
        if abs(pad.xcor()-ball.xcor()) < 50:
            print('catch')
        else:
            break
    else:
        print('strange behaviour?', check_vw, check_hw)


w.exitonclick()

# TODO class ball
# TODO class pad
# TODO class scoreboard
# TODO lives
