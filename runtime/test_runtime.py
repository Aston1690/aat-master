import unittest,tempfile,json,sys
from pathlib import Path
from unittest.mock import patch
import team
from PIL import Image
from pypdf import PdfWriter
class RuntimeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.brief=self.root/'brief.md';self.brief.write_text('SYNTHETIC ROUTING FIXTURE. Not client content, approval or design-quality evidence.')
 def job(self,kind,options=1):
  c=team.initialise(kind,self.root/kind,self.brief,options,'business' if kind=='linkedin-banner' else None);d=team.read(c/'case.json');p=team.read(c/'production.json')
  p.update(copy_approved=True,approval_evidence='SYNTHETIC TEST ONLY',variants_source='fixture')
  for row in p['options']:
   n=row['option'];row.update(thesis='Neutral routing fixture',copy_file='brief/brief.md',expected_artifacts=[f'option-{n}/source/layout.html'])
   (c/f'option-{n}/source/layout.html').write_text('<h1>Fixture only</h1>')
   (c/f'option-{n}/notes.md').write_text('Synthetic outputs; not a real skill production test.')
   Image.new('RGB',(600,300),'white').save(c/f'option-{n}/exports/fixture.png')
   widths=[1440,1024,768,390,320] if kind in ('landing-page-director','website') else [1280,390,360]
   for w in widths:Image.new('RGB',(w,100),'white').save(c/f'option-{n}/previews/view-{w}.png')
   if kind in ('bip','linkedin-carousel'):
    pdf=PdfWriter();pdf.add_blank_page(width=600,height=300)
    with (c/f'option-{n}/exports/fixture.pdf').open('wb') as f:pdf.write(f)
   team.write(c/f'option-{n}/checks/results.json',[{'id':x,'result':'pass','evidence':'Synthetic fixture, not executed production QA'} for x in row['required_checks']])
  team.write(c/'production.json',p);return c,d,p
 def test_all_seven_plan_and_artifact_routes(self):
  for name in team.cfg()['deliverables']:
   with self.subTest(deliverable=name):
    c,d,p=self.job(name);team.plan(c,d);team.artifacts(c,d,p);self.assertGreater(len(team.rubric(name)),10)
 def test_inputs_not_implicitly_approved(self):
  c=team.initialise('bip',self.root/'blocked',self.brief,1)
  with self.assertRaises(team.Stop):team.plan(c,team.read(c/'case.json'))
 def test_mandatory_checks_cannot_be_omitted(self):
  c,d,p=self.job('website');p['options'][0]['required_checks']=['made-up'];team.write(c/'production.json',p)
  with self.assertRaises(team.Stop):team.plan(c,d)
 def test_escape_rejected(self):
  c,d,p=self.job('bip');p['options'][0]['expected_artifacts']=['../outside'];team.write(c/'production.json',p)
  with self.assertRaises(team.Stop):team.plan(c,d)
 def test_unsupported_banner_destination(self):
  with self.assertRaises(team.Stop):team.initialise('linkedin-banner',self.root/'group',self.brief,1,'group')
 def test_missing_export_blocks(self):
  c,d,p=self.job('linkedin-static');(c/'option-1/exports/fixture.png').unlink()
  with self.assertRaises(team.Stop):team.artifacts(c,d,p)
 def test_carousel_page_mismatch_blocks(self):
  c,d,p=self.job('linkedin-carousel');Image.new('RGB',(600,300)).save(c/'option-1/exports/second.png')
  with self.assertRaises(team.Stop):team.artifacts(c,d,p)
 def test_missing_route_width_blocks(self):
  c,d,p=self.job('website');(c/'option-1/previews/view-320.png').unlink()
  with self.assertRaises(team.Stop):team.artifacts(c,d,p)
 def test_missing_mechanical_check_blocks(self):
  c,d,p=self.job('bip');team.write(c/'option-1/checks/results.json',[])
  with self.assertRaises(team.Stop):team.artifacts(c,d,p)
 def valid(self,result='pass'):return {'items':[{'id':'R001','result':result,'evidence':'fixture'}],'defects':[]}
 def test_valid_review(self):self.assertEqual(team.verdict(json.dumps(self.valid()),{'R001':'check'})['status'],'ready_for_human_review')
 def test_missing_review_items_cannot_pass(self):
  for v in [{},{'items':[],'defects':[]},{'items':None,'defects':[]}]:
   with self.assertRaises(team.Stop):team.verdict(json.dumps(v),{'R001':'check'})
 def test_duplicate_review_items_rejected(self):
  v=self.valid();v['items']*=2
  with self.assertRaises(team.Stop):team.verdict(json.dumps(v),{'R001':'check'})
 def test_failed_review_not_upgraded(self):self.assertEqual(team.verdict(json.dumps(self.valid('fail')),{'R001':'check'})['status'],'fail')
 def test_unperformed_review_incomplete(self):
  for x in ['blocked','not tested']:self.assertEqual(team.verdict(json.dumps(self.valid(x)),{'R001':'check'})['status'],'incomplete')
 def test_malformed_review_rejected(self):
  with self.assertRaises(team.Stop):team.verdict('```json\n{}\n```',{})
 def test_not_applicable_requires_reason(self):
  with self.assertRaises(team.Stop):team.verdict(json.dumps(self.valid('not applicable')),{'R001':'check'})
 def test_image_omission_rejected(self):
  with self.assertRaises(team.Stop):team.visual_result('{"images":[]}', ['image.png'])
 def test_unseen_image_rejected(self):
  with self.assertRaises(team.Stop):team.visual_result(json.dumps({'images':[{'file':'a','viewed':False,'findings':[],'observation':'not seen'}]}),['a'])
 def test_all_images_and_pdf_pages_kept(self):
  c,d,p=self.job('bip')
  for i in range(65):Image.new('RGB',(20,20),'white').save(c/'option-1/exports'/f'{i:03}.png')
  rd,snap,manifest=team.freeze(c,d,1);images=team.image_inventory(snap,1)
  self.assertEqual(len(images),140) # 66 exports + 3 previews + 1 PDF page, with all 70 feed views
  self.assertTrue(any('_pdf_pages' in str(p) for p in images));self.assertTrue((snap/'option-1/source/layout.html').exists())
  (c/'option-1/source/layout.html').write_text('changed')
  self.assertNotEqual(team.sha(c/'option-1/source/layout.html'),team.sha(snap/'option-1/source/layout.html'))
 def test_complete_routing_review_for_all_seven_with_stub_models(self):
  seq=[0]
  def fake(role,prompt,work,out,images=()):
   seq[0]+=1
   if images:
    value={'images':[{'file':str(x.relative_to(work)),'viewed':True,'observation':'Synthetic fixture observation','findings':[]} for x in images]}
   else:
    context=json.loads(prompt.split('\n',1)[1]);value={'items':[{'id':key,'result':'pass','evidence':'Synthetic fixture only'} for key in context['rubric']],'defects':[],'summary':'Synthetic protocol test, not a design assessment.'}
   team.write(out,value);return f'stub-{seq[0]}',json.dumps(value)
  for name in team.cfg()['deliverables']:
   with self.subTest(deliverable=name):
    c,d,p=self.job(name)
    with patch.object(team,'launch',side_effect=fake):result=team.review(c,d)
    self.assertEqual(result['options'][0]['status'],'ready_for_human_review');self.assertTrue((c/'review/round-1/snapshot').is_dir());self.assertTrue((c/'HANDOVER.md').exists())
 def test_structured_summary_handover(self):
  c,d,p=self.job('linkedin-static')
  team.handover(c,{'options':[{'option':1,'status':'fail','summary':{'conclusion':'wrong copy'},'defects':[]}]})
  self.assertIn('wrong copy',(c/'HANDOVER.md').read_text())
 def test_tall_images_receive_readable_detail_strips(self):
  c,d,p=self.job('linkedin-static');Image.new('RGB',(390,6000),'white').save(c/'option-1/previews/tall.png')
  rd,snap,manifest=team.freeze(c,d,1);images=team.image_inventory(snap,1)
  self.assertEqual(len([x for x in images if '_detail' in x.parts]),4)
 def test_bad_entry_types_rejected(self):
  with self.assertRaises(team.Stop):team.verdict('{"items":[42],"defects":[]}',{'R001':'check'})
  with self.assertRaises(team.Stop):team.visual_result('{"images":[42]}',['a'])
if __name__=='__main__':unittest.main(verbosity=2)
