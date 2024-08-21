#!/usr/bin/env python

from .environment import Environment
from .error import runtime_error
from .token import Token, TokenType
from .expr import *
from .stmt import *
from .visitor import visitor
import math

def is_truthy(obj):
    if obj == None: return False
    # Redundant cast, but whatever
    if isinstance(obj, bool): return bool(obj)
    return True

def is_equal(a, b):
    # This might be superfluous because we don't run the risk of
    # causing a null pointer dereference like in Java
    if a == None and b == None: return True
    if a == None: return False

    return a == b

class PloxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.token = token

# Unary checker
def check_number_operand(operator: Token, operand):
    if isinstance(operand, float): return
    raise PloxRuntimeError(operator, "Operand must be a number.")

# Binary checker
def check_number_operands(operator: Token, left, right):
    if isinstance(left, float) and isinstance(right, float):
        if math.isclose(right, 0.0):
            raise PloxRuntimeError(operator, "Attempting division by zero.")
        return
    raise PloxRuntimeError(operator, "Operands must be numbers.")

# TODO: Ternary checker

def stringify(obj):
    if object == None: return "nil"

    if isinstance(obj, float):
        text = str(obj)
        if text.endswith(".0"):
            text = text[:-2]
        return text

    return str(obj)

Uninitialized = object()

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except PloxRuntimeError as error:
            runtime_error(error)

    def execute(self, stmt: Stmt):
        self.visit(stmt)

    # Keep this for now
    def interpret_single_expr(self, expression: Expr):
        try:
            value = self.evaluate(expression)
            print(stringify(value))
        except PloxRuntimeError as error:
            runtime_error(error)

    def evaluate(self, expr: Expr):
        return self.visit(expr)

    # Statement methods (superclass Stmt)

    @visitor(Block)
    def visit(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def execute_block(self, statements: list[Stmt],
                      environment: Environment):
        previous: Environment = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previous

    @visitor(Expression)
    def visit(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    @visitor(If)
    def visit(self, stmt: If):
        if is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

        return None

    @visitor(Print)
    def visit(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(stringify(value))
        return None

    @visitor(Var)
    def visit(self, stmt: Var):
        # Use unique value instead of None to catch uninitialised variables
        value = Uninitialized
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

        return None

    @visitor(While)
    def visit(self, stmt: While):
        while is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

        return None

    # Expression methods (superclass Expr)

    @visitor(Assign)
    def visit(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    @visitor(Literal)
    def visit(self, expr: Literal):
        return expr.value

    @visitor(Logical)
    def visit(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if is_truthy(left): return left
        else:
            if not is_truthy(left): return left

        return self.evaluate(expr.right)


    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self.evaluate(expr.expression)

    @visitor(Unary)
    def visit(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not is_truthy(right)

        # Unreachable
        return None

    @visitor(Variable)
    def visit(self, expr: Variable):
        return self.environment.get(expr.name)

    @visitor(Binary)
    def visit(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)

            case TokenType.MINUS:
                check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                # If left and right are either but not the same
                if isinstance(left, (str, float)) and isinstance(right, (str, float)):
                    return stringify(left) + stringify(right)
                raise PloxRuntimeError(expr.operator,
                                       "Operands must be two numbers or two strings, or either of each.")
            case TokenType.SLASH:
                check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                check_number_operands(expr.operator, left, right)
                return float(left) * float(right)

            case TokenType.BANG_EQUAL: return False
            case TokenType.EQUAL_EQUAL: return True

        # Unreachable
        return None

    # TODO: Ternary method
