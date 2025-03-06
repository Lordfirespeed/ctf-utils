from typing import TYPE_CHECKING

from .protocols import *

if TYPE_CHECKING:
    from .io import *
else:
    from .io_dummy import *
