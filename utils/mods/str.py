from typed import *
import unicodedata

class str:
    @typed
    def join(iterators: List(Any)=[], separator: Str='') -> Str:
        its = []
        for iterator in iterators:
            its.append(separator.join(iterator))
        return separator.join(its)

    @typed
    def split(string: Str, separator: Str='') -> List[Str]:
        return string.split(separators)

    @typed
    def concat(*strings: Tuple(Str)) -> Str:
        return ''.join(strings)

    @typed
    def capitalize(*strings: Tuple(Str)) -> Union(Str, Tuple(Str)):
        if len(strings) == 1:
            return strings[0].capitalize()
        return (string.capitalize() for string in strings)

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
