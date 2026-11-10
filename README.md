<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/open-barcode-logo-dark.svg">
    <img src="assets/branding/open-barcode-logo.svg" alt="Open Barcode by Floms" width="420">
  </picture>
</p>

<p align="center"><em>Barcodes, made open.</em></p>

# Open Barcode for Python

Barcode module patterns for Python: UPC-A, EAN-13 and Code 39. The package has no runtime dependencies and supports Python 3.9 and later.

Open Barcode is available in several languages:

- Java: https://github.com/openbarcode/java
- C#: https://github.com/openbarcode/csharp
- Python: https://github.com/openbarcode/python
- PHP: https://github.com/openbarcode/php
- JavaScript: https://github.com/openbarcode/javascript

Project homepage: https://openbarcode.dev

## Installation

```sh
python -m pip install openbarcode
```

## Usage

Each class takes the code as a string and returns its module pattern from `barcode()`: a list of `1` (bar) and `0` (space) values. Rendering the pattern as an image or SVG is up to your application.

```python
from openbarcode.linear import UPC, EAN, Code39

upc = UPC("03600029145")      # 11 digits: the check digit is calculated
upc.code                      # "036000291452"
len(upc.barcode())            # 95

UPC("036000291452")           # 12 digits: the check digit is verified
EAN("400638133393")           # 12 digits: the check digit is calculated
Code39("hello world").code    # "HELLO WORLD": input is uppercased
```

Supported inputs:

- `UPC`: UPC-A, 11 or 12 digits.
- `EAN`: EAN-13, 12 or 13 digits.
- `Code39`: 0-9, A-Z, space, and `-.$/+%`.

Invalid input raises `ValueError`. This covers a wrong length, non-digits in UPC or EAN, a check digit that does not match, and characters Code 39 does not support. A non-string argument raises `TypeError`.

## Testing

The tests use the standard library `unittest` module. From a clone of this repository:

```sh
python -m pip install .
python -m unittest discover -s tests -t .
```

To run against the source tree without installing, set `PYTHONPATH=src`:

```sh
PYTHONPATH=src python -m unittest discover -s tests -t .
```

The continuous integration workflow in `.github/workflows/ci.yml` runs the same tests on Python 3.10 through 3.13.

This repository was split from the original multi-language project at
https://github.com/floms/Open-Barcode. The commit history was preserved
with git-filter-repo; commit hashes differ from the original.

Copyright 2013 Floms, LLC (Yoel Nunez)

Copyright 2026 Floms, Inc.

Licensed under the Apache License, Version 2.0. See LICENSE.md for details.
