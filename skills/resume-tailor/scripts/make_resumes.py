#!/usr/bin/env python3
"""Build tailored resumes (DOCX + PDF), shrink to one page if needed, and verify facts.

Usage: python3 make_resumes.py <facts.json> <outDir> [variant|all] [--pages 1]
Needs: node + docx (npm), LibreOffice (soffice) and poppler (pdfinfo, pdftotext).
"""
import json, os, subprocess, sys, glob, shutil

here = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if len(args) < 2:
    sys.exit(__doc__)
facts_path, out_dir = args[0], args[1]
which = args[2] if len(args) > 2 else 'all'
max_pages = int(sys.argv[sys.argv.index('--pages') + 1]) if '--pages' in sys.argv else 1
facts = json.load(open(facts_path))
keys = list(facts['variants']) if which == 'all' else which.split(',')
os.makedirs(out_dir, exist_ok=True)
soffice = shutil.which('soffice') or shutil.which('libreoffice')

def pages(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    return int(next(l.split()[-1] for l in out.splitlines() if l.startswith('Pages')))

def build(key, limits, nproj):
    subprocess.run(['node', os.path.join(here, 'build_resume.js'), facts_path, out_dir, key, ','.join(map(str, limits)), str(nproj)], check=True, capture_output=True)
    docx = os.path.join(out_dir, facts['variants'][key]['file'] + '.docx')
    subprocess.run([soffice, '--headless', '--convert-to', 'pdf', '--outdir', out_dir, docx], check=True, capture_output=True)
    return docx[:-5] + '.pdf'

report = []
for key in keys:
    limits = list(facts.get('limits', {}).get('bullets') or [len(r['bullets']) for r in facts['experience']])
    nproj = facts.get('limits', {}).get('projects', 3)
    while True:
        pdf = build(key, limits, nproj)
        n = pages(pdf)
        if n <= max_pages:
            break
        # shrink: projects first (keep >=1), then the longest role's bullets (keep >=3)
        if nproj > 1:
            nproj -= 1
        else:
            i = max(range(len(limits)), key=lambda j: limits[j])
            if limits[i] <= 3:
                break
            limits[i] -= 1
    text = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    missing = [m for m in facts.get('must_keep', []) if m not in text]
    report.append({'variant': key, 'pdf': pdf, 'pages': n, 'bullet_limits': limits, 'projects': nproj, 'missing_facts': missing})
print(json.dumps(report, indent=1))
