# Demo and evaluation honesty checklist

Use this before recording a demo, writing a README claim, or submitting a hackathon project.

## What is actually running?

- [ ] Label the path shown: live backend, deterministic local code, static fallback, or prerecorded/mock response.
- [ ] If a model is involved, name the provider and model actually used. Do not say “AI-powered” when the displayed result came from a canned response or local rule.
- [ ] Show errors and unavailable services honestly. A failed call is not a successful result; do not silently substitute a mock without a visible label.
- [ ] Keep demo data distinguishable from real users, customers, sources, or transactions.

## What evidence supports the claim?

- [ ] Link the actual source for factual claims and make it clear which text is a quote, summary, or inference.
- [ ] Separate observed user feedback from team assumptions and generated text.
- [ ] State who was included, how many people or cases were involved, when they were collected, and what was excluded.
- [ ] Do not describe a hand-written or development-tuned sample as an independent benchmark.
- [ ] Report the metric's denominator and the method used to compute it. Keep failed cases visible.

## What does the evaluation establish?

- [ ] Describe what the evaluation checks, and what it cannot check.
- [ ] Keep evaluation examples and success criteria separate from examples repeatedly used to tune the behavior.
- [ ] Do not turn a formatting, schema, or smoke check into an accuracy, safety, or user-value claim.
- [ ] Record the code, model, prompt, and dataset versions for any result that matters.

## What happens to user data?

- [ ] Say whether inputs leave the device, are stored, and when they are deleted.
- [ ] Keep API keys on the server; never put them in browser assets, screenshots, logs, or committed config.
- [ ] Use synthetic data in a public demo unless participants have agreed to the use shown.
- [ ] Identify authentication, access-control, or safety gaps before exposing a prototype publicly.

## Does the demo represent the product?

- [ ] A screenshot or video shows the actual app state; label edits, mock paths, and sped-up footage.
- [ ] Do not imply that an integration, deployment, test, or human review happened if it did not.
- [ ] Make the user action and the result visible; avoid narrating a result before it appears.
- [ ] Say what the prototype does not do, especially where a user might rely on it for a consequential decision.

## Current starter-specific disclosure

The included brief builder is deterministic template code. It makes no model calls, does not search the web, stores no submissions, and does not contact real participants. The included evaluation checks only output structure and input-text carry-through. It is a development smoke check, not evidence that a brief is useful or that a product idea has demand.
