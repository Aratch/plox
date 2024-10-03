#!/usr/bin/env python3

import unittest
import io
import contextlib

from plox.plox import Plox

from .nostderr import nostderr

class TestInterpreterFeatures(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def run_script(self, filepath: str) -> str:
        plox: Plox = Plox()

        f: io.StringIO = io.StringIO()
        with contextlib.redirect_stdout(f):
            plox.run_file(filepath)

        output = f.getvalue()
        return output

    def test_literal_prints(self):
        filepath = "tests/lox/print-statements.lox"
        output = self.run_script(filepath)

        self.assertIn("one", output)
        self.assertIn("True", output)
        self.assertIn("3", output)

    def test_print_from_for_loop(self):
        filepath = "tests/lox/for-loop.lox"
        output = self.run_script(filepath)

        expected = "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n"
        self.assertEqual(expected, output)

    def test_simple_variable(self):
        filepath = "tests/lox/var.lox"
        output = self.run_script(filepath)

        expected = "lox\n"
        self.assertEqual(expected, output)

    def test_lookup(self):
        filepath = "tests/lox/lookup.lox"
        output = self.run_script(filepath)

        expected = "True\n3\n"
        self.assertEqual(expected, output)

    def test_fibonacci_break(self):
        filepath = "tests/lox/fibonacci-break.lox"
        output = self.run_script(filepath)

        expected = "0\n1\n1\n2\n3\n5\n8\n13\n"
        self.assertEqual(expected, output)

    def test_while(self):
        filepath = "tests/lox/while.lox"
        output = self.run_script(filepath)

        expected = "1\n2\n3\n"
        self.assertEqual(expected, output)

    def test_lambda(self):
        filepath = "tests/lox/lambda.lox"
        output = self.run_script(filepath)

        expected = "1\n2\n3\n"
        self.assertEqual(expected, output)

    def test_closures(self):
        filepath = "tests/lox/closures.lox"
        output = self.run_script(filepath)

        expected = "1\n2\n"
        self.assertEqual(expected, output)

    def test_blocks_shadowing(self):
        filepath = "tests/lox/blocks-shadowing.lox"
        output = self.run_script(filepath)

        expected = """inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c\n"""
        self.assertEqual(expected, output)

    def test_warn_unused_var(self):
        filepath = "tests/lox/warn-unused-var.lox"
        output = self.run_script(filepath)

        expected="b is not used anywhere.\na is not used anywhere.\n"
        self.assertEqual(expected, output)

if __name__ == "__main__":
    unittest.main()
