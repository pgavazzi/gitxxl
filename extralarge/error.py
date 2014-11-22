

class Abort(Exception):
    """Raised if a command needs to print an error and exit."""
    def __init__(self, *args, **kw):
        Exception.__init__(self, *args)
        self.hint = kw.get('hint')