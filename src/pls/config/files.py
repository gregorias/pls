from __future__ import annotations

import itertools
import os
from pathlib import Path
from typing import Optional

from pls.globals import state


conf_name = ".pls.yml"
"""the name of the ``pls`` config file"""

max_height = os.getenv("PLS_MAX_HEIGHT", 8)
"""the maximum height upto which ``pls`` will search for configs"""


def _is_valid(path: Path) -> bool:
    """
    Check if the given path points to an existing file.

    :param path: the path to check for validity
    :return: ``True`` if the path is an existing file, ``False`` otherwise
    """

    return path.exists() and path.is_file()


def get_cwd_conf(curr_dir: Path) -> Optional[Path]:
    """
    Get the path to the ``pls`` config in the current directory itself.

    :param curr_dir: the directory being listed by ``pls``
    :return: the path to the ``pls`` config if it exists, ``None`` otherwise
    """

    test_path = curr_dir.joinpath(conf_name)
    return test_path if _is_valid(test_path) else None


def get_ancestor_confs(curr_dir: Path) -> list[Path]:
    """
    Get the paths to all ``pls`` configs in the current directory's ancestors. If the
    working directory is Git tracked, this will check upto the Git boundary and include
    the config in the Git root. Otherwise, it will traverse a fixed number of ancestors.

    :param curr_dir: the directory being listed by ``pls``
    :return: the path to the ``pls`` config if it exists, ``None`` otherwise
    """

    conf_paths = []

    git_root = state.state.git_root
    limit = float("inf") if git_root is not None else max_height

    for i in itertools.count(start=0):
        if i == limit:
            break

        try:
            test_dir = curr_dir.parents[i]
        except IndexError:
            # Ran out of parent directories.
            break

        test_path = test_dir.joinpath(conf_name)
        if _is_valid(test_path):
            conf_paths.append(test_path)

        if test_dir == git_root:
            break

    return conf_paths


def get_home_conf() -> Optional[Path]:
    """
    Get the path to the ``pls`` config in the user's home directory.

    :return: the path to the ``pls`` config if it exists, ``None`` otherwise
    """

    if state.state.home_dir is None:
        return None

    test_path = state.state.home_dir.joinpath(conf_name)
    return test_path if _is_valid(test_path) else None


def find_configs(node: Path) -> list[Path]:
    """
    Get the paths for all the relevant ``.pls.yml`` files.

    :param node: the file or directory being listed
    :return: a list of paths for all ``pls`` config files
    """

    curr_dir = node if node.is_dir() else node.parent

    conf_paths = []
    if cwd_conf := get_cwd_conf(curr_dir):
        conf_paths.append(cwd_conf)
    if ancestor_confs := get_ancestor_confs(curr_dir):
        conf_paths.extend(ancestor_confs)
    if (home_conf := get_home_conf()) and home_conf not in conf_paths:
        conf_paths.append(home_conf)

    return conf_paths
