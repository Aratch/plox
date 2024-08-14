#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Callable

def get_writer(f):
    def writer(line="", indent=0):
        print( (indent * 4 * " " ) + line, file=f)
    return writer

def define_type(writer: Callable, base_name: str, class_name: str, field_str: str):
    write = writer

    fields = [x.strip() for x in field_str.split(",")]

    write("@dataclass")
    write(f"class {class_name}({base_name}):")
    if len(fields) >= 1:
        for field in fields:
            field_type, field_name = field.split(" ")
            write(f"{field_name}: {field_type}", 1)
    else:
        write(f"pass", 1)
    write()

def define_ast(output_dir: Path, base_name: str, types: list[str]):
    path: Path = output_dir / (base_name.lower() + ".py")

    with path.open("w+") as f:
        write = get_writer(f)
        write("#!/usr/bin/env python3")
        write()
        write("from abc import ABC")
        write("from .token import Token")
        write("from dataclasses import dataclass")
        write()
        write(f"class {base_name}(ABC):")
        write(f"pass", 1)
        write()

        for type in types:
            class_name, fields = [s.strip() for s in type.split(":")]
            define_type(write, base_name, class_name, fields)

def main(argv: list):
    if len(argv) != 1:
        print("Usage: generate_ast.py <output_directory>")
        sys.exit(64)

    output_dir = Path(argv[0])

    if not output_dir.exists() and output_dir.is_dir():
        raise FileNotFoundError(f"Directory {argv[0]} does not exist.")

    define_ast(output_dir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : object value",
        "Unary    : Token operator, Expr right",
        "Ternary  : Token operator, Expr condition, Expr left, Expr right"
    ])

if __name__ == '__main__':
    main(sys.argv[1:])
