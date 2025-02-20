from __future__ import annotations

from enum import auto

from pls.config import constants
from pls.enums.base import AutoEnum


class NodeType(AutoEnum):
    """
    A node can be either of these:

    - a directory
    - a regular file
    - a name FIFO pipe
    - a file-based socket
    - a char device
    - a block device
    - a symlink to any of the above

    This enum lists these possibilities. Refer to `the Wikipedia article on Unix
    file types <https://en.wikipedia.org/wiki/Unix_file_types>`_ for more info.
    """

    SYMLINK = auto()  # symbolic link
    DIR = auto()  # directory
    FILE = auto()  # regular file
    FIFO = auto()  # named pipe
    SOCKET = auto()  # socket
    CHAR_DEVICE = auto()  # character special device file
    BLOCK_DEVICE = auto()  # block special device file
    UNKNOWN = auto()  # graceful handling of unrecognised type
    BROKEN = auto()  # handling of non-existent nodes


type_test_map: dict[NodeType, str] = {
    node_type: f"is_{node_type.value}"
    for node_type in list(NodeType)
    if node_type not in {NodeType.UNKNOWN, NodeType.BROKEN}
}
"""a mapping of node types with specific functions that evaluate it"""


def get_type_char(node_type: NodeType) -> str:
    """
    Get the unique, distinct type character associated with the given node type. Returns
    a blank string if no type character is associated.

    :return: the type character mapped to the given ``NodeType`` value
    """

    return constants.constants.lookup(["type_chars", node_type.value], "")


def get_type_suffix(node_type: NodeType) -> str:
    """
    Get the unique, distinct type suffix associated with the given node type. Returns
    a blank string if no type character is associated.

    :return: the type suffix mapped to the given ``NodeType`` value
    """

    return constants.constants.lookup(["type_suffixes", node_type.value], "")
