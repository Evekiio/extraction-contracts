# Validation record

Date: 27 October 2026. Stage: review scaffold, not an extraction product release.
Environment exercised: Linux, Python 3.12.14. Python 3.11+ is the declared target; other versions and
Windows/macOS have not been tested in this run.

## Passed locally

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m extraction_contracts validate-contract examples/due-date.contract.json
PYTHONPATH=src python -m extraction_contracts --version
```

- 25 unit/CLI tests passed, covering valid declarations, invalid fields, strict version/ID/relation handling,
  malformed paths, required/allowed/actual delta relationships, invariant/controlled-change rules, floats,
  nesting, duplicate keys, malformed UTF-8/JSON, oversized inputs, missing/null/zero/type distinctions,
  array and escaped-path behavior, and no input/path echo in CLI errors.
- Both synthetic declaration examples loaded successfully.
- CLI smoke output explicitly reports `extraction_evaluated: false`.
- Version output: `0.0.1`.
- Local Markdown relative links checked for existing destinations.
- Python files compiled with `compileall`; TOML parsed successfully.
- No workflow files, scheduled jobs, updater configurations, secrets, or third-party code/data bundled.

## Not run / not implemented

- No PDF generation, PDF rendering QA, actual extraction evaluation, adapter call, model benchmark, or HTML report.
- No cross-platform test matrix, formal verification, fuzzing campaign, or independent security audit.
- No hosted CI; automation is deliberately absent.
- Optional setuptools installation/build has not been exercised; documented direct-source commands were tested.
- Future feature acceptance criteria in PLAN.md are not present-tense test results.

## Review interpretation

These tests establish the behavior of the narrow declaration validator. They do not establish that a generated
document matches an answer key, that any extractor is correct, or that the proposed product is useful.
The evidence-spike gate remains open.
