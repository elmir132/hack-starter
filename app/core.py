"""Deterministic example flow used by the API, demo and small evaluation."""


def build_brief(project_name, audience, problem, approach):
    """Turn four inputs into a structured draft without calling a model or service."""
    project_name, audience, problem, approach = (
        value.strip() for value in (project_name, audience, problem, approach)
    )
    problem_text = problem.rstrip(" .!?")
    approach_text = approach.rstrip(" .!?")
    return {
        "project_name": project_name,
        "one_liner": f"{project_name} tests whether {audience} will {approach_text}.",
        "problem_statement": f"A current pain to validate: {problem_text}.",
        "hypothesis": f"We think {audience} may use this to address {problem_text}. That is an assumption to test.",
        "mvp": [
            f"One primary flow: help {audience} {approach_text}.",
            f"One visible outcome connected to: {problem_text}.",
            "One feedback step; defer integrations until a user test supports them.",
        ],
        "first_test": {
            "method": f"Show a clickable prototype to five people from {audience}.",
            "task": f"Ask each person to try the core action: {approach_text}.",
            "success_signal": (
                "Starting threshold: at least 3 of 5 complete the task without coaching. "
                "Adjust this before using it with real participants."
            ),
        },
        "interview_questions": [
            f"What happened the last time you faced this: {problem_text}?",
            "What did you try, and what was frustrating about that?",
            "What would need to change before you would try a solution like this?",
        ],
        "assumptions_to_check": [
            "This problem happens often enough for someone to try a new approach.",
            "The named audience can be reached for a prototype test.",
        ],
        "mode": "deterministic-template",
        "model_used": False,
        "notice": "Draft generated from the submitted text with fixed templates; no model or outside research was used.",
    }
