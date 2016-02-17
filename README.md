# AutoAFK

This is a plugin for [HexChat][hexchat] that will automatically change your
nickname whenever you are away from your keyboard (AFK). Unfortunately Hexchat
itself is missing such an essential feature. The plugin is written in Python.

## FEATURES

- Automatically changes your nickname whenever you are AFK

## INSTALLATION

Clone the repository and place and link to the AutoAFK.py file within your
hexchat's addon directory:

    cd ~
    git clone gitolite:users/kbabioch/hexchat-autoafk.git
    ln -s hexchat-autoafk/AutoAFK.py .config/hexchat/addons/

Don't forget to restart HexChat.

## USAGE

Run /AUTOAFK HELP to see available commands.

## DOCUMENTATION

See the inline comments for documentation.

## CONTRIBUTIONS

In case you are looking for something to work on, you probably want to take a
look at the `TODO` file within the projects root directory.

## LICENSE

[![GNU GPLv3](http://www.gnu.org/graphics/gplv3-127x51.png "GNU GPLv3")](http://www.gnu.org/licenses/gpl.html)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

[hexchat]: https://hexchat.github.io/

