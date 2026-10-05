#!/usr/bin/env python3
"""Local seven-deliverable Codex runtime. No publication actions."""
from __future__ import annotations
import argparse,concurrent.futures,contextlib,fcntl,hashlib,json,os,re,shutil,subprocess,sys,time,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SKILLS=ROOT/'.agents/skills'
CONFIG=ROOT/'config.toml'
class Stop(Exception):pass
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def cfg():return tomllib.loads(CONFIG.read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def local(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to(root.resolve()):raise Stop('Path escapes its case: '+str(name))
 return p
def pins():
 repo=ROOT.parent
 for name,h in read(repo/'source-pins.json').items():
  p=local(repo,name)
  if not p.is_file() or sha(p)!=h:raise Stop('Runtime or skill changed since packaging: '+name)
 state=ROOT/'installation.json'
 if not state.is_file():raise Stop('Run python3.11 install.py before using the runtime')
 profiles=read(state).get('profiles',{})
 if len(profiles)!=3:raise Stop('Installation must pin all three model profiles')
 for name,h in profiles.items():
  p=Path(name)
  if not p.is_file() or sha(p)!=h:raise Stop('Installed model profile changed: '+p.name)
@contextlib.contextmanager
def lock(path):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('a') as f:
  try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise Stop('Another operation is active: '+str(path))
  try:yield
  finally:fcntl.flock(f,fcntl.LOCK_UN)
def case(path):
 c=Path(path).resolve();d=read(c/'case.json')
 if d['deliverable'] not in cfg()['deliverables']:raise Stop('Unknown deliverable')
 return c,d
def initialise(deliverable,dest,brief,options=2,destination=None,mode='new'):
 if deliverable not in cfg()['deliverables']:raise Stop('Unknown deliverable')
 if options<1 or options>20:raise Stop('Options must be 1–20')
 if deliverable=='linkedin-banner' and destination not in ('personal','business'):raise Stop('Banner destination must be personal or business')
 dest=Path(dest).resolve()
 if dest.exists():raise Stop('Case folder already exists; refusing overwrite')
 brief=Path(brief).resolve()
 if not brief.is_file():raise Stop('Supply a real local brief file')
 dest.mkdir(parents=True);(dest/'brief').mkdir();shutil.copy2(brief,dest/'brief'/brief.name)
 write(dest/'case.json',{'deliverable':deliverable,'options':options,'mode':mode,'destination':destination,'created':time.time(),'reviews':[]})
 (dest/'case-notes.md').write_text('# Case notes\n\nRecord sources, approved copy, brand assets, specification/date, option-count source, art directions, image plan and unresolved facts.\n')
 rows=[]
 for i in range(1,options+1):
  for sub in ['source','site','assets','images','exports','previews','checks']:(dest/f'option-{i}'/sub).mkdir(parents=True)
  rows.append({'option':i,'thesis':'','copy_file':'','expected_artifacts':[],'required_checks':cfg()['deliverables'][deliverable]['required_checks']})
 write(dest/'production.json',{'copy_approved':False,'approval_evidence':'','blockers':[],'variants_source':'','options':rows})
 return dest
def plan(c,d):
 p=read(c/'production.json')
 if p.get('copy_approved') is not True or not p.get('approval_evidence'):raise Stop('Approved copy and approval evidence are required')
 if not p.get('variants_source'):raise Stop('Record the option-count source')
 if p.get('blockers'):raise Stop('Resolve build blockers: '+json.dumps(p['blockers']))
 rows=p.get('options',[])
 if [r.get('option') for r in rows]!=list(range(1,d['options']+1)):raise Stop('Plan must cover every option exactly once')
 for row in rows:
  if not row.get('thesis') or not local(c,row.get('copy_file','')).is_file():raise Stop('Each option needs a thesis and exact copy file')
  outputs=row.get('expected_artifacts',[])
  if not outputs or len(set(outputs))!=len(outputs):raise Stop('Inventory every expected output without duplicates')
  for name in outputs:
   path=local(c,name)
   if not path.is_relative_to(c/f'option-{row["option"]}'):raise Stop('An output belongs to the wrong option')
  if not row.get('required_checks') or len(set(row['required_checks']))!=len(row['required_checks']):raise Stop('Specify unique mechanical checks for every option')
  mandatory=set(cfg()['deliverables'][d['deliverable']]['required_checks'])
  if not mandatory.issubset(row['required_checks']):raise Stop('Plan omitted mandatory deliverable checks')
 return p
def rubric(skill):
 lines=[l[2:].strip() for l in (SKILLS/skill/'REVIEW.md').read_text().splitlines() if l.startswith('- ')]
 return {f'R{i:03}':text for i,text in enumerate(lines,1)}
def launch(role,prompt,work,out,images=()):
 pins();rc=cfg()['roles'][role];out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 argv=[shutil.which('codex') or 'codex','exec','--strict-config','--profile',rc['profile'],'--model',rc['model'],'--sandbox',rc['sandbox'],'--skip-git-repo-check','-C',str(work),'--json','-o',str(out)]
 for img in images:argv+=['-i',str(img)]
 argv+=['-']
 events=out.with_suffix('.events.jsonl');err=out.with_suffix('.stderr.txt')
 with events.open('w') as log,err.open('w') as errors:
  proc=subprocess.run(argv,input=prompt,text=True,stdout=log,stderr=errors,timeout=rc['timeout_minutes']*60)
 if proc.returncode:raise Stop(f'{role} failed ({proc.returncode}); see {err}')
 sessions=[]
 for line in events.read_text().splitlines():
  try:x=json.loads(line)
  except ValueError:continue
  if x.get('type')=='thread.started':sessions.append(x['thread_id'])
 if len(sessions)!=1:raise Stop('Cannot establish a fresh session identity: '+str(events))
 if not out.is_file():raise Stop('Model produced no final response')
 return sessions[0],out.read_text()
def build(c,d,repair=False):
 p=plan(c,d);skill=SKILLS/d['deliverable'];history=read(c/'build-history.json') if (c/'build-history.json').exists() else []
 local_failure=c/'review/local-failures.json'
 if repair and not local_failure.exists() and not (c/'review/latest.json').exists():raise Stop('Repair requires recorded local failures or an independent review')
 latest=(read(local_failure) if local_failure.exists() else read(c/'review/latest.json')) if repair else None
 repairs=int(d.get('repairs_started',0))
 if repair and repairs>=cfg()['workflow']['max_repair_rounds']:raise Stop('Repair budget exhausted')
 if history and not repair:raise Stop('Already built; use repair after independent review')
 selected=[r for r in p['options'] if not repair or any(o['option']==r['option'] and o['status']=='fail' for o in latest['options'])]
 if not selected:raise Stop('No builder-repairable options; resolve blockers with a person')
 if repair:
  d['repairs_started']=repairs+1;write(c/'case.json',d)
 def one(row):
  n=row['option'];folder=c/f'option-{n}';spec=cfg()['deliverables'][d['deliverable']]
  prompt=f'''Build exactly option {n} of {d['deliverable']}. You are a stage-specific Sol builder, not the orchestrator. Read {skill/'SKILL.md'} and {skill/'REVIEW.md'} fully, then {c/'case-notes.md'}, {c/'production.json'} and {local(c,row['copy_file'])}. Never edit these inputs, skills or config. Write only inside {folder}. Other options belong to other builders.
Plan: {json.dumps(row)}
Deliverable production requirements: {spec['requirements']}
Mechanical helper: {sys.executable} {ROOT/'tools/design.py'} (png/pdf/fullpng/preview/pagecheck/emailcheck/inspect/sheet). Images/reference art must already be supplied by the orchestrator using Codex image_gen; do not substitute coded shapes for required imagery. If missing, report BLOCKED. Preserve exact copy; do not invent facts or logos. Do not deploy, upload or send. For a web stage do not start another harness or nested workflow; implement only this assigned stage.
Run and record every required check in checks/results.json as an array of objects with id, result (pass/fail/not tested/not applicable), evidence (file/observation), and reason for exceptions. Record actual observations in notes.md. Save every expected artifact. A passing command is not design approval.
'''
  if repair:prompt+='\nRepair only these findings; never fill missing client inputs with inventions:\n'+json.dumps(latest)
  session,text=launch('builder',prompt,folder,folder/f'build-{len(history)+1}.txt')
  return {'option':n,'session':session,'model':cfg()['roles']['builder']['model'],'at':time.time(),'result':text}
 with concurrent.futures.ThreadPoolExecutor(max_workers=cfg()['workflow']['parallel_builders']) as pool:
  futures=[pool.submit(one,r) for r in selected]
  results=[];errors=[]
  for f in futures:
   try:results.append(f.result())
   except Exception as e:errors.append(str(e))
 history.extend(results);write(c/'build-history.json',history)
 if errors:raise Stop('\n'.join(errors))
 return results
def artifacts(c,d,p):
 for row in p['options']:
  n=row['option'];o=c/f'option-{n}'
  for name in row['expected_artifacts']:
   path=local(c,name)
   if not path.is_file() or not path.stat().st_size:raise Stop('Missing/empty expected artifact: '+name)
  for sub in ['source','site','exports','previews']:
   for f in (o/sub).rglob('*'):
    if f.is_symlink():raise Stop('Symlink in production output: '+str(f))
  exports=[f for f in (o/'exports').rglob('*') if f.is_file()]
  images=[f for f in exports if f.suffix.lower() in ('.png','.jpg','.jpeg','.webp')]
  pdfs=[f for f in exports if f.suffix.lower()=='.pdf']
  kind=d['deliverable'];previews=list((o/'previews').glob('*.png'))
  if kind in ('linkedin-banner','linkedin-static','linkedin-carousel') and not images:raise Stop('Missing native image exports')
  if kind in ('linkedin-carousel','bip') and len(pdfs)!=1:raise Stop('Each carousel/BIP option needs exactly one PDF')
  if kind=='linkedin-carousel':
   from pypdf import PdfReader
   if len(PdfReader(pdfs[0]).pages)!=len(images):raise Stop('Carousel image/PDF page counts differ')
  if kind=='linkedin-banner' and len(previews)<3:raise Stop('Banner requires desktop/mobile/phone prototype previews')
  if kind=='email-newsletter' and len(previews)<2:raise Stop('Newsletter requires complete desktop and phone previews')
  if kind in ('landing-page-director','website'):
   for w in [1440,1024,768,390,320]:
    if not any(str(w) in f.name for f in previews):raise Stop(f'Missing web width evidence: {w}')
  checks=o/'checks/results.json'
  if not checks.is_file():raise Stop('Missing mechanical check results')
  data=read(checks)
  if not isinstance(data,list):raise Stop('Check results must be a list')
  ids=[x.get('id') for x in data]
  if len(set(ids))!=len(ids):raise Stop('Duplicate mechanical check IDs')
  for key in row['required_checks']:
   rows=[x for x in data if x.get('id')==key]
   if len(rows)!=1 or rows[0].get('result')!='pass' or not rows[0].get('evidence'):raise Stop('Missing or nonpassing check: '+key)
def case_files(c):
 result={}
 for p in c.rglob('*'):
  rel=p.relative_to(c)
  if any(x in ('review','.git','node_modules','.venv','.codex-image') for x in rel.parts) or p.name.startswith('.env') or p.name=='.team.lock':continue
  if p.is_symlink():raise Stop('Symlink in case: '+str(rel))
  if p.is_file():result[str(rel)]=sha(p)
 return result
def freeze(c,d,rnd):
 root=c/'review'/f'round-{rnd}';root.mkdir(parents=True,exist_ok=False);snapshot=root/'snapshot';snapshot.mkdir()
 manifest=case_files(c)
 for name in manifest:
  target=snapshot/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(c/name,target)
 shutil.copytree(SKILLS,snapshot/'_skills')
 write(root/'source-manifest.json',manifest)
 return root,snapshot,manifest
def image_inventory(snapshot,n):
 from PIL import Image
 import pypdfium2 as pdfium
 o=snapshot/f'option-{n}';images=[]
 for sub in ['exports','previews']:
  for p in sorted((o/sub).rglob('*')):
   if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp'):
    with Image.open(p) as im:im.verify()
    images.append(p)
 for pdf in sorted((o/'exports').glob('*.pdf')):
  doc=pdfium.PdfDocument(str(pdf))
  for i in range(len(doc)):
   page=doc[i];p=snapshot/'_pdf_pages'/f'option-{n}'/f'{pdf.stem}-{i+1:03}.png';p.parent.mkdir(parents=True,exist_ok=True)
   page.render(scale=max(1,1440/page.get_width())).to_pil().save(p);images.append(p)
  doc.close()
 if not images:raise Stop('Nothing visual to inspect')
 # Native and contextual images are both kept; phone-scale inspection is an additional view, not a replacement.
 for p in list(images):
  with Image.open(p) as im:
   q=snapshot/'_feed'/p.relative_to(snapshot);q.parent.mkdir(parents=True,exist_ok=True)
   im.convert('RGB').resize((390,max(1,round(im.height*390/im.width)))).save(q.with_suffix('.png'));images.append(q.with_suffix('.png'))
 for p in list(images):
  if '_feed' in p.relative_to(snapshot).parts:continue
  with Image.open(p) as im:
   if im.height>2200:
    for start in range(0,im.height,1720):
     q=snapshot/'_detail'/p.relative_to(snapshot).parent/f'{p.stem}-{start:06}.png';q.parent.mkdir(parents=True,exist_ok=True)
     im.crop((0,start,im.width,min(im.height,start+1800))).save(q);images.append(q)
 return images
def json_result(text):
 try:value=json.loads(text)
 except ValueError:raise Stop('Malformed review JSON; no pass can be inferred')
 if not isinstance(value,dict):raise Stop('Review must be an object')
 return value
def visual_result(text,expected):
 v=json_result(text);rows=v.get('images')
 if not isinstance(rows,list) or not all(isinstance(x,dict) for x in rows):raise Stop('Visual records must be objects')
 if not isinstance(rows,list) or [x.get('file') for x in rows]!=expected:raise Stop('Reviewer omitted/reordered/duplicated images')
 for row in rows:
  if row.get('viewed') is not True or not isinstance(row.get('findings'),list) or not isinstance(row.get('observation'),str) or not row['observation'].strip():raise Stop('Missing visual observation')
 return v
def verdict(text,required):
 v=json_result(text);items=v.get('items');defects=v.get('defects')
 if not isinstance(items,list) or not isinstance(defects,list):raise Stop('Review lacks rubric items or defects')
 if not all(isinstance(x,dict) for x in items+defects):raise Stop('Review entries must be objects')
 ids=[x.get('id') for x in items]
 if len(ids)!=len(set(ids)) or set(ids)!=set(required):raise Stop('Review does not cover every rubric ID exactly once')
 allowed={'pass','fail','blocked','not tested','not applicable'}
 for it in items:
  if it.get('result') not in allowed or not isinstance(it.get('evidence'),str) or not it['evidence'].strip():raise Stop('Invalid rubric result/evidence')
  if it['result']=='not applicable' and not it.get('reason'):raise Stop('Not-applicable item needs a reason')
 for f in defects:
  if f.get('severity') not in ('must_fix','blocker','should_fix','note') or not all(f.get(k) for k in ('where','what','fix')):raise Stop('Malformed defect')
 if any(x['result']=='fail' for x in items) or any(x['severity']=='must_fix' for x in defects):v['status']='fail'
 elif any(x['result'] in ('blocked','not tested') for x in items) or any(x['severity']=='blocker' for x in defects):v['status']='incomplete'
 else:v['status']='ready_for_human_review'
 return v
def review(c,d):
 p=plan(c,d);failures=[]
 for row in p['options']:
  try:artifacts(c,d,{'options':[row]})
  except Stop as e:failures.append({'option':row['option'],'status':'fail','defects':[{'severity':'must_fix','where':f'option-{row["option"]}','what':str(e),'fix':'Complete the required output/check and record actual evidence. Do not weaken requirements.'}]})
 if failures:
  write(c/'review/local-failures.json',{'options':failures,'stage':'local structural checks, not model review'});raise Stop('Local evidence failed; see review/local-failures.json. Use repair for these recorded defects.')
 (c/'review/local-failures.json').unlink(missing_ok=True)
 if len(d['reviews'])>=cfg()['workflow']['max_repair_rounds']+1:raise Stop('Initial review plus repair budget exhausted')
 attempts=list((c/'review').glob('round-*'))
 rnd=max([int(x.name.split('-')[-1]) for x in attempts]+[0])+1
 if rnd>cfg()['workflow']['max_repair_rounds']+1:raise Stop('Review attempt budget exhausted; incomplete attempts are preserved')
 folder,snapshot,manifest=freeze(c,d,rnd)
 builds=read(c/'build-history.json') if (c/'build-history.json').exists() else []
 forbidden={x['session'] for x in builds}
 rubric_ids=rubric(d['deliverable']);results=[];sessions=[]
 try:
  with lock(ROOT/'.state/media-review.lock'):
   for n in range(1,d['options']+1):
    images=image_inventory(snapshot,n);batch_records=[];batchsize=cfg()['review']['images_per_batch']
    for start in range(0,len(images),batchsize):
     chunk=images[start:start+batchsize];names=[str(x.relative_to(snapshot)) for x in chunk]
     prompt='Independent visual evidence inspection. You did not brief or build these files; inspect the actual artifacts regardless of their stated provenance. Inspect every attached image individually. Do not edit files or use network. Report exact text/crop/legibility/design concerns, not approval. Names in attachment order: '+json.dumps(names)+'. Return ONLY {"images":[{"file":"exact listed name","viewed":true,"observation":"specific visible observation","findings":[]}]} with every image in order. If you cannot inspect an image, viewed=false; never assume it passed.'
     session,raw=launch('reviewer',prompt,snapshot,folder/f'option-{n}-visual-{start//batchsize+1}.json',chunk)
     if session in forbidden or session in sessions:raise Stop('Reviewer session reused')
     sessions.append(session);batch_records.append(visual_result(raw,names))
    context={'deliverable':d['deliverable'],'option':n,'rubric':rubric_ids,'visual_batches':batch_records,'previous_review':d['reviews'][-1] if d['reviews'] else None,'production_requirements':cfg()['deliverables'][d['deliverable']]['requirements']}
    prompt=f'''Independent final review of option {n}. Read _skills/{d['deliverable']}/SKILL.md and REVIEW.md, production.json, case-notes.md, approved copy, option-{n}/notes.md, source and checks under this frozen snapshot. You may read files and inspect images; never modify them or use external services. Use the complete visual-review observations below. Missing evidence is not tested; missing client facts are blocked. Human approval/release remain pending. Do not change findings merely to get a pass. Return ONLY JSON with items (one per exact rubric ID, id/result/evidence, reason for not applicable), defects (severity must_fix/blocker/should_fix/note, where/what/fix), summary. Results allowed: pass/fail/blocked/not tested/not applicable. Do not invent a pass for unperformed checks.\n{json.dumps(context)}'''
    session,raw=launch('reviewer',prompt,snapshot,folder/f'option-{n}-review.json')
    if session in forbidden or session in sessions:raise Stop('Reviewer session reused')
    sessions.append(session);v=verdict(raw,rubric_ids);v['option']=n;v['images_reviewed']=len(images);results.append(v)
  if case_files(c)!=manifest:raise Stop('Case changed during review; verdict is stale')
  # Reviewer sandbox is read-only; detect any unexpected mutation of the preserved source as well.
  for name,h in manifest.items():
   if sha(snapshot/name)!=h:raise Stop('Frozen evidence changed')
 except Exception as e:
  write(folder/'INCOMPLETE.json',{'error':str(e),'sessions':sessions,'at':time.time()});raise
 record={'round':rnd,'options':results,'sessions':sessions,'model':cfg()['roles']['reviewer']['model'],'at':time.time(),'human_review':'pending','release':'not performed'}
 write(folder/'result.json',record);write(c/'review/latest.json',record);d['reviews'].append(record);write(c/'case.json',d)
 handover(c,record);return record
def handover(c,record):
 results=record['options']
 hand=['# Local design handover','','Human review: pending. Nothing deployed, uploaded or sent.','']
 for v in results:hand += [f'## Option {v["option"]}: {v["status"]}',v.get('summary','') if isinstance(v.get('summary',''),str) else json.dumps(v['summary'],indent=2),json.dumps(v['defects'],indent=2),'']
 (c/'HANDOVER.md').write_text('\n'.join(hand))
def status():
 pins();problems=[]
 for mod in ['PIL','pypdf','pypdfium2']:
  try:__import__(mod)
  except ImportError:problems.append('Missing '+mod)
 for exe in ['codex','node']:
  if not shutil.which(exe):problems.append('Missing '+exe)
 if not (ROOT/'tools/node_modules/playwright-core').is_dir():problems.append('Missing renderer dependency')
 for skill in cfg()['deliverables']:
  for name in ['SKILL.md','REVIEW.md']:
   if not (SKILLS/skill/name).is_file():problems.append('Missing '+skill+'/'+name)
 print(json.dumps({'roles':cfg()['roles'],'deliverables':list(cfg()['deliverables']),'problems':problems},indent=2))
 return bool(problems)
def main():
 ap=argparse.ArgumentParser();subs=ap.add_subparsers(dest='command',required=True)
 subs.add_parser('status');p=subs.add_parser('new');p.add_argument('deliverable',choices=list(cfg()['deliverables']));p.add_argument('--case',required=True);p.add_argument('--brief',required=True);p.add_argument('--options',type=int,default=2);p.add_argument('--destination',choices=['personal','business']);p.add_argument('--mode',default='new')
 for name in ['preflight','build','repair','review','handover']:
  p=subs.add_parser(name);p.add_argument('case')
 p=subs.add_parser('probe');p.add_argument('role',choices=['orchestrator','builder','reviewer']);p.add_argument('--out',required=True)
 a=ap.parse_args()
 try:
  pins()
  if a.command=='status':return status()
  if a.command=='new':print(initialise(a.deliverable,a.case,a.brief,a.options,a.destination,a.mode));return 0
  if a.command=='probe':
   out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
   session,raw=launch(a.role,'Configuration routing probe only, not a design job. Do not read files, invoke tools or edit anything. Reply exactly ROUTE_OK.',out.parent,out)
   if raw.strip()!='ROUTE_OK':raise Stop('Probe response mismatch')
   print(json.dumps({'role':a.role,'model':cfg()['roles'][a.role]['model'],'session':session,'result':raw.strip()}));return 0
  c,d=case(a.case)
  with lock(c/'.team.lock'):
   if a.command=='preflight':plan(c,d);print('Inputs and output plan complete; no design quality claim.');return 0
   if a.command in ('build','repair'):print(json.dumps(build(c,d,a.command=='repair'),indent=2));return 0
   if a.command=='handover':
    record=read(c/'review/latest.json');expected=read(c/'review'/f'round-{record["round"]}'/'source-manifest.json');current=case_files(c)
    for data in [expected,current]:
     data.pop('case.json',None);data.pop('HANDOVER.md',None)
    if expected!=current:raise Stop('Source changed; a new review is required before handover')
    handover(c,record);print(c/'HANDOVER.md');return 0
   if a.command=='review':
    r=review(c,d);print(json.dumps(r,indent=2));return 0 if all(x['status']=='ready_for_human_review' for x in r['options']) else 1
 except (Stop,ValueError,KeyError,FileNotFoundError,subprocess.TimeoutExpired) as e:print('STOP: '+str(e),file=sys.stderr);return 3
if __name__=='__main__':sys.exit(main())
