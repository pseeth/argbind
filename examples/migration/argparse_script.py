import argparse

def main(
    arg1, arg2='arg2', arg3=1.0
):
    print(arg1, arg2, arg3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "arg1", type=int, help="The first argument (positional)",
    )
    parser.add_argument(
        "--arg2", type=str, help="The second argument (keyword)",
        default='arg2'
    )
    parser.add_argument(
        "--arg3", type=float, help="The third argument (keyword)",
        default=1.0
    )

    args = vars(parser.parse_args())
    main(args['arg1'], arg2=args['arg2'], arg3=['arg3'])