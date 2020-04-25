import turtle
import time

def draw_line_turn(draw):
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    turtle.right(90)


def draw_line_fd(draw):
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)


def draw_complet(a1, a2, a3, a4, a5, a6, a7):
    draw_line_turn(a1)
    draw_line_turn(a2)
    draw_line_turn(a3)
    draw_line_fd(a4)
    draw_line_turn(a5)
    draw_line_turn(a6)
    draw_line_turn(a7)
    


digit_dic = {0:(0,1,1,1,1,1,1), 1:(0,1,0,0,0,0,1), 2:(1,0,1,1,0,1,1), 3:(1,1,1,0,0,1,1), 4:(1,1,0,0,1,0,1)}



turtle.setup(1800, 1400)


for dg in digit_dic:
    turtle.penup()
    turtle.fd((dg+1)*80)
    a1, a2, a3, a4, a5, a6, a7 = digit_dic[dg]
    draw_complet(a1, a2, a3, a4, a5, a6, a7)
    # turtle.penup()
    # turtle.fd(120)
    time.sleep(1)
# a1, a2, a3, a4, a5, a6, a7 = digit_dic[2]
# draw_complet(a1, a2, a3, a4, a5, a6, a7)
