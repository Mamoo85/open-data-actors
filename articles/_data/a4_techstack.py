"""Article 4: what technology detection finds on 11 reachable sites (+1 deliberately unreachable domain). Input: techstack.json."""
import json, os, statistics as st, collections
H = os.path.dirname(os.path.abspath(__file__))


def compute():
    r = json.load(open(f'{H}/techstack.json', encoding='utf-8'))
    ok = [x for x in r if not x.get('error')]
    bad = [x for x in r if x.get('error')]
    names = collections.Counter(t['name'] for x in ok for t in x['technologies'])
    cats = collections.Counter(c for x in ok for c in {t['category'] for t in x['technologies']})
    cnt = [len(x['technologies']) for x in ok]
    lowconf = sum(1 for x in ok for t in x['technologies'] if (t.get('confidence') or 100) < 100)
    return {'requested': len(r), 'ok': len(ok), 'failed': [(x['url'], x['error']) for x in bad], 'techs_total': sum(cnt),
            'median_per_site': st.median(cnt), 'min_per_site': min(cnt), 'max_per_site': max(cnt),
            'top_techs': names.most_common(6), 'top_categories': cats.most_common(6), 'distinct_techs': len(names), 'below_full_confidence': lowconf,
            'servers': collections.Counter((x.get('server') or 'none') for x in ok).most_common(5), 'no_server_header': sum(1 for x in ok if not x.get('server'))}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=1))
