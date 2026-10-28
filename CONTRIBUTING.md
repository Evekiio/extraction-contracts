# Contributing

This initial proposal is open for review, not an invitation to expand into a platform.
Please discuss scope before adding a new document type, runtime, or service.

## Local checks

Requires Python 3.11 or newer. Runtime validation uses only the standard library.

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m extraction_contracts validate-contract examples/due-date.contract.json
PYTHONPATH=src python -m extraction_contracts --version
```

On PowerShell set `$env:PYTHONPATH="src"`, then run the same Python commands without the prefix.
Optional development installation: `python -m pip install -e .`. This uses setuptools and may
fetch build dependencies. Direct source execution above does not require package installation.

Use a feature branch, meaningful commits, and a draft PR. Include test results and any checks
that were not run. Do not add GitHub Actions, auto-merge, updater bots, or scheduled jobs.
No generated customer data, screenshots from work, secrets, or private code belong in a PR.

A regression test must fail for the intended reason before its fix and pass afterward.
Counterexamples should contain the smallest manually understandable synthetic case, but automated
PDF shrinking is out of scope. Favor explicit contracts and readable tests over abstractions.
