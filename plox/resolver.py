#!/usr/bin/env python3

from .error import error
from .visitor import visitor
from .token import Token
from .expr import *
from .stmt import *

class Resolver:
    def __init__(self, interpreter : 'Interpreter'):
        self.interpreter : 'Interpreter' = interpreter
        self.scopes : list[dict[str, bool]] = []

    def begin_scope(self):
        self.scopes.append(dict())

    def end_scope(self):
        self.scopes.pop()

    def resolve(self, statements: list[Stmt]):
        for statement in statements:
            self.visit(statement)

    def declare(self, name: Token):
        # More explicit than 'not self.scopes'
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                # TODO: Interpreter.resolve()
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)

    # HACK: Using the visitor decorator has come to bite me in the arse, it seems
    #
    @visitor(Block)
    def visit(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    @visitor(Var)
    def visit(self, stmt: Var):
        self.declare(stmt.name)

        if stmt.initializer:
            # IMPLEMENT: self.resolve(stmt.initializer)?
            self.visit(stmt.initializer)

        self.define(stmt.name)

    @visitor(Variable)
    def visit(self, expr: Variable):
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

        self.resolve_function(stmt)

    def resolve_function(self, function: Function):
        self.begin_scope()

        param: Token
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()

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
        if stmt.value:
            self.visit(stmt.value)

    @visitor(While)
    def visit(self, stmt: While):
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
        self.resolve_function(expr)

    def resolve_lambda(self, function: Lambda):
        self.begin_scope()

        param: Token
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()
