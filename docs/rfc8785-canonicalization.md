# RFC 8785 / JCS canonical identity

DCTR now uses RFC 8785 (JSON Canonicalization Scheme) rather than Python's native JSON
rendering as the contract-identity definition.

Consequences used by the regression suite:

- Boolean `true` remains distinct from numeric `1`.
- Numeric `1` and `1.0` canonicalize identically.
- Negative zero canonicalizes as `0`.
- NaN/Infinity are rejected by the JCS implementation.
- Object properties use deterministic RFC 8785 ordering.

Reference: RFC 8785, JSON Canonicalization Scheme (JCS).
Python dependency: `rfc8785==0.1.4`.
