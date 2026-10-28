# Architecture

## Implemented boundary

```text
local UTF-8 contract JSON
    → bounded reader and strict JSON decoder
    → version/shape/path validation
    → exact comparison of declared expected outputs
    → contract_valid or contract_invalid
```

This boundary does not open a PDF, invoke an extractor, compare actual outputs, or prove a fixture valid.
The CLI always reports `extraction_evaluated: false`. Runtime code depends only on Python's standard library.

## Proposed full pipeline

```text
canonical synthetic invoice + seed + transformation
    → original/changed fixture models + independently checked answer keys
    → original/changed PDF renderings + visual validation
    → explicit extractor adapter OR externally prepared JSON files
    → bounded output parsing and declared normalization
    → absolute correctness + paired relation + repeat-run stability
    → JSON results + self-contained HTML reproduction bundle
```

### Components and responsibilities

| Component | Owns | Must not own |
|---|---|---|
| Fixture model | Business facts, stable IDs, dependencies, Decimal calculations | Predictions from the extractor |
| Transform library | Preconditions and intended changes | Arbitrary edits to untrusted PDFs |
| Renderer | Faithful layout and source previews | Ground-truth decisions based on OCR output |
| Adapter boundary | Explicit invocation/import, version and config capture | Hidden credentials or model-generated shell commands |
| Evaluator | Exact expected values, declared tolerances, path deltas, result classification | Guessing truth from agreement |
| Reporter | Escaped, local, reproducible evidence | Uploading documents or claiming certification |

## Package shape

Current modules are deliberately few: `contracts.py` for parsing/validation, `cli.py` for process I/O,
and `__main__.py` for module invocation. Add separate `fixtures`, `transforms`, `evaluate`, and `report`
modules only as milestones are implemented. Avoid premature plugin registries or runtime discovery.

## Data and numeric choices

- Version every persisted contract and bundle format.
- Represent money as decimal strings. Proposed arithmetic uses `decimal.Decimal`, never binary floats.
- Keep dates unambiguous ISO strings; future accepted input formats must be declared.
- Keep missing properties different from explicit null, false, empty string, and zero.
- Use stable line-item identities in the future canonical model. Current declaration validation compares arrays by index;
  it performs no semantic row alignment. Added/removed arrays are atomic path changes.
- Normalization must be explicit and auditable, never a fuzzy repair that hides errors.
- Changing quantity may legitimately change multiple monetary fields. Contracts list all dependent paths.

## Planned result model

`PASS`: fixture valid, required outputs present, absolute assertions and relation assertions passed.
`FAIL`: valid evidence contradicts one or more assertions.
`INCONCLUSIVE`: outcome cannot be assessed (missing output, timeout, unresolved alignment, unstable run policy).
`INVALID_FIXTURE`: malformed contract or invalid/incorrectly rendered generated pair.

Stability is a separate dimension, not a replacement for these results. The final precedence and aggregate policy
must be specified and tested before implementation. An empty suite can never yield PASS.

## Reproduction bundle proposal

A future bundle should contain a manifest, contract, canonical before/after models, PDFs, previews,
expected outputs, observed outputs, run metadata, result JSON, and HTML. Manifest records generator/version,
seed, adapter identity/version, explicit settings, timestamps, and content hashes. Hashes detect changes;
they do not prove that a source is authoritative, truthful, private, or safe.

Replay verifies the retained artifact hashes and re-evaluates saved outputs; it must not call a model.
Re-execution is a distinct action because stochastic models may produce different outputs and paid services may
incur cost. Never silently substitute replay for a new evaluation or vice versa.

## Dependencies and deployment

Today: Python 3.11+, standard library at runtime, setuptools for optional package installation.
Planned PDF renderer must be selected after a small evaluation of licensing, reproducible fonts, cross-platform
behavior, and security maintenance. No PDF renderer is installed or claimed functional in this scaffold.
A static HTML template needs no web framework. A model/SDK dependency belongs in an optional adapter,
not the core. Record and manually review dependency versions when introduced.

No daemon, database, account system, telemetry, cloud dependency, container requirement, or network service.
Do not claim a sandbox because processing is local. Resource limits and operating-system isolation are distinct.
