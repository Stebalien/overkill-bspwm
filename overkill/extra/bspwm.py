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

from overkill.sinks import PipeSink
from overkill.sources import Source
from collections import namedtuple

Desktop = namedtuple('Desktop', ['name', 'focused', 'occupied'])
Monitor = namedtuple('Monitor', ['name', 'focused'])

class BSPWMSource(Source, PipeSink):
    publishes = ["monitors", "desktops"]
    cmd = ['bspc', 'control', '--subscribe']
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
        for field in line[1:].split(':'):
            if not field:
                continue
            key = field[0]
            value = field[1:]
            if key.lower() == "m":
                current_monitor_desktops = data[("desktops", value)] = []
                data["monitors"].append(Monitor(value, key.isupper()))
            elif key.lower() in ('f', 'o'):
                desk = Desktop(
                    value.split('/', 1)[-1],
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

