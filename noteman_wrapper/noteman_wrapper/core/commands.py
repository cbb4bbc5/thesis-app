class NotemanActions:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.api_resource_paths = {
            'tag': 'tags',
            'note': 'notes',
            'notetag': 'notetags',
        }

    def get_action(self, args):
        params = None
        if args.name:
            params = {
                'name': args.name,
            }
        try:
            response = self.wrapper.get_resource(
                self.api_resource_paths[args.resource],
                id=args.id, params=params
            )
            response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            if args.all or params:
                for r in response.json():
                    for k, v in r.items():
                        print(k, v)
            else:
                for k, v in response.json().items():
                    print(k, v)

    def mock_add_tag(self, args):
        passed = {arg for arg in vars(args) if getattr(args, arg) is not None}
        allowed = set(['resource', 'name', 'func'])
        additional = passed.difference(allowed)

        if bool(additional):
            print(f'{", ".join(additional)} not allowed for tags')
            print(f'{args.description}')
            return

        try:
            data = {'name': args.name}
            response = self.wrapper.send_resource(
                self.api_resource_paths[args.resource], data
            )
            response.raise_for_status()
        except Exception as exc:
            print(exc)
        else:
            print(f'adding tag with name {args.name}')

    def mock_add_notetag(self, args):
        if not (args.note or args.tag):
            print('those are required')
            return

        try:
            response_note = self.wrapper.get_resource(
                'notes', params={'name': args.note}
            )
            response_note.raise_for_status()
        except Exception as exc:
            print(exc)
            return

        try:
            response_tag = self.wrapper.get_resource(
                'tags', params={'name': args.tag}
            )
            response_tag.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            note_id = response_note.json()[0].get('id')
            tag_id = response_tag.json()[0].get('id')
        except IndexError as ie:
            print('Resource not found by name')
        else:
            data = {
                'note': note_id,
                'tag': tag_id,
            }
            try:
                response = self.wrapper.send_resource(
                    'notetags', data
                )
                response.raise_for_status()
            except Exception as exc:
                print(exc)

    def mock_add_connection(self, args):
        try:
            response_note = self.wrapper.get_resource(
                'notes', params={'name': args.destination}
            )
            response_source = self.wrapper.get_resource(
                'notes', params={'name': args.source}
            )
            response_note.raise_for_status()
            response_source.raise_for_status()
        except Exception as exc:
            print('Resource not found')
        try:
            note_id = response_note.json()[0].get('id')
            source_id = response_source.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            comment = args.comment if args.comment else ''
            data = {
                'note': note_id,
                'source': source_id,
                'comment': comment,
            }
            try:
                response = self.wrapper.send_resource(
                    'connections', data
                )
            except Exception as exc:
                print(exc)

    def mock_add_note(self, args):
        passed = [arg for arg in vars(args) if getattr(args, arg) is not None]
        if not args.name:
            print('name is required')
            return
        data = {}
        va = vars(args)
        for k, v in va.items():
            if v is not None:
                data[k] = v
        data.pop('func')
        data.pop('resource')
        data.pop('tags', None)
        data.pop('connections', None)
        try:
            response = self.wrapper.send_resource(
                self.api_resource_paths[args.resource], data
            )
            response.raise_for_status()
        except Exception as e:
            print(e)
            print(data)
        else:
            new_args = args
            if args.tags:
                tags = args.tags
                for tag in tags:
                    new_args.tag = tag
                    new_args.note = args.name
                    self.mock_add_notetag(new_args)
            if args.connections:
                new_args = args
                connections = args.connections
                for connection in connections:
                    new_args.source = connection
                    new_args.destination = args.name
                    self.mock_add_connection(args)

    def mock_delete_connection(self, args):
        try:
            response_note = self.wrapper.get_resource(
                'notes', params={'name': args.destination}
            )
            response_source = self.wrapper.get_resource(
                'notes', params={'name': args.source}
            )
            response_note.raise_for_status()
            response_source.raise_for_status()
        except Exception as exc:
            print('Resource not found')
        try:
            note_id = response_note.json()[0].get('id')
            source_id = response_source.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        try:
            response_connection = self.wrapper.get_resource(
                'connections', params={'note': note_id, 'source': source_id})
            response_connection.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            connection_id = response_connection.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            try:
                response = self.wrapper.delete_resource(
                    'connections', connection_id,
                )
                response.raise_for_status()
            except Exception as exc:
                print(exc)

    def mock_delete_by_name(self, args):
        resource = args.resource
        try:
            response = self.wrapper.get_resource(
                self.api_resource_paths[resource],
                params={'name': args.name}
            )
            response.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            resource_id = response.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            try:
                delete_response = self.wrapper.delete_resource(
                    self.api_resource_paths[resource],
                    resource_id
                )
                delete_response.raise_for_status()
            except Exception as exc:
                print(exc)

    def mock_delete_notetag(self, args):
        try:
            response_note = self.wrapper.get_resource(
                'notes', params={'name': args.note}
            )
            response_note.raise_for_status()
            response_tag = self.wrapper.get_resource(
                'tags', params={'name': args.tag}
            )
            response_tag.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            note_id = response_note.json()[0].get('id')
            tag_id = response_tag.json()[0].get('id')
        except IndexError as ie:
            print('Resource not found by name')
        try:
            response_notetag = self.wrapper.get_resource(
                'notetags', params={'note': note_id, 'tag': tag_id}
            )
            response_notetag.raise_for_status()
        except Exception as exc:
            print(f'Note {args.note} does not have tag named {args.tag}')
        try:
            resource_id = response_notetag.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            try:
                response = self.wrapper.delete_resource(
                    'notetags', resource_id
                )
                response.raise_for_status()
            except Exception as exc:
                print(exc)

    def mock_edit_connection(self, args):
        try:
            response_note = self.wrapper.get_resource(
                'notes', params={'name': args.destination}
            )
            response_source = self.wrapper.get_resource(
                'notes', params={'name': args.source}
            )
            response_note.raise_for_status()
            response_source.raise_for_status()
        except Exception as exc:
            print('Resource not found')
        try:
            note_id = response_note.json()[0].get('id')
            source_id = response_source.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        try:
            response_connection = self.wrapper.get_resource(
                'connections', params={'note': note_id, 'source': source_id})
            response_connection.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            connection_id = response_connection.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            data = {
                'note': note_id,
                'source': source_id,
                'comment': args.comment if args.comment else ''
            }
            try:
                response = self.wrapper.update_whole_resource(
                    'connections', id=connection_id, data=data
                )
            except Exception as exc:
                print(exc)

    def mock_edit_by_name(self, args):
        resource = args.resource
        try:
            response = self.wrapper.get_resource(
                self.api_resource_paths[resource],
                params={'name': args.name}
            )
            response.raise_for_status()
        except Exception as exc:
            print(exc)
            return
        try:
            resource_id = response.json()[0].get('id')
        except IndexError as ie:
            print('Empty response')
        else:
            if args.resource == 'tag':
                data = {
                    'name': args.new_name
                }
            # this is the branch for note resource because only it can be passed here
            else:
                response_json = response.json()[0]
                data = {
                    'name': args.new_name if args.new_name else args.name,
                    'cr_time': args.cr_time if args.cr_time else response_json.get('cr_time'),
                    'type': args.type if args.type else response_json.get('type'),
                    'description': args.description if args.description else response_json.get('description')
                }
            try:
                update_response = self.wrapper.update_resource(
                    self.api_resource_paths[resource],
                    id=resource_id,
                    data=data
                )
                update_response.raise_for_status()
            except Exception as exc:
                print(exc)
