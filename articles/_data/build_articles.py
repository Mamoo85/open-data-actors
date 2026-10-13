"""Builds /articles/index.html and the five article pages from the a1..a5 analysis scripts (every figure in the prose is computed here).
  python build_articles.py [site_root]      default site_root = the folder two levels up from this file."""
import html, os, re, sys, json, datetime
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(H))
BASE = 'https://mamoo85.github.io/open-data-actors/'
GH = 'https://github.com/Mamoo85/apify-actor-samples/blob/main/'
GHSCRIPT = 'https://github.com/Mamoo85/open-data-actors/blob/main/articles/_data/'
DATE = '2026-10-13'
CSS = re.search(r'<style>(.*?)</style>', open(f'{ROOT}/index.html', encoding='utf-8').read(), re.S).group(1)
import a1_salary_transparency as A1, a2_form_d as A2, a3_council as A3, a4_techstack as A4, a5_coverage as A5

e = html.escape
usd = lambda x: f'${x:,.0f}'
pct = lambda a, b: f'{100.0 * a / b:.0f}%'


def page(slug, title, desc, body):
    url = f'{BASE}articles/{slug}.html'
    nav = '<nav><a href="../index.html">All actors</a> | <a href="index.html">Articles</a> | <a href="../digest/">Digest</a> | <a href="../quality/">Data quality</a></nav>'
    ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'datePublished': DATE, 'description': desc, 'mainEntityOfPage': url}
    h = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>'
         f'<meta name="description" content="{html.escape(desc, quote=True)}"><link rel="canonical" href="{url}"><meta property="og:type" content="article">'
         f'<meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(desc, quote=True)}"><meta property="og:url" content="{url}">'
         f'<script type="application/ld+json">{json.dumps(ld)}</script><style>{CSS}</style></head><body>\n{nav}\n')
    open(f'{ROOT}/articles/{slug}.html', 'w', encoding='utf-8').write(h + body + '\n</body></html>\n')
    return url


def foot(actor, script, sample_note):
    return (f'<h2>Data and method</h2><p>{sample_note} The figures on this page are computed by <a href="{GHSCRIPT}{script}">{script}</a> '
            f'(run it from the <code>articles/_data</code> folder). Related: <a href="../{actor}.html">the actor page</a> and its <a href="{GH}{actor}/sample.csv">sample CSV</a>. '
            f'Published {DATE}. We build and maintain these actors.</p>')


ARTS = []


def art(slug, title, desc, body):
    page(slug, title, desc, body)
    ARTS.append((slug, title, desc))


# ---- 1 salary transparency
a = A1.compute()
bc = a['by_company']
rows = ''.join(f'<tr><td>{e(c)}</td><td>{e(v["ats"])}</td><td>{v["n"]}</td><td>{v["with_salary"]}</td></tr>' for c, v in bc.items())
zero = [c for c, v in bc.items() if v['with_salary'] == 0]
art('how-many-job-postings-state-a-salary', f'{a["with_salary"]} of {a["n"]} sampled job postings state a salary',
    'A count of salary ranges in 40 job postings pulled from eight career sites on eight different applicant tracking systems.',
    f'<h1>{a["with_salary"]} of {a["n"]} sampled job postings state a salary</h1>'
    f'<p>We pulled {a["n"]} postings, five each from {a["companies"]} companies that use {a["companies"]} different applicant tracking systems, and counted how many carry a machine-readable salary range. '
    f'<strong>{a["with_salary"]} of {a["n"]} ({a["share"]:g}%) do.</strong> Postings were published between {a["dates"][0]} and {a["dates"][1]}.</p>'
    f'<h2>Where the salaries are</h2><table><tr><th>Company</th><th>ATS</th><th>Postings</th><th>With salary range</th></tr>{rows}</table>'
    f'<p>All {a["with_salary"]} salary ranges come from {sum(1 for v in bc.values() if v["with_salary"])} companies. {len(zero)} of the {a["companies"]} companies ({e(", ".join(zero))}) show none in this sample. '
    f'The ranges are quoted per year; {e(", ".join(f"{k}: {v}" for k, v in a["currencies"].items()))}.</p>'
    f'<p>Among the USD ranges the median midpoint is {usd(a["median_midpoint"])} (lowest midpoint {usd(a["min_midpoint"])}, highest {usd(a["max_midpoint"])}). '
    f'The median range is {a["median_width_pct"]:g}% wide, measured as (max minus min) divided by min.</p>'
    f'<h2>Other fields</h2><p>Workplace type (on-site, hybrid, remote) is filled for {a["workplace_known"]} of {a["n"]} postings and employment type for {a["employment_known"]} of {a["n"]}. '
    'Which fields exist depends on what the ATS exposes, so a blank field usually means the vendor does not publish it.</p>'
    '<h2>Limits</h2><ul><li>Five postings per company, chosen by the tool, not a random draw. Company and ATS are the same thing here (one company per vendor), so you cannot separate a company habit from a vendor effect.</li>'
    '<li>Eight companies are not the job market. Do not read 20% as a market rate.</li>'
    '<li>We count salary fields in the structured data. A salary written only in the free-text description is not counted.</li></ul>'
    + foot('ats-open-roles', 'a1_salary_transparency.py', f'Input: {a["n"]} postings from a test run of the ats-open-roles actor, stored as ats_roles.json (the public sample CSV has 12 rows; this file is the larger test output).'))

