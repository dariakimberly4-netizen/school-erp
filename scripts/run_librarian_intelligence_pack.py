from pathlib import Path

wf = Path('.github/workflows/add-librarian-intelligence-pack.yml').read_text(encoding='utf-8')
marker = "python - <<'PY'"
start = wf.index(marker) + len(marker) + 1
end = wf.index("\n          PY", start)
raw = wf[start:end].splitlines()
code = "\n".join(line[10:] if line.startswith("          ") else line for line in raw)
exec(compile(code, 'embedded_librarian_intelligence_pack.py', 'exec'))
