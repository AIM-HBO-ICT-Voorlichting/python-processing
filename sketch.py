from processing import *

size(800, 500)
title("Rijdende auto")

# state
xPos = 0
yPos = 375
autoRijdt = False
richting = 1

def draw():
    global xPos, autoRijdt, richting

    # view
    background(255)
    rect(xPos, yPos, 200, 100)
    circle(xPos + 50,  yPos + 100, 50)
    circle(xPos + 150, yPos + 100, 50)

    # logic
    if autoRijdt:
        xPos += richting
    if xPos > 800 - 200:
        richting = -1
    if xPos < 0:
        richting = 1

def key_pressed(key):
    global autoRijdt
    autoRijdt = not autoRijdt

run()