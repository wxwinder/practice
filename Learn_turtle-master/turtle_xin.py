import turtle as t
def drawLine():
    for i in range(200):
        t.rt(0.98)
        t.fd(1)


def drawHeart():
    t.color('pink','red')
    t.begin_fill()
    t.seth(127)
    t.fd(143)
    drawLine()
    t.lt(130)
    drawLine()
    t.fd(143)
    t.end_fill()
if __name__ == '__main__':
    t.setup(500, 500, 600, 300)
    t.speed(5)
    t.pensize(3)
    drawHeart()
    t.done()
