"""Generates: tools/check-a-company.html, tools/cost-calculator*.html, tools/which-data-source.html.
Prices come from data/pricing.json (refresh with scripts/refresh_pricing.py, then rerun this)."""
from lib import *
from js_common import COMMON

A, GEN = load_actors()
GROUPS = [
    ('sales', 'Sales and lead generation', ['local-business-leads', 'fmcsa-new-carrier-leads', 'new-business-filings', 'shopify-store-leads', 'website-contact-extractor', 'building-permits-leads', 'company-enrichment-by-domain']),
    ('funding', 'Funding, grants and compliance', ['sec-form-d-funding-leads', 'federal-grants-contracts', 'sanctions-screening', 'warn-layoff-alerts', 'city-council-agendas']),
    ('hiring', 'Hiring and jobs', ['ats-open-roles', 'workday-jobs-scraper', 'linkedin-public-jobs']),
    ('web', 'Websites, SEO and tech', ['technical-seo-page-audit', 'sitemap-link-inventory', 'website-tech-stack-detector', 'domain-intelligence-lookup', 'developer-signals']),
    ('research', 'Monitoring and research', ['company-news-monitor', 'app-store-reviews', 'amazon-product-search', 'meta-ad-library']),
]
FREE = {'website-contact-extractor': 'email-extractor-mx-check', 'domain-intelligence-lookup': 'domain-dns-mail-health-check', 'ats-open-roles': 'ats-job-board-viewer',
        'technical-seo-page-audit': 'page-seo-audit-from-html', 'federal-grants-contracts': 'federal-awards-by-recipient', 'app-store-reviews': 'app-store-review-summary',
        'sitemap-link-inventory': 'sitemap-xml-analyzer', 'sanctions-screening': 'sanctions-name-match-explainer', 'fmcsa-new-carrier-leads': 'usdot-mc-number-checker',
        'website-tech-stack-detector': 'website-tech-stack-hint-checker'}
for g in GROUPS:  # every public actor must be in a family
    for s in g[2]: assert s in A, s
assert set(A) == {s for g in GROUPS for s in g[2]}, set(A) ^ {s for g in GROUPS for s in g[2]}


def unit_price(e):
    """USD for one event; for tiered events the FREE-plan tier (the highest list price)."""
    if 'usd' in e: return e['usd']
    t = e['tiers']
    return t.get('FREE', next(iter(t.values())))['tieredEventPriceUsd']


def main_event(a):
    ev = [(k, v) for k, v in a['events'].items() if k != 'apify-actor-start']
    return ev[0] if ev else None


PRICES = {s: {'title': a['title'], 'url': a['url'], 'page': a['page'], 'events': {k: {'title': v['title'], 'usd': unit_price(v), 'tiers': {t: x['tieredEventPriceUsd'] for t, x in v.get('tiers', {}).items()}} for k, v in a['events'].items()}} for s, a in A.items()}

