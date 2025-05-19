import time
from datetime import datetime

class date:
    def now(format="%d/%m/%Y"):
        return datetime.now().strftime(format)

    class time:
        def now():
            return int(time.time())

