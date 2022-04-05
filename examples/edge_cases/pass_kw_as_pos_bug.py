from ast import arg
import argbind

@argbind.bind()
def main(
    x: int = 5,
    y: int = 3,
):
    print(x, y)

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        main()
        main(3)
        main(3, 5)
        main(2, y=3)