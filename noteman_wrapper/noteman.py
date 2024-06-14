import sys

from noteman_wrapper.core.parser import NotemanParser

# from core.exceptions import ConnectionError


def main():
    noteman_parser = NotemanParser()
    try:
        args = noteman_parser.parser.parse_args(sys.argv[1:])
        args.func(args)
    except AttributeError as ae:
        print('Empty argument list')

if __name__ == '__main__':
    main()
