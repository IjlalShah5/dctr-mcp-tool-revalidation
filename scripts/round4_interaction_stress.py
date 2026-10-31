#!/usr/bin/env python3
"""Author-designed safe combinatorial policy model; NOT a security-validation study.

All individual mutation paths are stipulated L2. No external writes, network
connections, actual tool invocations, or human severity labels occur here.
"""
import itertools
import json

SCENARIOS=(
 ("known_pair",("write_enabled","external_enabled"),frozenset(("write_enabled","external_enabled"))),
 ("unknown_triple",("metadata_enabled","lookup_enabled","logging_disabled"),frozenset(("metadata_enabled","lookup_enabled","logging_disabled"))),
 ("benign_pair",("cache_enabled","format_enabled"),frozenset()),
)
KNOWN_PAIR=frozenset(("write_enabled","external_enabled"))

def run():
    cases=[]
    for scenario, fields, trigger in SCENARIOS:
        for enabled in itertools.product((False,True),repeat=len(fields)):
            active=frozenset(f for f,on in zip(fields,enabled) if on)
            effect=bool(trigger) and trigger.issubset(active)
            l2=2 if active else 0
            levels={
              "per_path_max":l2,
              "known_pairwise_guard":3 if KNOWN_PAIR.issubset(active) else l2,
              "conservative_two_or_more":3 if len(active)>=2 else l2,
            }
            cases.append({
              "scenario":scenario,"active":sorted(active),"test_only_compound_effect":effect,
              "policy_levels":levels
            })
    summary={}
    for policy in ("per_path_max","known_pairwise_guard","conservative_two_or_more"):
        cases_mut=[c for c in cases if c["active"]]
        summary[policy]={
          "mutations":len(cases_mut),
          "synthetic_effect_cases":sum(c["test_only_compound_effect"] for c in cases_mut),
          "blocked_compound_effect_cases":sum(c["test_only_compound_effect"] and c["policy_levels"][policy]>=3 for c in cases_mut),
          "unblocked_compound_effect_cases":sum(c["test_only_compound_effect"] and c["policy_levels"][policy]<=2 for c in cases_mut),
          "benign_combinations_escalated":sum(not c["test_only_compound_effect"] and c["policy_levels"][policy]>=3 for c in cases_mut)
        }
    return {
      "evidence_type":"AUTHOR_DEFINED_SYNTHETIC_MODEL_NOT_SECURITY_GROUND_TRUTH",
      "total_combinations":len(cases),
      "changed_contract_combinations":sum(bool(c["active"]) for c in cases),
      "summary":summary,
      "cases":cases,
      "limit":"These counts are not measured harm, deployed-MCP call effects, external L4 labels or accuracy."
    }

if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
