from utils.mods.general import Message

class Exception(BaseException):
    def __init__(self, message="", **kwargs):
        if message or kwargs:
            formatted_message = Message(message=message, **kwargs)
            super().__init__(formatted_message)
        else:
            super().__init__()

class AlreadyExists(Exception): pass
class NotExists(Exception): pass
class AlreadySet(Exception): pass
class NotMatch(Exception): pass
class NotSet(Exception): pass
