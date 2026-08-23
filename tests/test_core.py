from app.core import build_brief


def test_brief_keeps_user_inputs_and_labels_the_baseline():
    brief = build_brief(
        project_name="Campus Cart",
        audience="students living on campus",
        problem="finding a ride home after late labs",
        approach="match students with open seats",
    )

    assert brief["project_name"] == "Campus Cart"
    assert "students living on campus" in brief["one_liner"]
    assert "finding a ride home after late labs" in brief["problem_statement"]
    assert "match students with open seats" in brief["one_liner"]
    assert len(brief["mvp"]) == 3
    assert len(brief["interview_questions"]) == 3
    assert brief["mode"] == "deterministic-template"
    assert brief["model_used"] is False


def test_brief_does_not_claim_external_research():
    brief = build_brief("Room Map", "commuters", "finding a free seat", "show seat availability")

    assert "no model or outside research was used" in brief["notice"]
