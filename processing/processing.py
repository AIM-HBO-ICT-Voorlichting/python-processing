import pygame
import inspect

_width = 800
_height = 500
_fps = 60
_title = "Sketch"

_screen = None
_clock = None

def size(w, h):
    global _width, _height
    _width, _height = int(w), int(h)

def frame_rate(fps):
    global _fps
    _fps = int(fps)

def title(t):
    global _title
    _title = str(t)

def background(gray):
    g = int(gray)
    _screen.fill((g, g, g))

def rect(x, y, w, h):
    pygame.draw.rect(_screen, (0, 0, 0), (int(x), int(y), int(w), int(h)), 2)

def circle(x, y, d):
    pygame.draw.circle(_screen, (0, 0, 0), (int(x), int(y)), int(d) // 2, 2)

def run():
    """Start de sketch vanuit het bestand dat run() aanroept."""
    global _screen, _clock

    caller_globals = inspect.stack()[1].frame.f_globals
    sketch = type("Sketch", (object,), caller_globals)

    pygame.init()
    _screen = pygame.display.set_mode((_width, _height))
    pygame.display.set_caption(_title)
    _clock = pygame.time.Clock()

    if hasattr(sketch, "setup"):
        sketch.setup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and hasattr(sketch, "key_pressed"):
                sketch.key_pressed(event.key)

        if hasattr(sketch, "draw"):
            sketch.draw()

        pygame.display.flip()
        _clock.tick(_fps)

    pygame.quit()