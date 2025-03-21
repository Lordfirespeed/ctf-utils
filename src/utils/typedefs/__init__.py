from typing import TYPE_CHECKING

from .collections import *
from .factorise import *
from .protocols import *
from .like import *

if TYPE_CHECKING:
    from .shed import *
    from .io import *
else:
    # cheap dynamic import hack to prevent PyCharm from mistakenly replacing actual type annotations with the dummy ones
    from extras import importlib_extras
    importlib_extras.import_all_names_from(locals(), ".shed_dummy", __package__)
    importlib_extras.import_all_names_from(locals(), ".io_dummy", __package__)
