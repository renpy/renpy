#!/usr/bin/env python3

"""
This searches Ren'Py for places where an inner function calls itself recursively.
When that happens, the function winds up as part of a reference cycle, and has to be
garbage collected manually.
"""

import ast
import pathlib

current_path : pathlib.Path = pathlib.Path()
results : set[tuple[str, str]] = set()

class FindRecursiveInnerFunction(ast.NodeVisitor):
    def __init__(self, name):
        self.name = name

    def visit_Name(self, node):
        if node.id == self.name:
            results.add((current_path, self.name))

class FindInnerFunction(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        for i in node.body:
            FindRecursiveInnerFunction(node.name).visit(i)


class FindFunctions(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        for i in node.body:
            FindInnerFunction().visit(i)

def main():
    global current_path

    root = pathlib.Path(__file__).parent.parent

    for fn in root.glob("renpy/**/*.py"):

        current_path = fn

        with open(fn) as f:
            tree = ast.parse(f.read())
            FindFunctions().visit(tree)

    for fn, name in sorted(results):
        print(f"{fn}: {name}")


if __name__ == '__main__':
    main()
