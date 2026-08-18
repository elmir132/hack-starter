#!/usr/bin/env python3
"""Run a small structure-and-input-retention smoke check, not a quality benchmark."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core import build_brief  # noqa: E402


REQUIRED_SECTIONS = (
    "one_liner", "problem_statement", "hypothesis", "mvp", "first_test",
    "interview_questions", "assumptions_to_check", "notice",
)


def run_evaluation():
    cases = json.loads((ROOT / "eval" / "cases.json").read_text(encoding="utf-8"))
    section_checks = 0
    section_total = 0
    retained = 0
    retained_total = 0
    failed_cases = []
    for index, case in enumerate(cases, start=1):
        result = build_brief(**case["input"])
        serialized = json.dumps(result, ensure_ascii=False).casefold()
        structure_ok = all(result.get(key) for key in REQUIRED_SECTIONS)
        structure_ok = structure_ok and len(result["mvp"]) == 3 and len(result["interview_questions"]) == 3
        structure_ok = structure_ok and result["model_used"] is False and result["mode"] == "deterministic-template"
        section_checks += int(structure_ok)
        section_total += 1
        fragments_present = sum(fragment.casefold() in serialized for fragment in case["must_include"])
        retained += fragments_present
        retained_total += len(case["must_include"])
        if not structure_ok or fragments_present != len(case["must_include"]):
            failed_cases.append(index)

    report = {
        "evaluation": "template structure and input-retention smoke check",
        "cases": len(cases),
        "complete_cases": section_checks,
        "structure_pass_rate": round(section_checks / section_total, 3) if section_total else None,
        "input_fragments_retained": retained,
        "input_fragments_total": retained_total,
        "input_retention_rate": round(retained / retained_total, 3) if retained_total else None,
        "failed_case_numbers": failed_cases,
        "limit": "Checks deterministic output shape and verbatim input carry-through only; it does not assess usefulness, factual accuracy, or user value.",
    }
    print(json.dumps(report, indent=2))
    return 1 if failed_cases else 0


if __name__ == "__main__":
    raise SystemExit(run_evaluation())
