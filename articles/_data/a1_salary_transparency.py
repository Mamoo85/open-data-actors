"""Article 1: how many sampled job postings state a salary. Input: ats_roles.json (40 postings, 8 companies, 8 ATS vendors, 5 each)."""
import json, os, statistics as st, collections
H = os.path.dirname(os.path.abspath(__file__))


def compute():
    r = json.load(open(f'{H}/ats_roles.json', encoding='utf-8'))
    has = lambda x: x.get('salaryMin') is not None and x.get('salaryMax') is not None
    pay = [x for x in r if has(x)]
    by = collections.OrderedDict()
    for x in r:
        b = by.setdefault(x['company'], {'ats': x['ats'], 'n': 0, 'with_salary': 0})
        b['n'] += 1
        b['with_salary'] += has(x)
    mids = [(x['salaryMin'] + x['salaryMax']) / 2 for x in pay if x.get('salaryPeriod') == 'year' and x.get('salaryCurrency') == 'USD']  # USD only, so midpoints are comparable
    widths = [100.0 * (x['salaryMax'] - x['salaryMin']) / x['salaryMin'] for x in pay if x['salaryMin']]
    dates = [x['postedAt'][:10] for x in r if x.get('postedAt')]
    return {'n': len(r), 'companies': len(by), 'with_salary': len(pay), 'share': round(100.0 * len(pay) / len(r), 1), 'by_company': by,
            'currencies': dict(collections.Counter(x['salaryCurrency'] for x in pay)), 'periods': dict(collections.Counter(x['salaryPeriod'] for x in pay)),
            'median_midpoint': st.median(mids) if mids else None, 'min_midpoint': min(mids) if mids else None, 'max_midpoint': max(mids) if mids else None,
            'median_width_pct': round(st.median(widths), 1) if widths else None,
            'workplace_known': sum(1 for x in r if x.get('workplaceType')), 'employment_known': sum(1 for x in r if x.get('employmentType')),
            'dates': (min(dates), max(dates))}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=1))
