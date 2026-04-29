#!/usr/bin/env python3
"""
Checks if upstream skill sources have been updated since we imported them.
Opens a GitHub Issue if any updates are found.
NEVER modifies any file — read-only check only.

Protection guarantee:
- Only reads files, never writes
- Custom sections (between CUSTOM:START and CUSTOM:END) are shown in the
  issue so the maintainer knows exactly what to preserve
"""

import os
import re
import json
import requests
from datetime import datetime, timezone

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO_TOKEN = os.environ.get('REPO_TOKEN', '')
OWNER = 'Skills-Universal'
REPO = 'skills-universal'

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}
HEADERS_REPO = {
    'Authorization': f'token {REPO_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# Map: our skill path -> upstream source
# Format: 'our/path/SKILL.md': ('owner', 'repo', 'upstream/path/SKILL.md')
SKILL_SOURCES = {
    'L1-foundations/incremental-implementation/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/incremental-implementation/SKILL.md'
    ),
    'L1-foundations/debugging-and-error-recovery/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/debugging-and-error-recovery/SKILL.md'
    ),
    'L1-foundations/spec-driven-development/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/spec-driven-development/SKILL.md'
    ),
    'L1-foundations/planning-and-task-breakdown/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/planning-and-task-breakdown/SKILL.md'
    ),
    'L1-foundations/security-and-hardening/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/security-and-hardening/SKILL.md'
    ),
    'L1-foundations/documentation-and-adrs/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/documentation-and-adrs/SKILL.md'
    ),
    'L1-foundations/frontend-ui-engineering/SKILL.md': (
        'addyosmani', 'agent-skills', 'skills/frontend-ui-engineering/SKILL.md'
    ),
    'L4-vertical/odoo-19/SKILL.md': (
        'unclecatvn', 'agent-skills', 'skills/odoo-19.0/SKILL.md'
    ),
}


def get_upstream_sha(owner, repo, path):
    """Get SHA of file in upstream repo."""
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json().get('sha', '')
    return None


def get_our_sha(path):
    """Get SHA of file in our repo."""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}'
    r = requests.get(url, headers=HEADERS_REPO, timeout=10)
    if r.status_code == 200:
        return r.json().get('sha', '')
    return None


def get_our_custom_sections(path):
    """Extract custom sections from our skill file."""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}'
    r = requests.get(url, headers=HEADERS_REPO, timeout=10)
    if r.status_code != 200:
        return ''
    import base64
    content = base64.b64decode(r.json().get('content', '')).decode('utf-8')
    # Extract content between CUSTOM:START and CUSTOM:END
    match = re.search(
        r'<!--\s*CUSTOM:START.*?-->(.+?)<!--\s*CUSTOM:END\s*-->',
        content, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return ''


def get_existing_update_issue():
    """Check if an open update issue already exists."""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues'
    r = requests.get(url, headers=HEADERS_REPO, params={
        'state': 'open', 'labels': 'skill-update'
    }, timeout=10)
    if r.status_code == 200:
        issues = r.json()
        for issue in issues:
            if '[Skill Update Check]' in issue.get('title', ''):
                return issue['number']
    return None


def create_or_update_issue(updates):
    """Open a GitHub Issue listing all available upstream updates."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    title = f'[Skill Update Check] Upstream updates available — {today}'

    lines = [
        '## Upstream skill updates detected',
        '',
        f'Checked on: {today}',
        '',
        '> **This is a notification only.** No files have been modified.',
        '> Review each update and apply manually if useful.',
        '',
        '---',
        '',
    ]

    for skill_path, info in updates.items():
        owner, repo, upstream_path = info['source']
        custom = info.get('custom_sections', '')

        lines.append(f'### `{skill_path}`')
        lines.append(f'- **Source:** `{owner}/{repo}/{upstream_path}`')
        lines.append(f'- **Our SHA:** `{info["our_sha"][:12]}`')
        lines.append(f'- **Upstream SHA:** `{info["upstream_sha"][:12]}`')
        lines.append(f'- **Upstream URL:** https://github.com/{owner}/{repo}/blob/main/{upstream_path}')
        if custom:
            lines.append('')
            lines.append('**⚠️ Custom sections to preserve:**')
            lines.append('```')
            lines.append(custom[:500] + ('...' if len(custom) > 500 else ''))
            lines.append('```')
        lines.append('')

    lines += [
        '---',
        '',
        '## How to update a skill',
        '',
        '1. Read the upstream file via GitHub MCP',
        '2. Compare with our version',
        '3. Apply improvements, keep custom sections',
        '4. Close this issue after updating',
        '',
        '_Generated by `.github/workflows/check-skill-updates.yml`_',
    ]

    body = '\n'.join(lines)

    # Create label if it doesn't exist
    requests.post(
        f'https://api.github.com/repos/{OWNER}/{REPO}/labels',
        headers=HEADERS_REPO,
        json={'name': 'skill-update', 'color': '0075ca', 'description': 'Upstream skill update available'},
        timeout=10
    )

    # Close existing issue if present
    existing = get_existing_update_issue()
    if existing:
        requests.patch(
            f'https://api.github.com/repos/{OWNER}/{REPO}/issues/{existing}',
            headers=HEADERS_REPO,
            json={'state': 'closed'},
            timeout=10
        )

    # Open new issue
    r = requests.post(
        f'https://api.github.com/repos/{OWNER}/{REPO}/issues',
        headers=HEADERS_REPO,
        json={'title': title, 'body': body, 'labels': ['skill-update']},
        timeout=10
    )
    if r.status_code == 201:
        print(f'Issue created: {r.json()["html_url"]}')
    else:
        print(f'Failed to create issue: {r.status_code} {r.text}')


def main():
    print(f'Checking {len(SKILL_SOURCES)} skills against upstream sources...')
    updates = {}

    for our_path, (owner, repo, upstream_path) in SKILL_SOURCES.items():
        print(f'  Checking {our_path}...')

        our_sha = get_our_sha(our_path)
        upstream_sha = get_upstream_sha(owner, repo, upstream_path)

        if our_sha is None:
            print(f'    WARNING: our file not found: {our_path}')
            continue
        if upstream_sha is None:
            print(f'    WARNING: upstream not found: {owner}/{repo}/{upstream_path}')
            continue

        if our_sha != upstream_sha:
            print(f'    UPDATE AVAILABLE: {our_path}')
            custom = get_our_custom_sections(our_path)
            updates[our_path] = {
                'source': (owner, repo, upstream_path),
                'our_sha': our_sha,
                'upstream_sha': upstream_sha,
                'custom_sections': custom,
            }
        else:
            print(f'    OK: {our_path} is up to date')

    if updates:
        print(f'\n{len(updates)} updates available — opening GitHub Issue...')
        create_or_update_issue(updates)
    else:
        print('\nAll skills are up to date. No issue needed.')


if __name__ == '__main__':
    main()
