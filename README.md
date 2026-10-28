<div align="center">

# Extraction Contracts

### Change one fact. Catch every unintended change.

**A small, local-first testing toolkit for structured document extraction.**

[Review the plan](docs/PLAN.md) · [Architecture](docs/ARCHITECTURE.md) · [Contract format](docs/CONTRACTS.md) · [Validation](docs/VALIDATION.md)

</div>

---

## The idea in 30 seconds

An AI extractor can produce valid JSON and still read the wrong date, lose a line item,
or change a value that did not change in the document. This project asks a precise question:

**When we deliberately change a document, does the extracted data change exactly as it should?**

Start from a fictional invoice with a known answer key. Change its due date. The due-date field
should change; the invoice number, currency, and total should not. Rearrange the layout without
changing the facts, and the normalized output should stay the same.

The proposed toolkit turns these expectations into explicit, reproducible contracts. Its target
output is a portable report with the two documents, expected differences, actual differences, and
the rule that failed. It tests an extractor; it is not another extractor.

> **Status: review-stage / pre-alpha scaffold.** Only contract-declaration validation is implemented.
> PDF generation, extraction execution, output evaluation, and visual reports are planned, not shipped.
> The tagline describes the goal. Passing bounded tests will never prove that every real-world error is caught.

## What exists today

| Capability | Status | What it means |
|---|---|---|
| Python package and CLI | Implemented | Standard-library runtime, Python 3.11+ |
| Version-1 declaration validation | Implemented | Checks structure, exact expected deltas, and path rules |
| Synthetic JSON examples | Implemented | Due-date change and layout invariance declarations |
| Unit and CLI tests | Implemented | See dated local results in [VALIDATION](docs/VALIDATION.md) |
| Synthetic PDF pairs | Planned | Canonical data model, three controlled layouts |
| Extractor adapters and evaluation | Planned | Imported JSON first; explicit local adapter next |
| Static side-by-side HTML report | Planned | No hosted service, external assets, or telemetry |
| Accuracy benchmark / production readiness | Not claimed | No real extractor evaluation has been performed here |

## Try the part that works

From a checkout, with Python 3.11 or newer:

```sh
PYTHONPATH=src python -m extraction_contracts validate-contract examples/due-date.contract.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

The first command returns:

```json
{"contract_id": "due-date-isolation", "extraction_evaluated": false, "status": "contract_valid"}
```

That result validates the **declaration**, not an extractor. A command for generating PDFs or
scoring an extraction is intentionally not exposed yet. PowerShell and installation instructions
are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Planned demonstration

1. Render a clearly labeled synthetic invoice and its known answer key.
2. Change one due date, or one quantity with declared dependent totals.
3. Run the original and changed PDFs through the same extractor configuration.
4. Check both absolute correctness against the answer keys and the permitted output differences.
5. Display a failure such as “due date changed as expected; amount owed changed unexpectedly.”
6. Retain the documents, contract, outputs, versions, and hashes for offline reproduction.

A deliberately faulty demonstration adapter will be labeled as such. It demonstrates the test
mechanism, not a measured defect in a third-party model. Any later real-model result must include
its exact configuration, repeated runs, corpus, and limitations.

## Five bounded test families

| Transformation | Required behavior |
|---|---|
| Change an explicit due date | Only the due-date path changes |
| Change one line quantity | Quantity and declared dependent line/subtotal/total paths change |
| Change an invoice identifier | Only the identifier changes |
| Move a totals block without changing its contents | Business values remain invariant |
| Remove an optional purchase-order identifier | Follow the declared missing-value policy; do not retain or invent it |

Version one targets **synthetic, English, USD invoices in three layouts**. It is not a universal
PDF mutator. Changes originate in a canonical fixture model, then documents are rendered again.
This avoids blindly shuffling text and accidentally changing label/value relationships.

## Three separate questions

- **Correctness:** Does each output match its independently validated answer key?
- **Relationship:** Does the output delta obey the intended document change?
- **Stability:** Does repeating the same input produce inconsistent outputs?

Two consistently wrong answers must not pass correctness checks. An unstable extractor must not
be reported as deterministically broken without the appropriate evidence. Invalid fixtures,
missing outputs, malformed JSON, rendering failures, and timeouts must not become passes.

## Small by design

One Python package. One CLI. Explicit JSON contracts. Synthetic fixtures. A portable static report.

**Not in scope:** training a model, building OCR, arbitrary customer-document mutation, accounts,
a hosted dashboard, a database, vector search, agents, compliance certification, or automatic PDF
shrinking. No credentials or network calls in the default path. No GitHub Actions, scheduled jobs,
automated dependency updaters, or auto-merge.

The first go/no-go milestone is **ten valid document pairs and two independently implemented
extraction paths**. Continue only if they demonstrate a reproducible nontrivial failure or meaningfully
simpler regression diagnosis than existing tools. Otherwise narrow the proposal or contribute upstream.

## Engineering map

| Read | Purpose |
|---|---|
| [Project plan](docs/PLAN.md) | Requirements, phases, acceptance gates, and review decisions |
| [Architecture](docs/ARCHITECTURE.md) | Boundaries, data flow, dependencies, and operational choices |
| [Contract format](docs/CONTRACTS.md) | Current declaration schema and future evaluation semantics |
| [Threat model](docs/THREAT_MODEL.md) | Trust boundaries, privacy, and failure handling |
| [Prior art](docs/PRIOR_ART.md) | Existing work, honest differentiation, and source links |
| [Validation record](docs/VALIDATION.md) | Actual checks, not aspirational badges |

## Built on an existing idea, not a novelty claim

Metamorphic testing is established. [Wobbly](https://github.com/tarunagarwal1981/wobbly) already provides
generic relation-based AI testing; [Invoice Extraction Benchmark](https://github.com/DrewKraken/invoice-extraction-benchmark)
provides synthetic documents and scoring; [DocILE](https://github.com/rossumai/docile) evaluates document
fields and line items. This proposal focuses on **authored PDF pairs + explicit structured-output
change contracts + portable visual reproductions**. It does not claim to be the first of its kind.
No third-party implementation or dataset is bundled in this scaffold.

## Contribute and review

The current request is a project review. Proposed changes belong in draft PRs, with local verification
and clear distinctions between implemented behavior and roadmap. See [CONTRIBUTING](CONTRIBUTING.md),
[project orders](AGENTS.md), and [security notes](SECURITY.md).

Original scaffold code and documentation are available under the [MIT License](LICENSE).
