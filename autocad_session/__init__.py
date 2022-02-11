from pyautocad import Autocad


class Channel(object):
    instance = None

    def __init__(self):
        self._session = None

    @property
    def session(self):
        if not self._session:
            try:
                self._session = session = Autocad(create_if_not_exists=False)
                session.prompt("Python trying to connect...")
                session.prompt("Python connected!")
            except OSError:
                raise Exception("Could not connect to the AUTOCAD process. Please start AUTOCAD before running the script.")


if Channel.instance is None:
    Channel.instance = Channel()

channel = Channel.instance
