import pygame
import inspect

_width = 800
_height = 500
_fps = 60
_title = "Sketch"

_screen = None
_clock = None


# --------------------
# Processing-achtige API
# --------------------

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
    _require_screen("background")
    g = int(gray)
    _screen.fill((g, g, g))

def rect(x, y, w, h):
    _require_screen("rect")
    pygame.draw.rect(_screen, (0, 0, 0), (int(x), int(y), int(w), int(h)), 2)

def circle(x, y, d):
    _require_screen("circle")
    pygame.draw.circle(_screen, (0, 0, 0), (int(x), int(y)), int(d) // 2, 2)


# --------------------
# Helpers
# --------------------

def _require_screen(func_name: str):
    if _screen is None:
        raise RuntimeError(
            f"{func_name}() called before the window exists. "
            f"Call run() after your drawing code (or draw inside setup()/draw())."
        )

def _make_sketch_from_caller():
    caller_globals = inspect.stack()[2].frame.f_globals
    return type("Sketch", (object,), caller_globals)

def _init_window():
    global _screen, _clock
    pygame.init()
    _screen = pygame.display.set_mode((_width, _height))
    pygame.display.set_caption(_title)
    _clock = pygame.time.Clock()

def _shutdown():
    pygame.quit()


# --------------------
# Modes
# --------------------

def run(mode=None):
    """
    Processing-achtige runner met 2 modes:

    1) Static mode (default als er GEEN draw() is):
       - Je tekent direct (top-level) of in setup()
       - Geen animatieloop
       - Window blijft open tot sluiten

    2) Interactive mode (default als er draw() is):
       - Vereist: setup() én draw()
       - draw() wordt ~fps keer per seconde aangeroepen
       - key_pressed(key) optioneel

    Je kunt mode forceren met mode="static" of mode="interactive".
    """
    sketch = _make_sketch_from_caller()

    has_setup = hasattr(sketch, "setup")
    has_draw = hasattr(sketch, "draw")

    if mode is None:
        mode = "interactive" if has_draw else "static"
    else:
        mode = mode.lower().strip()

    if mode not in ("static", "interactive"):
        raise ValueError('mode must be None, "static", or "interactive"')

    _init_window()

    try:
        if mode == "interactive":
            # minimaal vereist
            if not has_setup or not has_draw:
                raise RuntimeError(
                    "Interactive mode requires both setup() and draw(). "
                    "Either define them, or remove draw() to use static mode."
                )

            # setup één keer
            sketch.setup()

            # loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and hasattr(sketch, "key_pressed"):
                        sketch.key_pressed(event.key)

                sketch.draw()

                pygame.display.flip()
                _clock.tick(_fps)

        else:  # static
            # In static mode mag setup() bestaan, draw() wordt genegeerd
            if has_setup:
                sketch.setup()

            # 1 frame renderen
            pygame.display.flip()

            # window openhouden
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                _clock.tick(30)

    finally:
        _shutdown()