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

# Structure

```
utils/
  |-- __init__.py  ..... importing everthing in main.py
  |-- main.py .......... importing the utility classes
  `-- mods/ ............ with files defining utility classes
```

# Mods and Classes

To each `mod` file there corresponds a namesake class. The class, in turn, provide the utility functions for the underlying context.

```
mod            class        meaning
-------------------------------------------
text.py        text         text utilities
json_.py       json         json utilities
path.py        path         path utilities
date.py        date         date utilities
color.py       color        color utilities
image.py       image        image utilities
markdown.py    markdown     markdown utilities
...
```

