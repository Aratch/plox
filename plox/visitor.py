#!/usr/bin/env python3

# This is lifted entirely from https://tavianator.com/2014/python_visitor.html
# found via https://stackoverflow.com/a/28398903
# Also:
#   - https://refactoring.guru/design-patterns/visitor
#   - https://refactoring.guru/design-patterns/visitor/python/example
#   - https://abhinnpandey.medium.com/understanding-the-visitor-pattern-in-python-a-practical-example-a911f17f0776

# A couple helper functions first

def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__

def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]

# Stores the actual visitor methods
_methods = {}

# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)

# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator
