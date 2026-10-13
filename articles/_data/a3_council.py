"""Article 3: what council agenda rows contain. Input: council_items.json (60 rows: Seattle and Denver).
Procedural = the title matches the phrase list in PROC below."""
import json, os, re, collections
H = os.path.dirname(os.path.abspath(__file__))
PROC = re.compile(r'(?i)(call to order|approval of (the )?(agenda|minutes)|adjournment|roll call|public comment|items of business|please note|this meeting also|pledge|announcements|recess|executive session)')


def has(v):
    return v not in (None, '', 'None')


def compute():
    r = json.load(open(f'{H}/council_items.json', encoding='utf-8'))
    cities = collections.OrderedDict()
    for x in r:
        c = cities.setdefault(x['city'], {'rows': 0, 'procedural': 0, 'with_matter_file': 0, 'with_action': 0, 'with_vote': 0, 'meetings': set()})
        c['rows'] += 1
        c['procedural'] += bool(PROC.search(x['title'] or ''))
        c['with_matter_file'] += has(x['matterFile'])
        c['with_action'] += has(x['action'])
        c['with_vote'] += has(x['voteResult'])
        c['meetings'].add((x['body'], x['meetingDate']))
    for c in cities.values():
        c['meetings'] = len(c['meetings'])
    mf = [x for x in r if has(x['matterFile'])]
    return {'n': len(r), 'cities': cities, 'procedural': sum(1 for x in r if PROC.search(x['title'] or '')), 'with_matter_file': len(mf),
            'matter_with_action': sum(1 for x in mf if has(x['action'])), 'matter_with_vote': sum(1 for x in mf if has(x['voteResult'])),
            'bodies': dict(collections.Counter(x['body'] for x in r)), 'dates': (min(x['meetingDate'] for x in r), max(x['meetingDate'] for x in r)),
            'matter_types': dict(collections.Counter(x['matterType'] for x in mf)), 'final_status': sum(1 for x in r if x['agendaStatus'] == 'Final')}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=1, default=list))
