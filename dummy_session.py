class DummySession():
    """ just an empty class to allow CodeWindow to initialise
    will eventually be replace by the Session class from BitQuest or
    something equivalent."""

    def __init__(self):
        pass

    def save_session(self, list_of_source_lines, list_of_errors):
        pass
