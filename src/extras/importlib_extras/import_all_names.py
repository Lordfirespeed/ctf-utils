import importlib
from typing import Any


class UniqueType(object):
    def __repr__(self):
        return "Unique"


Unique = UniqueType()


def import_all_names_from(_globals: dict[str, Any], name: str, package: str = None) -> None:
    """Import all names from a module (by adding them to the provided `globals()` dictionary).

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.
    """

    module = importlib.import_module(name, package)
    if not hasattr(module, "__all__"):
        raise NotImplementedError(f"caller tried to import all names from {module.__package__}, but that module has no `__all__` variable")

    for name in module.__all__:
        member = getattr(module, name)
        masked = _globals.get(name, Unique)
        if masked is member:
            continue
        if masked is not Unique:
            raise ValueError(f"caller tried to import {name} from {module.__package__} but doing so will mask {masked} in caller's scope")
        _globals[name] = member


__all__ = ("import_all_names_from",)
