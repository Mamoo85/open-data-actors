"""Article 2: one day of SEC Form D filings. Input: secd_filings.json (50 filings)."""
import json, os, statistics as st, collections
H = os.path.dirname(os.path.abspath(__file__))


def q(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def n(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def compute():
    r = json.load(open(f'{H}/secd_filings.json', encoding='utf-8'))
    off = [n(x['totalOfferingAmount']) for x in r if n(x['totalOfferingAmount'])]
    both = [(n(x['totalAmountSold']), n(x['totalOfferingAmount'])) for x in r if n(x['totalOfferingAmount']) and n(x['totalAmountSold']) is not None]
    inv = [n(x['numberOfInvestors']) for x in r if n(x['numberOfInvestors']) is not None]
    com = [x for x in r if (n(x['salesCommissionsUsd']) or 0) > 0 or (n(x['findersFeesUsd']) or 0) > 0]
    return {'n': len(r), 'filing_dates': sorted({x['filingDate'] for x in r}), 'with_offering': len(off),
            'offering': {'p25': q(off, .25), 'median': st.median(off), 'p75': q(off, .75), 'max': max(off), 'min': min(off)},
            'indefinite': sum(1 for x in r if str(x['offeringIsIndefinite']) == 'True'),
            'sold_to_offered_pct': round(100 * sum(a for a, b in both) / sum(b for a, b in both), 1), 'pairs': len(both),
            'zero_sold': sum(1 for a, b in both if a == 0), 'fully_sold': sum(1 for a, b in both if a >= b),
            'investors_median': st.median(inv) if inv else None, 'investors_max': max(inv) if inv else None,
            'industries': collections.Counter(x['industryGroup'] for x in r).most_common(5),
            'states': collections.Counter(x['issuerState'] for x in r).most_common(5),
            'entity_types': collections.Counter(x['entityType'] for x in r).most_common(4),
            'revenue_declined': sum(1 for x in r if x['revenueRange'] == 'Decline to Disclose'),
            'incorporated_2025_26': sum(1 for x in r if str(x['yearOfIncorporation']) in ('2025', '2026')),
            'year_known': sum(1 for x in r if x['yearOfIncorporation']), 'with_commissions': len(com),
            'amendments': sum(1 for x in r if str(x['isAmendment']) == 'True')}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=1))
