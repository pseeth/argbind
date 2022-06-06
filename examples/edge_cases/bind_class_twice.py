from ast import arg
import argbind

class Bound:
    def __init__(self, x: float = 1.0):
        self.x = x

for _ in range(2):
    argbind.bind(Bound)

args = {"args.debug": True, "Bound.x": 1.0}
with argbind.scope(args):
    Bound()