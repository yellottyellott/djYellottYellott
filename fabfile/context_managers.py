import contextlib
import os


@contextlib.contextmanager
def mktemp(path, remove=True):
    with open(path, 'w') as f:
        try:
            yield f
        finally:
            if remove:
                os.remove(path)
