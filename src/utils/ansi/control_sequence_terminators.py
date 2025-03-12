"""
See
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands
"""
from enum import UNIQUE, StrEnum, verify


@verify(UNIQUE)
class ControlSequenceTerminators(StrEnum):
    # region ANSI sequences
    cursor_up = "A"
    cursor_down = "B"
    cursor_forward = "C"
    cursor_back = "D"
    cursor_next_line = "E"
    cursor_previous_line = "F"
    cursor_horizontal_absolute = "G"
    cursor_position = "H"
    erase_in_display = "J"
    erase_in_line = "K"
    scroll_up = "S"
    scroll_down = "T"
    horizontal_vertical_position = "f"  # similar to cursor_position; see Wikipedia
    select_graphic_rendition = "m"
    # endregion

    # region popular private sequences
    save_current_cursor_position = "s"
    restore_saved_cursor_position = "u"
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
