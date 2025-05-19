class TextErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class ImageErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class ColorErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class JsonErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class MarkdownErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class DateErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class CmdErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class PathErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class CompressErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)
