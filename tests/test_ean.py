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

from openbarcode.linear import EAN
from openbarcode.linear import calculate_check_digit


class CheckDigitTest(unittest.TestCase):
    def test_known_check_digit(self):
        self.assertEqual(calculate_check_digit("400638133393"), 1)

    def test_twelve_digits_get_check_digit_appended(self):
        self.assertEqual(EAN("400638133393").code, "4006381333931")

    def test_correct_full_code_is_accepted(self):
        self.assertEqual(EAN("4006381333931").barcode(), EAN("400638133393").barcode())


class ValidationTest(unittest.TestCase):
    def test_wrong_check_digit_raises(self):
        with self.assertRaisesRegex(ValueError, "check digit mismatch"):
            EAN("4006381333932")

    def test_wrong_length_message_names_ean(self):
        for code in ["", "40063813339", "40063813339312", "40063813339331"]:
            with self.subTest(code=code):
                with self.assertRaisesRegex(ValueError, "^EAN-13 code must have 12 or 13 digits"):
                    EAN(code)

    def test_non_digits_raise(self):
        for code in ["40063813339X", "400638 33393", "+400638133393"]:
            with self.subTest(code=code):
                with self.assertRaisesRegex(ValueError, "only the digits 0-9"):
                    EAN(code)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            EAN(400638133393)


class StructureTest(unittest.TestCase):
    def test_module_count_and_guards(self):
        modules = EAN("400638133393").barcode()
        self.assertEqual(len(modules), 95)
        self.assertEqual(modules[0:3], [1, 0, 1])
        self.assertEqual(modules[45:50], [0, 1, 0, 1, 0])
        self.assertEqual(modules[92:95], [1, 0, 1])

    def test_first_digit_changes_left_half(self):
        # The first digit selects the left-half parity, so the same six digits
        # encode differently when the first digit differs.
        self.assertNotEqual(EAN("003600029145").barcode()[3:45],
                            EAN("103600029145").barcode()[3:45])


if __name__ == "__main__":
    unittest.main()
