# CS50 Library for Python

[![Build Status](https://travis-ci.org/cs50/python-cs50.svg?branch=master)](https://travis-ci.org/cs50/python-cs50)

Supports Python 2 and Python 3.

## Installation

```
pip install cs50
```

## Usage

    import cs50

    ...

    c = cs50.get_char();
    f = cs50.get_float();
    i = cs50.get_int();
    l = cs50.get_long(); # Python 2 only
    s = cs50.get_string();

## TODO
* Conditionally install for Python 2 and/or Python 3.
* Add targets for `pacman`, `rpm`.
* Add tests.
