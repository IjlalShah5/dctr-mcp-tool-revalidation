# Formal State Properties

Let \(O_t\) be the active operational baseline, \(H_t\) the last explicitly
human-reviewed baseline, and \(C\) the new candidate. The active grant binds
both stored baselines by digest:

\[
G_t = \langle server\_id, tool\_id, h(O_t), h(H_t), policy\_context, approval\_time \rangle.
\]

For a candidate \(C\):

\[
D_t^{local}=\Delta(O_t,C), \qquad
D_t^{cum}=\Delta(H_t,C)
\]

and

\[
L_t(C)=\max\{L(D_t^{local}),L(D_t^{cum})\}.
\]

Automatic L0-L2 continuation may advance \(O_t\) and its operational digest,
but not \(H_t\) or the human-reviewed digest. Explicit human approval advances
both baselines and binds both digests to the approved candidate.

## Integrity precondition

Before stability or cumulative comparison is evaluated, the reference design
recomputes both \(h(O_t)\) and \(h(H_t)\). A mismatch against either
grant-bound digest fails closed. This prevents corruption or tampering of the
human-reviewed anchor from silently changing the cumulative comparison.

## Lemma 1 — No stability laundering

If \(h(C) \neq h(O_t)\) and continuation is not authorised, repeated observation of
\(C\) cannot produce `STABLE_ACCEPT`.

**Proof sketch.** The first mismatch fails the stable predicate. Because continuation is
not authorised, the state-update rule preserves \(O_t\) and its grant digest. The next
refresh therefore evaluates the same unequal hashes. By induction, any finite sequence of
pending or denied repetitions preserves the mismatch until an authorised state transition
occurs.

## Lemma 2 — Cumulative staircase escalation

If a sequence of L0-L2 automatic continuations advances the operational baseline while
the human-reviewed anchor remains fixed, then any candidate satisfying
\(L(\Delta(H_t,C)) \ge 3\) has effective level at least L3 even if its immediate local
step is L0-L2.

**Scope.** This lemma is conditional on the semantic classifier assigning a level to the
cumulative delta that captures the relevant interaction. DCTR composes path-level levels
with a maximum operator; it does not prove detection of emergent cross-path interactions
when every individual path is classified as bounded in isolation. For example, two
separately bounded path edits can jointly change how a newly introduced option is used.
Such interaction-sensitive classification remains a semantic-analysis obligation and is
listed as a limitation rather than implied by the staircase property.

## Lemma 3 — Withdrawal breaks approval inheritance

If an approved Tool transitions to the absence state (\(\bot\)), the reference state
revokes the active grant and clears both approval baselines. A later
\(\bot \rightarrow C\) presentation therefore follows `INITIAL_TRUST` rather than
revalidation against the withdrawn grant.

## Fail-closed boundaries

The reference implementation blocks trust transfer on operational-baseline integrity
failure, human-anchor integrity failure, canonicalisation failure, grant identity
mismatch, differencing failure/inconsistency, or policy-engine failure. Explicit semantic
uncertainty maps to minimum L3 revalidation with the approval state unchanged. L4 remains
quarantine/remediation and is not converted to ordinary continuation merely because an
approval flag is supplied.

These are properties of the reference state-update rules, conditional on correct hashing,
differencing, classification, and atomic persistence; they are not proofs of runtime
security.
