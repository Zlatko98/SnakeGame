from pathlib import Path
from threading import Timer, Thread, Event

from PyQt5.QtWidgets import QPushButton


class PerpetualTimer:

    def __init__(self, interval, f, *args, **kwargs):
        self.interval = interval
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.is_alive = False
        self.timer = None

    def callback(self):
        self.f(*self.args, **self.kwargs)
        self.start()

    def cancel(self):
        self.timer.cancel()
        self.is_alive = False
    def start(self):
        self.timer = Timer(self.interval, self.callback)
        self.timer.start()
        self.is_alive = True


def load_res(name: str) -> str:
    mod_path = Path(__file__).parent
    path = str(mod_path.parent) + '\\res\\' + name
    return path


def load_style_res(name: str) -> str:
    mod_path = Path(__file__).parent
    path = str(mod_path.parent) + '\\res\\' + name
    return path.replace('\\', '/')


def init_button(name: str):
    btn = QPushButton(name)
    btn.setMinimumHeight(50)
    btn.setMaximumWidth(200)

    return btn
