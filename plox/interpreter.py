#!/usr/bin/env python

from .exceptions import *
from .plox_callable import PloxCallable, PloxFunction, PloxLambda
from .environment import Environment
from .error import runtime_error
from .token import Token, TokenType
from .expr import *
from .stmt import *
from .visitor import visitor

from typing import Any

import math

import time

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


# Unary checker
def check_number_operand(operator: Token, operand):
    if isinstance(operand, float): return
    raise PloxRuntimeError(operator, "Operand must be a number.")

# Binary checker
def check_number_operands(operator: Token, left, right):
    if isinstance(left, float) and isinstance(right, float):
        if math.isclose(right, 0.0) and operator.type == TokenType.SLASH:
            raise PloxRuntimeError(operator, "Attempting division by zero.")
        return
    raise PloxRuntimeError(operator, f"Token: {operator}\nLeft: {left}\nRight: {right}\nOperands must be numbers.")

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
        self.globals = Environment()
        self.environment = self.globals

        self.locals: dict[Expr, int] = dict()

        # DONE: Finish this ungodly abomination
        # https://stackoverflow.com/q/1123000
        # https://mihfazhillah.medium.com/anonymous-class-in-python-39e42140db94
        # FIXME: Maybe replace this with saner (for Python-world) pre-defined classes
        # DONE: This does not work because the 'self' argument in the lambdas is not automatically
        # added
        # NOTE: I'm an idiot, I have to instantiate this anonymous class afterwards
        self.globals.define("clock",
                       type("__Plox_clock__",
                            (PloxCallable,),
                            {
                                "arity" : lambda self: 0,
                                "call"  : lambda self, interpreter, arguments: time.time(),
                                "__str__" : lambda self: "<native fn>"
                            }
                            )()
                       )

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except PloxRuntimeError as error:
            runtime_error(error)

    def execute(self, stmt: Stmt):
        self.visit(stmt)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

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

    @visitor(Function)
    def visit(self, stmt: Function):
        function: PloxFunction = PloxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
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

    @visitor(Return)
    def visit(self, stmt: Return):
        value = None

        if stmt.value:
            value = self.evaluate(stmt.value)

        raise PloxReturnException(value, stmt.keyword)

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
            try:
                self.execute(stmt.body)
            except LoopBreakException:
                return None

        return None

    @visitor(Break)
    def visit(self, stmt: Break):
        raise LoopBreakException(stmt.token, "'break' statements are only allowed inside loops.")

    # Expression methods (superclass Expr)

    @visitor(Assign)
    def visit(self, expr: Assign):
        value = self.evaluate(expr.value)

        distance: int | None = self.locals.get(expr)
        if distance != None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

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
    def visit(self, expr: Variable) -> Any:
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance: int | None = self.locals.get(expr)
        if distance != None:
            returned_var = self.environment.get_at(distance, name.lexeme)
            return returned_var
        else:
            return self.globals.get(name)

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

    @visitor(Call)
    def visit(self, expr: Call):
        callee = self.evaluate(expr.callee)

        arguments = []

        argument: Expr
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, PloxCallable):
            raise PloxRuntimeError(expr.paren,
                                   "Can only call functions and classes.")

        # NOTE: In the original Java, function is cast to the interface type (LoxCallable)
        # So... how do I do this in Python?
        # abstract classes, Multiple-Inheritance, Protocols, Informal Interfaces, or metaclasses?
        # Going with abc.ABCMeta for now, because
        # - we have to rely on some kind of runtime checks, e.g. isinstance(), as seen above
        # - I have no idea what the class hierarchy might look like, anyway
        function: PloxCallable = callee

        if len(arguments) != function.arity():
            raise PloxRuntimeError(expr.paren,
                                   f"Expected {function.arity()} arguments but got {len(arguments)}.")

        return function.call(self, arguments)

    @visitor(Lambda)
    def visit(self, expr: Lambda):
        function: PloxLambda = PloxLambda(expr, self.environment)
        return function

    # TODO: Interpret Ternary operator
    # TODO: Interpret ',' sequence operator
