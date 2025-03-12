"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
"""
from enum import UNIQUE, IntEnum, verify


@verify(UNIQUE)
class StyleOrdinal(IntEnum):
    # region Modes and Resets
    reset_all = 0

    weight_bold = 1
    weight_light = 2
    italic = 3
    underline = 4
    blinking = 5
    reverse = 7
    invisible = 8
    strikethrough = 9

    reset_weight = 22
    reset_italic = 23
    reset_underline = 24
    reset_blinking = 25
    reset_reverse = 27
    reset_invisible = 28
    reset_strikethrough = 29
    # endregion

    # region 8-16 (ISO) Colours
    black_foreground = 30
    red_foreground = 31
    green_foreground = 32
    yellow_foreground = 33
    blue_foreground = 34
    magenta_foreground = 35
    cyan_foreground = 36
    white_foreground = 37
    default_foreground = 39

    black_background = 40
    red_background = 41
    green_background = 42
    yellow_background = 43
    blue_background = 44
    magenta_background = 45
    cyan_background = 46
    white_background = 47
    default_background = 49
    # endregion

    # region Bright Colours
    bright_black_foreground = 90
    bright_red_foreground = 91
    bright_green_foreground = 92
    bright_yellow_foreground = 93
    bright_blue_foreground = 94
    bright_magenta_foreground = 95
    bright_cyan_foreground = 96
    bright_white_foreground = 97

    bright_black_background = 100
    bright_red_background = 101
    bright_green_background = 102
    bright_yellow_background = 103
    bright_blue_background = 104
    bright_magenta_background = 105
    bright_cyan_background = 106
    bright_white_background = 107
    # endregion


# region Modes and Resets
reset_all = StyleOrdinal.reset_all

weight_bold = StyleOrdinal.weight_bold
weight_light = StyleOrdinal.weight_light
italic = StyleOrdinal.italic
underline = StyleOrdinal.underline
blinking = StyleOrdinal.blinking
reverse = StyleOrdinal.reverse
invisible = StyleOrdinal.invisible
strikethrough = StyleOrdinal.strikethrough

reset_weight = StyleOrdinal.reset_weight
reset_italic = StyleOrdinal.reset_italic
reset_underline = StyleOrdinal.reset_underline
reset_blinking = StyleOrdinal.reset_blinking
reset_reverse = StyleOrdinal.reset_reverse
reset_invisible = StyleOrdinal.reset_invisible
reset_strikethrough = StyleOrdinal.reset_strikethrough
# endregion

# region 8-16 (ISO) Colours
black_foreground = StyleOrdinal.black_foreground
red_foreground = StyleOrdinal.red_foreground
green_foreground = StyleOrdinal.green_foreground
yellow_foreground = StyleOrdinal.yellow_foreground
blue_foreground = StyleOrdinal.blue_foreground
magenta_foreground = StyleOrdinal.magenta_foreground
cyan_foreground = StyleOrdinal.cyan_foreground
white_foreground = StyleOrdinal.white_foreground
default_foreground = StyleOrdinal.default_foreground

black_background = StyleOrdinal.black_background
red_background = StyleOrdinal.red_background
green_background = StyleOrdinal.green_background
yellow_background = StyleOrdinal.yellow_background
blue_background = StyleOrdinal.blue_background
magenta_background = StyleOrdinal.magenta_background
cyan_background = StyleOrdinal.cyan_background
white_background = StyleOrdinal.white_background
default_background = StyleOrdinal.default_background
# endregion

# region Bright Colours
bright_black_foreground = StyleOrdinal.bright_black_foreground
bright_red_foreground = StyleOrdinal.bright_red_foreground
bright_green_foreground = StyleOrdinal.bright_green_foreground
bright_yellow_foreground = StyleOrdinal.bright_yellow_foreground
bright_blue_foreground = StyleOrdinal.bright_blue_foreground
bright_magenta_foreground = StyleOrdinal.bright_magenta_foreground
bright_cyan_foreground = StyleOrdinal.bright_cyan_foreground
bright_white_foreground = StyleOrdinal.bright_white_foreground

bright_black_background = StyleOrdinal.bright_black_background
bright_red_background = StyleOrdinal.bright_red_background
bright_green_background = StyleOrdinal.bright_green_background
bright_yellow_background = StyleOrdinal.bright_yellow_background
bright_blue_background = StyleOrdinal.bright_blue_background
bright_magenta_background = StyleOrdinal.bright_magenta_background
bright_cyan_background = StyleOrdinal.bright_cyan_background
bright_white_background = StyleOrdinal.bright_white_background
# endregion

__all__ = (
    "StyleOrdinal",
    "reset_all",
    "weight_bold",
    "weight_light",
    "italic",
    "underline",
    "blinking",
    "reverse",
    "invisible",
    "strikethrough",
    "reset_weight",
    "reset_italic",
    "reset_underline",
    "reset_blinking",
    "reset_reverse",
    "reset_invisible",
    "reset_strikethrough",
    "black_foreground",
    "red_foreground",
    "green_foreground",
    "yellow_foreground",
    "blue_foreground",
    "magenta_foreground",
    "cyan_foreground",
    "white_foreground",
    "default_foreground",
    "black_background",
    "red_background",
    "green_background",
    "yellow_background",
    "blue_background",
    "magenta_background",
    "cyan_background",
    "white_background",
    "default_background",
    "bright_black_foreground",
    "bright_red_foreground",
    "bright_green_foreground",
    "bright_yellow_foreground",
    "bright_blue_foreground",
    "bright_magenta_foreground",
    "bright_cyan_foreground",
    "bright_white_foreground",
    "bright_black_background",
    "bright_red_background",
    "bright_green_background",
    "bright_yellow_background",
    "bright_blue_background",
    "bright_magenta_background",
    "bright_cyan_background",
    "bright_white_background",
)
