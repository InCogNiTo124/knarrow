# SPDX-FileCopyrightText: 2021-present InCogNiTo124 <msmetko@msmetko.xyz>
#
# SPDX-License-Identifier: Apache-2.0

from typing import Tuple, Union

VERSION_TUPLE = Tuple[Union[int, str], ...]

__version_tuple__: VERSION_TUPLE
version_tuple: VERSION_TUPLE

__version_tuple__ = version_tuple = (0, 9, 1)
__version__ = version = ".".join(map(str, version_tuple))

__all__ = ["__version__", "__version_tuple__", "version", "version_tuple"]
