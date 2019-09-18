from .exceptions import MissingPreprocessFunctionError


def _preprocess(path):
    preprocessor_globals = {}
    with open(path) as f:
        exec(f.read(), preprocessor_globals)
    if 'preprocess' not in preprocessor_globals:
        raise MissingPreprocessFunctionError(
            f'failed to find `preprocess` function in {path}'
        )
    return preprocessor_globals['preprocess']
