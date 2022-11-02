from gist_api.environment_variable_names import ENVVAR_NAMES


class EmptyGistIdentifierError(Exception):
    """Raised when instantiating a `Gist` object with a blank identifier."""

    def __init__(self):
        super().__init__('Gist identifier must not be empty!')


class MissingGistDetails(RuntimeError):
    """Raised when attempting to read/write but some info is missing."""

    def __init__(self, gist_identifier: str, details_type: str):
        self.gist_identifier = gist_identifier
        self.details_type = details_type
        self.details_type_str = {
            'pat': 'PAT',
            'filename': 'file name'
        }.get(details_type, '<unknown>')

    def __str__(self):
        envvar = ENVVAR_NAMES.get(self.details_type)
        if envvar is None:
            envvar = '?'
        else:
            envvar = envvar.format(self.gist_identifier)
        return (
            f'Could not determine a {self.details_type_str} for the gist '
            f'"{self.gist_identifier}"! Make sure to specify it in the '
            f'environment variable "{envvar} or in the credentials file.'
        )
