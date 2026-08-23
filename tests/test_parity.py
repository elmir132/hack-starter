"""The brief builder exists twice: Python (API) and JavaScript (offline demo). They must agree."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from app.core import build_brief

ROOT = Path(__file__).resolve().parent.parent

EDGE_CASES = [
    {"project_name": "X!", "audience": "people...", "problem": "it is slow?!", "approach": "use it . . ."},
    {"project_name": "Café Ünï", "audience": "студенти", "problem": "пошук житла", "approach": "порівняти ціни"},
    {"project_name": "  Padded  ", "audience": " a b ", "problem": "  p q  ", "approach": " r s "},
]

NODE_SCRIPT = """
const fs = require("fs");
const src = fs.readFileSync(process.argv[1], "utf8");
const body = src.slice(src.indexOf("function makeLocalBrief"), src.indexOf("function setConnection"));
const makeLocalBrief = new Function(body + "; return makeLocalBrief;")();
const cases = JSON.parse(fs.readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(cases.map(makeLocalBrief)));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_javascript_fallback_matches_the_python_builder():
    fixtures = [case["input"] for case in json.loads((ROOT / "eval" / "cases.json").read_text(encoding="utf-8"))]
    cases = fixtures + EDGE_CASES
    # the page trims form values before calling the JS builder (see formValues in web/app.js); Python trims itself
    trimmed = [{key: value.strip() for key, value in case.items()} for case in cases]
    result = subprocess.run(
        ["node", "-e", NODE_SCRIPT, str(ROOT / "web" / "app.js")],
        input=json.dumps(trimmed), capture_output=True, text=True, check=True,
    )
    from_js = json.loads(result.stdout)
    assert len(from_js) == len(cases)
    for case, js_brief in zip(cases, from_js):
        assert js_brief == build_brief(**case), case
