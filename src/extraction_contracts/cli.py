"""A deliberately narrow CLI: validate a declaration, never claim extraction passed."""
import argparse
import json
import sys
from . import __version__
from .contracts import ContractError, load_contract

def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an extraction contract declaration (pre-alpha).")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate-contract", help="Validate JSON declaration only; no extractor runs")
    validate.add_argument("path")
    args = parser.parse_args(argv)
    try:
        contract = load_contract(args.path)
    except (OSError, ContractError) as exc:
        # Do not echo document contents, local paths, or native parser diagnostics.
        code = "contract_invalid" if isinstance(exc, ContractError) else "input_unreadable"
        print(json.dumps({"status": code, "extraction_evaluated": False}), file=sys.stderr)
        return 2
    print(json.dumps({"status": "contract_valid", "contract_id": contract["id"], "extraction_evaluated": False}, sort_keys=True))
    return 0
