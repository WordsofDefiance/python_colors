def colorPrinter(foreground, background):
    return f"\033[38;5;{foreground}m\033[48;5;{background}m"

def endColorPrinter():
    return "\033[0m"

"""
Usage: 

print(f"{colorPrinter(129, 16)}Some random text????{endColorPrinter()}")
"""
