from typed import *
import unicodedata

class str:
    @typed
    def join(iterators: List(Union(List(Str), Tuple(Str), Set(Str)))=[], separator: Str='') -> Str:
        its = []
        for iterator in iterators:
            its.append(separator.join(iterator))
        return separator.join(its)

    @typed
    def slugify(string: Str="") -> Str:
        if not string:
            raise ValueError("Cannot create slug: no string provided")
        string_normalized = unicodedata.normalize('NFKD', string)
        string_ascii = string_normalized.encode('ascii', 'ignore').decode('ascii')
        slug = string_ascii.replace(' ', '-').lower()
        clean_slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return clean_slug
