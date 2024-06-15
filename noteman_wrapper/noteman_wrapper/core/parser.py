import argparse

from noteman_wrapper.core.commands import NotemanActions
from noteman_wrapper.core.wrapper import NotemanWrapper


class NotemanParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Noteman parser')
        self.actions = NotemanActions(NotemanWrapper())
        self.subparsers = self.parser.add_subparsers()
        self._initialize_parsers()

    def _initialize_parsers(self):
        self._initialize_list_parser()
        self._initialize_create_parser()
        self._initialize_delete_parser()
        self._initialize_edit_parser()

    def _initialize_list_parser(self):
        self.list_parser = self.subparsers.add_parser('list')
        self.list_parser.add_argument('resource', choices=['note', 'tag'])
        self.list_group = self.list_parser.add_mutually_exclusive_group()
        self.list_group.add_argument('--id', dest='id')
        self.list_group.add_argument('--name', dest='name')
        self.list_group.add_argument('--all', action='store_true')
        self.list_group.set_defaults(func=self.actions.get_action)

    def _initialize_create_parser(self):
        self.create_parser = self.subparsers.add_parser('add')
        self.create_parser.add_argument(
            'resource', choices=['note', 'tag', 'connection', 'notetag']
        )
        self.create_parser.set_defaults(func=self._handle_add_command)

        self.create_connection_parser = self.create_parser.add_argument_group('connection')
        self.create_connection_parser.add_argument('--from', dest='source')
        self.create_connection_parser.add_argument('--to', dest='destination')
        self.create_connection_parser.add_argument('--comment', dest='comment')

        self.create_tag_parser = self.create_parser.add_argument_group('tag')
        self.create_tag_parser.add_argument('--name', dest='name')

        self.create_note_parser = self.create_parser.add_argument_group('note')
        self.create_note_parser.add_argument('--creation-time', dest='cr_time')
        self.create_note_parser.add_argument('--type', dest='type')
        self.create_note_parser.add_argument('--description', dest='description')
        self.create_note_parser.add_argument('--tags', type=str, nargs='*')
        self.create_note_parser.add_argument('--connections', type=str, nargs='*')

        self.create_notetag_parser = self.create_parser.add_argument_group('notetag')
        self.create_notetag_parser.add_argument('--note', dest='note')
        self.create_notetag_parser.add_argument('--tag', dest='tag')

    def _initialize_delete_parser(self):
        self.delete_parser = self.subparsers.add_parser('remove')
        self.delete_parser.add_argument(
            'resource', choices=['note', 'tag', 'notetag', 'connection']
        )
        self.delete_parser.set_defaults(func=self._handle_delete_command)

        self.delete_connection_parser = self.delete_parser.add_argument_group('connection')
        self.delete_connection_parser.add_argument('--from', dest='source')
        self.delete_connection_parser.add_argument('--to', dest='destination')

        self.delete_notetag_parser = self.delete_parser.add_argument_group('notetag')
        self.delete_notetag_parser.add_argument('--note', dest='note')
        self.delete_notetag_parser.add_argument('--tag', dest='tag')

        # also used for deleting notes
        self.delete_tag_parser = self.delete_parser.add_argument_group('tag')
        self.delete_tag_parser.add_argument('--name', dest='name')

    def _initialize_edit_parser(self):
        self.edit_parser = self.subparsers.add_parser('edit')
        # there is no reason to modify notetag
        self.edit_parser.add_argument(
            'resource', choices=['note', 'tag', 'connection']
        )
        self.edit_parser.set_defaults(func=self._handle_edit_command)

        self.edit_connection_parser = self.edit_parser.add_argument_group('connection')
        self.edit_connection_parser.add_argument('--from', dest='source')
        self.edit_connection_parser.add_argument('--to', dest='destination')
        self.edit_connection_parser.add_argument('--comment', dest='comment')

        # also used for updating notes
        self.edit_tag_parser = self.edit_parser.add_argument_group('note_tag')
        self.edit_tag_parser.add_argument('--name', dest='name')
        self.edit_tag_parser.add_argument('--new-name', dest='new_name')

        self.edit_note_parser = self.edit_parser.add_argument_group('note')
        self.edit_note_parser.add_argument('--creation-time', dest='cr_time')
        self.edit_note_parser.add_argument('--type', dest='type')
        self.edit_note_parser.add_argument('--description', dest='description')

    def _handle_add_command(self, args):
        if args.resource in ['note', 'tag']:
            if args.source or args.destination:
                self.parser.error("--from and --to are not allowed for 'note' or 'tag'")
                return
            if args.resource == 'tag':
                self.actions.mock_add_tag(args)
            elif args.resource == 'note':
                self.actions.mock_add_note(args)
        elif args.resource == 'connection':
            if args.source and args.destination and not args.name:
                self.actions.mock_add_connection(args)
            else:
                self.parser.error("'connection' requires --from and --to options or two positional arguments")
        elif args.resource == 'notetag':
            self.actions.mock_add_notetag(args)

    def _handle_delete_command(self, args):
        if args.resource == 'connection':
            if args.source and args.destination:
                self.actions.mock_delete_connection(args)
            else:
                self.parser.error('--from and --to options are required')
        elif args.resource in ['tag', 'note']:
            if args.name:
                self.actions.mock_delete_by_name(args)
            else:
                self.parser.error('Name is required')
        elif args.resource == 'notetag':
            if args.tag and args.note:
                self.actions.mock_delete_notetag(args)
            else:
                self.parser.error('Note and tag are required')

    def _handle_edit_command(self, args):
        if args.resource == 'connection':
            if args.destination and args.source:
                self.actions.mock_edit_connection(args)
            else:
                self.parser.error('All arguments are required for editing connection')
        elif args.resource in ['tag', 'note']:
            if args.name:
                self.actions.mock_edit_by_name(args)
            else:
                self.parser.error('Name must be specified')
