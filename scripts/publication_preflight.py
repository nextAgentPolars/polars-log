#!/usr/bin/env python3
"""Read-only publication gate. Inspect committed bytes, never a live log export."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def scan(text):
    patterns = {
        'credential': r'(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})',
        'private-key': r'-----BEGIN (?:[A-Z ]*PRIVATE KEY)',
        'encrypted-payload': r'gAAAAA[A-Za-z0-9_-]{30,}',
        'internal-protocol': r'Engram Persistent Memory|base_instructions|<environment_context>|<permissions instructions>',
        'auth-header': r'(?i)(?:authorization\s*[:=]\s*["\x27]?bearer\s+)[A-Za-z0-9._-]{12,}',
        'url-credential': r'https?://[^\s/@:]+:[^\s/@]+@',
        'jwt': r'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]+',
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def validate_manifest(manifest, read):
    assert manifest['schema'] == 'polars.public-evidence-batch.v1'
    assert manifest['coverage']['session_coverage'] == 'not_exported'
    assert manifest['verification']['tests_rerun'] is False
    seen = set()
    for entry in manifest['files']:
        path = entry['path']
        assert path not in seen and not Path(path).is_absolute() and '..' not in Path(path).parts
        seen.add(path)
        data = read(path)
        assert len(data) == entry['bytes'], 'size mismatch: ' + path
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], 'digest mismatch: ' + path
        findings = scan(data.decode('utf-8'))
        assert not findings, 'publication scan failed: ' + path + ' categories=' + ','.join(findings)
    return seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-head', required=True)
    args = parser.parse_args()
    head = git('rev-parse', 'HEAD').decode().strip()
    assert head == args.expected_head, 'HEAD drift'
    assert not git('status', '--porcelain', '--untracked-files=no').strip(), 'tracked worktree/index dirty'
    git('diff', '--check', 'HEAD')
    paths = git('ls-tree', '-r', '--name-only', 'HEAD').decode().splitlines()
    manifests = [p for p in paths if p.startswith('batches/') and p.endswith('/manifest.json')]
    count = 0
    for path in manifests:
        prefix = str(Path(path).parent) + '/'
        raw = git('show', 'HEAD:' + path)
        assert not scan(raw.decode()), 'manifest publication scan failed'
        manifest = json.loads(raw)
        listed = validate_manifest(manifest, lambda p: git('show', 'HEAD:' + prefix + p))
        actual = {p[len(prefix):] for p in paths if p.startswith(prefix) and p != path}
        assert listed == actual, 'unlisted or missing batch files'
        count += len(listed)
    print(json.dumps({
        'schema': 'polars-log.publication-preflight.v1', 'status': 'passed',
        'worktree': str(ROOT), 'head': head,
        'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
        'publication_repository': 'nextAgentPolars/polars-log',
        'batches': len(manifests), 'hashed_files': count,
        'untracked_files_excluded': len(git('ls-files', '--others', '--exclude-standard').decode().splitlines()),
        'scope': 'committed batch hashes and pattern scan; not proof of complete redaction or historical test execution'
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
