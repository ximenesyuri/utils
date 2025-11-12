from typed import typed, Str, Maybe, DatetimeFormat, DateFormat, TimeFormat, TimeZone
from datetime import datetime as _datetime
from zoneinfo import ZoneInfo
from utils.err import DatetimeErr

class datetime:
    @typed
    def now(tz: Maybe(TimeZone)=None, format: Maybe(DatetimeFormat)=None) -> Str:
        try:
            if tz:
                if format:
                    return _datetime.now(ZoneInfo(tz)).strftime(format)
                return _datetime.now(ZoneInfo(tz)).isoformat()
            if format:
                return _datetime.now().strftime(format)
            return _datetime.now().isoformat()
        except Exception as e:
            raise DatetimeErr(e)

    class date:
        @typed
        def now(tz: Maybe(TimeZone)=None, format: DateFormat='%Y-%m-%d') -> Str:
            try:
                if tz:
                    if format:
                        return _datetime.now(ZoneInfo(tz)).strftime(format)
                    return _datetime.now(ZoneInfo(tz)).isoformat()
                if format:
                    return _datetime.now().strftime(format)
                return _datetime.now().isoformat()
            except Exception as e:
                raise DatetimeErr(e)

    class time:
        @typed
        def now(tz: Maybe(TimeZone)=None, format: TimeFormat='%H:%m:%s') -> Str:
            try:
                if tz:
                    if format:
                        return _datetime.now(ZoneInfo(tz)).strftime(format)
                    return _datetime.now(ZoneInfo(tz)).isoformat()
                if format:
                    return _datetime.now().strftime(format)
                return _datetime.now().isoformat()
            except Exception as e:
                raise DatetimeErr(e)
