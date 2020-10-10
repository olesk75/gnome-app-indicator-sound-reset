#!/usr/bin/python3
# Simple program that puts a small icon in the appindicator bar for Gnome (top right default),
# which allows the user to manually reset the sound. This fixes (at least in my case), the 
# problem with HDMI sound not coming back after monitor sleep.

import os
import signal
import subprocess

from time import sleep
from urllib.request import Request, urlopen
import gi

gi.require_versions(
    {
        'Gtk': '3.0',
        'Wnck': '3.0',
        'Gst': '1.0',
        'Notify': '0.7',
        'AppIndicator3': '0.1',
    }
)
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'sound-wakeup'


def build_menu():
    menu = gtk.Menu()

    item_myapp = gtk.MenuItem(label='Reset sound')
    item_myapp.connect('activate', myapp)
    menu.append(item_myapp)

    item_quit1 = gtk.MenuItem(label='Quit')
    item_quit1.connect('activate', quit1)
    menu.append(item_quit1)

    menu.show_all()
    return menu


def sound_reset():
    while True:
        try:
            subprocess.run(["/usr/bin/pulseaudio", "--kill"], check=True, timeout=3)
            sleep(1)
            subprocess.run(["/usr/bin/pulseaudio", "--start"], check=True, timeout=10)
            sleep(1)
            subprocess.run(["/usr/bin/amixer set", "'Master'",  "100%",  "unmute"], check=False)
        except:
            pass
        else:
            break

# We do a double try here, as exerience shows it sometimes failes on the first try, but never on the second
def myapp(_):
    sound_reset()
    subprocess.run(["/usr/bin/paplay", "/usr/share/sounds/gnome/default/alerts/sonar.ogg"], check=True)
    return myapp


def quit1(_):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, os.path.abspath('sample_icon.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()
