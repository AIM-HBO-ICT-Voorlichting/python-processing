import inspect
import pygame


_width = 800
_height = 500
_fps = 60
_title = "Sketch"

_screen = None
_clock = None

# drawing state
_fill_enabled = True
_stroke_enabled = True
_fill_color = (255, 255, 255)
_stroke_color = (0, 0, 0)
_stroke_weight = 1
_text_size = 12
_font = None


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

def background(*args):
    _require_screen("background")
    # grayscale or rgb overload
    if len(args) == 1:
        g = int(args[0])
        col = (g, g, g)
    elif len(args) == 3:
        col = tuple(int(v) for v in args)
    else:
        raise TypeError("background() takes 1 or 3 arguments")
    _screen.fill(col)

def rect(x, y, w, h):
    _require_screen("rect")
    x, y, w, h = map(int, (x, y, w, h))
    if _fill_enabled:
        pygame.draw.rect(_screen, _fill_color, (x, y, w, h), 0)
    if _stroke_enabled:
        pygame.draw.rect(_screen, _stroke_color, (x, y, w, h), int(_stroke_weight))

def circle(x, y, d):
    _require_screen("circle")
    x, y, d = int(x), int(y), int(d)
    radius = d // 2
    if _fill_enabled:
        pygame.draw.circle(_screen, _fill_color, (x, y), radius, 0)
    if _stroke_enabled:
        pygame.draw.circle(_screen, _stroke_color, (x, y), radius, int(_stroke_weight))

# additional primitives

def point(x, y):
    _require_screen("point")
    x, y = int(x), int(y)
    if _stroke_enabled:
        _screen.set_at((x, y), _stroke_color)

def line(x1, y1, x2, y2):
    _require_screen("line")
    pts = _apply_coords((x1, y1, x2, y2))
    if _stroke_enabled:
        pygame.draw.line(_screen, _stroke_color, pts[:2], pts[2:], int(_stroke_weight))

def triangle(x1, y1, x2, y2, x3, y3):
    _require_screen("triangle")
    pts = _apply_coords((x1, y1, x2, y2, x3, y3))
    if _fill_enabled:
        pygame.draw.polygon(_screen, _fill_color, [pts[0:2], pts[2:4], pts[4:6]])
    if _stroke_enabled:
        pygame.draw.polygon(_screen, _stroke_color, [pts[0:2], pts[2:4], pts[4:6]], int(_stroke_weight))

def quad(x1, y1, x2, y2, x3, y3, x4, y4):
    _require_screen("quad")
    pts = _apply_coords((x1, y1, x2, y2, x3, y3, x4, y4))
    pts_list = [pts[i:i+2] for i in range(0, 8, 2)]
    if _fill_enabled:
        pygame.draw.polygon(_screen, _fill_color, pts_list)
    if _stroke_enabled:
        pygame.draw.polygon(_screen, _stroke_color, pts_list, int(_stroke_weight))

def ellipse(x, y, w, h):
    _require_screen("ellipse")
    x, y, w, h = map(int, (x, y, w, h))
    rect = (x - w//2, y - h//2, w, h)
    if _fill_enabled:
        pygame.draw.ellipse(_screen, _fill_color, rect, 0)
    if _stroke_enabled:
        pygame.draw.ellipse(_screen, _stroke_color, rect, int(_stroke_weight))

# style functions

def fill(r, g=None, b=None):
    global _fill_enabled, _fill_color
    _fill_enabled = True
    if g is None:
        g = r
        _fill_color = (int(r), int(r), int(r))
    else:
        _fill_color = (int(r), int(g), int(b))

def noFill():
    global _fill_enabled
    _fill_enabled = False

def stroke(r, g=None, b=None):
    global _stroke_enabled, _stroke_color
    _stroke_enabled = True
    if g is None:
        g = r
        _stroke_color = (int(r), int(r), int(r))
    else:
        _stroke_color = (int(r), int(g), int(b))

def noStroke():
    global _stroke_enabled
    _stroke_enabled = False

def strokeWeight(w):
    global _stroke_weight
    _stroke_weight = int(w)

# helpers for colors and text

def color(r, g=None, b=None, a=None):
    if g is None:
        return (int(r), int(r), int(r))
    col = (int(r), int(g), int(b))
    if a is not None:
        col = (*col, int(a))
    return col

def textSize(sz):
    global _text_size, _font
    _text_size = int(sz)
    _font = None  # will recreate on next draw

def text(txt, x, y):
    _require_screen("text")
    _ensure_font()
    surf = _font.render(str(txt), True, _fill_color if _fill_enabled else _stroke_color)
    _screen.blit(surf, _apply_coords((x, y)))

def arc(x, y, w, h, start, stop):
    _require_screen("arc")
    rect = pygame.Rect(_apply_coords((x - w/2, y - h/2, w, h)))
    if _stroke_enabled:
        pygame.draw.arc(_screen, _stroke_color, rect, float(start), float(stop), int(_stroke_weight))

def bezier(x1, y1, x2, y2, x3, y3, x4, y4, segments=20):
    _require_screen("bezier")
    pts = _apply_coords((x1, y1, x2, y2, x3, y3, x4, y4))
    path = []
    for i in range(segments + 1):
        t = i / segments
        # cubic bezier formula
        x = ( (1-t)**3 * pts[0] + 3*(1-t)**2*t * pts[2] + 3*(1-t)*t**2 * pts[4] + t**3 * pts[6] )
        y = ( (1-t)**3 * pts[1] + 3*(1-t)**2*t * pts[3] + 3*(1-t)*t**2 * pts[5] + t**3 * pts[7] )
        path.append((int(x), int(y)))
    if _stroke_enabled and len(path) > 1:
        pygame.draw.lines(_screen, _stroke_color, False, path, int(_stroke_weight))


# --------------------
# Helpers
# --------------------

def _ensure_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont(None, _text_size)

def _apply_coords(vals):
    return tuple(int(v) for v in vals)

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
    pygame.font.init()
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