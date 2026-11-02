#!/usr/bin/env python3
"""CLI utility to ingest an Experiment HTML submission file, extract Python code,
pad to 50 lines, embed theory in comments, and generate a custom PowerShell delivery command."""

import sys
import re
import html
import textwrap
import urllib.request
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

def clean_artifacts(text: str) -> str:
    replacements = {
        '\u2011': '-',
        '\u2013': '-',
        '\u2014': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2022': '-',
        '\u2500': '-',
        '\u00b0': ' deg ',
        '\xa0': ' ',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def parse_experiment_html(html_path: Path):
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'b', 'strong'])

    # 1. Aim / Title
    title = ""
    for h in headings:
        txt = h.get_text().strip().lower()
        if 'aim' in txt or 'objective' in txt:
            curr = h.next_sibling
            while curr:
                if getattr(curr, 'name', None) in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    break
                if getattr(curr, 'get_text', None):
                    t = curr.get_text().strip()
                    if t:
                        title = t
                        break
                curr = curr.next_sibling
            if title:
                break
    if not title:
        title = soup.title.string.strip() if soup.title else html_path.stem.replace('_', ' ')

    # 2. Theory
    theory = ""
    for h in headings:
        txt = h.get_text().strip().lower()
        if 'theory' in txt:
            parts = []
            curr = h.next_sibling
            while curr:
                if getattr(curr, 'name', None) in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    break
                if getattr(curr, 'get_text', None):
                    t = curr.get_text().strip()
                    if t:
                        parts.append(t)
                curr = curr.next_sibling
            theory = '\n\n'.join(parts)
            break

    # 3. Source Code
    code = ""
    for h in headings:
        txt = h.get_text().strip().lower()
        if 'source code' in txt or 'code' in txt:
            curr = h.next_sibling
            while curr:
                if getattr(curr, 'name', None) in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    break
                if getattr(curr, 'name', None) == 'pre' or (getattr(curr, 'find', None) and curr.find('pre')):
                    code = curr.get_text().strip()
                    break
                curr = curr.next_sibling
            if code:
                break

    if not code:
        for pre in soup.find_all(['pre', 'code']):
            t = pre.get_text().strip()
            if any(k in t for k in ['def ', 'import ', 'print(', 'class ']):
                code = t
                break

    if not code:
        raise ValueError(f"Could not locate Python source code in {html_path}")

    # Clean code artifacts
    code = clean_artifacts(code)
    code = re.sub(r'for_in\s+', 'for _ in ', code)
    code = code.replace('visited=sewt()', 'visited = set()')
    code = re.sub(r'\breturn true\b', 'return True', code)
    code = re.sub(r'\breturn false\b', 'return False', code)

    # Pad code to at least 50 lines
    lines = code.strip().split('\n')
    while len(lines) < 50:
        if len(lines) == 49:
            lines.append('# --- Line 50: Execution & Theory Division ---')
        else:
            lines.append('')
    padded_code = '\n'.join(lines)

    # Format theory comment block
    clean_theory = clean_artifacts(theory)
    theory_lines = [
        "",
        "# " + "=" * 76,
        "# EXPERIMENT THEORY (from AISC Laboratory Submission):",
        "# " + "=" * 76,
    ]
    for para in clean_theory.split('\n'):
        para = para.strip()
        if not para:
            theory_lines.append("#")
        else:
            for w in textwrap.wrap(para, width=74):
                theory_lines.append("# " + w)
    theory_lines.append("# " + "=" * 76)

    final_code = padded_code + "\n" + "\n".join(theory_lines) + "\n"
    return title, final_code

def publish_to_dpaste(filename: str, code: str) -> str:
    script = f"""# LabX Remote - Custom Experiment Delivery
$filename = "{filename}"
$code = @'
{code}
'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " [OK] Experiment code saved to: $filename" -ForegroundColor Green
Write-Host " Theory is embedded after line 50. Ready to execute!" -ForegroundColor White
Write-Host " Run: py $filename" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
"""
    data = urllib.parse.urlencode({
        'content': script,
        'format': 'url',
        'expiry_days': '30'
    }).encode('utf-8')

    req = urllib.request.Request('https://dpaste.org/api/', data=data, method='POST')
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip()
        slug = url.split('/')[-1]
        return f"irm https://aisccli.netlify.app/s/{slug} | iex"

def main():
    if len(sys.argv) < 2:
        print("Usage: py scripts/ingest_html.py <path_to_experiment.html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"File not found: {html_path}")
        sys.exit(1)

    print(f"Ingesting: {html_path.name}...")
    title, final_code = parse_experiment_html(html_path)
    total_lines = len(final_code.splitlines())
    filename = html_path.stem.lower().replace('-', '_') + ".py"

    print(f"[OK] Title: {title}")
    print(f"[OK] Code lines: {total_lines} (Theory begins after line 50)")

    # Save local copy
    out_file = Path(filename)
    out_file.write_text(final_code, encoding='utf-8')
    print(f"[OK] Saved local file: {out_file.resolve()}")

    try:
        cmd = publish_to_dpaste(filename, final_code)
        print("\n" + "=" * 60)
        print(" YOUR CUSTOM POWERSHELL DELIVERY COMMAND:")
        print("=" * 60)
        print(f"\n  {cmd}\n")
        print("=" * 60)
        print("Run that command from any PowerShell terminal to pull this code!")
    except Exception as e:
        print(f"Could not publish online: {e}")

if __name__ == "__main__":
    main()

