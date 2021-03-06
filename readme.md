# Mine Sweeper

[![Build Status](https://travis-ci.org/christianreimer/sweeper.svg?branch=master)](https://travis-ci.org/christianreimer/sweeper) [![Coverage Status](https://coveralls.io/repos/github/christianreimer/sweeper/badge.svg?branch=master)](https://coveralls.io/github/christianreimer/sweeper?branch=master) ![Python Version 3.6](https://img.shields.io/badge/python-3.6-blue.svg) ![Python Version 3.7](https://img.shields.io/badge/python-3.7-blue.svg)

A simple terminal version of the Mine Sweeper game.

![Short Game](https://raw.githubusercontent.com/christianreimer/sweeper/artifacts/game.gif)

The loop above shows a short example game, illustrating the interface, how to select a square, a handy cheat, and what happens when you step on a bomb. You will have to actually play to find out what happens when you clear the board and thus win ...

```
$ ./sweeper.py --help

A simple terminal version of Mine Sweeper.

Usage: sweeper.py [--size=<s>] [--bombs=<b>]

Options:
  --size=<s>   Size of the board [default: 8]
  --bombs=<b>  Number of bombs on board [default: 12]
  --help       This message
```


