#!/usr/bin/env python2

import sys

from gi.repository import Gio, Gtk, Gdk


class App(Gtk.Application):
    def __init__(self):
        self._ui = self._load_ui()
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.geysigning",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)

    @staticmethod
    def _load_ui():
        b = Gtk.Builder()
        b.add_from_file("ui.glade")
        def g(elem):
            return b.get_object(elem)
        ui = {
            'app-window': [
                'window',
                'own-key',
                'other-key',
            ],
            'key-blueprint': None
        }
        return ui

    def on_activate(self, app):
        ui = self._ui
        ui_app_window = ui['app-window']
        w = ui_app_window['window']
        app.add_window(w)

        own_key = ui_app_window['own-key']
        key = ui['key-blueprint']
        # own_key.attach(key)

        w.show()


if __name__ == '__main__':
    import signal
    import threading

    app = App()
    Gdk.threads_init()
    def sigint(sig_no, frame):
        sys.exit(0)
    def tmp():
        app.run(sys.argv)
        signal.signal(signal.SIGINT, sigint)
    threading.Thread(target=tmp)
    app.run(sys.argv)
