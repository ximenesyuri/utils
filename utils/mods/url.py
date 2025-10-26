from typed import typed, Any, Url, Hostname, Dict, List, Str, Maybe, Protocol
from urllib.parse import urlparse, parse_qs
from utils.err import UrlErr

class url:
    @typed
    def hostname(u: Url('http', 'https', 'file', 'ssh')) -> Maybe(Hostname):
        try:
            return urlparse(u).hostname
        except Exception as e:
            raise UrlErr(e)
    domain = hostname

    @typed
    def tld(u: Url('http', 'https')) -> Maybe(Str):
        try:
            return url.hostname(u).split('.')[-1]
        except Exception as e:
            raise UrlErr(e)

    @typed
    def subdomain(u: Url('http', 'https')) -> Maybe(Str):
        try:
            parts = url.hostname(u).split('.')
            if len(parts) > 2:
                return '.'.join(parts[0: len(parts)-2])
            return None
        except Exception as e:
            raise UrlErr(e)

    @typed
    def scheme(u: Url('http', 'https')) -> Protocol:
        try:
            return urlparse(u).scheme
        except Exception as e:
            raise UrlErr(e)
    protocol = scheme

    class query:
        @typed
        def __new__(cls: Any, u: Url('http', 'https')) -> Str:
            try:
                return urlparse(u).query
            except Exception as e:
                raise UrlErr(e)

        @typed
        def params(u: Url('http', 'https')) -> Dict(Str, List(Str)):
            try:
                query = parse_qs(urlparse(u).query)
                query_dict = {}
                for key, values in query.items():
                    if len(values) == 1:
                        query_dict[key] = values[0]
                    else:
                        query_dict[key] = values

                return query_dict

            except Exception as e:
                raise UrlErr(e)

    @typed
    def netloc(u: Url('http', 'https')) -> Str:
        try:
            return urlparse(u).netloc
        except Exception as e:
            raise UrlErr(e)

    args = params