# ------------------------------------------------------------------ calculators
CALC_JS = r"""
var P=%PRICES%,SL=%SLUGS%,ST=%START%;
function fmt(n){return n>=1?'$'+n.toFixed(2):'$'+n.toFixed(4).replace(/0+$/,'').replace(/\.$/,'')}
function price(ev,tier){return(ev.tiers&&ev.tiers[tier]!=null)?ev.tiers[tier]:ev.usd}
function calc(){var tier=$('tier').value,total=0,h='';
SL.forEach(function(s){var a=P[s],rows='',sub=0,runs=+document.getElementById('r_'+s).value||0;
Object.keys(a.events).forEach(function(k){var ev=a.events[k],pr=price(ev,tier);
if(k===ST){var c=pr*runs;sub+=c;rows+='<tr><td>'+esc(ev.title)+' (per run)</td><td>'+fmt(pr)+'</td><td>'+runs+' runs</td><td>'+fmt(c)+'</td></tr>';return}
var q=+document.getElementById('q_'+s+'_'+k).value||0,c=pr*q;sub+=c;rows+='<tr><td>'+esc(ev.title)+'</td><td>'+fmt(pr)+'</td><td>'+q.toLocaleString()+'</td><td>'+fmt(c)+'</td></tr>'});
total+=sub;document.getElementById('t_'+s).innerHTML=rows;document.getElementById('s_'+s).textContent=fmt(sub)});
document.getElementById('tot').textContent=fmt(total)}
function build(){var h='';SL.forEach(function(s){var a=P[s],inp='<div class="row"><div><label>Runs per month</label><input type="number" min="0" value="4" id="r_'+s+'" oninput="calc()"></div>';
Object.keys(a.events).forEach(function(k){if(k===ST)return;inp+='<div><label>'+esc(a.events[k].title)+' per month</label><input type="number" min="0" value="1000" id="q_'+s+'_'+k+'" oninput="calc()"></div>'});
h+='<div class="card"><h3><a href="'+esc(a.page)+'">'+esc(a.title)+'</a></h3>'+inp+'</div><table><tr><th>Event</th><th>Price each</th><th>Quantity</th><th>Cost</th></tr><tbody id="t_'+s+'"></tbody><tr><th colspan="3">Subtotal per month</th><th id="s_'+s+'"></th></tr></table><p><a class="btn" href="'+esc(a.url)+'">Open on Apify Store</a></p>'});
document.getElementById('cards').innerHTML=h;calc()}
var hasTier=SL.some(function(s){return Object.keys(P[s].events).some(function(k){return P[s].events[k].tiers&&Object.keys(P[s].events[k].tiers).length})});
if(!hasTier)document.getElementById('tierwrap').style.display='none';
build();
"""

NAV = ' | '.join(f'<a href="{BASE}tools/cost-calculator-{k}.html">{n}</a>' for k, n, _ in GROUPS)


def calc_page(key, name, slugs):
    start = 'apify-actor-start'
    body = (f'<p class="note">Estimates what these actors cost on Apify\'s pay-per-event pricing, using the actual event prices published on each actor page (snapshot taken {GEN[:10]}, refreshed by script). '
            f'It counts only the actor\'s own event charges. It does not include any Apify subscription plan fee, and your free monthly platform credit, discounts or later price changes are not modelled. The Store page is always the authority on price.</p>'
            f'<p class="muted">Other families: {NAV}</p>'
            f'<div id="tierwrap"><label for="tier">Your Apify plan (some events are cheaper on paid plans)</label><select id="tier"><option value="FREE">Free</option><option value="BRONZE">Starter (Bronze)</option><option value="SILVER">Scale (Silver)</option><option value="GOLD">Business (Gold)</option></select></div>'
            f'<div id="cards"></div><h2>Total per month: <span id="tot"></span></h2>')
    body += '<script>document.getElementById("tier")&&document.getElementById("tier").addEventListener("change",function(){calc()})</script>'
    js = COMMON + CALC_JS.replace('%PRICES%', json.dumps({s: PRICES[s] for s in slugs})).replace('%SLUGS%', json.dumps(slugs)).replace('%START%', json.dumps(start))
    write(f'tools/cost-calculator-{key}.html', page(f'cost-calculator-{key}', f'Cost Calculator: {name}',
          f'Estimate the monthly pay-per-event cost of the {name.lower()} actors from their live published prices.', body, 'tools', js))


for key, name, slugs in GROUPS:
    calc_page(key, name, slugs)

rows = ''
for key, name, slugs in GROUPS:
    rows += f'<h2><a href="{BASE}tools/cost-calculator-{key}.html">{esc(name)}</a></h2><table><tr><th>Actor</th><th>Main event</th><th>Per 1,000</th></tr>'
    for s in slugs:
        me = main_event(A[s])
        if me:
            rows += f'<tr><td><a href="{A[s]["page"]}">{esc(A[s]["title"])}</a></td><td>{esc(me[1]["title"])}</td><td>${unit_price(me[1]) * 1000:,.2f}</td></tr>'
    rows += '</table>'