# ---- 2 form d
b = A2.compute(); o = b['offering']
ind = ', '.join(f'{k} ({v})' for k, v in b['industries'][:4]); stt = ', '.join(f'{k} ({v})' for k, v in b['states'][:4]); ent = ', '.join(f'{k} ({v})' for k, v in b['entity_types'][:3])
art('one-day-of-sec-form-d-filings', f'One day of SEC Form D filings: {b["n"]} filings, median offering {usd(o["median"])}',
    'What fifty Form D filings from a single filing date say about offering size, how much was sold and who files.',
    f'<h1>One day of SEC Form D filings: {b["n"]} filings, median offering {usd(o["median"])}</h1>'
    f'<p>Form D is the notice a company files with the SEC when it raises money without a public offering. We looked at {b["n"]} filings dated {e(", ".join(b["filing_dates"]))}.</p>'
    f'<h2>Size</h2><p>{b["with_offering"]} filings state a total offering amount. The median is {usd(o["median"])}, the middle half runs from {usd(o["p25"])} to {usd(o["p75"])}, '
    f'and the range is {usd(o["min"])} to {usd(o["max"])}. {b["indefinite"]} filings describe the offering as indefinite (no fixed amount).</p>'
    f'<h2>How much was sold</h2><p>For the {b["pairs"]} filings with both a total offering and an amount sold, the sold total is {b["sold_to_offered_pct"]:g}% of the offered total. '
    f'{b["zero_sold"]} report nothing sold yet and {b["fully_sold"]} report the offering fully sold. The median number of investors is {b["investors_median"]:g} (largest: {b["investors_max"]:g}).</p>'
    f'<h2>Who files</h2><p>Industry groups: {e(ind)}. Most common states: {e(stt)}. Entity types: {e(ent)}. '
    f'{b["revenue_declined"]} of {b["n"]} filers chose "Decline to Disclose" for revenue range. Where the year of incorporation is given ({b["year_known"]} filings), {b["incorporated_2025_26"]} were incorporated in 2025 or 2026. '
    f'{b["with_commissions"]} filings report sales commissions or finders fees.</p>'
    '<h2>Limits</h2><ul><li>One filing date. Filings cluster around deadlines and weekdays, so another day will look different.</li>'
    '<li>The "Other" industry group is the largest, which tells you little about what these companies do.</li>'
    '<li>Amounts are as reported by the filer. We did not check them against anything else.</li>'
    '<li>The ratio of sold to offered is dominated by a few large filings.</li></ul>'
    + foot('sec-form-d-funding-leads', 'a2_form_d.py', f'Input: {b["n"]} filings from a test run of the sec-form-d-funding-leads actor, stored as secd_filings.json with phone, street address and named-person fields removed (the public sample CSV has 12 rows).'))

