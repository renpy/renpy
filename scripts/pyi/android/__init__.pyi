from typing import Any

import android.apk

expansion = android.apk.APK

def init(): ...

activity : Any

def vibrate(s) -> None:...

def get_dpi() -> int: ... 

def open_url(url : str) -> None: ...

def wakelock(active : bool) -> None: ...
