from overkill.sinks import PipeSink
from overkill.sources import Source
import os
from collections import namedtuple

Desktop = namedtuple('Desktop', ['name', 'focused', 'occupied'])
Monitor = namedtuple('Monitor', ['name', 'focused'])

class BSPWMSource(Source, PipeSink):
    publishes = ["monitors", "desktops"]
    cmd = ['bspc', 'control', '--subscribe']

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