# ---- 3 council
c = A3.compute(); cs = c['cities']
crow = ''.join(f'<tr><td>{e(k)}</td><td>{v["rows"]}</td><td>{v["meetings"]}</td><td>{v["procedural"]}</td><td>{v["with_matter_file"]}</td><td>{v["with_action"]}</td><td>{v["with_vote"]}</td></tr>' for k, v in cs.items())
art('what-city-council-agendas-contain', f'What is in a city council agenda feed: {c["procedural"]} of {c["n"]} rows are procedure',
    'A count of procedural lines versus legislative matters in 60 agenda rows from Seattle and Denver, and which fields are filled.',
    f'<h1>What is in a city council agenda feed: {c["procedural"]} of {c["n"]} rows are procedure</h1>'
    f'<p>We looked at {c["n"]} agenda rows for meetings between {c["dates"][0]} and {c["dates"][1]} in {len(cs)} cities. A row is called procedural when its title matches a short phrase list (call to order, approval of the agenda or minutes, adjournment, roll call, public comment, announcements and similar; the list is in the script). '
    f'By that rule {c["procedural"]} rows ({pct(c["procedural"], c["n"])}) are procedural.</p>'
    f'<table><tr><th>City</th><th>Rows</th><th>Meetings</th><th>Procedural</th><th>Linked to a matter file</th><th>With action</th><th>With vote result</th></tr>{crow}</table>'
    f'<h2>Substance</h2><p>{c["with_matter_file"]} rows link to a legislative matter file. Of those, {c["matter_with_action"]} have an action recorded and {c["matter_with_vote"]} have a vote result. '
    f'Matter types present: {e(", ".join(f"{k} ({v})" for k, v in c["matter_types"].items()))}.</p>'
    '<p>The practical point for anyone watching zoning, contracts or appointments: filter on matter-linked rows, not on all rows, or most of what you read will be housekeeping.</p>'
    '<h2>Limits</h2><ul><li>Two cities, one with a single meeting in the sample. Seattle and Denver publish differently, so the per-city split reflects the portals as much as the councils.</li>'
    '<li>Whether an action or vote is filled depends on whether the meeting has happened and the clerk has entered it, so recent agendas look emptier.</li>'
    '<li>The procedural phrase list is ours and will miss some lines and catch some others.</li></ul>'
    + foot('city-council-agendas', 'a3_council.py', f'Input: {c["n"]} rows from a test run of the city-council-agendas actor, stored as council_items.json with attachment links and note text removed (the public sample CSV has 12 rows).'))

# ---- 4 tech stack
d = A4.compute()
tt = ', '.join(f'{k} ({v})' for k, v in d['top_techs'][:6]); tc = ', '.join(f'{k} ({v})' for k, v in d['top_categories'][:6])
art('what-tech-detection-finds-on-11-sites', f'What tech detection finds on {d["ok"]} well-known sites: {d["techs_total"]} detections',
    'A tally of the technologies, categories and servers detected on eleven public sites, plus one deliberately broken domain.',
    f'<h1>What tech detection finds on {d["ok"]} well-known sites: {d["techs_total"]} detections</h1>'
    f'<p>We ran the website tech stack detector on {d["requested"]} addresses: {d["ok"]} real sites and one made-up domain to see how a failure is reported. '
    f'The failed one came back as <code>{e(d["failed"][0][1])}</code> instead of as an empty result, so a dead domain does not look like a site with no technology.</p>'
    f'<h2>Counts</h2><p>{d["techs_total"]} detections across {d["ok"]} sites, {d["distinct_techs"]} distinct technologies. A site returns between {d["min_per_site"]} and {d["max_per_site"]} (median {d["median_per_site"]:g}).</p>'
    f'<p>Most common technologies: {e(tt)}. Most common categories (sites per category): {e(tc)}.</p>'
    f'<p>The top entries are security headers and metadata (HSTS, Open Graph), not products. That is what a header-and-HTML detector sees first; products that leave no trace in headers or markup are not found. '
    f'Server headers: {e(", ".join(f"{k} ({v})" for k, v in d["servers"]))}.</p>'
    f'<p>{d["below_full_confidence"]} of {d["techs_total"]} detections carry a confidence below 100, so the confidence field is worth filtering on if you need precision.</p>'
    '<h2>Limits</h2><ul><li>Eleven sites, picked by us, mostly well-known tech and developer sites. Not a web-wide survey.</li>'
    '<li>One page per site (the address we gave). A technology used only on other pages is not seen.</li>'
    '<li>Detection is by headers, scripts and markup patterns; it can miss or misattribute.</li></ul>'
    + foot('website-tech-stack-detector', 'a4_techstack.py', f'Input: {d["requested"]} results from a test run of the website-tech-stack-detector actor, stored as techstack.json with evidence strings removed.'))

