import os, sys, json, datetime, xml.etree.ElementTree as ET
root = ET.parse('results.xml').getroot()
tests=[]
for case in root.iter('testcase'):
    fail = case.find('failure')
    error = case.find('error')
    issue = fail if fail is not None else error
    skipped = case.find('skipped')
    status = 'failed' if issue is not None else 'skipped' if skipped is not None else 'passed'
    tests.append({'name':case.get('name'), 'result':status, 'failure_message':(issue.get('message') or issue.text or '')[:2000] if issue is not None else None})
passed=sum(t['result']=='passed' for t in tests)
failed=sum(t['result']=='failed' for t in tests)
report={'repository':os.getenv('GITHUB_REPOSITORY','local'), 'branch':os.getenv('GITHUB_REF_NAME','local'), 'commit_sha':os.getenv('GITHUB_SHA','local'), 'pipeline_run_id':os.getenv('GITHUB_RUN_ID','local'), 'execution_timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'tests':tests,'total':len(tests),'passed':passed,'failed':failed,'overall_status':'passed' if failed==0 and passed==len(tests) and tests else 'failed'}
with open('report-output.json','w') as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
