import unicodedata

class text:
    def slugify(name):
        if not name:
            raise ValueError("Cannot create slug: no name provided")
        name_normalized = unicodedata.normalize('NFKD', name)
        name_ascii = name_normalized.encode('ascii', 'ignore').decode('ascii')
        slug = name_ascii.replace(' ', '-').lower()
        clean_slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return clean_slug
