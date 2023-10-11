import argparse


def check_nabeatsu(value):
    if int(value) % 3 == 0 or "3" in str(value):
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "value",
        help="Check value"
    )
    args = parser.parse_args()

    print(args.value, check_nabeatsu(args.value))


if __name__ == "__main__":
    main()
