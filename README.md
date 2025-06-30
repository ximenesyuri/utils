```ruby
             /00     /00 /00
            | 00    |__/| 00
 /00   /00 /000000   /00| 00  /0000000
| 00  | 00|_  00_/  | 00| 00 /00_____/
| 00  | 00  | 00    | 00| 00|  000000
| 00  | 00  | 00 /00| 00| 00 \____  00
|  000000/  |  0000/| 00| 00 /0000000/
 \______/    \___/  |__/|__/|_______/ 
```

# About

`utils` is a collection of Python helper typed functions.

# Overview

1. The functions provided by `utils` are typed in the sense [pythonalta/typed](https://github.com/pythonalta/typed). This means that they are type-checked at runtime, providing type safety. 
2. Even as possible, `utils` provide solutions to minor external libraries. For example, for management of `envs` we have our own functions, which works as a replacement for `pythondotenv`.
3. We try to avoid dependencies at most. However, if a dependency is needed, it is automatically installed at runtime if needed.

# Install

With `pip`:

```bash
pip install git+https://github.com/pythonalta/utils  
```

With [py](https://github.com/ximenesyuri/py):

```bash
py i pythonalta/utils  
```

# Dependences

The only global dependency is [typed](https://github.com/pythonalta/typed).

# Structure

```
utils/
  |-- __init__.py  ..... importing everthing in main.py
  |-- main.py .......... importing the utility classes
  |-- err.py ........... with error classes
  └-- mods/ ............ with files defining utility classes
```

# Mods, Classes and Errors

To each `mod` file in `mods/` there corresponds a namesake class. The class, in turn, provide the utility functions for the underlying context. To each `mod` in `mods/` there also corresponds an `error` class, as below, which is an extension of the base class `Exception`.

```
mod         class     meaning             error 
-----------------------------------------------------
str.py      str       string utilities    StrErr
json_.py    json      json utilities      JsonErr
path.py     path      path utilities      PathErr
file.py     file      file utilities      FileErr
lib.py      lib       libs utilities      LibErr
date.py     date      date utilities      DateErr
color.py    color     color utilities     ColorErr
img.py      img       image utilities     ImgErr
md.py       md        markdown utilities  MDErr
...         ...       ...                 ...
```

# Utilities

A `utility` is a function in a `mod` file satisfying the following conditions: 
1. it is `typed` in the sense of [typed](https://pythonalta/typed)
2. all types used in the function type hints are constructed in the `typed` library
3. it has a global `try/except` block that raises the corresponding `error` class of the `mod`.

This means that the general form of a `utility` is as follows:

```python
from typed import typed, SomeType, OtherType, ReturnType, ...
from utils.err import SomeModErr

class some_mod:
    ...
    @typed
    def some_utility(x: SomeType, y: OtherType, ...) -> ReturType:
        try:
            ...
        except Exception as e:
            raise SomeModErr
```
