from pathlib import Path
from typing import Iterable


def find_repo_root(markers: Iterable[str] = ('README.md', 'setup.py', '.git')) -> Path:
    p = Path.cwd().resolve()
    for parent in (p, *p.parents):
        if any((parent / m).exists() for m in markers) or (parent / 'hotels_csv.csv').exists():
            return parent
    return p


def data_file(*parts: str) -> Path:
    root = find_repo_root()
    return root.joinpath(*parts)
