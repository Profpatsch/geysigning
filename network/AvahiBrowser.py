#!/usr/bin/env python

import logging

import avahi, dbus
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import Gio
from gi.repository import GObject


__all__ = ["AvahiBrowser"]


class AvahiBrowser(GObject.GObject):
    __gsignals__ = {
        'new_service': (GObject.SIGNAL_RUN_LAST, None,
            # name, address (could be an int too (for IPv4)), port
            (str, str, int))
    }


    def __init__(self, loop=None, service='_geysign._tcp'):
        GObject.GObject.__init__(self)
        
        self.log = logging.getLogger()

        self.service = service
        # It seems that these are different loops..?!
        self.loop = loop or DBusGMainLoop()
        self.bus = dbus.SystemBus(mainloop=self.loop)

        self.log.info("Acquiring server")
        if not self.bus.name_has_owner('org.freedesktop.Avahi'):
            self.log.error("Avahi service does not seem to be running, "\
                           "org.freedesktop.Avahi is not owned on the bus")
            self.server = None
        else:
            self.server = dbus.Interface( self.bus.get_object(avahi.DBUS_NAME, '/'),
                    'org.freedesktop.Avahi.Server',
                    )
        
            self.sbrowser = dbus.Interface(self.bus.get_object(avahi.DBUS_NAME,
                self.server.ServiceBrowserNew(avahi.IF_UNSPEC,
                    avahi.PROTO_UNSPEC, self.service, 'local', dbus.UInt32(0))),
                avahi.DBUS_INTERFACE_SERVICE_BROWSER)

            self.sbrowser.connect_to_signal("ItemNew", self.on_new_item)

    def on_new_item(self, interface, protocol, name, stype, domain, flags):
        print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

        if flags & avahi.LOOKUP_RESULT_LOCAL:
            # FIXME skip local services
            pass

        self.server.ResolveService(interface, protocol, name, stype,
            domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
            reply_handler=self.on_service_resolved,
            error_handler=self.on_error)

    def on_service_resolved(self, *args):
        '''called when the browser successfully found a service'''
        name = args[2]
        address = args[7]
        port = args[8]
        print 'service resolved'
        print 'name:', name
        print 'address:', address
        print 'port:', port
        retval = self.emit('new_service', name, address, port)
        print "emitted", retval

    def on_error(self, *args):
        print 'error_handler'
        print args[0]

def main():
    loop = GObject.MainLoop()
    # We're not passing the loop to DBus, because... well, it
    # does't work... It seems to expect a DBusMainLoop, not
    # an ordinary main loop...
    ab = AvahiBrowser()

    def print_signal(*args):
        print "Signal ahoi", args

    ab.connect('new_service', print_signal)
    loop.run()


if __name__ == "__main__":
    main()