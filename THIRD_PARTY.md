# Third-party software

`third_party/rfc8785/` vendors Trail of Bits' `rfc8785.py` version 0.1.4,
a pure-Python implementation of RFC 8785 / JSON Canonicalization Scheme (JCS),
distributed under Apache-2.0.

Upstream: https://github.com/trailofbits/rfc8785.py

The normal installation path remains `rfc8785==0.1.4` from `requirements.txt`.
The vendored copy is an offline fallback for reproducibility environments where package
installation is unavailable. DCTR does not claim authorship of this canonicalizer.
