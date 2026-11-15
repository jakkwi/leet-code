"""Import a problem's solution.py by path.

Every problem has a module called ``solution``; importing them by name would
make them collide in ``sys.modules``. Each one gets a unique module name instead.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_sibling(test_file: str, module: str = "solution") -> ModuleType:
    path = Path(test_file).resolve().parent / f"{module}.py"
    unique = "lc_" + "_".join(path.parent.parent.parts[-2:]) + f"_{module}"
    spec = importlib.util.spec_from_file_location(unique, path)
    if spec is None or spec.loader is None:
        msg = f"cannot load {path}"
        raise ImportError(msg)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
