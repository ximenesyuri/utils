from typed import *
import unicodedata

class str:
    @typed
    def join(iterator: Union(List(Str), Tuple(Str), Set(Str))=[], separator: Str='') -> Str:
        return separator.join(iterator)    

    @typed
    def slugify(string: Str="") -> Str:
        if not string:
            raise ValueError("Cannot create slug: no string provided")
        string_normalized = unicodedata.normalize('NFKD', string)
        string_ascii = string_normalized.encode('ascii', 'ignore').decode('ascii')
        slug = string_ascii.replace(' ', '-').lower()
        clean_slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return clean_slug
