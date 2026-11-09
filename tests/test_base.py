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

from openbarcode.linear import EAN, UPC, Code39, LinearBarcode


class IndependentInstancesTest(unittest.TestCase):
    """Regression test: the module pattern used to live in a class-level list shared by every instance."""

    def test_code39_instances_do_not_share_modules(self):
        a = Code39("A")
        b = Code39("B")
        self.assertEqual(len(a.barcode()), 38)
        self.assertEqual(len(b.barcode()), 38)
        self.assertEqual(a.barcode(), Code39("A").barcode())
        self.assertNotEqual(a.barcode(), b.barcode())

    def test_creating_other_instances_does_not_change_existing_ones(self):
        upc = UPC("03600029145")
        before = upc.barcode()
        EAN("400638133393")
        Code39("HELLO WORLD")
        UPC("01234567890")
        self.assertEqual(upc.barcode(), before)
        self.assertEqual(len(before), 95)

    def test_barcode_returns_a_copy(self):
        upc = UPC("03600029145")
        upc.barcode().clear()
        self.assertEqual(len(upc.barcode()), 95)


class AbstractBaseTest(unittest.TestCase):
    def test_base_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            LinearBarcode("ABC")

    def test_subclass_missing_abstract_methods_cannot_be_instantiated(self):
        class Incomplete(LinearBarcode):
            pass

        with self.assertRaises(TypeError):
            Incomplete("ABC")


if __name__ == "__main__":
    unittest.main()
