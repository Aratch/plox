#!/usr/bin/env python3
import sys
from enum import Enum
from .error import error
from .visitor import visitor
from .token import Token
from .expr import *
from .stmt import *

class FunctionType(Enum):
    NONE = 1
    FUNCTION = 2
    LAMBDA = 3

class Resolver:
    def __init__(self, interpreter : 'Interpreter'):
        self.interpreter : 'Interpreter' = interpreter
        self.scopes : list[dict[str, bool]] = []
        self.current_function : FunctionType = FunctionType.NONE

        self.usage : list[dict[str, bool]] = [dict()]

    def begin_scope(self):
        self.scopes.append(dict())
        self.usage.append(dict())

    def end_scope(self):
        self.scopes.pop()
        self.check_usages()

    def check_usages(self):
        usage_scope = self.usage.pop()
        for name, used in usage_scope.items():
            if not used:
                print(f"{name} is not used anywhere.")

    def resolve(self, statements: list[Stmt]):
        for statement in statements:
            self.visit(statement)

        if len(self.usage) == 1:
            self.check_usages()

    def record_usage(self, name: Token):
        for i in range(len(self.usage) -1, -1, -1):
            if name.lexeme in self.usage[i]:
                self.usage[i][name.lexeme] = True

    def declare(self, name: Token):
        usage_scope = self.usage[-1]
        usage_scope[name.lexeme] = False

        # More explicit than 'not self.scopes'
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            error(name,
                  "Already a variable with this name in this scope.")

        scope[name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return # XXX: DID I FORGET THIS??

    # HACK: Using the visitor decorator has come to bite me in the arse, it seems
    #
    @visitor(Block)
    def visit(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    @visitor(Class)
    def visit(self, stmt: Class):
        self.declare(stmt.name)
        self.define(stmt.name)

    @visitor(Var)
    def visit(self, stmt: Var):
        self.declare(stmt.name)

        if stmt.initializer:
            # IMPLEMENT: self.resolve(stmt.initializer)?
            self.visit(stmt.initializer)

        self.define(stmt.name)

    @visitor(Variable)
    def visit(self, expr: Variable):
        self.record_usage(expr.name)
        if len(self.scopes) > 0 and \
        self.scopes[-1].get(expr.name.lexeme) == False:
            error(expr.name,
                  "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)

    @visitor(Assign)
    def visit(self, expr: Assign):
        self.visit(expr.value)
        self.resolve_local(expr, expr.name)

    @visitor(Function)
    def visit(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def resolve_function(self,
                         function: Function | Lambda,
                         type: FunctionType):
        self.begin_scope()

        enclosing_function = self.current_function
        self.current_function = type

        param: Token
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    ## Remaining, "uninteresting" ast nodes

    @visitor(Expression)
    def visit(self, stmt: Expression):
        self.visit(stmt.expression)

    @visitor(If)
    def visit(self, stmt: If):
        self.visit(stmt.condition)
        self.visit(stmt.then_branch)

        if stmt.else_branch:
            self.visit(stmt.else_branch)

    @visitor(Print)
    def visit(self, stmt: Print):
        self.visit(stmt.expression)

    @visitor(Return)
    def visit(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            error(stmt.keyword,
                  "Can't return from top-level code.")
        if stmt.value:
            self.visit(stmt.value)

    @visitor(While)
    def visit(self, stmt: While):
        # DONE: Check if in case of for-loop,
        # initializer (which is the first statement in stmt.body)
        # should somehow be visited first
        # because this might be why for loops are broken
        # NOTE: This is a non-issue because the parser already wraps the entire
        # for statement in a block as (Initializer, While)
        self.visit(stmt.condition)
        self.visit(stmt.body)

    @visitor(Break)
    def visit(self, stmt: Break):
        return

    ## Expressions
    ##
    @visitor(Binary)
    def visit(self, expr: Binary):
        self.visit(expr.left)
        self.visit(expr.right)

    @visitor(Call)
    def visit(self, expr: Call):
        self.visit(expr.callee)

        argument: Expr
        for argument in expr.arguments:
            self.visit(argument)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        self.visit(expr.expression)

    @visitor(Literal)
    def visit(self, expr: Literal):
        return

    @visitor(Logical)
    def visit(self, expr: Logical):
        self.visit(expr.left)
        self.visit(expr.right)

    @visitor(Unary)
    def visit(self, expr: Unary):
        self.visit(expr.right)

    @visitor(Lambda)
    def visit(self, expr: Lambda):
        self.resolve_function(expr,
                              FunctionType.LAMBDA)

    # def resolve_lambda(self, function: Lambda):
    #     self.begin_scope()

    #     param: Token
    #     for param in function.params:
    #         self.declare(param)
    #         self.define(param)

    #     self.resolve(function.body)
    #     self.end_scope()
