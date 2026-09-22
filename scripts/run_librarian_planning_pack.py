from pathlib import Path
p=Path('docs/index.html')
c=p.read_text(encoding='utf-8')

def rep(a,b,label):
    global c
    if a not in c:
        raise SystemExit('Missing '+label)
    c=c.replace(a,b,1)

rep("""'Librarian:demand-analytics':'librarian-demand-analytics-2026-09-22-v1',
'Librarian:curriculum-mapping':'librarian-curriculum-mapping-2026-09-22-v1',
'Librarian:usage-heatmap':'librarian-usage-heatmap-2026-09-22-v1',
'Librarian:command-center':'librarian-command-center-2026-09-22-v1'""",
"""'Librarian:collection-gap':'librarian-collection-gap-2026-09-22-v1',
'Librarian:budget-forecast':'librarian-budget-forecast-2026-09-22-v1',
'Librarian:reading-achievement':'librarian-reading-achievement-2026-09-22-v1',
'Librarian:document-generator':'librarian-document-generator-2026-09-22-v1'""",'release batch')

rep("""if(role==='Librarian'&&label==='Book Demand / Waitlist Analytics')return 'Librarian:demand-analytics';
if(role==='Librarian'&&label==='Curriculum Resource Mapping')return 'Librarian:curriculum-mapping';
if(role==='Librarian'&&label==='Library Usage Heatmap')return 'Librarian:usage-heatmap';
if(role==='Librarian'&&label==='Librarian Command Center')return 'Librarian:command-center';
return null;""",
"""if(role==='Librarian'&&label==='Collection Gap Analysis')return 'Librarian:collection-gap';
if(role==='Librarian'&&label==='Library Budget Forecast')return 'Librarian:budget-forecast';
if(role==='Librarian'&&label==='Reading Achievement Dashboard')return 'Librarian:reading-achievement';
if(role==='Librarian'&&label==='Document Generator')return 'Librarian:document-generator';
return null;""",'feature ids')

rep("""if(activeRole==='Librarian'&&b.classList.contains('node')){
  if(label==='Library Dashboard'&&featureUnseen('Librarian:command-center'))unseen=true;
  if(label==='Catalog & Collection'&&featureUnseen('Librarian:curriculum-mapping'))unseen=true;
  if(label==='Reports'&&(featureUnseen('Librarian:demand-analytics')||featureUnseen('Librarian:usage-heatmap')))unseen=true;
}""",
"""if(activeRole==='Librarian'&&b.classList.contains('node')){
  if(label==='Catalog & Collection'&&featureUnseen('Librarian:collection-gap'))unseen=true;
  if(label==='Acquisitions'&&featureUnseen('Librarian:budget-forecast'))unseen=true;
  if(label==='Reports'&&(featureUnseen('Librarian:reading-achievement')||featureUnseen('Librarian:document-generator')))unseen=true;
}""",'highlights')

rep("'Catalog & Collection':['Book Catalog','New Arrivals','Shelf Location Finder','Barcode / ISBN Lookup','Digital Resources','Book Donation Management','Bulk Import Books','Archive / Withdrawn Books','Accession Register','Periodicals / Magazine Management','Subscription Renewal Alerts','Curriculum Resource Mapping','Duplicate / Data Quality Checker','Collection Weeding Review'],",
"'Catalog & Collection':['Book Catalog','New Arrivals','Shelf Location Finder','Barcode / ISBN Lookup','Digital Resources','Book Donation Management','Bulk Import Books','Archive / Withdrawn Books','Accession Register','Periodicals / Magazine Management','Subscription Renewal Alerts','Curriculum Resource Mapping','Collection Gap Analysis','Duplicate / Data Quality Checker','Collection Weeding Review'],",'catalog menu')
rep("'Acquisitions':['Acquisition Requests','Book Request Approval Queue','Approved Requests','Ordered Books','Received Books','Teacher Resource Requests','Budget & Acquisition Tracking','Publisher / Supplier Directory'],",
"'Acquisitions':['Acquisition Requests','Book Request Approval Queue','Approved Requests','Ordered Books','Received Books','Teacher Resource Requests','Budget & Acquisition Tracking','Library Budget Forecast','Publisher / Supplier Directory'],",'acquisitions menu')
rep("'Reports':['Reports & Export Center','Circulation Report','Overdue Report','Inventory Report','Visitor Report','Reading Program Report','Year-End Statistics Dashboard','Library KPI Dashboard','Book Demand / Waitlist Analytics','Library Usage Heatmap','Collection Age Analysis','Library Audit Trail','Library Incident & Behavior Log','Full Library Backup & Restore']",
"'Reports':['Reports & Export Center','Circulation Report','Overdue Report','Inventory Report','Visitor Report','Reading Program Report','Year-End Statistics Dashboard','Library KPI Dashboard','Reading Achievement Dashboard','Document Generator','Book Demand / Waitlist Analytics','Library Usage Heatmap','Collection Age Analysis','Library Audit Trail','Library Incident & Behavior Log','Full Library Backup & Restore']",'reports menu')

