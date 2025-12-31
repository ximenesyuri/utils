import json
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Optional,
    Union,
    Sequence,
    Tuple,
    Literal,
)


class Response:
    """
    Minimal Response object similar to requests.Response.

    Attributes:
        code (int): HTTP status code.
        headers (dict): Response headers.
        url (str): Final URL (after redirects if followed).
        content: Parsed response body:
                 - dict/list if JSON
                 - str if text
                 - bytes otherwise
    """

    def __init__(self, code: int, headers: Dict[str, str], body: bytes, url: str):
        self.code = code
        self.headers = headers
        self.url = url
        self._body = body
        self._content: Any = None

    def _get_encoding(self) -> str:
        ctype = self.headers.get("Content-Type", "").lower()
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("charset="):
                return part.split("=", 1)[1].strip() or "utf-8"
        return "utf-8"

    def _parse_content(self) -> Any:
        if self._body is None:
            return None

        ctype = self.headers.get("Content-Type", "").lower()

        # Try JSON first if content-type suggests it
        if "json" in ctype:
            try:
                text = self._body.decode(self._get_encoding(), errors="strict")
                return json.loads(text)
            except Exception:
                # Fall back to text/bytes if JSON parsing fails
                pass

        if ctype.startswith("text/") or "charset=" in ctype:
            try:
                return self._body.decode(self._get_encoding(), errors="replace")
            except Exception:
                return self._body

        try:
            return self._body.decode("utf-8")
        except Exception:
            return self._body

    @property
    def content(self) -> Any:
        if self._content is None:
            self._content = self._parse_content()
        return self._content


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Disable automatic redirect following."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class Header:
    """
    High-level header model.

    Fields:
        token: optional auth token to be used as Bearer token.
        type:  how the body should be treated:
               - 'json' -> JSON content
               - 'text' -> plain text
               - 'bin'  -> binary data
        extra: additional raw headers to merge in.
    """

    token: Optional[str] = None
    type: Literal["json", "text", "bin"] = "json"
    extra: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        if self.type == "json":
            headers.setdefault(
                "Content-Type", "application/json; charset=utf-8"
            )
            headers.setdefault(
                "Accept", "application/json, text/*;q=0.8, */*;q=0.5"
            )
        elif self.type == "text":
            headers.setdefault(
                "Content-Type", "text/plain; charset=utf-8"
            )
            headers.setdefault(
                "Accept", "text/plain, text/*;q=0.9, */*;q=0.8"
            )
        elif self.type == "bin":
            headers.setdefault("Content-Type", "application/octet-stream")
            headers.setdefault("Accept", "*/*")

        if self.extra:
            headers.update(self.extra)

        return headers


class Params(dict):
    """
    Convenience class for URL parameters.

    Example:
        params = Params(some="aaa", thing="bbb")
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)


class http:
    """
    Minimal HTTP client based only on urllib, with a requests-like interface.

    Usage:
        resp = http.get(
            "https://example.com",
            params=Params(q="test"),
            headers=Header(token="abc", type="json"),
        )
        print(resp.code, resp.headers, resp.content)
    """

    @staticmethod
    def _make_opener(follow: bool) -> urllib.request.OpenerDirector:
        if follow:
            return urllib.request.build_opener()
        else:
            return urllib.request.build_opener(_NoRedirectHandler())

    @staticmethod
    def _apply_params(
        url: str,
        params: Optional[
            Union[
                Dict[str, Any],
                Sequence[Tuple[str, Any]],
                Params,
            ]
        ],
    ) -> str:
        if not params:
            return url

        new_query = urllib.parse.urlencode(params, doseq=True)

        parsed = urllib.parse.urlsplit(url)
        if parsed.query:
            merged_query = parsed.query + "&" + new_query
        else:
            merged_query = new_query

        parsed = parsed._replace(query=merged_query)
        return urllib.parse.urlunsplit(parsed)

    @staticmethod
    def _normalize_headers(
        headers: Optional[Union[Dict[str, str], Header]]
    ) -> Dict[str, str]:
        if headers is None:
            return {}
        if isinstance(headers, Header):
            return headers.to_dict()
        if isinstance(headers, dict):
            return dict(headers)
        raise TypeError(
            "headers must be dict, Header or None; got "
            f"{type(headers).__name__}"
        )

    @staticmethod
    def _request(
        method: str,
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Union[Dict[str, str], Header]] = None,
        follow: bool = True,
        timeout: Optional[float] = None,
        params: Optional[
            Union[
                Dict[str, Any],
                Sequence[Tuple[str, Any]],
                Params,
            ]
        ] = None,
    ) -> Response:
        url = http._apply_params(url, params)

        headers_dict = http._normalize_headers(headers)

        body_bytes: Optional[bytes] = None

        if data is not None:
            if isinstance(data, dict):
                # Form-encode dictionaries
                body_bytes = urllib.parse.urlencode(data).encode("utf-8")
                headers_dict.setdefault(
                    "Content-Type",
                    "application/x-www-form-urlencoded; charset=utf-8",
                )
            elif isinstance(data, str):
                body_bytes = data.encode("utf-8")
                headers_dict.setdefault(
                    "Content-Type", "text/plain; charset=utf-8"
                )
            elif isinstance(data, (bytes, bytearray)):
                body_bytes = bytes(data)
            else:
                raise TypeError(
                    "data must be dict, str, bytes or bytearray; got "
                    f"{type(data).__name__}"
                )

        req = urllib.request.Request(
            url, data=body_bytes, headers=headers_dict, method=method
        )
        opener = http._make_opener(follow)

        try:
            with opener.open(req, timeout=timeout) as resp:
                code = resp.getcode()
                resp_headers = dict(resp.headers.items())
                raw_body = resp.read()
                final_url = resp.geturl()
        except urllib.error.HTTPError as e:
            code = e.code
            resp_headers = dict(e.headers.items()) if e.headers else {}
            raw_body = e.read()
            final_url = e.geturl()

        return Response(code=code, headers=resp_headers, body=raw_body, url=final_url)

    @staticmethod
    def get(
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Union[Dict[str, str], Header]] = None,
        follow: bool = True,
        timeout: Optional[float] = None,
        params: Optional[
            Union[
                Dict[str, Any],
                Sequence[Tuple[str, Any]],
                Params,
            ]
        ] = None,
    ) -> Response:
        """
        Perform an HTTP GET request.
        """
        return http._request(
            method="GET",
            url=url,
            data=data,
            headers=headers,
            follow=follow,
            timeout=timeout,
            params=params,
        )

    @staticmethod
    def post(
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Union[Dict[str, str], Header]] = None,
        follow: bool = True,
        timeout: Optional[float] = None,
        params: Optional[
            Union[
                Dict[str, Any],
                Sequence[Tuple[str, Any]],
                Params,
            ]
        ] = None,
    ) -> Response:
        """
        Perform an HTTP POST request.
        """
        return http._request(
            method="POST",
            url=url,
            data=data,
            headers=headers,
            follow=follow,
            timeout=timeout,
            params=params,
        )


if __name__ == "__main__":
    resp1 = http.get(
        url="https://google.com/",
        headers=Header(
            token="some_token",
            type="text",
        ),
        data=None,
        follow=False,
        params=Params(
            some="aaa",
            thing="bbb",
        ),
    )

    resp2 = http.get(
        url="https://google.com/",
        headers={
            "Authorization": "Bearer some_token",
            "Content-Type": "text/plain; charset=utf-8",
            "Accept": "text/plain, text/*;q=0.9, */*;q=0.8",
        },
        data=None,
        follow=False,
        params=Params(
            some="aaa",
            thing="bbb",
        ),
    )

