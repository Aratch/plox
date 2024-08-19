#!/usr/bin/env python3

import sys
from plox.plox import Plox

def main(argv: list):
    if len(argv) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(argv) == 1:
        plox = Plox()
        plox.run_file(argv[0])
    else:
        plox = Plox()
        plox.run_prompt()

if __name__ == '__main__':
    main(sys.argv[1:])
