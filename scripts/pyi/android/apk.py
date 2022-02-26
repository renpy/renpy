from typing import BinaryIO
import zipfile
import io

class SubFile(object):

    def __init__(self, name : str , base : int, length : int): ...

    def open(self) -> None : ...

    def __enter__(self): ...

    def __exit__(self, _type, value, tb) -> bool: ...

    def read(self, length : int = None) -> bytes: ...

    def readline(self, length : int = None) -> bytes: ...

    def readlines(self, length : int = None) -> list[bytes]: ...


    def xreadlines(self):
        return self

    def __iter__(self):
        return self

    def next(self):
        rv = self.readline()

        if not rv:
            raise StopIteration()

        return rv

    def flush(self):
        return

    def seek(self, offset : int, whence : int=0) -> int : ...

    def tell(self) -> int: ...

    def close(self) -> None: ...


class APK(object):

    def __init__(self, apk : str|None=None, prefix : str="assets/"): ...

    def list(self) -> list[zipfile.ZipInfo]: ...

    def open(self, fn) -> io.BytesIO: ...
