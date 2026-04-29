#!/usr/bin/env python3
"""
Checks if upstream skill sources have new H2 sections not present in our version.
Uses content-based comparison (not SHA) to avoid false positives from condensed imports.

Logic:
- Download upstream file
- Extract all H2 section headings (## Title)
- Download our file, extract our H2 headings (excluding CUSTOM sections)
- If upstream has H2 sections we don't have → real update, open Issue
- SHA differences alone are ignored (expected: we condense imports)

NEVER modifies any file — read-only check only.
Custom sections (CUSTOM:START / CUSTOM:END) are always preserved and shown in Issue.
"""

import os
import re
import base64
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


def get_file_content(owner, repo, path, headers):
    """Fetch and decode file content from GitHub API."""
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return None
    data = r.json()
    try:
        return base64.b64decode(data.get('content', '')).decode('utf-8')
    except Exception:
        return None


def extract_h2_sections(text):
    """
    Extract all H2 headings (## Title) from markdown text.
    Normalize: lowercase, strip punctuation, collapse spaces.
    Returns a set of normalized heading strings.
    """
    headings = re.findall(r'^##\s+(.+)$', text, re.MULTILINE)
    normalized = set()
    for h in headings:
        # Normalize: lowercase, strip special chars, collapse spaces
        clean = re.sub(r'[^\w\s]', '', h.lower())
        clean = re.sub(r'\s+', ' ', clean).strip()
        normalized.add(clean)
    return normalized


def strip_custom_sections(text):
    """Remove CUSTOM:START...CUSTOM:END blocks before comparing."""
    return re.sub(
        r'<!--\s*CUSTOM:START.*?-->.+?<!--\s*CUSTOM:END\s*-->',
        '',
        text,
        flags=re.DOTALL
    )


def extract_custom_sections(text):
    """Extract content between CUSTOM:START and CUSTOM:END markers."""
    match = re.search(
        r'<!--\s*CUSTOM:START.*?-->(.+?)<!--\s*CUSTOM:END\s*-->',
        text, re.DOTALL
    )
    return match.group(1).strip() if match else ''


def get_existing_update_issue():
    """Check if an open update issue already exists."""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues'
    r = requests.get(url, headers=HEADERS_REPO, params={
        'state': 'open', 'labels': 'skill-update'
    }, timeout=10)
    if r.status_code == 200:
        for issue in r.json():
            if '[Skill Update Check]' in issue.get('title', ''):
                return issue['number']
    return None


def create_issue(updates):
    """Open a GitHub Issue listing all genuine upstream updates."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    title = f'[Skill Update Check] New upstream sections detected — {today}'

    lines = [
        '## New upstream skill sections detected',
        '',
        f'Checked on: {today}',
        '',
        '> **This is a notification only.** No files have been modified.',
        '> These are H2 sections present upstream but missing in our version.',
        '> Review each and add to our skill if useful.',
        '',
        '---',
        '',
    ]

    for skill_path, info in updates.items():
        owner, repo, upstream_path = info['source']
        new_sections = info['new_sections']
        custom = info.get('custom_sections', '')

        lines.append(f'### `{skill_path}`')
        lines.append(f'- **Source:** `{owner}/{repo}/{upstream_path}`')
        lines.append(f'- **Upstream URL:** https://github.com/{owner}/{repo}/blob/main/{upstream_path}')
        lines.append(f'- **New sections ({len(new_sections)}):**')
        for s in sorted(new_sections):
            lines.append(f'  - `{s}`')
        if custom:
            lines.append('')
            lines.append('**⚠️ Our custom sections to preserve when updating:**')
            lines.append('```')
            lines.append(custom[:600] + ('...' if len(custom) > 600 else ''))
            lines.append('```')
        lines.append('')

    lines += [
        '---',
        '',
        '## How to update a skill',
        '',
        '1. Read the upstream file via GitHub MCP',
        '2. Identify the new sections listed above',
        '3. Add them to our SKILL.md (before the CUSTOM:START block)',
        '4. Keep all content between CUSTOM:START and CUSTOM:END unchanged',
        '5. Close this issue after updating',
        '',
        '_Generated by `.github/workflows/check-skill-updates.yml`_',
        '_Comparison method: new H2 sections in upstream not present in our version_',
    ]

    body = '\n'.join(lines)

    # Ensure label exists
    requests.post(
        f'https://api.github.com/repos/{OWNER}/{REPO}/labels',
        headers=HEADERS_REPO,
        json={'name': 'skill-update', 'color': '0075ca',
              'description': 'Upstream skill update available'},
        timeout=10
    )

    # Close existing open issue if present
    existing = get_existing_update_issue()
    if existing:
        requests.patch(
            f'https://api.github.com/repos/{OWNER}/{REPO}/issues/{existing}',
            headers=HEADERS_REPO,
            json={'state': 'closed'},
            timeout=10
        )

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
    print(f'Checking {len(SKILL_SOURCES)} skills for new upstream sections...')
    updates = {}

    for our_path, (owner, repo, upstream_path) in SKILL_SOURCES.items():
        print(f'\n  Checking: {our_path}')

        upstream_text = get_file_content(owner, repo, upstream_path, HEADERS)
        if upstream_text is None:
            print(f'    WARNING: upstream not found: {owner}/{repo}/{upstream_path}')
            continue

        our_text = get_file_content(OWNER, REPO, our_path, HEADERS_REPO)
        if our_text is None:
            print(f'    WARNING: our file not found: {our_path}')
            continue

        # Compare H2 sections (ignoring our custom sections)
        our_text_clean = strip_custom_sections(our_text)
        upstream_h2 = extract_h2_sections(upstream_text)
        our_h2 = extract_h2_sections(our_text_clean)

        new_sections = upstream_h2 - our_h2

        if new_sections:
            print(f'    NEW SECTIONS FOUND ({len(new_sections)}):')
            for s in sorted(new_sections):
                print(f'      - {s}')
            custom = extract_custom_sections(our_text)
            updates[our_path] = {
                'source': (owner, repo, upstream_path),
                'new_sections': new_sections,
                'custom_sections': custom,
            }
        else:
            print(f'    OK: no new sections upstream')

    if updates:
        print(f'\n{len(updates)} skills have new upstream sections — opening Issue...')
        create_issue(updates)
    else:
        print('\nAll skills are up to date. No issue needed.')


if __name__ == '__main__':
    main()