# ---- 5 coverage
f = A5.compute()
lo = ', '.join(f'{k} ({v:g}%)' for k, v in f['lowest']); hi = ', '.join(f'{k} ({v:g}%)' for k, v in f['highest'])
art('how-complete-is-our-sample-data', f'How complete is our own sample data: {f["mean_cov"]:g}% of fields filled across {f["files"]} files',
    'Field coverage computed over all 24 sample CSVs: how many columns are fully filled, how many are empty, and how contact fields compare.',
    f'<h1>How complete is our own sample data: {f["mean_cov"]:g}% of fields filled across {f["files"]} files</h1>'
    f'<p>Every actor has a free sample CSV. We computed, for every column in every sample, the share of rows where the value is non-empty. That is {f["columns"]} columns over {f["rows_total"]} rows in total ({f["rows_min"]} to {f["rows_max"]} rows per file).</p>'
    f'<ul><li>Mean coverage across all columns: <strong>{f["mean_cov"]:g}%</strong>; the median file averages {f["median_file_avg"]:g}%.</li>'
    f'<li>{f["full"]} of {f["columns"]} columns ({pct(f["full"], f["columns"])}) are filled in every row. {f["empty"]} columns are empty in every row, spread over {f["files_with_empty_col"]} files.</li>'
    f'<li>Least complete files: {e(lo)}. Most complete: {e(hi)}.</li>'
    f'<li>Contact columns (anything named email or phone): {f["contact_cols"]} columns, mean coverage {f["contact_mean"]:g}%, and only {f["contact_full"]} are filled in every row.</li></ul>'
    '<p>Public sources do not publish every field for every record, and a contact detail is the field most often missing. Judge a sample by the columns you need, not the average. The <a href="../quality/">data quality pages</a> show the same coverage table for each source.</p>'
    '<h2>Limits</h2><ul><li>Samples of 4 to 12 rows. A column that is 100% filled in 5 rows can be half empty in 5,000.</li>'
    '<li>"Empty" means blank, <code>None</code>, <code>[]</code> or <code>{}</code>. A column that holds a value like "unknown" counts as filled.</li>'
    '<li>The samples have personal contact data masked, which does not change whether a value is present.</li></ul>'
    f'<h2>Data and method</h2><p>Computed by <a href="{GHSCRIPT}a5_coverage.py">a5_coverage.py</a> over the CSVs in <a href="https://github.com/Mamoo85/apify-actor-samples">apify-actor-samples</a> (pass the folder path as the first argument). Published {DATE}. We build and maintain these actors.</p>')

# ---- index
li = ''.join(f'<li><a href="{s}.html">{e(t)}</a><br><span class="muted">{e(dsc)}</span></li>' for s, t, dsc in ARTS)
body = ('<nav><a href="../index.html">All actors</a> | <a href="../digest/">Digest</a> | <a href="../quality/">Data quality</a></nav>'
        f'<h1>Articles</h1><p>Short analyses of the sample data our actors return. Each one states its sample size and limits, and links to the script that computes the figures.</p><ul>{li}</ul>')
open(f'{ROOT}/articles/index.html', 'w', encoding='utf-8').write(
    f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Articles from our open data</title>'
    f'<meta name="description" content="Five short analyses computed from the sample data of our public-data Apify actors, with scripts and stated limits."><link rel="canonical" href="{BASE}articles/">'
    f'<style>{CSS}.muted{{color:#666;font-size:14px}}</style></head><body>\n{body}\n</body></html>\n')
# sitemap
sm = open(f'{ROOT}/sitemap.xml', encoding='utf-8').read(); add = ''
for u in [BASE + 'articles/'] + [f'{BASE}articles/{s}.html' for s, _, _ in ARTS]:
    if f'<loc>{u}</loc>' not in sm: add += f'<url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n'
if add: open(f'{ROOT}/sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', add + '</urlset>'))
print('articles', len(ARTS))
