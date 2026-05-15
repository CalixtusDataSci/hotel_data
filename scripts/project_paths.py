from pathlib import Path
from typing import Iterable
import os


def find_repo_root(markers: Iterable[str] = ('README.md', 'setup.py', '.git')) -> Path:
    p = Path.cwd().resolve()
    for parent in (p, *p.parents):
        if any((parent / m).exists() for m in markers) or (parent / 'hotels_csv.csv').exists():
            return parent
    return p


def data_file(*parts: str) -> Path:
    root = find_repo_root()
    return root.joinpath(*parts)


def resolve_path(path_like) -> Path:
    """Resolve a path-like input to an absolute Path inside the repo when appropriate.

    - If `path_like` is an absolute path or already exists, return it as Path.
    - If `path_like` is a simple filename or relative path, join it to repo root.
    """
    root = find_repo_root()
    if isinstance(path_like, Path):
        if path_like.is_absolute() or path_like.exists():
            return path_like
        return root.joinpath(path_like)

    s = str(path_like)
    p = Path(s)
    if p.is_absolute() or p.exists():
        return p

    # split on forward or backward slashes to support mixed inputs
    parts = s.split('/') if '/' in s else s.split(os.sep)
    return root.joinpath(*parts)
