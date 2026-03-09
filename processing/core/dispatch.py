import inspect


def invoke_handler(sketch, name, *args):
    if not hasattr(sketch, name):
        return

    handler = getattr(sketch, name)
    sig = inspect.signature(handler)
    params = list(sig.parameters.values())
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)

    if has_varargs:
        handler(*args)
        return

    positional = [
        p
        for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]

    if not positional:
        handler()
    else:
        handler(*args[: len(positional)])
