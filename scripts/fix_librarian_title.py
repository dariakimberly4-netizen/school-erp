from pathlib import Path
p=Path('docs/index.html')
c=p.read_text(encoding='utf-8')
old="function syncChild(){$('child-bar').hidden=activeRole!=='Parent';if(activeRole==='Parent'){$('child-select').replaceChildren(...children.map(c=>{const o=el('option',c.name+' · '+c.grade);o.value=c.id;return o}));$('child-select').value=selectedChild;$('welcome').textContent=child().name+'’s school orbit'}else $('welcome').textContent='Your school orbit'}"
new="function syncChild(){$('child-bar').hidden=activeRole!=='Parent';if(activeRole==='Parent'){$('child-select').replaceChildren(...children.map(c=>{const o=el('option',c.name+' · '+c.grade);o.value=c.id;return o}));$('child-select').value=selectedChild;$('welcome').textContent=child().name+'’s school orbit'}else $('welcome').textContent=activeRole==='Librarian'?'Librarian Orbit':'Your school orbit'}"
if old not in c:
    raise SystemExit('syncChild title logic not found')
c=c.replace(old,new,1)
p.write_text(c,encoding='utf-8')
