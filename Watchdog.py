import datetime as dt

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import streamlit as st


class Watchdog(FileSystemEventHandler):
    def __init__(self, hook):
        self.hook = hook

    def on_modified(self, event):
        self.hook()


def update_dummy_module():
    # Rewrite the dummy.py module. Because this script imports dummy,
    # modifiying dummy.py will cause Streamlit to rerun this script.
    dummy_path = reload_test.dummy.__file__
    with open(dummy_path, "w") as fp:
        fp.write(f'timestamp = "{dt.datetime.now()}"')


@st.cache
def install_monitor():
    # Because we use st.cache, this code will be executed only once,
    # so we won't get a new Watchdog thread each time the script runs.
    observer = Observer()
    observer.schedule(
        Watchdog(update_dummy_module),
        path="reload_test/data",
        recursive=False)
    observer.start()


install_monitor()
st.write("data file updated!", dt.datetime.now())