write('tools/cost-calculator.html', page('cost-calculator', 'Pay-per-Event Cost Calculator',
      f'What do these Apify actors cost? Prices read from each actor\'s published pay-per-event pricing (snapshot {GEN[:10]}).',
      '<p class="note">Pick a family to open its calculator. The table shows the main per-record event price times 1,000, on the Free plan where prices are tiered. Event prices are set by the publisher and can change; the Apify Store page is the authority.</p>' + rows, 'tools', ''))

# ------------------------------------------------------------------ quiz
GOALS = [  # (group label, [(goal text, actor slug, which input you need)])
    ('Find new customers or leads', [
        ('Local businesses by type and city (plumbers, dentists, cafes)', 'local-business-leads'),
        ('Newly authorised trucking and freight carriers', 'fmcsa-new-carrier-leads'),
        ('Newly registered companies (state business filings)', 'new-business-filings'),
        ('Shopify store owners', 'shopify-store-leads'),
        ('Contact details from a list of websites I already have', 'website-contact-extractor'),
        ('Companies pulling building permits (contractors, projects)', 'building-permits-leads'),
        ('Fill in company details from a list of domains', 'company-enrichment-by-domain')]),
    ('Funding, public sector and compliance', [
        ('Companies that just raised money (SEC Form D)', 'sec-form-d-funding-leads'),
        ('Federal grants and contract awards', 'federal-grants-contracts'),
        ('Screen names against sanctions lists', 'sanctions-screening'),
        ('Layoff notices (WARN)', 'warn-layoff-alerts'),
        ('Local government meetings and agenda items', 'city-council-agendas')]),
    ('Jobs and hiring signals', [
        ('Open jobs on company career pages (Greenhouse, Lever, Ashby)', 'ats-open-roles'),
        ('Jobs at large employers on Workday', 'workday-jobs-scraper'),
        ('Public LinkedIn job listings', 'linkedin-public-jobs')]),
    ('Websites, SEO and technology', [
        ('Audit on-page SEO across many URLs', 'technical-seo-page-audit'),
        ('List every URL on a site and check the links', 'sitemap-link-inventory'),
        ('Find out what technology websites use', 'website-tech-stack-detector'),
        ('DNS, mail provider and registration data for domains', 'domain-intelligence-lookup'),
        ('Developer trends: Hacker News and package registries', 'developer-signals')]),
    ('Research and monitoring', [
        ('News about specific companies', 'company-news-monitor'),
        ('App Store listings and reviews', 'app-store-reviews'),
        ('Amazon product search results', 'amazon-product-search'),
        ('Competitor ads in the Meta Ad Library', 'meta-ad-library')]),
]
QUIZ_DATA = {'groups': [{'label': g, 'goals': [{'t': t, 's': s} for t, s in gl]} for g, gl in GOALS],
             'actors': {s: {'title': A[s]['title'], 'url': A[s]['url'], 'page': A[s]['page'], 'desc': A[s]['desc'],
                            'free': (BASE + 'tools/' + FREE[s] + '.html') if s in FREE else '',
                            'ev': (lambda m: {'title': m[1]['title'], 'usd': unit_price(m[1])} if m else None)(main_event(A[s]))} for s in A}}
