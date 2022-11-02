import random
import string

import requests


def create_new_gist(pat: str, text: str):
    """Create a new private gist and return its ID and filename, and a log string."""
    filename = ''.join(random.choices(
        string.ascii_lowercase + string.digits,
        k=random.randint(12, 20)
    ))
    response = requests.post(
        url = 'https://api.github.com/gists',
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'token ' + pat
        },
        json = {
            'description': '',
            'public': False,
            'files': {
                filename: {
                    'content': text
                }
            }
        }
    )
    new_gist_id = response.json().get('id')
    logstr = (
        f'Created gist (ID={new_gist_id}, filename={filename}). API response '
        f'(after {response.elapsed}): {response.status_code} {response.reason}'
    )
    return new_gist_id, filename, logstr
