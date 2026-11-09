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

from openbarcode.linear import Code39
from openbarcode.linear.code39 import _PATTERNS

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"


class PatternTest(unittest.TestCase):
    def test_every_pattern_has_nine_elements_and_three_wide(self):
        for char, pattern in _PATTERNS.items():
            with self.subTest(char=char):
                self.assertEqual(len(pattern), 9)
                self.assertEqual(pattern.count("w"), 3)

    def test_table_covers_standard_alphabet_and_start_stop(self):
        self.assertEqual(set(_PATTERNS), set(ALPHABET) | {"*"})

    def test_every_single_character_is_38_modules(self):
        # Three 12-module symbols (start, character, stop) and two 1-module gaps.
        for char in ALPHABET:
            with self.subTest(char=char):
                self.assertEqual(len(Code39(char).barcode()), 38)

    def test_gaps_only_between_characters(self):
        modules = Code39("A").barcode()
        self.assertEqual(modules[12], 0)
        self.assertEqual(modules[25], 0)
        self.assertEqual(modules[-1], 1)  # the stop symbol ends with a bar, no trailing gap
        self.assertEqual(len(Code39("CODE39").barcode()), 103)
        self.assertEqual(len(Code39("HELLO WORLD").barcode()), 168)


class EncodingTest(unittest.TestCase):
    def test_input_is_uppercased(self):
        self.assertEqual(Code39("code39").code, "CODE39")
        self.assertEqual(Code39("code39").barcode(), Code39("CODE39").barcode())

    def test_start_and_stop_are_framing_symbols(self):
        modules = Code39("A").barcode()
        self.assertEqual(modules[0:12], [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1])  # "*"
        self.assertEqual(modules[13:25], [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1])  # "A"
        self.assertEqual(modules[26:38], [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1])  # "*"

    def test_values_are_zero_or_one(self):
        self.assertTrue(set(Code39("HELLO WORLD").barcode()) <= {0, 1})

    def test_empty_code_raises(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            Code39("")


class ValidationTest(unittest.TestCase):
    def test_unsupported_character_raises_value_error_naming_it(self):
        with self.assertRaisesRegex(ValueError, "does not support '@'"):
            Code39("AB@C")

    def test_unsupported_lowercase_input_is_reported_uppercased(self):
        with self.assertRaisesRegex(ValueError, "'\\?'"):
            Code39("a?")

    def test_star_is_reserved_for_start_and_stop(self):
        with self.assertRaisesRegex(ValueError, "does not support '\\*'"):
            Code39("A*B")

    def test_non_ascii_raises_value_error_not_key_error(self):
        with self.assertRaises(ValueError):
            Code39("é")

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            Code39(39)


if __name__ == "__main__":
    unittest.main()
