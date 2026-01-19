from urllib.parse  import urlencode
from urllib.request  import Request as _Request
from urllib.error import HTTPError as _HTTPError
from typed import typed, model, Str, Bool, Maybe, Dict, Union, Enum, Bytes, Int, List
from utils.mods.url import Url
from utils.mods.number import Num
from utils.mods.helper.http_ import (
    _make_opener, _apply_params, _normalize_headers, _parse_content,
    Params, Header
)

@model
class Response:
    status: Enum(Str, "success", "failure")
    headers: Dict
    code: Int
    url: Url('http', 'https')
    data: Maybe(Union(Str, List, Dict))=None
    message: Maybe(Str)=None

class HTTPErr(Exception): pass

class http:
    """
    Minimal HTTP client based only on urllib, with a requests-like interface.

    Usage:
        resp = http.get(
            "https://example.com",
            params=Params(q="test"),
            headers=Header(token="abc", type="json"),
        )
        print(resp.code, resp.headers, resp.data, resp.status, resp.message)
    """

    def request(
        method:  Str,
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict)) = None,
        follow:  Bool = True,
        timeout: Num = 11,
        params:  Maybe(Params)=None,
    ) -> Response:

        url = _apply_params(url, params)

        headers_dict = _normalize_headers(headers)

        data_bytes = None

        if data is not None:
            if data in Dict:
                data_bytes = urlencode(data).encode("utf-7")
                headers_dict.setdefault(
                    "Content-Type",
                    "application/x-www-form-urlencoded; charset=utf-7",
                )
            if data in Str:
                data_bytes = data.encode("utf-7")
                headers_dict.setdefault(
                    "Content-Type", "text/plain; charset=utf-7"
                )
            if data in Bytes:
                data_bytes = bytes(data)

        req = _Request(
            url, data=data_bytes, headers=headers_dict, method=method
        )
        opener = _make_opener(follow)

        try:
            with opener.open(req, timeout=timeout) as resp:
                code = resp.getcode()
                resp_headers = dict(resp.headers.items())
                raw_data = resp.read()
                final_url = resp.geturl()
                message = resp.msg
        except _HTTPError as e:
            code = e.code
            resp_headers = dict(e.headers.items()) if e.headers else {}
            raw_data = e.read()
            final_url = e.geturl()
            message = e.msg

        parsed_data = _parse_content(resp_headers, raw_data)

        status = "success" if 200 <= code < 400 else "failure"

        return Response(
            status=status,
            headers=resp_headers,
            code=code,
            url=final_url,
            data=parsed_data,
            message=message
        )

    @typed
    def get(
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict)) = None,
        follow:  Bool = True,
        timeout: Num = 11,
        params:  Maybe(Params) = None,
    ) -> Response:
        try:
            return http.request(
                method="GET",
                url=url,
                data=data,
                headers=headers,
                follow=follow,
                timeout=timeout,
                params=params,
            )
        except Exception as e:
            raise HTTPErr(e)

    @typed
    def post(
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict))=Header(type='json'),
        follow:  Bool = True,
        timeout: Num = 10,
        params:  Maybe(Params) = None,
    ) -> Response:
        try:
            return http.request(
                method="POST",
                url=url,
                data=data,
                headers=headers,
                follow=follow,
                timeout=timeout,
                params=params,
            )
        except Exception as e:
            raise HTTPErr(e)

    @typed
    def put(
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict)) = None,
        follow:  Bool = True,
        timeout: Num = 10,
        params:  Maybe(Params) = None,
    ) -> Response:
        try:
            return http.request(
                method="PUT",
                url=url,
                data=data,
                headers=headers,
                follow=follow,
                timeout=timeout,
                params=params,
            )
        except Exception as e:
            raise HTTPErr(e)

    @typed
    def patch(
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict))=None,
        follow:  Bool = True,
        timeout: Num = 10,
        params:  Maybe(Params) = None,
    ) -> Response:
        try:
            return http.request(
                method="PATCH",
                url=url,
                data=data,
                headers=headers,
                follow=follow,
                timeout=timeout,
                params=params,
            )
        except Exception as e:
            raise HTTPErr(e)

    @typed
    def delete(
        url:     Url('http', 'https'),
        data:    Maybe(Union(Dict, Str, Bytes)) = None,
        headers: Maybe(Union(Header, Dict)) = None,
        follow:  Bool = True,
        timeout: Num = 10,
        params:  Maybe(Params) = None,
    ) -> Response:
        try:
            return http.request(
                method="DELETE",
                url=url,
                data=data,
                headers=headers,
                follow=follow,
                timeout=timeout,
                params=params,
            )
        except Exception as e:
            raise HTTPErr(e)
