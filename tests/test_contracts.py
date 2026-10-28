import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from extraction_contracts.contracts import ContractError, validate_contract, load_contract, changed_paths, MAX_BYTES
from extraction_contracts.cli import main

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/due-date.contract.json'

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(EXAMPLE.read_text())

    def test_valid_controlled_change(self):
        self.assertIsNone(validate_contract(self.contract))

    def test_valid_invariant(self):
        self.contract.update(relation='invariant', allowed_changes=[], required_changes=[],
                             expected_after=copy.deepcopy(self.contract['expected_before']))
        validate_contract(self.contract)

    def test_missing_and_unknown_fields(self):
        for key in self.contract:
            with self.subTest(key=key):
                value = self.contract.copy(); del value[key]
                with self.assertRaises(ContractError): validate_contract(value)
        self.contract['secret'] = 'x'
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_version_not_bool_or_future(self):
        for version in (True, '1', 2, None):
            with self.subTest(version=version):
                self.contract['version'] = version
                with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_invalid_ids(self):
        for value in ('', '../secret', 'Upper', 'a'*65, None, '-start'):
            self.contract['id'] = value
            with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_unknown_relation(self):
        self.contract['relation'] = 'guess'
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_paths_must_be_unique_array(self):
        for value in ('/due_date', None, ['/due_date', '/due_date'], [1]):
            self.contract['allowed_changes'] = value
            with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_invalid_pointer_syntax(self):
        for path in ('', 'due_date', '/a~2', '/a~'):
            self.contract['allowed_changes'] = [path]
            self.contract['required_changes'] = [path]
            with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_required_must_be_allowed(self):
        self.contract['allowed_changes'] = []
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_required_must_actually_change(self):
        self.contract['expected_after'] = self.contract['expected_before'].copy()
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_unexpected_delta_rejected(self):
        self.contract['expected_after']['total'] = '999.00'
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_invariant_rejects_change(self):
        self.contract['relation'] = 'invariant'
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_controlled_change_needs_required_path(self):
        self.contract['required_changes'] = []
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_expected_root_must_be_object(self):
        self.contract['expected_before'] = []
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_float_rejected_from_library(self):
        self.contract['expected_before']['total'] = 120.0
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_depth_limit(self):
        value = {}; leaf = value
        for _ in range(34): leaf['x'] = {}; leaf = leaf['x']
        self.contract['expected_before'] = value
        with self.assertRaises(ContractError): validate_contract(self.contract)

    def test_missing_null_and_zero_are_distinct(self):
        self.assertEqual(changed_paths({}, {'x':None}), {'/x'})
        self.assertEqual(changed_paths({'x':None}, {'x':0}), {'/x'})
        self.assertEqual(changed_paths({'x':True}, {'x':1}), {'/x'})
        self.assertEqual(changed_paths({'x':0}, {'x':0}), set())

    def test_pointer_escaping(self):
        self.assertEqual(changed_paths({'a/b': {'~x': 1}}, {'a/b': {'~x': 2}}), {'/a~1b/~0x'})

    def test_array_semantics(self):
        self.assertEqual(changed_paths({'x':[1,2]}, {'x':[1,3]}), {'/x/1'})
        self.assertEqual(changed_paths({'x':[1,2]}, {'x':[1]}), {'/x'})

    def test_removed_container_is_atomic(self):
        self.assertEqual(changed_paths({'x':{'a':1}}, {}), {'/x'})

    def test_valid_example_files(self):
        for path in EXAMPLE.parent.glob('*.contract.json'): load_contract(path)

    def test_loader_rejects_bad_json(self):
        bad = [b'{', b'\xff', b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1.5}', b'[]', b'x'*(MAX_BYTES+1)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input.json'
            for value in bad:
                with self.subTest(prefix=value[:30]):
                    path.write_bytes(value)
                    with self.assertRaises(ContractError): load_contract(path)

    def test_cli_is_explicit_not_evaluation(self):
        out = io.StringIO()
        with redirect_stdout(out): code = main(['validate-contract', str(EXAMPLE)])
        result = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result['status'], 'contract_valid')
        self.assertIs(result['extraction_evaluated'], False)

    def test_cli_error_does_not_echo_input_or_path(self):
        err = io.StringIO()
        with redirect_stderr(err): code = main(['validate-contract', '/nonexistent/private-name'])
        self.assertEqual(code, 2)
        self.assertNotIn('private-name', err.getvalue())
        self.assertEqual(json.loads(err.getvalue())['status'], 'input_unreadable')

    def test_cli_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'bad.json'; path.write_text('{"private":"secret"}')
            err = io.StringIO()
            with redirect_stderr(err): code = main(['validate-contract', str(path)])
            self.assertEqual(code, 2)
            self.assertNotIn('secret', err.getvalue())
            self.assertEqual(json.loads(err.getvalue())['status'], 'contract_invalid')

if __name__ == '__main__': unittest.main()