anchor='const librarianModuleBase=openModule;'
if anchor not in c: raise SystemExit('Missing module anchor')
block=r'''
/* Librarian collection gap, budget forecast, reading achievement, and document generator pack */
const libraryViewPlanningBase=libraryView;
libraryView=function(view){
  const special=['Collection Gap Analysis','Library Budget Forecast','Reading Achievement Dashboard','Document Generator'];
  if(!special.includes(view))return libraryViewPlanningBase(view);
  featureOpened(view);currentModule=view;
  if(typeof libraryAudit==='function')libraryAudit('Opened '+view,view);
  const r=demoPanel(view,'Librarian workspace · Demo');
  $('module-back').hidden=true;

  if(view==='Collection Gap Analysis'){
    const books=Array.isArray(libraryState.books)?libraryState.books:[];
    const maps=Array.isArray(libraryState.curriculumMappings)?libraryState.curriculumMappings.filter(x=>x.status!=='Archived'):[];
    const keyMap=new Map();
    maps.forEach(m=>{
      const key=(m.grade||'Unspecified')+'|'+(m.subject||'Unspecified');
      if(!keyMap.has(key))keyMap.set(key,{grade:m.grade||'Unspecified',subject:m.subject||'Unspecified',mapped:new Set(),competencies:new Set()});
      keyMap.get(key).mapped.add(m.bookId);
      if(m.competency)keyMap.get(key).competencies.add(m.competency);
    });
    const rows=[...keyMap.values()].map(x=>{
      const mapped=x.mapped.size;
      const target=5;
      const gap=Math.max(0,target-mapped);
      return [x.grade,x.subject,mapped,x.competencies.size,target,gap,gap===0?'Adequate':gap<=2?'Needs Attention':'Priority Gap'];
    }).sort((a,b)=>b[5]-a[5]);
    const mappedIds=new Set(maps.map(x=>x.bookId));
    const unmapped=books.filter(b=>!mappedIds.has(b.id));
    r.append(card('COLLECTION GAP ANALYSIS',[
      books.length+' catalog title(s)',
      maps.length+' active curriculum mapping record(s)',
      rows.filter(x=>x[5]>0).length+' grade/subject area(s) below the demo target of 5 mapped resources',
      unmapped.length+' catalog title(s) are not yet mapped to the curriculum.'
    ]));
    if(rows.length)r.append(table(['Grade','Subject','Mapped Titles','Competencies','Target','Gap','Status'],rows));
    else r.append(card('NO CURRICULUM MAPPINGS YET',['Add curriculum mappings first to generate collection-gap results.']));
    if(unmapped.length)r.append(table(['Unmapped Book ID','Title','Category','Shelf'],unmapped.slice(0,25).map(b=>[b.id,b.title,b.category||'—',b.shelf||'—'])));
  }

  if(view==='Library Budget Forecast'){
    const acquisitions=Array.isArray(libraryState.acquisitions)?libraryState.acquisitions:[];
    const periodicals=Array.isArray(libraryState.periodicals)?libraryState.periodicals:[];
    const maintenance=Array.isArray(libraryState.maintenanceRequests)?libraryState.maintenanceRequests:[];
    const repairs=Array.isArray(libraryState.repairs)?libraryState.repairs:[];
    const teacherRequests=Array.isArray(libraryState.teacherRequests)?libraryState.teacherRequests:[];
    const approved=acquisitions.filter(x=>['Approved','Ordered','Received','Committed','Paid'].includes(x.status));
    const acquisitionEstimate=approved.reduce((s,x)=>s+Number(x.amount||x.cost||x.total||0),0);
    const subscriptionEstimate=periodicals.reduce((s,x)=>s+Number(x.renewalCost||x.cost||0),0);
    const maintenanceEstimate=maintenance.filter(x=>!['Resolved','Completed','Closed'].includes(x.status)).reduce((s,x)=>s+Number(x.estimatedCost||x.cost||0),0);
    const repairEstimate=repairs.filter(x=>!['Completed','Closed','Returned'].includes(x.status)).reduce((s,x)=>s+Number(x.estimatedCost||x.cost||0),0);
    const requestEstimate=teacherRequests.filter(x=>!['Declined','Rejected'].includes(x.status)).reduce((s,x)=>s+Number(x.estimatedCost||x.cost||0),0);
    const total=acquisitionEstimate+subscriptionEstimate+maintenanceEstimate+repairEstimate+requestEstimate;
    const budgetObj=libraryState.budget||{};
    const approvedBudget=Number(budgetObj.amount||budgetObj.annual||budgetObj.total||0);
    const remaining=approvedBudget?approvedBudget-total:null;
    r.append(card('LIBRARY BUDGET FORECAST',[
      'Projected commitments from current demo records · ₱'+total.toLocaleString(),
      approvedBudget?'Configured annual budget · ₱'+approvedBudget.toLocaleString():'No annual budget amount is configured yet.',
      approvedBudget?'Projected remaining · ₱'+remaining.toLocaleString():'Use Budget & Acquisition Tracking to maintain official demo budget figures.'
    ]));
    r.append(table(['Forecast Area','Projected Amount'],[
      ['Approved / active acquisitions','₱'+acquisitionEstimate.toLocaleString()],
      ['Periodical / subscription renewals','₱'+subscriptionEstimate.toLocaleString()],
      ['Open maintenance requests','₱'+maintenanceEstimate.toLocaleString()],
      ['Open book repairs','₱'+repairEstimate.toLocaleString()],
      ['Teacher resource requests','₱'+requestEstimate.toLocaleString()],
      ['TOTAL FORECAST','₱'+total.toLocaleString()]
    ]));
    r.append(card('FORECAST NOTE',['This planning view uses values already stored in the browser-local demo. Missing cost fields are treated as ₱0.']));
  }

  if(view==='Reading Achievement Dashboard'){
    const loans=Array.isArray(libraryState.loans)?libraryState.loans:[];
    const programs=Array.isArray(libraryState.readingPrograms)?libraryState.readingPrograms:[];
    const completedLoans=loans.filter(x=>x.returned);
    const readers=new Map();
    completedLoans.forEach(l=>{
      const name=l.borrower||l.name||l.student||'Unknown Reader';
      readers.set(name,(readers.get(name)||0)+1);
    });
    const ranking=[...readers.entries()].sort((a,b)=>b[1]-a[1]);
    const categories={};
    completedLoans.forEach(l=>{
      const b=typeof libraryBook==='function'?libraryBook(l.bookId):null;
      const cat=(b&&b.category)||'Uncategorized';categories[cat]=(categories[cat]||0)+1;
    });
    r.append(card('READING ACHIEVEMENT DASHBOARD',[
      completedLoans.length+' completed / returned loan record(s)',
      ranking.length+' reader(s) with completed borrowing activity',
      programs.length+' reading-program record(s) in the demo.'
    ]));
    if(ranking.length)r.append(table(['Rank','Reader','Books Completed','Achievement'],ranking.slice(0,20).map((x,i)=>[i+1,x[0],x[1],x[1]>=10?'Gold Reader':x[1]>=5?'Silver Reader':x[1]>=3?'Bronze Reader':'Reading Starter'])));
    else r.append(card('NO COMPLETED READING DATA YET',['Returned loan records will build the reader achievement ranking.']));
    const catRows=Object.entries(categories).sort((a,b)=>b[1]-a[1]);
    if(catRows.length)r.append(table(['Category','Completed Reads'],catRows));
    if(programs.length)r.append(table(['Program','Participant / Group','Progress','Status'],programs.slice(0,20).map(x=>[x.title||x.program||x.name||'Reading Program',x.participant||x.student||x.group||'—',x.progress||x.booksRead||x.count||'—',x.status||'Active'])));
  }

  if(view==='Document Generator'){
    if(!libraryState.documentDraft)libraryState.documentDraft={type:'Library Clearance',name:'',reference:'',details:''};
    r.append(card('DOCUMENT GENERATOR',[
      'Create a printable demo document from common library transactions.',
      'Available: Library Clearance, Lost Book Notice, Donation Acknowledgement, Overdue Notice, Inventory Report, Borrowing Confirmation.'
    ]));
    const f=form([
      {key:'type',label:'Document type',options:['Library Clearance','Lost Book Notice','Donation Acknowledgement','Overdue Notice','Inventory Report','Borrowing Confirmation']},
      {key:'name',label:'Student / donor / borrower / recipient'},
      {key:'reference',label:'Reference / ID / book ID'},
      {key:'details',label:'Additional details',type:'textarea'}
    ],'GENERATE PREVIEW',v=>{
      libraryState.documentDraft={...v,date:staffDate()};librarySave();libraryView(view);
    });
    r.append(f);
    const d=libraryState.documentDraft;
    if(d&&d.date){
      const lines=[
        'CHILD DEVELOPMENT & GUIDANCE CENTER',
        'LIBRARY SERVICES',
        d.type.toUpperCase(),
        'Date · '+d.date,
        d.name?'Name / Recipient · '+d.name:'',
        d.reference?'Reference · '+d.reference:'',
        d.details?'Details · '+d.details:'',
        'Generated from School Orbit Librarian Demo'
      ].filter(Boolean);
      r.append(card(d.type,lines));
      r.append(action('PRINT DOCUMENT',()=>window.print(),'primary'));
      r.append(action('CLEAR PREVIEW',()=>{libraryState.documentDraft={type:'Library Clearance',name:'',reference:'',details:''};librarySave();libraryView(view)},'outline'));
      if(typeof libraryAudit==='function')libraryAudit('Generated '+d.type,'Document Generator');
    }
  }
  syncFeatureHighlights();
};
'''
c=c.replace(anchor,block+'\n'+anchor,1)
p.write_text(c,encoding='utf-8')
