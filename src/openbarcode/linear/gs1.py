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

"""GS1 check digit, input validation and EAN-13 encoding shared by UPC-A and EAN-13."""

_DIGITS = frozenset("0123456789")


def _bits(pattern):
    return [int(bit) for bit in pattern]


# GS1 digit encodings, 7 modules each. L and G are used on the left half of an
# EAN-13 symbol and R on the right half. R is the bitwise complement of L.
_L = tuple(_bits(code) for code in (
    "0001101", "0011001", "0010011", "0111101", "0100011",
    "0110001", "0101111", "0111011", "0110111", "0001011"))
_G = tuple(_bits(code) for code in (
    "0100111", "0110011", "0011011", "0100001", "0011101",
    "0111001", "0000101", "0010001", "0001001", "0010111"))
_R = tuple(tuple(1 - bit for bit in digit) for digit in _L)

_START_GUARD = _bits("101")
_CENTER_GUARD = _bits("01010")
_END_GUARD = _bits("101")

# Left-half parity for digits 2-7 of EAN-13, selected by the first digit.
_PARITY = (
    "LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
    "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL")


def calculate_check_digit(payload):
    """Return the GS1 mod-10 check digit for ``payload``, a string of digits without its check digit.

    Digits are weighted 3, 1, 3, 1, ... counting from the right.
    """
    total = sum(int(digit) * (3 if index % 2 == 0 else 1)
                for index, digit in enumerate(reversed(payload)))
    return (10 - total) % 10


def validate_gs1(name, code, payload_length):
    """Check a UPC-A or EAN-13 input and return the full code with its check digit."""
    if len(code) not in (payload_length, payload_length + 1):
        raise ValueError(
            "%s code must have %d or %d digits, got %d: %r"
            % (name, payload_length, payload_length + 1, len(code), code))
    if not _DIGITS.issuperset(code):
        raise ValueError("%s code must contain only the digits 0-9: %r" % (name, code))

    payload = code[:payload_length]
    expected = calculate_check_digit(payload)
    if len(code) == payload_length + 1 and int(code[-1]) != expected:
        raise ValueError(
            "%s check digit mismatch in %r: expected %d, got %s"
            % (name, code, expected, code[-1]))
    return payload + str(expected)


def encode_ean13(digits):
    """Return the 95-module EAN-13 pattern for a 13-digit string (check digit included)."""
    modules = list(_START_GUARD)
    for digit, side in zip(digits[1:7], _PARITY[int(digits[0])]):
        modules += _L[int(digit)] if side == "L" else _G[int(digit)]
    modules += _CENTER_GUARD
    for digit in digits[7:]:
        modules += _R[int(digit)]
    modules += _END_GUARD
    return modules
