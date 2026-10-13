"""Article 5: field coverage across all sample CSVs. Input: the apify-actor-samples checkout (pass its path, or set ODA_SAMPLES)."""
import csv, glob, json, os, re, sys, statistics as st
SAMPLES = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('ODA_SAMPLES', 'D:/gng_tmp/samples_clone')
PII = re.compile(r'(?i)(e-?mail|phone)')


def empty(v):
    return v is None or str(v).strip() in ('', 'None', 'null', '[]', '{}')


def compute():
    files = {}
    for p in sorted(glob.glob(f'{SAMPLES}/*/sample.csv')):
        rows = list(csv.DictReader(open(p, encoding='utf-8-sig')))
        d = {c: 100.0 * sum(not empty(r.get(c)) for r in rows) / len(rows) for c in rows[0]}
        files[os.path.basename(os.path.dirname(p))] = (len(rows), d)
    allc = [(s, c, v) for s, (n, d) in files.items() for c, v in d.items()]
    avg = {s: sum(d.values()) / len(d) for s, (n, d) in files.items()}
    pii = [v for s, c, v in allc if PII.search(c)]
    return {'files': len(files), 'columns': len(allc), 'rows_total': sum(n for n, d in files.values()),
            'rows_min': min(n for n, d in files.values()), 'rows_max': max(n for n, d in files.values()),
            'full': sum(1 for a in allc if a[2] == 100), 'empty': sum(1 for a in allc if a[2] == 0), 'mean_cov': round(sum(a[2] for a in allc) / len(allc), 1),
            'median_file_avg': round(st.median(avg.values()), 1),
            'lowest': [(s, round(v, 1)) for s, v in sorted(avg.items(), key=lambda kv: kv[1])[:3]],
            'highest': [(s, round(v, 1)) for s, v in sorted(avg.items(), key=lambda kv: -kv[1])[:3]],
            'contact_cols': len(pii), 'contact_mean': round(sum(pii) / len(pii), 1) if pii else None, 'contact_full': sum(1 for v in pii if v == 100),
            'files_with_empty_col': sum(1 for n, d in files.values() if any(v == 0 for v in d.values()))}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=1))
