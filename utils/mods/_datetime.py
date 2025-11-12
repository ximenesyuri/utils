import time
from datetime import datetime as _datetime

class date:
    def now(format="%d/%m/%Y"):
        return datetime.now().strftime(format)

    class time:
        def now():
            return int(time.time())

