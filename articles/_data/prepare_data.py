"""Copies the actor sample outputs used by the articles into small public JSON files, dropping contact and address fields.
Needs the private run outputs, so it is only for refreshing the data; the analysis scripts (a1..a5) need only the JSON files next to them.
  python prepare_data.py C:/gng/lanes/apify"""
import json, sys, os
SRC = sys.argv[1] if len(sys.argv) > 1 else 'C:/gng/lanes/apify'
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return json.load(open(f'{SRC}/{p}', encoding='utf-8'))
def dump(name, rows): json.dump(rows, open(f'{HERE}/{name}', 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
keep = lambda rows, keys: [{k: r.get(k) for k in keys} for r in rows]
dump('ats_roles.json', keep(load('ats-open-roles/samples/output.json'),
     ['company', 'ats', 'title', 'department', 'location', 'remote', 'workplaceType', 'employmentType', 'postedAt', 'salaryMin', 'salaryMax', 'salaryCurrency', 'salaryPeriod']))
dump('secd_filings.json', keep(load('sec-form-d-funding-leads/samples/output.json'),
     ['filingDate', 'formType', 'isAmendment', 'entityType', 'jurisdictionOfIncorporation', 'yearOfIncorporation', 'issuerState', 'industryGroup', 'revenueRange',
      'totalOfferingAmount', 'totalAmountSold', 'totalRemaining', 'offeringIsIndefinite', 'minimumInvestment', 'numberOfInvestors', 'salesCommissionsUsd', 'findersFeesUsd']))
dump('council_items.json', keep(load('city-council-agendas/samples/dataset-sample.json'),
     ['city', 'body', 'meetingDate', 'agendaStatus', 'title', 'matterFile', 'matterType', 'matterStatus', 'action', 'voteResult', 'voteTally']))
ts = load('website-tech-stack/samples/OUTPUT.json')
dump('techstack.json', [{'url': r['url'], 'status': r.get('status'), 'error': r.get('error'), 'server': r.get('server'),
                         'technologies': [{'name': t['name'], 'category': t.get('category'), 'confidence': t.get('confidence')} for t in (r.get('technologies') or [])]} for r in ts])
print('ok')
