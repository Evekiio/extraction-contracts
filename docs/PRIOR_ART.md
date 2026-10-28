# Prior art and positioning

Research snapshot: 27 October 2026. These links establish related work, not product endorsements or independently
reproduced benchmark results. Source descriptions may evolve. No third-party source or dataset is bundled here.

## Existing approaches

- [Wobbly](https://github.com/tarunagarwal1981/wobbly): generic metamorphic testing with custom relations and
  receipt-total examples. It supports invariance and scaling. We should reuse or credit suitable work rather than
  claim a new method. The proposed contribution here is document-specific fixture authoring and structured-output
  contracts around rendered pairs, not the invention of relation-based testing.
- [Invoice Extraction Benchmark](https://github.com/DrewKraken/invoice-extraction-benchmark): synthetic invoice
  documents, generator, answer keys, and scoring. Synthetic invoices and deterministic scoring are not new.
  Our proposed emphasis is explicit paired changes for a user's pipeline and a portable regression reproduction.
- [DocILE](https://github.com/rossumai/docile): document information localization/extraction and line-item recognition
  benchmark with evaluation tooling. Our small controlled suite is not a replacement for broad benchmark coverage.
- [Evidence-bound document extraction](https://github.com/LucidPaths/evidence-bound-document-extraction): exact source
  identity and quoted-span checks, explicitly distinct from proving semantic support. This project instead proposes
  behavioral tests under controlled changes; citation location and extraction correctness are different questions.

## Evidence of practical need

[AWS's document-processing sample documentation](https://github.com/aws-solutions-library-samples/accelerated-intelligent-document-processing-on-aws/blob/main/docs/extraction-and-confidence.md)
discusses incomplete structured extraction, row-count signals, and configuration-dependent failure handling.
It illustrates why successful execution or valid JSON alone is not sufficient evidence of complete extraction.
It is not a claim that every AWS deployment has that behavior.

[Consistent Document-Level Relation Extraction via Counterfactuals](https://arxiv.org/abs/2407.06699)
studies consistency under controlled entity replacements in relation extraction. That task is not invoice OCR;
it is relevant background on counterfactual testing, not validation of this proposed implementation.

## Honest distinction

The proposed combination is **controlled PDF pairs + multi-field expected-change contracts + reproducible visual
failure reports**. We have not established that no similar tool exists, and do not claim a world first, scientific
novelty, or market demand. The evidence spike must compare the workflow with existing options and justify why a
separate small package is worthwhile. Contributing upstream is a valid outcome.

## Reuse and licensing

The initial scaffold is original code and documentation under MIT. Before copying code, fonts, images, datasets,
or examples, inspect their exact licenses, preserve notices, and review compatibility. Links and methodological
acknowledgments do not grant permission to redistribute third-party artifacts. No client material is needed.
