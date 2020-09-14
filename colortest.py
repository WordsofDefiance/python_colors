#!/Users/accomazzod/Projects/web/python_colors/bin/python3
""" Resources
    * https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
      * Good resource on how to manipulate terminal commands with Python
    * https://askubuntu.com/questions/821157/print-a-256-color-test-pattern-in-the-terminal
      * Contains links to powerful libraries that do similar things as this, as well as ways
        to do the same thing in bash
    * https://github.com/Markus00000/colorschemer/blob/master/colorschemer.py
      * Contains good explanation on how contrast gets calculated.
    * https://jonasjacek.github.io/colors/
      * contains JSON of xterm color/name/hex/rgb/hsl
    * https://medium.muz.li/the-science-of-color-contrast-an-expert-designers-guide-33e84c41d156
      * Good article on accessibility contrast calculations
      * Might want to use this instead of color delta calculations
      * https://www.w3.org/TR/WCAG20/#relativeluminancedef
        * How WCAG defines contrast

    TO DO:
    Convert to using WCAG contrast definitions instead of delta calcs
"""

# Python colors
import sys
import argparse
import time
import json

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000, delta_e_cie1994

# Dull Colors
def dullForegroundColors():
    print("Standard (Dull) Colors")
    for i in range(30, 38):
        print("\033[{}m {} \033[0m \\033[{}m".format(i, i, i))


# Bright Colors
def brightForegroundColors():
    print("Bright Colors")
    for i in range(30, 38):
        print(
            "\033[{};1m {} \033[0m \\033[{};1m".format(
                i,
                i,
                i,
            )
        )


# 256 Color range
def allForegroundColors():
    print("All 256 Color Foregrounds")
    for i in range(0, 256):
        num = str(i)
        color = f"\033[38;5;{num}m {num} \033[0m \\033[38;5;{num}m"
        sys.stdout.write(color.ljust(4))
        if i % 5 == 0 and i != 0:
            print("")


# Background Dull Colors
def dullBackgroundColors():
    print("Background Dull Colors")
    for i in range(40, 48):
        print(f"\033[{i}m {i} \033[0m \\033[{i}m")


# Background Bright Colors
def brightBackgroundColors():
    print("Background Bright Colors")
    for i in range(40, 48):
        print(f"\033[{i};1m {i} \033[0m \\033[{i};1m")


# Background 256 Colors
def allBackgroundColors():
    print("All 256 Color Backgrounds")
    for i in range(0, 256):
        num = str(i)
        color = f"\033[48;5;{num}m {num} \033[0m \\033[48;5;{num}m"
        sys.stdout.write(color.ljust(4))
        if i % 5 == 0 and i != 0:
            print("")


# Getting Crazy with it
def allForegroundAllBackground():
    for i in range(0, 256):
        time.sleep(0.01)
        for j in range(0, 256):
            time.sleep(0.001)
            foreground = str(j)
            background = str(i)
            color = f"\033[38;5;{foreground}m\033[48;5;{background}m {foreground} on {background}\033[0m "
            sys.stdout.write(color.ljust(4))
            if j % 16 == 0 and j != 0:
                print("")
    print("All 65,536 permutations printed.")


# Test out a foreground on a background
def testForegroundOnBackground(foreground, background):
    if foreground and background in range(0, 256):
        print(f"Testing {foreground} on {background}")
        print(
            f"\n\\033[38;5;{foreground}m\\033[48;5;{background}m TEXT HERE \\033[0m\n"
        )
        print(
            f"\033[38;5;{foreground}m\033[48;5;{background}m{foreground} on {background} test\033[0m"
        )
        print(
            f"\033[38;5;{foreground}m\033[48;5;{background}mThe quick brown fox jumps over the lazy dog. \033[0m"
        )
        print(
            f"\033[38;5;{foreground}m\033[48;5;{background}mABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789\033[0m"
        )
    else:
        print("Both foreground and background number must be between 0 and 255")


# Print out all 256 foreground and background
def allForegroundAndAllBackground():
    allForegroundColors()
    allBackgroundColors()


# Create a map of all ANSI colors and their conversions to different formats
def _getColorMap():
    f = open("colors.json")
    data = json.load(f)
    # Map the ANSI code to actual color dict
    colorsDict = {}
    for i in data:
        colorsDict[i["colorId"]] = i
    return colorsDict


def _getRGBDictFromANSICode(color):
    colorMap = _getColorMap()
    return {
        "r": colorMap[color]["rgb"]["r"],
        "g": colorMap[color]["rgb"]["g"],
        "b": colorMap[color]["rgb"]["b"],
    }


