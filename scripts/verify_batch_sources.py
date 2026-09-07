#!/usr/bin/env python3
"""Reproduce source artifacts from immutable local Git objects, without checkout."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from publication_preflight import validate_manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-repo', required=True)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    batch = Path(args.batch)
    manifest = json.loads((batch / 'manifest.json').read_text())
    validate_manifest(manifest, lambda p: (batch / p).read_bytes())

    def git(*argv):
        return subprocess.check_output(['git', '-C', args.source_repo, *argv])

    assert git('rev-parse', manifest['source_end_commit'] + '^{tree}').decode().strip() == manifest['source_end_tree']
    verified = 0
    for entry in manifest['files']:
        source = entry['provenance']
        kind = source['kind']
        if kind == 'editorial_navigation':
            continue
        if kind == 'git_command':
            argv = source['argv']
            assert argv[:4] == ['show', '--format=', '--no-ext-diff', '--no-renames']
            assert argv[4] == source['commit'] and argv[5] == '--'
            assert all(p.endswith('.go') and not p.startswith('-') for p in argv[6:])
            actual = git(*argv)
            assert git('rev-parse', source['commit'] + '^{tree}').decode().strip() == source['tree']
        elif kind == 'git_blob_lines':
            ref = source['commit'] + ':' + source['path']
            raw = git('show', ref)
            assert git('rev-parse', ref).decode().strip() == source['blob']
            assert hashlib.sha256(raw).hexdigest() == source['source_sha256']
            actual = b''.join(raw.splitlines(keepends=True)[source['line_start'] - 1:source['line_end']])
        elif kind == 'git_commit_inventory':
            rows = []
            for commit in git('rev-list', '--reverse', source['reachable_from']).decode().splitlines():
                fields = git('show', '-s', '--format=%H%x00%T%x00%P%x00%cI%x00%s', commit).decode().strip().split('\0')
                if datetime.datetime.fromisoformat(fields[3]) <= datetime.datetime.fromisoformat(source['committer_time_after_exclusive']):
                    continue
                rows.append(dict(zip(source['fields'], fields)))
            assert len(rows) == manifest['coverage']['commit_count']
            actual = ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows).encode()
        else:
            raise ValueError('unknown provenance kind')
        assert actual == (batch / entry['path']).read_bytes(), 'source mismatch: ' + entry['path']
        verified += 1
    print(json.dumps({'schema': 'polars-log.source-verification.v1', 'status': 'passed',
                      'source_end_commit': manifest['source_end_commit'],
                      'source_artifacts_reproduced': verified,
                      'manifest_sha256': hashlib.sha256((batch / 'manifest.json').read_bytes()).hexdigest(),
                      'tests_rerun': False}))


if __name__ == '__main__':
    main()
