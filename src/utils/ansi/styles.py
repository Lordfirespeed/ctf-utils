"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
"""
from . import style_ordinals as ordinals
from .escape_builder import StyleEscapeBuilder


def _b(ordinal: int) -> str:
    return StyleEscapeBuilder.quick(ordinal)


# region Modes and Resets
reset_all = _b(ordinals.reset_all)

weight_bold = _b(ordinals.weight_bold)
weight_light = _b(ordinals.weight_light)
italic = _b(ordinals.italic)
underline = _b(ordinals.underline)
blinking = _b(ordinals.blinking)
reverse = _b(ordinals.reverse)
invisible = _b(ordinals.invisible)
strikethrough = _b(ordinals.strikethrough)

reset_weight = _b(ordinals.reset_weight)
reset_italic = _b(ordinals.reset_italic)
reset_underline = _b(ordinals.reset_underline)
reset_blinking = _b(ordinals.reset_blinking)
reset_reverse = _b(ordinals.reset_reverse)
reset_invisible = _b(ordinals.reset_invisible)
reset_strikethrough = _b(ordinals.reset_strikethrough)
# endregion

# region 8-16 (ISO) Colours
black_foreground = _b(ordinals.black_foreground)
red_foreground = _b(ordinals.red_foreground)
green_foreground = _b(ordinals.green_foreground)
yellow_foreground = _b(ordinals.yellow_foreground)
blue_foreground = _b(ordinals.blue_foreground)
magenta_foreground = _b(ordinals.magenta_foreground)
cyan_foreground = _b(ordinals.cyan_foreground)
white_foreground = _b(ordinals.white_foreground)
default_foreground = _b(ordinals.default_foreground)

black_background = _b(ordinals.black_background)
red_background = _b(ordinals.red_background)
green_background = _b(ordinals.green_background)
yellow_background = _b(ordinals.yellow_background)
blue_background = _b(ordinals.blue_background)
magenta_background = _b(ordinals.magenta_background)
cyan_background = _b(ordinals.cyan_background)
white_background = _b(ordinals.white_background)
default_background = _b(ordinals.default_background)
# endregion

# region Bright Colours
bright_black_foreground = _b(ordinals.bright_black_foreground)
bright_red_foreground = _b(ordinals.bright_red_foreground)
bright_green_foreground = _b(ordinals.bright_green_foreground)
bright_yellow_foreground = _b(ordinals.bright_yellow_foreground)
bright_blue_foreground = _b(ordinals.bright_blue_foreground)
bright_magenta_foreground = _b(ordinals.bright_magenta_foreground)
bright_cyan_foreground = _b(ordinals.bright_cyan_foreground)
bright_white_foreground = _b(ordinals.bright_white_foreground)

bright_black_background = _b(ordinals.bright_black_background)
bright_red_background = _b(ordinals.bright_red_background)
bright_green_background = _b(ordinals.bright_green_background)
bright_yellow_background = _b(ordinals.bright_yellow_background)
bright_blue_background = _b(ordinals.bright_blue_background)
bright_magenta_background = _b(ordinals.bright_magenta_background)
bright_cyan_background = _b(ordinals.bright_cyan_background)
bright_white_background = _b(ordinals.bright_white_background)
# endregion

__all__ = (
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
