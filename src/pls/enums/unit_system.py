from __future__ import annotations

from enum import auto

from pls.enums.base import AutoEnum


class UnitSystem(AutoEnum):
    """
    Bytes can be converted to higher units in two ways:

    - the decimal system where powers of 10 (factor: 10^3) are used
    - the binary system where powers of 2 (factor: 2^10) are used

    This enum lists these possibilities.
    """

    BINARY = auto()
    DECIMAL = auto()


def get_base_and_pad_and_units(us: UnitSystem) -> tuple[int, int, list[str]]:
    """
    Get the base factor i.e. the ratio between any two successive orders of
    magnitude and the units corresponding to each multiplication of the base
    factor.

    :param us: the unit system in use
    :return: the base factor and the list of units
    """

    units = [
        "K",  # kibi | kilo
        "M",  # mebi | mega
        "G",  # gibi | giga
        "T",  # tebi | tera
        "P",  # pebi | peta
        "E",  # exbi | exa
        "Z",  # zebi | zetta
        "Y",  # yobi | yotta
    ]

    if us == UnitSystem.BINARY:
        base = pow(2, 10)
        pad = 3  # units will be 3 chars e.g. KiB, GiB
        units = ["", *map(lambda i: f"{i}i", units)]
    else:  # us == UnitSystem.DECIMAL:
        base = pow(10, 3)
        pad = 2  # units will be 2 chars e.g. KB, GB
        units = ["", *units]
    return base, pad, units
