from typed import Int, Bool, Union, Float, Filter

def _is_natural(x: Int) -> Bool:
    return x >= 0

def _is_odd(x: Int) -> Bool:
  return x % 2 != 0

def _is_even(x: Int) -> Bool:
  return x % 2 == 0

def _is_positive(x: Int) -> Bool:
    return x > 0

def _is_negative(x: Int) -> Bool:
    return x < 0

Num  = Union(Int, Float)
Nat  = Filter(Int, _is_natural)
Odd  = Filter(Int, _is_odd)
Even = Filter(Int, _is_even)
Pos  = Filter(Int, _is_positive)
Neg  = Filter(Int, _is_negative)

Num.__display__  = "Num"
Nat.__display__  = "Nat"
Odd.__display__  = "Odd"
Even.__display__ = "Even"
Pos.__display__  = "Pos"
Neg.__display__  = "Neg"

Num.__null__  = 0.0
Nat.__null__  = 0
Odd.__null__  = None
Even.__null__ = 0
Pos.__null__  = None
Neg.__null__  = None