def getContrast(color1, color2):
    colorMap = _getColorMap()
    rgb1 = sRGBColor(
        colorMap[color1]["rgb"]["r"],
        colorMap[color1]["rgb"]["g"],
        colorMap[color1]["rgb"]["b"],
        True,
    )
    rgb2 = sRGBColor(
        colorMap[color2]["rgb"]["r"],
        colorMap[color2]["rgb"]["g"],
        colorMap[color2]["rgb"]["b"],
        True,
    )
    lab1 = convert_color(rgb1, LabColor)
    lab2 = convert_color(rgb2, LabColor)

    diff = delta_e_cie1994(lab1, lab2)
    return diff


def getAllFgBgWithDiff(delta):
    print(f"Requested Delta: {delta}")
    for i in range(0, 256):
        for j in range(0, 256):
            contrast = getContrast(i, j)
            if contrast >= delta:
                foreground = str(j)
                background = str(i)
                color = f"\033[38;5;{foreground}m\033[48;5;{background}m {foreground} on {background}\033[0m. Contrast: {round(contrast)}"
                sys.stdout.write(color.ljust(4))


def printColorsByDeltaOnBg(background, delta):
    print(
        f"Printing all foreground colors that are delta {delta} on background {background}"
    )
    for i in range(0, 256):
        contrast = getContrast(i, background)
        if contrast >= delta:
            foreground = str(i)
            _background = str(background)
            color = f"\033[38;5;{foreground}m\033[48;5;{_background}m {foreground} on {_background}\033[0m. Delta: {round(contrast)} "
            sys.stdout.write(color.ljust(4))


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", dest="command")

dullForegroundColorsParser = subparsers.add_parser(
    "dullFg", help="display the 8 dull foreground colors"
)
brightForegroundColorsParser = subparsers.add_parser(
    "brightFg", help="display the 8 bright foreground colors"
)
dullBackgroundColorsParser = subparsers.add_parser(
    "dullBg", help="display the 8 dull background colors"
)
backgroundBrightColorsParser = subparsers.add_parser(
    "brightBg", help="display the 8 bright background colors"
)
allForegroundColorsParser = subparsers.add_parser(
    "allFg", help="display 256 foreground colors"
)
allBackgroundColorsParser = subparsers.add_parser(
    "allBg", help="display 256 background colors"
)
allForegroundAllBackgroundParser = subparsers.add_parser(
    "allFgBg", help="display all 256 foreground and background colors separately"
)
allForegroundAllBackgroundParser = subparsers.add_parser(
    "getFreaky", help="Display every combination of foreground and background color"
)
testForegroundOnBackgroundParser = subparsers.add_parser(
    "test", help="Enter a foreground code and a background code and test it out"
)
testForegroundOnBackgroundParser.add_argument(
    "FOREGROUND", type=int, help="foreground, must be between 0 and 256"
)
testForegroundOnBackgroundParser.add_argument(
    "BACKGROUND", type=int, help="background, must be between 0 and 256"
)

getContrastParser = subparsers.add_parser(
    "contrast", help="Print out a color test and get the contrast values"
)
getContrastParser.add_argument("COLOR1", type=int, help="Must be between 0 and 256")
getContrastParser.add_argument("COLOR2", type=int, help="Must be between 0 and 256")

printContrastParser = subparsers.add_parser(
    "filterContrast", help="Print out all the combos that meet a given delta."
)
printContrastParser.add_argument("DELTA", type=int, help="Pick a color delta")

printColorsByDeltaParser = subparsers.add_parser(
    "printGoodContrasts",
    help="Print out all the combos on a certain bg of a specified delta.",
)
printColorsByDeltaParser.add_argument(
    "BACKGROUND", type=int, help="background, must be between 0 and 255"
)
printColorsByDeltaParser.add_argument(
    "DELTA", type=int, help="Delta, the specified difference level between colors"
)


args = parser.parse_args()

if args.command == "dullFg":
    dullForegroundColors()
elif args.command == "brightFg":
    brightForegroundColors()
elif args.command == "dullBg":
    dullBackgroundColors()
elif args.command == "brightBg":
    brightBackgroundColors()
elif args.command == "allFg":
    allForegroundColors()
elif args.command == "allBg":
    allBackgroundColors()
elif args.command == "allFgBg":
    allForegroundAndAllBackground()
elif args.command == "getFreaky":
    allForegroundAllBackground()
elif args.command == "test":
    testForegroundOnBackground(args.FOREGROUND, args.BACKGROUND)
elif args.command == "contrast":
    print(_getRGBDictFromANSICode(args.COLOR1))
    print(_getRGBDictFromANSICode(args.COLOR2))
    print(f"Difference between two colors is: {getContrast(args.COLOR1, args.COLOR2)}")
    testForegroundOnBackground(args.COLOR1, args.COLOR2)
elif args.command == "filterContrast":
    getAllFgBgWithDiff(args.DELTA)
elif args.command == "printGoodContrasts":
    printColorsByDeltaOnBg(args.BACKGROUND, args.DELTA)
else:
    parser.print_help()
