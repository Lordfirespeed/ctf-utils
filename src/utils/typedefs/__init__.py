from typing import TYPE_CHECKING

from .protocols import *
from .like import *

if TYPE_CHECKING:
    from .io import *
else:
    from .io_dummy import *
