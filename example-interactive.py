from processing import *

x = 0
speed = 0
direction = 0

def setup():
    global x, speed, direction
    size(400,400)
    title("Interactive mode example")
    x = 25
    speed = 5
    direction = 1

def draw():
    global x, direction

    background(255)
    fill(229, 0, 68)
    circle(x, 200, 50)

    x += speed*direction

    if x > width - 25:
        x = width - 25
        direction = -1
    elif x < 25:
        x = 25
        direction = 1

    request_input("New speed: ") # does not block and is not executed every frame, only if no input has been given via input_received()

def input_received(text_line):
    global speed
    try:
        speed = int(text_line)
    except ValueError:
        print("Invalid input: " + text_line)
        
# Interactive mode requires a call to run() at the end of the sketch:  
run()