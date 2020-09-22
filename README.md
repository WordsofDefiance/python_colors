# Python Colors

A script that prints ANSI color combos to the terminal.

```
usage: colortest.py [-h]
                    {dullFg,brightFg,dullBg,brightBg,allFg,allBg,allFgBg,getFreaky,test,contrast,filterContrast,printGoodContrasts}
                    ...

optional arguments:
  -h, --help            show this help message and exit

commands:
  {dullFg,brightFg,dullBg,brightBg,allFg,allBg,allFgBg,getFreaky,test,contrast,filterContrast,printGoodContrasts}
    dullFg              display the 8 dull foreground colors
    brightFg            display the 8 bright foreground colors
    dullBg              display the 8 dull background colors
    brightBg            display the 8 bright background colors
    allFg               display 256 foreground colors
    allBg               display 256 background colors
    allFgBg             display all 256 foreground and background colors separately
    getFreaky           Display every combination of foreground and background color
    test                Enter a foreground code and a background code and test it out
    contrast            Print out a color test and get the contrast values
    filterContrast      Print out all the combos that meet a given delta.
    printGoodContrasts  Print out all the combos on a certain bg of a specified delta.
```
