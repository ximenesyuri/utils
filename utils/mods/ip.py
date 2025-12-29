from typed import typed, Str, Bool, Filter
from ipaddress import IPv6Address, IPv4Address

@typed
def _is_ipv4(string: Str) -> Bool:
    try:
        IPv4Address(string)
        return True
    except:
        return False

@typed
def _is_ipv6(string: Str) -> Bool:
    try:
        IPv6Address(string)
        return True
    except:
        return False

IPv4 = Filter(Str, _is_ipv4)
IPv6 = Filter(Str, _is_ipv6)

IPv4.__display__ = "IPv4"
IPv6.__display__ = "IPv6"

IPv4.__null__ = "127.0.0.1"
