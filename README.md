# gist_api

Very simple library for reading and writing [Gist](https://gist.github.com/) files.

## Installation

```sh
pip install git+https://github.com/v5CrnD1p25/gist_api@main
```

## Usage

Instantiate a `Gist` object with an internal identifier string:

```python
from gist_api import Gist
gist = Gist('foobar')
text = gist.read()
gist.write(text + '\\nI was here')
```

This assumes that the following three environment variables are set:

```sh
GIST_foobar_ID=...
GIST_foobar_PAT=...
GIST_foobar_FILENAME=...
```

Alternatively, pass the path to a credentials file to the `Gist` constructor. The file should have the following structure:

```json
{
    "foobar": {
        "gist_id": "...",
        "gist_pat": "...",
        "gist_filename": "..."
    }
}
```
