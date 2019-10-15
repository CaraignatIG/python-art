# This module appends color code instructions to strings so that the terminal displays colored text
# References:
# Activating VT100 on Windows 10 https://stackoverflow.com/questions/51091680/activating-vt100-via-os-system
# Color codes: 
# - https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
# - https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python

import platform
import os

class ANSIColor:
    """Holds the ANSI escaped color code sequences"""
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'

class ColorTerm(ANSIColor):
    """Holds the color code instructions to be applied to any string that will be printed
    to the stdout. The following colors are implemented:
    BLUE
    GREEN
    RED
    MAGENTA
    Methods Implemented:
    colorful_ascii_chars(str) -> str
    Takes a string parameter and adds color codes based on ascii character selection
    Static Methods Implemented:
    colorful_string(str, ANSIColor) -> str
    Takes a string as the first paramenter and adds the color specified by the second parameter
    """
    def __init__(self):
        # Checks if OS is Windows to activate VT100
        # NOTE: this only works for Windows 10, prior Windows versions don't support ANSI escape sequences
        if platform.system() == 'Windows':
            os.system('')
        self.enabled = False
        self.color_stats = ""

    def enable(self):
        """Enable color functionality"""
        self.enabled = True

    def disable(self):
        """Disable color functionality"""
        self.enabled = False

    def ascii_color_chars(self, text: str) -> str:
        """Add color codes based on some ascii character selection
        Characters used are: 3, &, =, +, *
        By defaul this is disable, make sure to call enable() before usage
        """
        if self.enabled:
            colored_text = ''
            colors_used = {
                self.BLUE : 0
                , self.RED : 0
                , self.GREEN : 0
                , self.MAGENTA : 0
                , self.CYAN : 0
                , self.RESET : 0
            }

            for char in text:
                if char == '3':
                    colored_text += self.BLUE + char + self.RESET
                    colors_used[self.BLUE] += 1
                elif char == '&':
                    colored_text += self.RED + char + self.RESET
                    colors_used[self.RED] += 1
                elif char == '=':
                    colored_text += self.GREEN + char + self.RESET
                    colors_used[self.GREEN] += 1
                elif char == '+' or char == '*':
                    colored_text += self.MAGENTA + char + self.RESET
                    colors_used[self.MAGENTA] += 1
                elif char == '#' or char == '?':
                    colored_text += self.CYAN + char + self.RESET
                    colors_used[self.CYAN] += 1
                else:
                    colored_text += char
                    if char != " ":
                        colors_used[self.RESET] += 1

            self.build_color_stats(colors_used)
            return colored_text
        else:
            return text

    @staticmethod
    def colored_string(text: str, color: ANSIColor) -> str:
        """Adds ANSI color codes to the string
        colorful_string(string, ANSIColor) -> str
        Example:
        colorful_string('Hello', ANSIColor.RED) -> '\033[31mHello\033[0m'
        """
        return color + text + ANSIColor.RESET

    def build_color_stats(self, colors_used: dict):
        """Builds a string representing the distribution of colors used in
        the colored ascii image.
        :param colors_used: dictionary - key: ANSIColor, value: total number
                                              of chars with that color.
        """
        total = sum(colors_used.values())
        self.color_stats = "\n\n-------------------\nColor distribution in ASCII image:\n"

        for color in colors_used:
            self.color_stats += self.colored_string("\n"+'█'*(int(colors_used[color]/total*50)), color)

    def warning(self, text: str) -> str:
        """Returns the passed string text with the ANSI color
        coded equivalent of YELLOW
        """
        return self.YELLOW + text + self.RESET
    
    def error(self, text: str) -> str:
        """Returns the passed string text with the ANSI color
        coded equivalent of RED
        """
        return self.RED + text + self.RESET

    def info(self, text: str) -> str:
        """Returns the passed string text with the ANSI color
        coded equivalent of CYAN
        """
        return self.CYAN + text + self.RESET

    def success(self, text: str) -> str:
        """Returns the passed string text with the ANSI color
        coded equivalent of GREEN
        """
        return self.GREEN + text + self.RESET
