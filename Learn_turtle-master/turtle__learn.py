import turtle as t
t.setup(1000,500,600,300)
t.shape('turtle')
t.pensize(5)
t.speed(3)
'''
# 同心圆
for i in range(9):
    t.pu()
    t.goto(0,-20*(i+1))
    t.pd()
    t.circle(20*(i+1))
t.done()
'''

'''
# 等边n边形

n = 10
angle_ =180 -  180*(n - 2 ) / n
for i in range(n):
    t.fd(100)
    t.left(angle_)
'''

'''

def drawSnake(rad, angle, len, neckrad):
    for i in range(len):
        t.circle(rad, angle)
        t.circle(-rad, angle)
    t.circle(rad, angle/2)
    t.fd(rad)
    t.circle(neckrad+1, 180)
    t.fd(rad*2/3)

def main():
    t.setup(1300, 800, 0, 0)
    pythonsize = 30
    t.pensize(pythonsize)
    t.pencolor("red")
    t.seth(-40)
    drawSnake(40, 80, 5, pythonsize/2)

main()
'''
t.seth(60)
t.fd(200)
t.seth(30)
t.fd(400)
t.done()
