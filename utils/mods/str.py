import unicodedata
import re
from typed import (
    typed,
    List,
    Any,
    Str,
    Tuple,
    Union,
    Dict,
    Pattern,
    Int,
    Bool,
    Nill
)

class str:
    @typed
    def join(iterator: List(Any)=[], separator: Str='') -> Str:
        return separator.join(iterator)

    @typed
    def split(string: Str, separator: Str='', stop_in: Int=-1) -> List(Str):
        return string.split(separator, stop_in)

    @typed
    def strip(string: Str) -> Str:
        return string.strip()

    @typed
    def concat(*strings: Tuple(Str)) -> Str:
        return ''.join(strings)

    @typed
    def begins(*strings: Tuple(Str), substring: Str) -> Bool:
        return all(string.startswith(substring) for string in strings)

    @typed
    def ends(*strings: Tuple(Str), substring: Str) -> Bool:
        return all(string.endswith(substring) for string in strings)

    @typed
    def capitalize(*strings: Tuple(Str)) -> Union(Str, Tuple(Str)):
        if len(strings) == 1:
            return strings[0].capitalize()
        return (string.capitalize() for string in strings)
    cap = capitalize

    @typed
    def lower(*strings: Tuple(Str)) -> Union(Str, Tuple(Str)):
        if len(strings) == 1:
            return strings[0].lower()
        return (string.lower() for string in strings)

    @typed
    def upper(*strings: Tuple(Str)) -> Union(Str, Tuple(Str)):
        if len(strings) == 1:
            return strings[0].upper()
        return (string.upper() for string in strings)

    @typed
    def replace(string: Str='', replacements: Dict(Str)={}) -> Str:
        for k,v in replacements.items():
            string = string.replace(k, v)
        return string

    @typed
    def subs(string: Str='', pattern: Pattern=r'', replacement: Str='' ) -> Str:
        return re.sub(pattern, replacement, string)

    @typed
    def escape(string: Str) -> Str:
        return re.escape(string)

    @typed
    def slugify(*strings: Tuple(Str)) -> Union(Tuple(Str), Str, Nill):
        if not strings:
            return None
        if len(strings) == 1:
            string_normalized = unicodedata.normalize('NFKD', strings[0])
            string_ascii = string_normalized.encode('ascii', 'ignore').decode('ascii')
            slug = string_ascii.replace(' ', '-').lower()
            clean_slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            return clean_slug
        return (str.slugify(string) for string in strings)
