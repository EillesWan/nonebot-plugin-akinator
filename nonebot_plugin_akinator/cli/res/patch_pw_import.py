#!/usr/bin/env python3


def patch():
    import builtins
    from collections.abc import Mapping, Sequence
    from functools import wraps
    from types import ModuleType

    _old_import = __import__

    @wraps(_old_import)
    def _new_import(
        name: str,
        globals: Mapping[str, object] | None = None,  # noqa: A002
        locals: Mapping[str, object] | None = None,  # noqa: A002
        fromlist: Sequence[str] = (),
        level: int = 0,
    ) -> ModuleType:
        if level == 0 and (name == "playwright" or name.startswith("playwright.")):
            name = name.replace("playwright", "patchright", 1)
        return _old_import(name, globals, locals, fromlist, level)

    builtins.__import__ = _new_import  # noqa: A001