QUIZ_JS = r"""
var D=%DATA%,st={g:null,s:null,v:null,f:null};
var VOL=[['Under 50 records',25],['50 to 1,000',500],['1,000 to 50,000',10000],['More than 50,000',100000]];
var FRQ=[['One time','once'],['Repeating (weekly or monthly)','rep']];
function money(n){return n>=100?'$'+Math.round(n).toLocaleString('en-US'):n>=1?'$'+n.toFixed(2):'$'+n.toFixed(3)}
function opts(list,fn){return list.map(function(x,i){return '<button class="alt" style="display:block;width:100%;text-align:left" onclick="'+fn+'('+i+')">'+esc(x)+'</button>'}).join('')}
function show(){var o=$('q');
if(st.g===null){o.innerHTML='<h2>1. What are you trying to do?</h2>'+opts(D.groups.map(function(g){return g.label}),'pickG');return}
if(st.s===null){o.innerHTML='<h2>2. Which is closest?</h2>'+opts(D.groups[st.g].goals.map(function(g){return g.t}),'pickS')+'<p><button onclick="reset()">Start over</button></p>';return}
if(st.v===null){o.innerHTML='<h2>3. How many records do you need?</h2>'+opts(VOL.map(function(v){return v[0]}),'pickV')+'<p><button onclick="reset()">Start over</button></p>';return}
if(st.f===null){o.innerHTML='<h2>4. One time or repeating?</h2>'+opts(FRQ.map(function(v){return v[0]}),'pickF')+'<p><button onclick="reset()">Start over</button></p>';return}
result()}
function pickG(i){st.g=i;show()}function pickS(i){st.s=D.groups[st.g].goals[i].s;show()}function pickV(i){st.v=i;show()}function pickF(i){st.f=FRQ[i][1];show()}
function reset(){st={g:null,s:null,v:null,f:null};show()}
function result(){var a=D.actors[st.s],n=VOL[st.v][1],h='<div class="card"><h2>Recommended: <a href="'+esc(a.page)+'">'+esc(a.title)+'</a></h2><p>'+esc(a.desc)+'</p>';
if(a.ev){var c=a.ev.usd*n;h+='<p><b>Rough cost:</b> '+esc(a.ev.title)+' at '+money(a.ev.usd)+' each, so about <b>'+money(c)+'</b> for '+n.toLocaleString()+' records'+(st.f==='rep'?' per run':'')+'. This counts only the actor\'s per-record charge; the run-start fee and any second event type are small extras. Use the <a href="../tools/cost-calculator.html">cost calculator</a> for a full estimate.</p>'}
h+='<p><a class="btn" href="'+esc(a.url)+'">Open on Apify Store</a><a class="btn alt" href="'+esc(a.page)+'">Details and free sample CSV</a></p></div>';
if(st.v===0)h+='<div class="note"><b>Honest take:</b> for a few dozen records a manual search or the free tool below may be enough. '+(a.free?'':'We do not have a free browser tool for this one. ')+'The actor earns its keep when the list is big or you need it on a schedule.</div>';
if(a.free)h+='<p><b>Try the free version first:</b> <a href="'+esc(a.free)+'">free in-browser tool</a> (no sign-up, runs on what you paste).</p>';
if(st.f==='rep')h+='<p>For repeating needs, schedule the actor on Apify and send the results to a Google Sheet, webhook or your own storage. The first run with a small limit shows you the data shape and cost before you scale.</p>';
if(st.v>=2)h+='<p>For this volume, run a small test first (set the maximum results low) and check the data before the full run, since you pay per record returned.</p>';
h+='<p class="muted">Data and price snapshot: %GEN%. Prices can change; confirm on the Store page.</p><p><button onclick="reset()">Start over</button></p>';$('q').innerHTML=h}
show();
"""
quiz_body = '<p class="note">Four quick questions, then a single recommendation with an honest cost estimate. Nothing you click is sent anywhere or stored.</p><div id="q"></div>'
write('tools/which-data-source.html', page('which-data-source', 'Which Data Source Do I Need?',
      'Answer four questions and get a recommendation for which of our public-data actors fits, a rough cost, and a free option where one exists.',
      quiz_body, 'tools', COMMON + QUIZ_JS.replace('%DATA%', json.dumps(QUIZ_DATA)).replace('%GEN%', GEN[:10])))

