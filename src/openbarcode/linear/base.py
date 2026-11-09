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

"""Base class for linear barcodes."""

from abc import ABC, abstractmethod


class LinearBarcode(ABC):
    """Base class for linear (one-dimensional) barcodes.

    Subclasses implement ``_normalize``, which validates the input and returns the
    canonical code, and ``_encode``, which returns the module pattern. The pattern is
    built once per instance, so instances do not share any state.
    """

    def __init__(self, code):
        if not isinstance(code, str):
            raise TypeError("%s code must be a str, not %s"
                            % (type(self).__name__, type(code).__name__))
        self.code = self._normalize(code)
        self._modules = self._encode()

    @abstractmethod
    def _normalize(self, code):
        """Validate ``code`` and return the canonical form stored in ``self.code``."""

    @abstractmethod
    def _encode(self):
        """Return the module pattern as a list of 0 (space) and 1 (bar)."""

    def barcode(self):
        """Return the module pattern as a new list of 0 (space) and 1 (bar) values."""
        return list(self._modules)
