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

"""UPC-A barcode."""

from .base import LinearBarcode
from .gs1 import encode_ean13, validate_gs1


class UPC(LinearBarcode):
    """UPC-A barcode, 95 modules.

    Pass 11 digits to have the check digit calculated, or all 12 digits to have the
    given check digit verified. A mismatch raises ValueError.
    """

    def _normalize(self, code):
        return validate_gs1("UPC-A", code, 11)

    def _encode(self):
        # UPC-A is EAN-13 with a leading zero, so both share one encoder.
        return encode_ean13("0" + self.code)
