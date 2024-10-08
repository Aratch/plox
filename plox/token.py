#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from dataclasses import dataclass
import typing


TokenType = Enum("TokenType",
                 """LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE
                 COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,
                 BANG, BANG_EQUAL,
                 EQUAL, EQUAL_EQUAL,
                 GREATER, GREATER_EQUAL,
                 LESS, LESS_EQUAL,
                 IDENTIFIER, STRING, NUMBER,
                 AND, CLASS, ELSE, FALSE, FUN, FOR IF, NIL OR,
                 PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE,
                 BREAK,
                 QUESTION_MARK, COLON,
                 EOF""")

# https://stackoverflow.com/a/28130684
globals().update(TokenType.__members__)

@dataclass(eq=True, frozen=True, unsafe_hash=True)
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
    # id: object = object()

    # def __hash__(self) -> int:
    #     return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
