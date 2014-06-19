from gi.repository import GLib
from gi.repository import Gtk

from AvahiBrowse import AvahiBrowser
from Sections import KeySignSection, GetKeySection

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Geysign")
        self.set_border_width(10)

        # create notebook container
        notebook = Gtk.Notebook()
        notebook.append_page(KeySignSection(), Gtk.Label('Keys'))
        notebook.append_page(GetKeySection(), Gtk.Label('Get Key'))
        self.add(notebook)

        # setup signals
        self.connect("delete-event", Gtk.main_quit)
        
        self.avahi_browser = None
        self.avahi_service_name = '_demo._tcp'
        self.discovered_services = []
        GLib.idle_add(self.setup_avahi_browser)


    def setup_avahi_browser(self):
        # FIXME: place a proper service string there
        self.avahi_browser = AvahiBrowser(service=self.avahi_service_name)
        self.avahi_browser.connect('new_service', self.on_new_service)
        
        return False


    def on_new_service(self, browser, name, address, port):
        if self.verify_service(name, address, port):
            GLib.idle_add(self.add_discovered_service, name, address, port)


    def verify_service(self, name, address, port):
        '''A tiny function to return whether the service
        is indeed something we are interested in'''
        if name == self.avahi_service_name:
            return True
        else:
            return False

    def add_discovered_service(self, name, address, port):
        self.discovered_services += (name, address, port)

        return False
