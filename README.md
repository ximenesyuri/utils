# About

`utils` is a collection of random Python functions and minor wrappers.

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

