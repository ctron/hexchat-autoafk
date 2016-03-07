#! /usr/bin/env python

"""Addon for HexChat that automatically changes your nickname when you are AFK."""

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
import re

__module_name__ = 'AutoAFK'
__module_version__ = '1.0'
__module_author__ = 'Karol Babioch <karol@babioch.de>'
__module_description__ = 'Automatically change your nickname whenever you leave your computer.' 

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


# Global flags used by poll_dbus
# TODO Replace by proper OOP design (class)
away = False

def poll_dbus(userdata):
    """Checks whether the screensaver is active and invokes a name change. It
    uses the D-Bus interface provided by GNOME to detect whether the
    screensaver is currently active."""

    # Immediately return and re-schedule if plugin is disabled
    if not hexchat.get_pluginpref('autoafk_enabled'):

        return 1

    # Flag that indicates whether user is AFK and we changed the nick
    global away

    delay = hexchat.get_pluginpref('autoafk_delay')

    try:

        # Query D-Bus interface provided by GNOME
        bus = dbus.SessionBus()
        screensaver = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        iface = dbus.Interface(screensaver, 'org.gnome.ScreenSaver')

        # Check whether screensaver is active and user has not been handled yet
        if iface.GetActiveTime() > delay and not away:

            # Iterate over all networks
            for network in get_networks():

                nick = hexchat.get_info('nick')

                context = hexchat.find_context(server=network)
                context.command('NICK {0}{1}{2}'.format(hexchat.get_pluginpref('autoafk_prefix'), nick, hexchat.get_pluginpref('autoafk_suffix')))


            # Set global flags
            away = True

        elif iface.GetActiveTime() == 0 and away:

            # Iterate over all networks
            for network in get_networks():

                nick = hexchat.get_info('nick')

                prefix = re.escape(hexchat.get_pluginpref('autoafk_prefix'))
                suffix = re.escape(hexchat.get_pluginpref('autoafk_suffix'))

                # Restore original nick using regular expressions
                nick = re.sub(r'(' + prefix + ')(?P<nick>.*)(' + suffix + ')', '\g<nick>', nick)

                context = hexchat.find_context(server=network)
                context.command('NICK {0}'.format(nick))

            # Mark user as back
            away = False

    except DBusException as e:

        print('AutoAFK: DBus exception: '.format(e))

    # Return 1 to keep timer in hexchat scheduler
    return 1

class SubcommandException(Exception):
    pass

def autoafk_help(word, word_eol, userdata):

    print('{0} module version {1} by {2}.'.format(__module_name__, __module_version__, __module_author__))
    print('')
    print('  Usage:')
    print('')
    print('    /AUTOAFK HELP                Outputs this usage help');
    print('    /AUTOAFK INFO                Outputs information about current state of addon');
    print('    /AUTOAFK ON|OFF              Turns this addon on or off (default is on)');
    print('    /AUTOAFK DELAY <seconds>     Waits given amount of seconds before considering for you to be AFK (default is 0)');
    print('    /AUTOAFK PREFIX <prefix>     Puts a prefix in front of your nick when being AFK (default is empty)');
    print('    /AUTOAFK SUFFIX <suffix>     Attaches suffix to your nick when being AFK (default is |AFK)');
    print('')

# Text decorations
TEXT_BOLD = '\002'
TEXT_COLOR = '\003'
TEXT_HIDDEN = '\010'
TEXT_UNDERLINE = '\037'
TEXT_ORIGINAL = '\017'
TEXT_REVERSE_COLOR = '\026'
TEXT_BEEP = '\007'
TEXT_ITALIC = '\035'

