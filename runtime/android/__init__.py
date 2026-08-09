from jnius import autoclass

import os
import android.apk as apk

expansion = os.environ.get("ANDROID_EXPANSION", None)
assets = apk.APK(apk=expansion)


def init():
    pass


PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
activity = PythonSDLActivity.mActivity


def vibrate(s):
    """
    Vibrate for `s` seconds.
    """

    activity.vibrate(s)


def get_dpi():
    return activity.getDPI()


def open_url(url):
    activity.openUrl(url)


def wakelock(active):
    activity.setWakeLock(active)


# Web browser support.
class AndroidBrowser:
    def open(self, url, new=0, autoraise=True):
        open_url(url)

    def open_new(self, url):
        open_url(url)

    def open_new_tab(self, url):
        open_url(url)


import webbrowser

webbrowser.register("android", AndroidBrowser, None, preferred=True)
