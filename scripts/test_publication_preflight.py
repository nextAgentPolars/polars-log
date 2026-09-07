import hashlib
import unittest
from publication_preflight import scan, validate_manifest


class PublicationGateTests(unittest.TestCase):
    def fixture(self):
        data = b'public source evidence\n'
        return data, {'schema': 'polars.public-evidence-batch.v1',
                      'coverage': {'session_coverage': 'not_exported'},
                      'verification': {'tests_rerun': False},
                      'files': [{'path': 'evidence.txt', 'bytes': len(data),
                                 'sha256': hashlib.sha256(data).hexdigest()}]}

    def test_valid(self):
        data, manifest = self.fixture()
        self.assertEqual(validate_manifest(manifest, lambda _: data), {'evidence.txt'})

    def test_tampering_rejected(self):
        data, manifest = self.fixture()
        with self.assertRaises(AssertionError):
            validate_manifest(manifest, lambda _: data.replace(b'public', b'edited'))

    def test_traversal_rejected(self):
        data, manifest = self.fixture()
        manifest['files'][0]['path'] = '../escape'
        with self.assertRaises(AssertionError):
            validate_manifest(manifest, lambda _: data)

    def test_synthetic_credential_rejected(self):
        self.assertIn('credential', scan('sk-' + 'x' * 30))

    def test_duplicate_rejected(self):
        data, manifest = self.fixture()
        manifest['files'] *= 2
        with self.assertRaises(AssertionError):
            validate_manifest(manifest, lambda _: data)


if __name__ == '__main__':
    unittest.main()
