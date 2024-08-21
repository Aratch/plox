#!/usr/bin/env python3

from .token import TokenType, Token
from .error import *

import typing
Char : typing.TypeAlias = str

globals().update(TokenType.__members__)

class Scanner:
    """plox Scanner/Lexer"""

    keywords = {
        "and" : AND,
        "class" : CLASS,
        "else" : ELSE,
        "false": FALSE,
        "for" : FOR,
        "fun": FUN,
        "if": IF,
        "nil": NIL,
        "or": OR,
        "print": PRINT,
        "return": RETURN,
        "super": SUPER,
        "this": THIS,
        "true": TRUE,
        "var": VAR,
        "while": WHILE,
        "break": BREAK
    }

    def __init__(self, source: str):
        self.__source = source
        self.__tokens : list[Token] = list()

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.__tokens

    def scan_token(self):
        c : Char = self.advance()
        match c:
            case '(': self.add_token(LEFT_PAREN)
            case ')': self.add_token(RIGHT_PAREN)
            case '{': self.add_token(LEFT_BRACE)
            case '}': self.add_token(RIGHT_BRACE)
            case ',': self.add_token(COMMA)
            case '.': self.add_token(DOT)
            case '-': self.add_token(MINUS)
            case '+': self.add_token(PLUS)
            case ';': self.add_token(SEMICOLON)
            case '*': self.add_token(STAR)
            case '?': self.add_token(QUESTION_MARK)
            case ':': self.add_token(COLON)

            case '!':
                self.add_token(BANG_EQUAL if self.match("=") else BANG)
            case '=':
                self.add_token(EQUAL_EQUAL if self.match("=") else EQUAL)
            case '<':
                self.add_token(LESS_EQUAL if self.match("=") else LESS)
            case '>':
                self.add_token(GREATER_EQUAL if self.match("=") else GREATER)


            case '/':
                if self.match("/"):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                elif self.match("*"):
                    self.block_comment()
                else:
                    self.add_token(SLASH)

            case ' ' | '\r' | '\t':
                pass

            case '\n':
                self.line += 1

            case '"': self.string()

            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    error(self.line, "Unexpected character.")

    def is_alpha(self, c: Char) -> bool:
        return (c >= 'a' and c <= 'z') or \
            (c >= 'A' and c <= 'Z') or c == '_'

    def is_alphanumeric(self, c: Char) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: Char) -> bool:
        return c >= '0' and c <= '9'

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        text: str = self.__source[self.start:self.current]
        type = Scanner.keywords.get(text)

        if type == None:
            type = IDENTIFIER

        self.add_token(type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(NUMBER,
                       float(self.__source[self.start:self.current]))


    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.__source[self.start+1:self.current-1]
        self.add_token(STRING, value)

    def block_comment(self):
        while self.peek() != "*" and self.peek_next() != "/" and \
                not self.is_at_end():
            c = self.advance()
            if c == '\n':
                self.line += 1
        self.current += 2

    def advance(self) -> Char:
        c : Char = self.__source[self.current]
        self.current += 1
        return c

    def peek(self) -> Char:
        if self.is_at_end(): return '\0'
        return self.__source[self.current]

    def peek_next(self) -> Char:
        if self.current + 1 >= len(self.__source): return '\0'
        return self.__source[self.current + 1]

    def match(self, expected: Char):
        if self.is_at_end(): return False
        if self.__source[self.current] != expected: return False

        self.current += 1
        return True

    def add_token(self, type: TokenType, literal=None):
        text : str = self.__source[self.start:self.current]
        self.__tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self):
        return self.current >= len(self.__source)
