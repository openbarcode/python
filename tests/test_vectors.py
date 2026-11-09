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

"""Exact module patterns for the cross-language test vectors.

These strings are the reference output that every Open Barcode implementation must match.
They were generated from the standard GS1 and Code 39 tables, not from this package.
"""

import unittest

from openbarcode.linear import Code39, EAN, UPC

UPC_A_INPUT = "03600029145"  # check digit 2, full code 036000291452
EAN_13_INPUT = "400638133393"  # check digit 1, full code 4006381333931

UPC_A_MODULES = "10100011010111101010111100011010001101000110101010110110011101001100110101110010011101101100101"
EAN_13_MODULES = "10100011010100111010111101111010001001011001101010100001010000101000010111010010000101100110101"
CODE39_CODE39_MODULES = "1001011011010110110100101011010110100101010110010110110101100101011011001010101011001011010100101101101"
CODE39_HELLO_WORLD_MODULES = "100101101101011010100110101101011001010101101010011010110101001101101011010010100110101101011001101010101101011010010110101011001010110101001101010110010110100101101101"


def _as_string(modules):
    return "".join(str(module) for module in modules)


class VectorTest(unittest.TestCase):
    def test_upc_a_vector(self):
        self.assertEqual(UPC(UPC_A_INPUT).code, "036000291452")
        self.assertEqual(_as_string(UPC(UPC_A_INPUT).barcode()), UPC_A_MODULES)

    def test_ean_13_vector(self):
        self.assertEqual(EAN(EAN_13_INPUT).code, "4006381333931")
        self.assertEqual(_as_string(EAN(EAN_13_INPUT).barcode()), EAN_13_MODULES)

    def test_code39_vector(self):
        self.assertEqual(_as_string(Code39("CODE39").barcode()), CODE39_CODE39_MODULES)

    def test_code39_space_vector(self):
        self.assertEqual(_as_string(Code39("HELLO WORLD").barcode()), CODE39_HELLO_WORLD_MODULES)

    def test_first_and_last_30_bits(self):
        self.assertEqual(_as_string(UPC(UPC_A_INPUT).barcode())[:30], "101000110101111010101111000110")
        self.assertEqual(_as_string(UPC(UPC_A_INPUT).barcode())[-30:], "100110101110010011101101100101")
        self.assertEqual(_as_string(EAN(EAN_13_INPUT).barcode())[:30], "101000110101001110101111011110")
        self.assertEqual(_as_string(EAN(EAN_13_INPUT).barcode())[-30:], "000010111010010000101100110101")
        self.assertEqual(_as_string(Code39("CODE39").barcode())[:30], "100101101101011011010010101101")
        self.assertEqual(_as_string(Code39("CODE39").barcode())[-30:], "010101011001011010100101101101")
        self.assertEqual(_as_string(Code39("HELLO WORLD").barcode())[:30], "100101101101011010100110101101")
        self.assertEqual(_as_string(Code39("HELLO WORLD").barcode())[-30:], "001101010110010110100101101101")

    def test_vector_lengths(self):
        self.assertEqual(len(UPC_A_MODULES), 95)
        self.assertEqual(len(EAN_13_MODULES), 95)
        self.assertEqual(len(CODE39_CODE39_MODULES), 103)
        self.assertEqual(len(CODE39_HELLO_WORLD_MODULES), 168)


if __name__ == "__main__":
    unittest.main()
