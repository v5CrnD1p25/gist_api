import json
import os
from pathlib import Path

import requests

from gist_api.errors import MissingGistDetails, EmptyGistIdentifierError
from gist_api.environment_variable_names import ENVVAR_NAMES


class Gist():
    """Main class for reading and writing gists."""

    def __init__(self, identifier: str, credsfile: 'str|Path' = None):
        if not identifier:
            raise EmptyGistIdentifierError()
        self.identifier = identifier

        if credsfile is None:
            # set attributes from environment variables
            self.id_ = os.getenv(ENVVAR_NAMES['id'].format(self.identifier))
            self.pat = os.getenv(ENVVAR_NAMES['pat'].format(self.identifier))
            self.filename = os.getenv(ENVVAR_NAMES['filename'].format(self.identifier))
        else:
            credsfile = Path(credsfile).resolve()
            if credsfile.exists():
                # set attributes from credentials json file
                try:
                    with credsfile.open(encoding='utf-8') as f:
                        credsfile_data: dict = json.load(f).get(self.identifier, {})
                except json.decoder.JSONDecodeError:
                    pass
                self.id_ = credsfile_data.get('gist_id')
                self.pat = credsfile_data.get('gist_pat')
                self.filename = credsfile_data.get('gist_filename')

        self.url = 'https://api.github.com/gists/' + self.id_
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'token ' + self.pat
        }


    def _can_write(self):
        if not self.pat:
            raise MissingGistDetails(self.identifier, 'pat')
        if not self.filename:
            raise MissingGistDetails(self.identifier, 'filename')


    def write(self, text: str):
        """Update the contents of the gist to `text` and return a logstring."""
        self._can_write()
        response = requests.patch(
            url = self.url,
            headers = self.headers,
            data = json.dumps({
                'files': {
                    self.filename: {
                        'content': text
                    }
                }
            })
        )
        return (
            f'Wrote to gist "{self.identifier}". API response (after '
            f'{response.elapsed}): {response.status_code} {response.reason}'
        )


    def _can_read(self):
        if not self.filename:
            raise MissingGistDetails(self.identifier, 'filename')


    def read(self):
        """Return the contents of the gist."""
        self._can_read()
        response = requests.get(url=self.url, headers=self.headers)
        gist_data: dict = response.json().get('files', {}).get(self.filename)
        if gist_data['truncated']:
            # gist file content is too large, getting raw file
            return requests.get(
                url = gist_data.get('raw_url'),
                headers = self.headers
            ).text
        return gist_data.get('content')

