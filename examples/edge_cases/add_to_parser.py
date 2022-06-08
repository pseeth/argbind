import argbind

@argbind.bind(without_prefix=True)
def func(pos, x: int = 5):
    print(f"pos={pos}")
    print(f"x={x}")

if __name__ == "__main__":
    parser = argbind.build_parser()
    parser.add_argument("pos", nargs="+")

    args = argbind.parse_args(parser)
    with argbind.scope(args):
        func(args["pos"])
