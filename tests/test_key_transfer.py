from tests.fixtures import pytest

from gi.repository import GLib

import Keyserver as keyserver
# import Sections

@pytest.fixture
def running_keyserver(request, key):
    import dbus
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    k = keyserver.ServeKeyThread(key.hash())
    k.start()
    request.addfinalizer(lambda: k.shutdown())
    return k

# FU Sections.py
# def test_server_and_verification_key_the_same(running_keyserver, key):
#     host = 'localhost'
#     port = running_keyserver.port
#     served_key = Sections.GetKeySection.download_key_http(host, port)
#     verificated_key = Sections.GetKeySection.verify_fingerprint(key.hash())
#     assert served_key == verificated_key
