import os

from .exceptions import EditorMissingError


def _split_path():
    return os.getenv('PATH').split(':')


def which(binary):
    for path_dir in _split_path():
        path = os.path.join(path_dir, binary)
        if os.path.isfile(path):
            return path
    return None


def get_editor():
    editor = os.getenv('EDITOR')
    if editor:
        if which(editor):
            return which(editor)
        raise EditorMissingError(f'cant find editor {editor!r}')
    for editor in ('nano', 'vim', 'vi', 'emacs'):
        binary = which(editor)
        if binary:
            return binary
    raise EditorMissingError('cant find any editor from: nano, vim, vi, emacs')
