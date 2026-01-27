from utils.mods.general import Message

class Exception(BaseException):
    def __init__(self, message="", **kwargs):
        if message or kwargs:
            formatted_message = Message(message=message, **kwargs)
            super().__init__(formatted_message)
        else:
            super().__init__()

class AlreadySet(Exception): pass
class AlreadyExists(Exception): pass
class AlreadyRegistered(Exception): pass
class AlreadyDefined(Exception): pass
class AlreadyConnected(Exception): pass

class NotSet(Exception): pass
class NotExists(Exception): pass
class NotRegistered(Exception): pass
class NotDefined(Exception): pass
class NotConnected(Exception): pass

class NotMatch(Exception): pass
class NotFound(Exception): pass

