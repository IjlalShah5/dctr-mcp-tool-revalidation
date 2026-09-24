# Formal State Properties

Let \(O_t\) be the active operational baseline, \(H_t\) the last explicitly
human-reviewed baseline, and \(C\) the new candidate.

\[
D_t^{local}=\Delta(O_t,C), \qquad
D_t^{cum}=\Delta(H_t,C)
\]

\[
L_t(C)=\max\{L(D_t^{local}),L(D_t^{cum})\}.
\]

Automatic L0–L2 continuation may advance \(O_t\), but not \(H_t\). Explicit human
approval advances both.

## Lemma 1 — No stability laundering

If \(h(C)\neq h(O_t)\) and continuation is not authorised, repeated observation of
\(C\) cannot produce `STABLE_ACCEPT`.

**Proof sketch.** The first mismatch fails the stable predicate. Because continuation is
not authorised, the state-update rule preserves \(O_t\) and its grant digest. The next
refresh therefore evaluates the same unequal hashes. By induction, any finite sequence of
pending or denied repetitions preserves the mismatch until an authorised state transition
occurs.

## Lemma 2 — Cumulative staircase escalation

If a sequence of L0–L2 automatic continuations advances the operational baseline while
the human-reviewed anchor remains fixed, then any candidate satisfying
\(L(\Delta(H_t,C))\ge 3\) has effective level at least L3 even if its immediate local
step is L0–L2.

These are properties of the reference state-update rules, conditional on correct hashing,
differencing, classification, and atomic persistence; they are not proofs of runtime
security.
