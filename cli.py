import sys
import hypha.core.builder as builder
import argparse

# Logic with system arguments

def build():
    builder.build()


def main():
    parser = argparse.ArgumentParser(
        prog="Hypha",
        description="The Javascript Framework for PHP"
    )

    parser.add_argument("cmd", type=str, help="build / dev")
    parser.add_argument("-p", "--port")

    args = parser.parse_args()

    if (args.cmd == "build"):
        build()
    elif (args.cmd == "dev"):
        # Start dev server with automatic building and reloading
        pass

if (__name__ == "__main__"):
    main()