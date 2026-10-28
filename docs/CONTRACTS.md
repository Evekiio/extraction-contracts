# Contract declaration format, version 1

This document describes the **implemented declaration validator**. It does not describe a shipped extraction
runner or a general JSON Schema implementation. The format may change before a stable release.

## Required and only accepted fields

| Field | Current rule |
|---|---|
| `version` | Integer 1; Boolean true is not accepted as integer 1 |
| `id` | 1-64 lowercase letters/digits/hyphens; first character letter or digit |
| `relation` | `invariant` or `controlled_change` |
| `allowed_changes` | Unique non-root JSON Pointer strings |
| `required_changes` | Unique non-root JSON Pointer strings, subset of allowed changes |
| `expected_before` | JSON object containing the declared original answer key |
| `expected_after` | JSON object containing the declared changed answer key |

Unknown fields and duplicate JSON keys are rejected. Input is UTF-8 and at most 1 MiB. Expected-value nesting
is capped at 32 levels. JSON floats, Infinity, and NaN are rejected; use decimal strings such as `"120.00"`
for monetary values. Integers, strings, booleans, null, objects, and arrays are supported.

The two [example declarations](../examples/) demonstrate a due-date change and layout invariance. They are
synthetic JSON only: no rendered PDFs or actual extractor results accompany them yet.

## Path and comparison semantics

Paths follow non-root RFC 6901 syntax: `/due_date`, `/items/0/quantity`, or `/a~1b` for key `a/b`.
Use `~0` for a literal tilde and `~1` for a slash. Other tilde escapes are invalid. A path is an exact location,
not a wildcard or an authorization for every descendant. Root replacement is not supported.

Current change calculation is structural and type-sensitive:

- Changed scalar or type: that path changes; `true` and `1` are different.
- Added or removed object key: the path of that key changes, including when its value is a container.
- Two existing objects: compare keys recursively.
- Equal-length arrays: compare items by index.
- Different-length arrays: the array path changes atomically.

Thus optional-field deletion is different from setting it to null. An array removal is not evidence of correct
line-item alignment. Semantic alignment is planned and must not be inferred from this validator.

Every declared expected delta must be allowed; every required path must actually change. Invariant contracts
must have no allowed/required/actual changes. Controlled-change contracts must require at least one actual change.
The validator does not know whether the answer keys describe a real or correctly rendered document.

## Current process interface

`validate-contract PATH` exits 0 for a valid declaration and prints JSON with `status: contract_valid`,
`contract_id`, and `extraction_evaluated: false`. Invalid/unreadable input exits 2, emits a stable status code
to stderr, and still reports `extraction_evaluated: false`. Argument syntax errors use argparse's normal exit 2.
`--version` prints the scaffold version.

No evaluate/run/generate command is implemented. A valid declaration is not a passing extraction test.

## Future extensions, not implemented

A separately versioned run record will bind contract ID/hash, source PDFs and fixture hashes, adapter/configuration,
outputs and repeat index. Evaluation must independently compare each observed output against its own answer key,
then verify the pair's intended delta. Contract consistency alone cannot detect a consistently wrong extractor.

Future normalization policies must declare decimal precision, date handling, accepted missing representation,
unknown keys, ordering, and row identity. Do not silently coerce types or round to make a test pass. Add an explicit
schema migration and compatibility tests before changing these semantics.
