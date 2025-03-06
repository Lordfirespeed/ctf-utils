from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .io import *
else:
    from .io_dummy import *
