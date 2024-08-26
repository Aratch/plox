#!/usr/bin/env python3

from typing import Any
from .token import Token

class PloxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.token = token

class LoopBreakException(PloxRuntimeError):
    pass


# TODO: Figure out if I need to suppress the more involved exception handling features
# like in the Java original, e.g.
# by overriding sys.excepthook as in
# https://gist.github.com/jhazelwo/86124774833c6ab8f973323cb9c7e251
class PloxReturnException(PloxRuntimeError):
    def __init__(self, value: Any,
                 token: Token,
                 message = "'return' statements are only allowed inside functions."):
        super().__init__(token, message)
        self.value = value
