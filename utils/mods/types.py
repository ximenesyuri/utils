from typed import Len, Regex, Str

Char     = Len(Str, 1)
Email    = Regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

Char.__display__  = "Char"
Email.__display__ = "Email"
