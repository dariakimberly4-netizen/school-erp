from pathlib import Path
p=Path('docs/index.html')
c=p.read_text(encoding='utf-8')
marker='/* LIBRARIAN VISUAL CLEANUP 2026-09-22 */'
if marker in c:
    print('Visual cleanup already applied')
    raise SystemExit(0)

old="""banner.hidden=false;
banner.classList.toggle('features-unseen',pending);
const title=banner.querySelector('strong');
const titleText=activeRole==='Staff'?'CONNECTED STAFF WORKFLOWS':activeRole==='Librarian'?'NEW LIBRARY FEATURES':'STAFF OPERATIONS';
if(title&&title.textContent!==(pending?'NEW · ':'')+titleText)title.textContent=(pending?'NEW · ':'')+titleText;
if(activeRole==='Librarian'){
  const p=banner.querySelector('p');
  if(p)p.textContent=pending?'Gold modules are newly added. Open one and its highlight disappears.':'All new Librarian features have been opened.';
}"""
new="""if(activeRole==='Librarian'&&!pending){
  banner.hidden=true;
  banner.classList.remove('features-unseen');
}else{
  banner.hidden=false;
  banner.classList.toggle('features-unseen',pending);
  const title=banner.querySelector('strong');
  const titleText=activeRole==='Staff'?'CONNECTED STAFF WORKFLOWS':activeRole==='Librarian'?'NEW LIBRARY FEATURES':'STAFF OPERATIONS';
  if(title&&title.textContent!==(pending?'NEW · ':'')+titleText)title.textContent=(pending?'NEW · ':'')+titleText;
  if(activeRole==='Librarian'){
    const p=banner.querySelector('p');
    if(p)p.textContent='Gold modules are newly added. Open one and its highlight disappears.';
  }
}"""
if old not in c:
    raise SystemExit('Missing Librarian banner logic')
c=c.replace(old,new,1)

style_anchor='/* LIBRARIAN QA CLEANUP 2026-09-22 */'
if style_anchor not in c:
    raise SystemExit('Missing QA style anchor')
css="""\n/* LIBRARIAN VISUAL CLEANUP 2026-09-22 */\n#orbit .library-hub-center .center-count{background:var(--cdgc-green)!important;color:#fff!important;border:1px solid rgba(255,255,255,.8);box-shadow:none!important}\n#new-feature-banner[hidden]{display:none!important;margin:0!important;padding:0!important}\n#app:has(#new-feature-banner[hidden]) .orbit-wrap{margin-top:0!important}\n"""
c=c.replace(style_anchor,marker+'\n'+css+style_anchor,1)
p.write_text(c,encoding='utf-8')
