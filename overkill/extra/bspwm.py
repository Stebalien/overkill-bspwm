##
#    This file is part of Overkill-bspwm.
#
#    Overkill-bspwm is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Overkill-bspwm is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Overkill-bspwm.  If not, see <http://www.gnu.org/licenses/>.
##

from overkill.sinks import PipeSink, Sink
from overkill.sources import Source
from collections import namedtuple
import subprocess

Desktop = namedtuple('Desktop', ['name', 'index', 'focused', 'occupied'])
Monitor = namedtuple('Monitor', ['name', 'index', 'focused'])

class BSPWMSource(Source, PipeSink):
    publishes = ["monitors", "desktops"]
    cmd = ['bspc', 'subscribe']
    restart = True

    def is_publishing(self, sub):
        try:
            return (sub[0] if isinstance(sub, tuple) else sub) in self.publishes
        except:
            return False

    def handle_input(self, line):
        data = {"monitors": [], "desktops": []}
        if line[0] != 'W':
            return
        desktop_index = 0
        monitor_index = 0
        for field in line[1:].split(':'):
            if not field:
                continue
            key = field[0]
            value = field[1:]
            if key.lower() == "m":
                monitor_index += 1
                current_monitor_desktops = data[("desktops", value)] = []
                data["monitors"].append(Monitor(value, monitor_index, key.isupper()))
            elif key.lower() in ('f', 'o'):
                desktop_index += 1
                desk = Desktop(
                    value,
                    desktop_index,
                    key.isupper(),
                    key.lower() == 'o'
                )
                current_monitor_desktops.append(desk)
                data["desktops"].append(desk)
        # Only update changed.
        for key in tuple(data.keys()):
            if key in self.published_data and self.published_data[key] == data[key]:
                del data[key]
        self.push_updates(data)

class BSPWMSink(Sink):
    def on_start(self):
        self.subscribe_to("wm.desktop.focus")
        self.subscribe_to("wm.desktop.layout")

    def handle_updates(self, updates, source):
        if "wm.desktop.focus" in updates:
            subprocess.Popen(["bspc", "desktop", "-f", "^%s" % updates["wm.desktop.focus"]])
        if "wm.desktop.layout" in updates:
            subprocess.Popen(["bspc", "desktop", "-l", updates["wm.desktop.layout"]])

    def handle_unsubscribe(self, subscription, source):
        pass
