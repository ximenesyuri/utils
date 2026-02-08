from typed import typed, Str
from utils.mods.general import message as _message

class Exception(BaseException):
    def __init__(self, message="", **kwargs):
        if message or kwargs:
            formatted_message = _message(message=message, **kwargs)
            super().__init__(formatted_message)
        else:
            super().__init__()

@typed
def newerr(err: Str) -> type:
    return type(err, (Exception,), {"__name__": err, "__display__": err})

AlreadySet = newerr('AlreadySet')
AlreadyExists = newerr('AlreadyExists')
AlreadyRegistered = newerr('AlreadyRegistered')
AlreadyDefined = newerr('AlreadyDefined')
AlreadyConnected = newerr('AlreadyConnected')

NotSet = newerr('NotSet')
NotExists = newerr('NotExists')
NotRegistered = newerr('NotRegistered')
NotDefined = newerr('NotDefined')
NotConnected = newerr('NotConnected')

NotMatch = newerr('NotDefined')
NotFound = newerr('NotConnected')
