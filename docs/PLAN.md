# Project plan and software development outline

**Stage:** design review plus a narrow declaration-validator scaffold. **Target:** a small open-source
engineering tool, not a document-processing platform. No delivery date or production-readiness promise.

## Problem and intended users

Engineers maintaining PDF-to-JSON pipelines need to know when a prompt, parser, model, normalization
rule, or layout change silently alters structured facts. Schema-valid output is not enough. A regression
report should identify the smallest understandable controlled comparison, not just give an opaque score.

Primary users are document-automation engineers and developers reviewing extraction changes. A recruiter
should understand the demonstration without understanding model internals. An engineer should be able
to reproduce the failure, read its oracle, and challenge its assumptions.

## Product hypothesis

Document-specific paired fixtures will make some extraction regressions easier to diagnose than a fixed
corpus score or a generic input/output relation engine. This is a hypothesis to test, not established demand.
The project must earn its scope through an initial experiment, not grow because more features are possible.

## Requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| EC-01 | Original synthetic canonical fixture model | No client data; schema and independently checked expected values |
| EC-02 | Controlled fact and layout transformations | Each transform states its preconditions, changed facts, and dependent values |
| EC-03 | Three English/USD layouts | Rendered inspection confirms labels, table grouping, dates, and totals |
| EC-04 | Five initial transformation families | At least two valid pairs per family before expansion |
| EC-05 | Absolute and relational evaluation | Negative controls cannot pass through consistent wrong answers |
| EC-06 | Explicit missing/null/zero rules | Removal tests and type-sensitive assertions |
| EC-07 | Decimal-safe arithmetic | Decimal strings, declared precision, tax/rounding fixtures |
| EC-08 | Provider-neutral output import | JSON files; no built-in credential requirement |
| EC-09 | Repeat-run stability measurement | Same-input repeats; unstable results separated from deterministic failure |
| EC-10 | Reproducible report bundle | Inputs, versions, hashes, contract, outputs, and local replay instructions |
| EC-11 | Safe default operation | No telemetry, no uploads, no execution of document instructions |
| EC-12 | Honest result classes | Pass, fail, inconclusive, invalid fixture are distinguished |
| EC-13 | Small maintainable codebase | One package; new dependencies justified; no service stack |
| EC-14 | Manual release process | Local tests, branch, commit, draft PR, explicit review; no automated Actions |

## Milestone 0: review this proposal

Delivered scaffold: a strict JSON declaration validator, two original examples, package metadata, unit tests,
and these design documents. Review the problem, boundaries, license, first schema, terminology, and acceptance
gates. The validator checks declaration consistency only; it is not an evaluation engine.

Decision: accept the direction, narrow it, or stop. Do not treat approval of the proposal as proof of its hypothesis.

## Milestone 1: evidence spike / go-no-go

Produce ten valid pairs across five transformations. Run two independently implemented extraction paths with
pinned versions. Include one intentionally faulty implementation as a separate negative control, never as one
of the two independent paths used to substantiate external usefulness. A corrected reference establishes the
harness's mechanics, not model quality.

Record transformation validity, expected values, all observed outputs, full denominators, timing, and repeated
unchanged-input baselines. Continue if at least one nontrivial reproducible real-path failure is found OR the
workflow demonstrably reduces diagnosis/reproduction effort compared with a documented existing approach.
If neither occurs, narrow or contribute to existing tooling; do not manufacture a win.

## Milestone 2: fixture and contract engine

Implement a canonical invoice model, Decimal-based calculations, ISO dates, explicit optional fields, stable
line-item identities, three renderers, and the five transforms. Independently check rendered PDFs against fixture
values. No arbitrary PDF edits. Keep rendering and evaluation separate so extraction never supplies its own truth.

Advance when fixtures are visually inspected, repeated generation is stable under pinned dependencies, invalid
transformations are rejected, and both positive and negative oracle tests pass.

## Milestone 3: evaluation and replay

First accept previously produced JSON files. Then add a deliberately configured local adapter. Normalize only
what the contract explicitly permits. Check all expected fields, then the pair relationship, then stability.
Record missing, null, zero, malformed output, unmatched line items, ambiguous dates, and unsupported formats
separately. Report unresolved alignment as inconclusive, not a guessed match.

Advance when planted defects are detected for their intended reasons, correct outputs pass, corrupted bundles
are refused, timeouts cannot become pass, and reports replay without a model call.

## Milestone 4: presentation and release candidate

Build static HTML with side-by-side previews, expected/actual diffs, readable failure explanations, provenance,
and limitations. Escape all untrusted text, embed only local assets, and verify no outbound requests. Add a short
screen recording using synthetic examples. Keep terminal JSON output suitable for scripting.

Publish measured results with the exact dataset and versions. A bounded suite pass is not a security certification,
production reliability guarantee, or comparative model leaderboard. Manually test supported platforms before
listing them as tested. Release only after maintainer review, with reversible versioned commits.

## Proposed completion criteria

- All EC-01 through EC-14 requirements have linked evidence or an explicit deferred decision.
- A fresh checkout can reproduce the documented demo without an account or network request.
- Reference outputs pass and intentional failures fail for the stated reason.
- No hidden network, customer data, or cloud-model requirement in the default path.
- The README accurately reflects shipped behavior; every claim is backed by an artifact or labeled proposal.
- User-facing errors identify invalid/inconclusive conditions without leaking file contents or secrets.

## Main risks and mitigation

1. **False alarms from invalid mutations.** Generate from a canonical model; preserve dependencies and validate rendered pairs.
2. **Two wrong answers look consistent.** Require independent answer keys in addition to relation checks.
3. **Flaky models obscure regressions.** Repeat unchanged inputs and report stability separately; never selectively retain favorable runs.
4. **Scope grows into OCR/platform work.** Keep adapters external; defer arbitrary PDFs, multi-currency, and additional formats.
5. **Synthetic overfitting.** Publish template limitations; do not generalize synthetic success to real documents.
6. **Existing tools already suffice.** Compare against prior art during the evidence spike and prefer upstream contributions if appropriate.
7. **Report leaks input data.** Synthetic-only default; sharing any external dataset remains an explicit user decision.

## Review checklist

- Is the problem valuable enough for this narrow tool?
- Are five transformations and three layouts the right first boundary?
- Is exact JSON Pointer matching sufficiently clear before adding schema-aware normalization?
- Which two independent local extraction paths should the evidence spike evaluate?
- Is MIT appropriate for the original project, with third-party licenses reviewed before reuse?
- Are the go/no-go criteria demanding enough to avoid a demo-only repository?