# ------------------------------------------------------------------ check a company
CO_JS = r"""
function slugs(name,dom){var s={},add=function(x){x=x.toLowerCase().replace(/[^a-z0-9]/g,'');if(x.length>1)s[x]=1};
if(dom)add(dom.split('.')[0]);var w=name.toLowerCase().replace(/\b(inc|llc|ltd|corp|corporation|co|company|gmbh|plc)\b\.?/g,'').trim().split(/\s+/);add(w.join(''));if(w.length>1)add(w.join('-'));add(w[0]);
return Object.keys(s).slice(0,4)}
function sec(title,html){return '<div class="card"><h3>'+title+'</h3>'+html+'</div>'}
function block(id,title){var d=document.createElement('div');d.id=id;d.innerHTML=sec(title,'<p class="muted">Checking...</p>');$('out').appendChild(d);return function(h){d.innerHTML=sec(title,h)}}
function run(){var name=$('n').value.trim(),dom=$('d').value.trim().toLowerCase().replace(/^https?:\/\//,'').replace(/^www\./,'').split('/')[0];
if(name.length<2){$('out').innerHTML='<p class="bad">Enter a company name.</p>';return}$('out').innerHTML='';
var q=encodeURIComponent(name);
// GLEIF
var g=block('g','Legal entity registry (GLEIF)');getJson('https://api.gleif.org/api/v1/lei-records?filter%5Bfulltext%5D='+q+'&page%5Bsize%5D=5').then(function(j){var r=j.data||[];
if(!r.length){g('<p>No Legal Entity Identifier found. Most small private companies have none; this is not a sign of a problem.</p>');return}
g('<table><tr><th>Legal name</th><th>Country</th><th>Entity</th><th>LEI</th></tr>'+r.map(function(x){var e=x.attributes.entity,a=e.legalAddress||{};return'<tr><td>'+esc(e.legalName.name)+'</td><td>'+esc(a.country||'')+(a.city?', '+esc(a.city):'')+'</td><td>'+esc(e.status)+' / '+esc(x.attributes.registration.status)+'</td><td>'+esc(x.attributes.lei)+'</td></tr>'}).join('')+'</table><p class="muted">Free-text match, so the first rows may be a different company. Only companies that obtained an LEI appear (mostly financial and large firms).</p>')}).catch(function(e){g('<p class="bad">Lookup failed: '+esc(e.message)+'</p>')});
// Wikidata
var w=block('w','Encyclopedic facts (Wikidata)');getJson('https://www.wikidata.org/w/api.php?action=wbsearchentities&search='+q+'&language=en&type=item&limit=3&format=json&origin=*').then(function(j){var s=j.search||[];
if(!s.length){w('<p>No Wikidata entry. Smaller companies usually have none.</p>');return}
return getJson('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+s[0].id+'&props=claims&format=json&origin=*').then(function(d){var c=d.entities[s[0].id].claims||{};function v(p){var x=(c[p]||[])[0];x=x&&x.mainsnak&&x.mainsnak.datavalue&&x.mainsnak.datavalue.value;return x}
var site=v('P856'),inc=v('P571'),emp=v('P1128');
w('<p><b>'+esc(s[0].label)+'</b> &mdash; '+esc(s[0].description||'no description')+' (<a href="https://www.wikidata.org/wiki/'+s[0].id+'" rel="noopener">'+s[0].id+'</a>)</p><table>'+(site?'<tr><th>Website</th><td>'+esc(typeof site==='string'?site:'')+'</td></tr>':'')+(inc?'<tr><th>Founded</th><td>'+esc((inc.time||'').replace(/^\+/,'').slice(0,10).replace(/-00-00$/,'').replace(/-00$/,''))+'</td></tr>':'')+(emp?'<tr><th>Employees (listed)</th><td>'+esc(String(emp.amount||'').replace(/^\+/,''))+'</td></tr>':'')+'</table><p class="muted">Top search hit only; verify it is the right company. Other hits: '+s.slice(1).map(function(x){return esc(x.label)+' ('+esc(x.description||'?')+')'}).join('; ')+'</p>')})}).catch(function(e){w('<p class="bad">Lookup failed: '+esc(e.message)+'</p>')});
// USAspending
var u=block('u','US federal money received (USAspending.gov)');getJson('https://api.usaspending.gov/api/v2/recipient/',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({keyword:name,limit:5,order:'desc',sort:'amount'})}).then(function(j){var r=j.results||[];
if(!r.length){u('<p>No federal award recipient matches this name.</p>');return}
u('<table><tr><th>Recipient</th><th>Level</th><th>Total awards (all time, as recorded)</th></tr>'+r.map(function(x){return'<tr><td>'+esc(x.name)+'</td><td>'+(x.recipient_level==='P'?'parent':x.recipient_level==='C'?'child':'single')+'</td><td>$'+Math.round(x.amount||0).toLocaleString('en-US')+'</td></tr>'}).join('')+'</table><p class="muted">Name match, may include unrelated companies with similar names. Federal awards only: no state, local or private contracts.</p>')}).catch(function(e){u('<p class="bad">Lookup failed: '+esc(e.message)+'</p>')});
// Jobs
var jb=block('j','Open jobs on public job boards');var sl=slugs(name,dom),found=[];
Promise.all(sl.map(function(s){return Promise.all([
getJson('https://boards-api.greenhouse.io/v1/boards/'+s+'/jobs').then(function(j){if((j.jobs||[]).length)found.push('Greenhouse: '+j.jobs.length+' jobs (board "'+s+'")')}).catch(function(){}),
getJson('https://api.lever.co/v0/postings/'+s+'?mode=json').then(function(j){if(j.length)found.push('Lever: '+j.length+' jobs (board "'+s+'")')}).catch(function(){}),
getJson('https://api.ashbyhq.com/posting-api/job-board/'+s).then(function(j){if((j.jobs||[]).length)found.push('Ashby: '+j.jobs.length+' jobs (board "'+s+'")')}).catch(function(){})])})).then(function(){
jb(found.length?'<ul>'+found.map(function(f){return'<li>'+esc(f)+'</li>'}).join('')+'</ul><p class="muted">Board names are guessed from the company name; a hit could in rare cases be a different company. See them in the <a href="ats-job-board-viewer.html">job board viewer</a>.</p>':'<p>No Greenhouse, Lever or Ashby board found under the guessed names ('+sl.map(esc).join(', ')+'). The company may use another system or a different board name.</p>')});
// HN
var h=block('h','Tech community mentions (Hacker News)');getJson('https://hn.algolia.com/api/v1/search?query='+encodeURIComponent('"'+name+'"')+'&tags=story&hitsPerPage=5').then(function(j){var r=j.hits||[];
h(r.length?'<p>'+(j.nbHits||0).toLocaleString()+' matching stories. Top results:</p><ul>'+r.map(function(x){return'<li><a href="https://news.ycombinator.com/item?id='+esc(x.objectID)+'" rel="noopener">'+esc(x.title||'')+'</a> <span class="muted">('+esc((x.created_at||'').slice(0,10))+', '+(x.points||0)+' points)</span></li>'}).join('')+'</ul>':'<p>No Hacker News stories mention this name.</p>')}).catch(function(e){h('<p class="bad">Lookup failed: '+esc(e.message)+'</p>')});
// Domain
if(/^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(dom)){var dm=block('dm','Domain and email setup ('+esc(dom)+')');var qq=function(n,t){return doh(n,t).catch(function(){return null})};
Promise.all([qq(dom,'MX'),qq(dom,'TXT'),qq('_dmarc.'+dom,'TXT'),getJson('https://rdap.org/domain/'+encodeURIComponent(dom)).catch(function(){return null})]).then(function(r){
var mx=(r[0]||[]).filter(function(x){return x.type===15}),tx=(r[1]||[]).filter(function(x){return x.type===16&&/v=spf1/i.test(x.data)}),dm2=(r[2]||[]).filter(function(x){return x.type===16&&/DMARC1/i.test(x.data)}),reg='';
if(r[3]&&r[3].events){var e=r[3].events.filter(function(x){return x.eventAction==='registration'})[0];if(e)reg=((Date.now()-Date.parse(e.eventDate))/(365.25*864e5)).toFixed(1)+' years (registered '+e.eventDate.slice(0,10)+')'}
dm('<table><tr><th>Receives email (MX)</th><td>'+(mx.length?'Yes: '+esc(mx[0].data.split(' ').slice(1).join(' ').replace(/\.$/,'')):'No MX record')+'</td></tr><tr><th>SPF / DMARC</th><td>'+(tx.length?'SPF yes':'no SPF')+' / '+(dm2.length?'DMARC yes':'no DMARC')+'</td></tr><tr><th>Domain age</th><td>'+(reg||'not available from RDAP')+'</td></tr></table>')})}
// Not covered
var nc=document.createElement('div');nc.innerHTML=sec('What this page cannot tell you','<ul><li><b>Whether the company is legally registered and in good standing.</b> US state registries have no open browser API. Search the Secretary of State site for the state, or <a href="https://opencorporates.com/companies?q='+q+'" rel="noopener">OpenCorporates</a>.</li><li><b>SEC filings.</b> SEC EDGAR blocks browser requests, so open <a href="https://www.sec.gov/cgi-bin/browse-edgar?company='+q+'&type=&action=getcompany" rel="noopener">EDGAR company search</a> yourself. Our <a href="https://apify.com/transparent_meteorite/sec-form-d-funding-leads">Form D actor</a> covers funding filings in bulk.</li><li><b>Sanctions screening.</b> Use the <a href="https://sanctionssearch.ofac.treas.gov/" rel="noopener">official OFAC search</a>; the <a href="sanctions-name-match-explainer.html">name match explainer</a> shows how matching works.</li><li><b>Contacts, financials, ownership, litigation, credit, reviews, news.</b> Not available from free open sources in the browser.</li></ul><p>To check many companies at once, run the <a href="https://apify.com/transparent_meteorite/company-enrichment-by-domain">company enrichment actor</a> on a list of domains.</p>');$('out').appendChild(nc)}
$('n').addEventListener('keydown',function(e){if(e.key==='Enter')run()});$('d').addEventListener('keydown',function(e){if(e.key==='Enter')run()});
"""
co_body = ('<p class="note">Looks a company up across free, key-free public sources, directly from your browser: GLEIF (legal entity registry), Wikidata, USAspending.gov, public job board APIs, Hacker News search, and (if you give a domain) public DNS and RDAP. '
           'It is a quick first look, not due diligence. The section at the bottom lists what it cannot do.</p>'
           '<div class="row"><div><label for="n">Company name</label><input id="n" placeholder="e.g. Stripe"></div><div><label for="d">Website domain (optional)</label><input id="d" placeholder="stripe.com"></div></div>'
           '<button onclick="run()">Check company</button><div id="out"></div>')
write('tools/check-a-company.html', page('check-a-company', 'Check a Company: Free Open-Source Lookup',
      'Look up a company in GLEIF, Wikidata, USAspending, job boards, Hacker News and DNS from your browser, with a clear list of what it cannot check.',
      co_body, 'tools', COMMON + CO_JS))

# ------------------------------------------------------------------ tools index
import glob
items = []
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', '*.html'))):
    n = os.path.basename(f)[:-5]
    if n == 'index': continue
    s = open(f, encoding='utf-8').read()
    t = re.search(r'<title>([^<]*)', s); d = re.search(r'<meta name="description" content="([^"]*)"', s)
    items.append(f'<li><a href="{n}.html"><b>{t.group(1) if t else n}</b></a><br><span class="muted">{d.group(1) if d else ""}</span></li>')
write('tools/index.html', page('index', 'Free Data Tools', 'Free in-browser tools, a company lookup, cost calculators and a data source quiz. No sign-up, no tracking, no API keys.',
      '<ul>' + ''.join(items) + '</ul>', 'tools', ''))
