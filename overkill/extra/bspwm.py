from overkill.sinks import FifoSink
from overkill.sources import Source
import os, subprocess
from collections import namedtuple

Desktop = namedtuple('Desktop', ['name', 'focused', 'occupied'])
Monitor = namedtuple('Monitor', ['name', 'focused'])

class BSPWMSource(Source, FifoSink):
    publishes = ["monitors", "desktops"]
    fifo_path = os.path.expandvars("$XDG_RUNTIME_DIR/bspwm-panel-fifo")

    def on_start(self):
        subprocess.call(["bspc", "put_status"])

    def is_publishing(self, sub):
        try:
            return (sub[0] if isinstance(sub, tuple) else sub) in self.publishes
        except:
            return False

    def handle_input(self, line):
        data = {"monitors": [], "desktops": []}
        for field in line.split(':'):
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