def autoafk_info(word, word_eol, userdata):

    enabled = hexchat.get_pluginpref('autoafk_enabled')
    delay = hexchat.get_pluginpref('autoafk_delay')
    prefix = hexchat.get_pluginpref('autoafk_prefix')
    suffix = hexchat.get_pluginpref('autoafk_suffix')

    print('')
    print('AutoAFK:')
    print('')
    # TODO Use decorate function
    print('Status:  ' + TEXT_ITALIC + TEXT_BOLD + ('enabled' if enabled else 'disabled'))
    print('Delay:   ' + TEXT_ITALIC + TEXT_BOLD + str(delay) + TEXT_ORIGINAL + ' seconds')
    print('Prefix:  ' + (TEXT_ITALIC + TEXT_BOLD + prefix if len(prefix) > 0 else TEXT_ITALIC + 'disabled'))
    print('Suffix:  ' + (TEXT_ITALIC + TEXT_BOLD + suffix if len(suffix) > 0 else TEXT_ITALIC + 'disabled'))
    print('')

def autoafk_on(word, word_eol, userdata):

    hexchat.set_pluginpref('autoafk_enabled', True) # TODO Evaluate return value
    print('AutoAFK: Addon enabled.')

def autoafk_off(word, word_eol, userdata):

    hexchat.set_pluginpref('autoafk_enabled', False) # TODO Evaluate return value
    print('AutoAFK: Addon disabled.')

def autoafk_delay(word, word_eol, userdata):

    if len(word) < 2:

        raise SubcommandException('No argument provided')

    try:

        delay = int(word[1])
        hexchat.set_pluginpref('autoafk_delay', delay) # TODO Evaluate return value
        print('AutoAFK: Delay set to ' + str(delay) + ' seconds.')

    except ValueError:

        raise SubcommandException('Invalid delay specified')

def autoafk_prefix(word, word_eol, userdata):

    if len(word) < 2:

        prefix = ''

    else:

        prefix = word[1]

    hexchat.set_pluginpref('autoafk_prefix', prefix) # TODO Evaluate return value
    print('AutoAFK: Prefix set: ' + (TEXT_ITALIC + TEXT_BOLD + prefix if len(prefix) > 0 else TEXT_ITALIC + 'disabled'))

def autoafk_suffix(word, word_eol, userdata):

    if len(word) < 2:

        suffix = ''

    else:

        suffix = word[1]

    hexchat.set_pluginpref('autoafk_suffix', suffix) # TODO Evaluate return value
    print('AutoAFK: Suffix set: ' + (TEXT_ITALIC + TEXT_BOLD + suffix if len(suffix) > 0 else TEXT_ITALIC + 'disabled'))

def autoafk(word, word_eol, userdata):

    # Dispatch table for subcommands
    subcmds = {

        'HELP': autoafk_help,

        'INFO': autoafk_info,

        'ON': autoafk_on,
        'OFF': autoafk_off,

        'DELAY': autoafk_delay,

        'PREFIX': autoafk_prefix,
        'SUFFIX': autoafk_suffix,

    }

    # Check if there is a valid subcommand
    if len(word) > 1 and word[1] in subcmds:

        # Remove first elements (since we are consuming them here)
        word.pop(0)
        word_eol.pop(0)

        try:

            # Invoke function for subcommand
            subcmds[word[0]](word, word_eol, userdata)

        except SubcommandException as e:

            print('AutoAFK: ' + e.args[0])

    else:

        print('AutoAFK: Invalid command. Consult the output of /AUTOAFK HELP for a list of available commands')

    return hexchat.EAT_ALL

# Register hooks
hexchat.hook_timer(1000, poll_dbus)
hexchat.hook_command('AUTOAFK', autoafk, help='Use /AUTOAFK HELP for a more detailed description of available commands') 

# Set default preferences if not yet set
if not hexchat.get_pluginpref('autoafk_enabled'):
    hexchat.set_pluginpref('autoafk_enabled', True) # TODO Evaluate return value

if not hexchat.get_pluginpref('autoafk_delay'):
    hexchat.set_pluginpref('autoafk_delay', 0) # TODO Evaluate return value

if not hexchat.get_pluginpref('autoafk_prefix'):
    hexchat.set_pluginpref('autoafk_prefix', '') # TODO Evaluate return value

if not hexchat.get_pluginpref('autoafk_suffix'):
    hexchat.set_pluginpref('autoafk_suffix', '|AFK') # TODO Evaluate return value

# Print message once everything is set up and loaded
print('{0} module version {1} by {2} loaded.'.format(__module_name__, __module_version__, __module_author__))

