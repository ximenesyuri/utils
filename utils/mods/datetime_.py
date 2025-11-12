import time
from datetime import datetime as _datetime

class datetime:
    class date:
        def now(format="%d/%m/%Y"):
            return _datetime.now().strftime(format)

    class time:
        def now():
            return int(time.time())

