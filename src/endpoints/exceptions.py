class URLNotSupported(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Unsupported URL format"

    def __str__(self):
        return f"Error: {self.message}"
