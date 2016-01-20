#! /usr/bin/env python

"""Addon for HexChat automatically changing your nickname when you are AFK."""

# Copyright (C) 2015, 2016 Karol Babioch <karol@babioch.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import hexchat


__module_name__ = 'AutoAFK'
__module_version__ = '1.0'
__module_author__ = 'Karol Babioch <karol@babioch.de>'
__module_description__ = 'Automatically change your nickname whenever you leave your computer.' 


# Flag that indicates whether user was already marked as away or not
marked_away = False

def get_networks():
    """Returns an unique list of networks currently connected to"""

    # Initialize networks
    networks = []

    # Get list of channels currently joined
    channels = hexchat.get_list("channels")

    # Iterate over all channels, get unique networks
    for channel in channels:

        # Check if network is unique
        if channel.network not in networks:
        
            networks.append(channel.network)

    return networks


def check_active(userdata):
    """Checks whether the screensaver is active and invokes a name change. It
    uses the D-Bus interface provided by GNOME to detect whether the
    screensaver is currently active."""

    global marked_away

    # Query D-Bus interface provided by GNOME
    bus = dbus.SessionBus()
    screensaver = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
    iface = dbus.Interface(screensaver, 'org.gnome.ScreenSaver')
    
    # Check whether screensaver is active and user has not been handled yet
    if iface.GetActiveTime() != 0 and not marked_away:
    
        # Iterate over all networks
        for network in get_networks():
    
            context = hexchat.find_context(server=network)
            context.command('NICK kbabioch|AFK')
            #context.command('AWAY I\'m currently away from my keyboard.')
    
            # Mark user as away
            marked_away = True

    elif iface.GetActiveTime() == 0 and marked_away:

        # Iterate over all networks    
        for network in get_networks():
    
            context = hexchat.find_context(server=network)
            context.command('NICK kbabioch')
            #context.command('BACK')
    
            # Mark user as back
            marked_away = False

    # Return 1 to keep timer in hexchat scheduler
    return 1


# Register hooks
hexchat.hook_timer(1000, check_active)

# Print message once everything is setup and loaded
print('{0} module version {1} by {2} loaded.'.format(__module_name__, __module_version__, __module_author__))

