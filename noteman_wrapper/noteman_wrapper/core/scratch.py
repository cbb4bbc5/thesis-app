






def mock_add(args):
    if args.resource == 'note':
        mock_add_note(args)
        return
    elif args.resource == 'tag':
        mock_add_tag(args)
        return
    elif args.resource == 'connection':
        print(f'adding connection from {args.source} to {args.destination}')
        return
    print(f'adding new {args.resource}')


if __name__ == "__main__":
    nw = NotemanWrapper()
    p = NotemanParser(nw)
    args = parser.parse_args(['list', 'tag', '--id', '5'])
    args.func(args)

    # args = parser.parse_args(['list', 'tag', '--all'])
    # args.func(args)

    args = parser.parse_args(['list', 'note', '--id', '95'])
    args.func(args)

    args = parser.parse_args(['add', 'tag', '--name', '7'])
    args.func(args)

