from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .io import *
else:
    SupportsFlush = None
    SupportsWrite = None
    Writable = None
