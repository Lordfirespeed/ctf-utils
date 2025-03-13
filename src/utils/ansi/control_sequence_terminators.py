"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands
"""
from enum import UNIQUE, verify

from utils.enum_extras import BytesEnum


@verify(UNIQUE)
class ControlSequenceTerminators(BytesEnum):
    # region ANSI sequences
    cursor_up = b"A"
    cursor_down = b"B"
    cursor_forward = b"C"
    cursor_back = b"D"
    cursor_next_line = b"E"
    cursor_previous_line = b"F"
    cursor_horizontal_absolute = b"G"
    cursor_position = b"H"
    erase_in_display = b"J"
    erase_in_line = b"K"
    scroll_up = b"S"
    scroll_down = b"T"
    horizontal_vertical_position = b"f"  # similar to cursor_position; see Wikipedia
    select_graphic_rendition = b"m"
    # endregion

    # region popular private sequences
    save_current_cursor_position = b"s"
    restore_saved_cursor_position = b"u"
    # endregion


# region ANSI sequences
cursor_up = ControlSequenceTerminators.cursor_up
cursor_down = ControlSequenceTerminators.cursor_down
cursor_forward = ControlSequenceTerminators.cursor_forward
cursor_back = ControlSequenceTerminators.cursor_back
cursor_next_line = ControlSequenceTerminators.cursor_next_line
cursor_previous_line = ControlSequenceTerminators.cursor_previous_line
cursor_horizontal_absolute = ControlSequenceTerminators.cursor_horizontal_absolute
cursor_position = ControlSequenceTerminators.cursor_position
erase_in_display = ControlSequenceTerminators.erase_in_display
erase_in_line = ControlSequenceTerminators.erase_in_line
scroll_up = ControlSequenceTerminators.scroll_up
scroll_down = ControlSequenceTerminators.scroll_down
horizontal_vertical_position = ControlSequenceTerminators.horizontal_vertical_position
select_graphic_rendition = ControlSequenceTerminators.select_graphic_rendition
# endregion

# region popular private sequences
save_current_cursor_position = ControlSequenceTerminators.save_current_cursor_position
restore_saved_cursor_position = ControlSequenceTerminators.restore_saved_cursor_position
# endregion


__all__ = (
    "ControlSequenceTerminators",
    "cursor_up",
    "cursor_down",
    "cursor_forward",
    "cursor_back",
    "cursor_next_line",
    "cursor_previous_line",
    "cursor_horizontal_absolute",
    "cursor_position",
    "erase_in_display",
    "erase_in_line",
    "scroll_up",
    "scroll_down",
    "horizontal_vertical_position",
    "select_graphic_rendition",
    "save_current_cursor_position",
    "restore_saved_cursor_position",
)
