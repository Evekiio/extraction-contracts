# Threat model and limits

## Assets and trust boundaries

Protect local documents, extracted values, credentials, output integrity, and the user's confidence in reports.
Inputs and model outputs are data, never instructions. A fixture author and evaluator maintainer may make mistakes;
the design must make these mistakes inspectable rather than conceal them behind scores.

The implemented boundary is local JSON declaration validation only. Future PDF parsing/rendering and adapters
increase the attack surface and require separate review before shipment.

| Threat | Implemented now | Required before the relevant feature ships |
|---|---|---|
| Malformed/ambiguous JSON | Duplicate-key, unsupported-field/type, nesting and size rejection | Fuzz tests and stable failure classes |
| Floating-point monetary errors | JSON floats rejected; examples use strings | Decimal arithmetic, precision and rounding contracts |
| False pass without extraction | Explicit `extraction_evaluated: false` | Nonempty suite and complete evidence requirements |
| File/network exfiltration | No network or adapter implementation | No hidden network; explicit remote opt-in and data approval |
| Document prompt injection | No document/model execution | Treat document/model text as inert data; never run proposed commands |
| HTML/script injection | No report renderer yet | Escape text, local assets, no active document payloads, network checks |
| Malicious PDF / resource exhaustion | No PDF support yet | Bounded parsing, file/page limits, timeout isolation, pinned maintained dependencies |
| Ground-truth contamination | Declaration-only scope clearly stated | Independent fixture/render validation and negative controls |
| Stochastic output misdiagnosed | No extractor results yet | Same-input repeats and separate stability evidence |
| Corrupted reproduction bundle | No bundle implementation yet | Hash verification; reject inconsistent metadata rather than silently repair |

## Privacy defaults

Use fictional invoices only. Do not include client names, documents, screenshots, credentials, production traces,
or private code in this repository. A report is a copy of its inputs and outputs and can itself be sensitive.
Local processing does not make public sharing safe. No automatic upload, export to a third party, or telemetry.

A future external adapter must state destination, data, expected cost, and retention assumptions before use.
It must not inherit arbitrary credentials or commands from document text. No browser/session automation is required.

## What the project cannot prove

A passing finite synthetic suite cannot prove correctness on arbitrary real documents, eliminate hallucinations,
establish regulatory compliance, or certify an extractor as secure. A hash does not establish truth. A low error
rate on one template does not transfer to another. Agreement between models is not an answer key. No claim of
production readiness should appear until supported by appropriate review and operational evidence, and even then
it must remain bounded to an explicit use case.
