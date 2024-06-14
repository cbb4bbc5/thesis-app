import requests


class NotemanWrapper:
    def __init__(self, base_url=None, token=None):
        self._noteman_port = 35329
        # trailing slash is important
        self.base_url = base_url if base_url else f'http://localhost:{self._noteman_port}/api/'
        self.session = self._create_session(token)


    def _create_session(self, token):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}' if token else None
        })
        return session


    def _get(self, endpoint, params=None):
        url = f'{self.base_url}{endpoint}'
        response = self.session.get(url, params=params)
        return response


    def _post(self, endpoint, data):
        url = f'{self.base_url}{endpoint}'
        response = self.session.post(url, json=data)
        return response


    def _put(self, endpoint, data):
        url = f'{self.base_url}{endpoint}'
        response = self.session.put(url, json=data)
        return response


    def _patch(self, endpoint, data):
        url = f'{self.base_url}{endpoint}'
        response = self.session.patch(url, json=data)
        return response


    def _delete(self, endpoint):
        url = f'{self.base_url}{endpoint}'
        response = self.session.delete(url)
        return response


    def get_resource(self, resource, **kwargs):
        """
        Returns a single resource by id or all of them if id is None
        """
        resource_id = kwargs.get('id')
        params = kwargs.get('params')
        endpoint = f'{resource}/{resource_id}/' if resource_id else f'{resource}/'
        return self._get(endpoint, params)


    def send_resource(self, resource, data):
        endpoint = f'{resource}/'
        return self._post(endpoint, data)


    def delete_resource(self, resource, resource_id):
        endpoint = f'{resource}/{resource_id}/'
        return self._delete(endpoint)


    def update_whole_resource(self, resource, **kwargs):
        resource_id = kwargs.get('id')
        endpoint = f'{resource}/{resource_id}/'
        data = kwargs.get('data')
        return self._put(endpoint, data)


    def update_resource(self, resource, **kwargs):
        resource_id = kwargs.get('id')
        endpoint = f'{resource}/{resource_id}/'
        data = kwargs.get('data')
        return self._patch(endpoint, data)
