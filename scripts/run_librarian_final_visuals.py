from pathlib import Path
p=Path('docs/index.html')
c=p.read_text(encoding='utf-8')
marker='/* LIBRARIAN FINAL VISUALS 2026-09-22 */'
if marker in c:
    print('Final Librarian visuals already applied')
    raise SystemExit(0)

old="$('welcome').textContent='Library operations hub';"
new="$('welcome').textContent='Librarian Orbit';"
if old not in c:
    raise SystemExit('Missing Librarian title assignment')
c=c.replace(old,new,1)

anchor='/* LIBRARIAN VISUAL CLEANUP 2026-09-22 */'
if anchor not in c:
    raise SystemExit('Missing Librarian visual cleanup anchor')
css="""\n/* LIBRARIAN FINAL VISUALS 2026-09-22 */\n#app:has(#new-feature-banner[hidden]) .orbit-wrap:has(#orbit .librarian-node){margin-top:-76px!important}\n@media(max-width:650px){#app:has(#new-feature-banner[hidden]) .orbit-wrap:has(#orbit .librarian-node){margin-top:-38px!important}}\n"""
c=c.replace(anchor,marker+'\n'+css+anchor,1)
p.write_text(c,encoding='utf-8')
