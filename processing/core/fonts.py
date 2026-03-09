def ensure_font(state, pygame):
    if state["_font"] is None:
        state["_font"] = pygame.font.SysFont(None, state["_text_size"])
