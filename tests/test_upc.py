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

import unittest

from openbarcode.linear import EAN, UPC
from openbarcode.linear import calculate_check_digit


class CheckDigitTest(unittest.TestCase):
    def test_known_check_digits(self):
        self.assertEqual(calculate_check_digit("03600029145"), 2)
        self.assertEqual(calculate_check_digit("01234567890"), 5)  # 012345678905

    def test_eleven_digits_get_check_digit_appended(self):
        self.assertEqual(UPC("03600029145").code, "036000291452")

    def test_correct_full_code_is_accepted(self):
        self.assertEqual(UPC("036000291452").code, "036000291452")
        self.assertEqual(UPC("036000291452").barcode(), UPC("03600029145").barcode())


class ValidationTest(unittest.TestCase):
    def test_wrong_check_digit_raises(self):
        with self.assertRaisesRegex(ValueError, "check digit mismatch"):
            UPC("036000291453")

    def test_wrong_length_raises(self):
        for code in ["", "0360002914", "0360002914523", "03600029145234"]:
            with self.subTest(code=code):
                with self.assertRaisesRegex(ValueError, "UPC-A code must have 11 or 12 digits"):
                    UPC(code)

    def test_non_digits_raise(self):
        for code in ["0360002914X", "03600 29145", "+3600029145", "0360002914-"]:
            with self.subTest(code=code):
                with self.assertRaisesRegex(ValueError, "only the digits 0-9"):
                    UPC(code)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            UPC(3600029145)


class StructureTest(unittest.TestCase):
    def test_module_count_and_guards(self):
        modules = UPC("03600029145").barcode()
        self.assertEqual(len(modules), 95)
        self.assertEqual(modules[0:3], [1, 0, 1])
        self.assertEqual(modules[45:50], [0, 1, 0, 1, 0])
        self.assertEqual(modules[92:95], [1, 0, 1])

    def test_values_are_zero_or_one(self):
        self.assertTrue(set(UPC("03600029145").barcode()) <= {0, 1})

    def test_upc_a_is_ean_13_with_leading_zero(self):
        self.assertEqual(UPC("03600029145").barcode(), EAN("0036000291452").barcode())


if __name__ == "__main__":
    unittest.main()
