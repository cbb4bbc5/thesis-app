import sys

from noteman_wrapper.core.parser import NotemanParser

# from core.exceptions import ConnectionError


def main():
    parser_helper = NotemanParser()
    try:
        args = parser_helper.parser.parse_args(sys.argv[1:])
        args.func(args)
    except AttributeError:
        print('Error processing request')


if __name__ == '__main__':
    main()
