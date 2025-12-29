from typed import Len, Regex, Str, Union
from utils.mods.path import Path

Char    = Len(Str, 1)
Email   = Regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PathUrl = Union(Path, Url("http", "https"))

Char.__display__  = "Char"
Email.__display__ = "Email"
PathUrl.__display__ = "PathUrl"

PathUrl.__null__ = ""
