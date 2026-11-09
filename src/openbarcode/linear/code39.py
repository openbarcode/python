#
# Copyright 2013 Floms, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

"""Code 39 barcode."""

from .base import LinearBarcode

# Standard Code 39 symbol patterns. A symbol has 9 elements that alternate bar, space,
# starting with a bar. "n" is a narrow element and "w" a wide one; exactly 3 of the 9
# elements are wide.
_PATTERNS = {
    "0": "nnnwwnwnn", "1": "wnnwnnnnw", "2": "nnwwnnnnw", "3": "wnwwnnnnn",
    "4": "nnnwwnnnw", "5": "wnnwwnnnn", "6": "nnwwwnnnn", "7": "nnnwnnwnw",
    "8": "wnnwnnwnn", "9": "nnwwnnwnn", "A": "wnnnnwnnw", "B": "nnwnnwnnw",
    "C": "wnwnnwnnn", "D": "nnnnwwnnw", "E": "wnnnwwnnn", "F": "nnwnwwnnn",
    "G": "nnnnnwwnw", "H": "wnnnnwwnn", "I": "nnwnnwwnn", "J": "nnnnwwwnn",
    "K": "wnnnnnnww", "L": "nnwnnnnww", "M": "wnwnnnnwn", "N": "nnnnwnnww",
    "O": "wnnnwnnwn", "P": "nnwnwnnwn", "Q": "nnnnnnwww", "R": "wnnnnnwwn",
    "S": "nnwnnnwwn", "T": "nnnnwnwwn", "U": "wwnnnnnnw", "V": "nwwnnnnnw",
    "W": "wwwnnnnnn", "X": "nwnnwnnnw", "Y": "wwnnwnnnn", "Z": "nwwnwnnnn",
    "-": "nwnnnnwnw", ".": "wwnnnnwnn", " ": "nwwnnnwnn", "$": "nwnwnwnnn",
    "/": "nwnwnnnwn", "+": "nwnnnwnwn", "%": "nnnwnwnwn", "*": "nwnnwnwnn",
}

_ALPHABET = frozenset(char for char in _PATTERNS if char != "*")


def _expand(pattern):
    """Expand a narrow/wide pattern into modules: a narrow element is 1 module, a wide one 2."""
    modules = []
    for index, width in enumerate(pattern):
        bar = 1 if index % 2 == 0 else 0
        modules += [bar] * (1 if width == "n" else 2)
    return modules


_SYMBOLS = {char: _expand(pattern) for char, pattern in _PATTERNS.items()}


class Code39(LinearBarcode):
    """Code 39 barcode.

    The input is uppercased. Supported characters are 0-9, A-Z, space, and ``-.$/+%``.
    Symbols are separated by a 1-module narrow space. There is no space before the
    start character or after the stop character. ``Code39("CODE39")`` gives 103 modules.
    """

    def _normalize(self, code):
        normalized = code.upper()
        if not normalized:
            raise ValueError("Code 39 code must not be empty")
        unsupported = sorted(set(normalized) - _ALPHABET)
        if unsupported:
            raise ValueError("Code 39 does not support %s in %r"
                             % (", ".join(repr(char) for char in unsupported), code))
        return normalized

    def _encode(self):
        modules = []
        for index, char in enumerate("*" + self.code + "*"):
            if index:
                modules.append(0)
            modules += _SYMBOLS[char]
        return modules
