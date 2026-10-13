"""Generates the 7 free in-browser tools into tools/. Run: python scripts/build_tools.py"""
from lib import *
from js_common import COMMON

A, GEN = load_actors()
T = {}

# 1 ---------------------------------------------------------------- sitemap analyzer
T['sitemap-xml-analyzer'] = dict(
    title='Sitemap XML Analyzer',
    desc='Paste a sitemap.xml and get URL counts by section, duplicates, stale lastmod dates and format problems, all in your browser.',
    body='''<p class="note">Browsers block one site from fetching another site's sitemap, so open your sitemap URL, copy the XML (Ctrl+A, Ctrl+C) and paste it here. It handles a normal sitemap (urlset) and a sitemap index. It does not fetch or check whether each URL actually loads.</p>
<textarea id="in" placeholder="Paste sitemap XML here"></textarea><button onclick="run()">Analyze</button><button class="alt" onclick="csv()">Download URL list (CSV)</button><div id="out"></div>'''
          + scale_box(A, 'sitemap-link-inventory', 'To crawl a whole site, follow nested sitemaps and check that every link still returns a good status, '),
    js='''var rows=[];
function run(){var x=$("in").value.trim(),o=$("out");rows=[];if(!x){o.innerHTML="";return}
var d=new DOMParser().parseFromString(x,"application/xml");if(d.querySelector("parsererror")){o.innerHTML='<p class="bad">This is not valid XML. Check you copied the raw sitemap, not the rendered page.</p>';return}
var isIdx=d.getElementsByTagName("sitemapindex").length>0,tag=isIdx?"sitemap":"url",els=d.getElementsByTagName(tag),seen={},dups=0,sec={},bad=[],old=0,withMod=0,now=Date.now(),mn=null,mx=null;
for(var i=0;i<els.length;i++){var l=els[i].getElementsByTagName("loc")[0],m=els[i].getElementsByTagName("lastmod")[0];if(!l)continue;var u=l.textContent.trim(),lm=m?m.textContent.trim():"";
if(seen[u])dups++;seen[u]=1;rows.push([u,lm]);
if(!/^https:/.test(u))bad.push(u+" (not https)");if(/[A-Z]/.test(u.replace(/^https?:\\/\\/[^/]+/,"").split("?")[0]))bad.push(u+" (uppercase in path)");if(/\\s/.test(u))bad.push(u+" (whitespace)");if(u.indexOf("?")>-1)bad.push(u+" (query string)");
try{var p=new URL(u).pathname.split("/")[1]||"(root)";sec[p]=(sec[p]||0)+1}catch(e){bad.push(u+" (unparseable)")}
if(lm){var t=Date.parse(lm);if(!isNaN(t)){withMod++;if(now-t>365*864e5)old++;if(mn===null||t<mn)mn=t;if(mx===null||t>mx)mx=t}else bad.push(u+" (bad lastmod: "+lm+")")}}
var h="<h2>"+(isIdx?"Sitemap index":"URL sitemap")+"</h2><table><tr><th>Entries</th><td>"+rows.length+"</td></tr><tr><th>Duplicates</th><td class='"+(dups?"bad":"ok")+"'>"+dups+"</td></tr>";
if(!isIdx){h+="<tr><th>With lastmod</th><td>"+withMod+" of "+rows.length+"</td></tr>";if(withMod)h+="<tr><th>Older than 1 year</th><td>"+old+" ("+Math.round(100*old/withMod)+"%)</td></tr><tr><th>lastmod range</th><td>"+new Date(mn).toISOString().slice(0,10)+" to "+new Date(mx).toISOString().slice(0,10)+"</td></tr>"}
h+="<tr><th>Protocol limit</th><td class='"+(rows.length>50000?"bad":"ok")+"'>"+(rows.length>50000?"Over 50,000 entries: split it":"Within 50,000 entries")+"</td></tr></table>";
if(isIdx)h+='<p class="muted">This is an index of sitemaps. Paste each child sitemap separately to analyze the URLs inside.</p>';
else{var k=Object.keys(sec).sort(function(a,b){return sec[b]-sec[a]});h+="<h2>By top-level section</h2><table><tr><th>Section</th><th>URLs</th></tr>"+k.slice(0,25).map(function(s){return"<tr><td>/"+esc(s)+"</td><td>"+sec[s]+"</td></tr>"}).join("")+"</table>"}
if(bad.length)h+="<h2>Format notes ("+bad.length+")</h2><p class='muted'>Not errors by the sitemap spec, but worth a look.</p><table>"+bad.slice(0,50).map(function(b){return"<tr><td class='warn'>"+esc(b)+"</td></tr>"}).join("")+"</table>"+(bad.length>50?"<p class='muted'>Showing 50 of "+bad.length+".</p>":"");
o.innerHTML=h}
function csv(){if(!rows.length)run();if(rows.length)dl("sitemap-urls.csv",toCsv([["url","lastmod"]].concat(rows)))}'''
)

# 2 ---------------------------------------------------------------- email extractor
T['email-extractor-mx-check'] = dict(
    title='Email Extractor and MX Check',
    desc='Paste any text and pull out the email addresses, de-duplicated, with role inboxes flagged and an optional check that each domain can receive mail.',
    body='''<p class="note">Everything is parsed in your browser. The optional MX check sends only the unique domain names (not the addresses) to Cloudflare's public DNS-over-HTTPS service. An MX record means the domain accepts mail; it cannot prove that a specific mailbox exists. Handles "name [at] domain [dot] com" style obfuscation.</p>
<textarea id="in" placeholder="Paste page text, a contact page, a CSV, anything"></textarea><button onclick="run(false)">Extract</button><button onclick="run(true)">Extract and check MX</button><button class="alt" onclick="csv()">Download CSV</button><div id="out"></div>'''
          + scale_box(A, 'website-contact-extractor', 'To crawl many company websites and collect contact pages, emails and social links automatically, '),
    js='''var res=[];var ROLE=/^(info|sales|admin|support|contact|hello|office|help|team|billing|accounts|enquiries|inquiries|marketing|careers|jobs|press|media|webmaster|postmaster|abuse|noreply|no-reply|donotreply|service|orders|booking|reservations|hr|privacy|legal)$/i;
var FREE={"gmail.com":1,"yahoo.com":1,"hotmail.com":1,"outlook.com":1,"aol.com":1,"icloud.com":1,"proton.me":1,"protonmail.com":1,"live.com":1,"msn.com":1,"gmx.com":1,"mail.com":1,"yandex.com":1};
function run(mx){var t=$("in").value;if(!t.trim()){$("out").innerHTML="";return}
t=t.replace(/\\s*[\\[(]\\s*at\\s*[\\])]\\s*/gi,"@").replace(/\\s*[\\[(]\\s*dot\\s*[\\])]\\s*/gi,".");
var m=t.match(/[A-Za-z0-9._%+\\-]+@[A-Za-z0-9\\-]+(?:\\.[A-Za-z0-9\\-]+)*\\.[A-Za-z]{2,}/g)||[],seen={},tot=m.length;res=[];
m.forEach(function(e){e=e.replace(/[.]+$/,"");var k=e.toLowerCase();if(seen[k])return;seen[k]=1;var p=k.split("@");res.push({email:k,local:p[0],domain:p[1],role:ROLE.test(p[0]),free:!!FREE[p[1]],mx:""})});
if(/\\.(png|jpe?g|gif|svg|webp)$/i.test("")){}
res=res.filter(function(r){return !/\\.(png|jpe?g|gif|svg|webp|css|js)$/i.test(r.domain)});
draw(tot);if(mx)checkMx(tot)}
function draw(tot){var o=$("out");if(!res.length){o.innerHTML="<p>No email addresses found.</p>";return}
o.innerHTML="<p>"+tot+" found, "+res.length+" unique.</p><table><tr><th>Email</th><th>Type</th><th>Domain mail (MX)</th></tr>"+res.map(function(r){return"<tr><td>"+esc(r.email)+"</td><td>"+(r.role?"role inbox":r.free?"free webmail":"named / company")+"</td><td class='"+(r.mx&&r.mx.indexOf("No")===0?"bad":r.mx?"ok":"")+"'>"+esc(r.mx||"not checked")+"</td></tr>"}).join("")+"</table>"}
function checkMx(tot){var doms=[];res.forEach(function(r){if(doms.indexOf(r.domain)<0)doms.push(r.domain)});doms=doms.slice(0,50);
Promise.all(doms.map(function(d){return doh(d,"MX").then(function(a){var mxs=a.filter(function(x){return x.type===15}).map(function(x){return x.data.split(" ").slice(1).join(" ").replace(/\\.$/,"")});return[d,mxs.length?"Yes: "+mxs.slice(0,2).join(", "):"No MX record"]}).catch(function(){return[d,"Lookup failed"]})})).then(function(p){var mp={};p.forEach(function(x){mp[x[0]]=x[1]});res.forEach(function(r){r.mx=mp[r.domain]||"Skipped (limit 50 domains)"});draw(tot)})}
function csv(){if(!res.length)run(false);dl("emails.csv",toCsv([["email","type","domain","mx"]].concat(res.map(function(r){return[r.email,r.role?"role":r.free?"free":"named",r.domain,r.mx]}))))}'''
)

# 3 ---------------------------------------------------------------- domain dns/mail
T['domain-dns-mail-health-check'] = dict(
    title='Domain DNS and Email Setup Checker',
    desc="Look up a domain's A, MX, NS, SPF and DMARC records and its registration age, using free public DNS and RDAP services.",
    body='''<p class="note">Calls two free public services directly from your browser: Cloudflare DNS-over-HTTPS (records) and the RDAP bootstrap at rdap.org (registration date and registrar). Nothing goes through our servers. RDAP data for some country domains is limited or blocked, and DNS cannot tell you what is on the website itself.</p>
<label for="d">Domain (no https://)</label><input id="d" placeholder="example.com" value=""><button onclick="run()">Check</button><div id="out"></div>'''
          + scale_box(A, 'domain-intelligence-lookup', 'To run DNS, email-provider and registration lookups on a list of thousands of domains, '),
    js='''function clean(v){return v.trim().toLowerCase().replace(/^https?:\\/\\//,"").replace(/^www\\./,"").split("/")[0]}
function run(){var d=clean($("d").value),o=$("out");if(!/^[a-z0-9-]+(\\.[a-z0-9-]+)+$/.test(d)){o.innerHTML='<p class="bad">Enter a domain like example.com</p>';return}
o.innerHTML="<p>Looking up "+esc(d)+"...</p>";
var q=function(n,t){return doh(n,t).catch(function(){return null})};
Promise.all([q(d,"A"),q(d,"MX"),q(d,"NS"),q(d,"TXT"),q("_dmarc."+d,"TXT"),getJson("https://rdap.org/domain/"+encodeURIComponent(d)).catch(function(){return null})]).then(function(r){
var A=r[0],MX=r[1],NS=r[2],TX=r[3],DM=r[4],RD=r[5];function txt(a){return(a||[]).filter(function(x){return x.type===16}).map(function(x){return x.data.replace(/^"|"$/g,"").replace(/"\\s*"/g,"")})}
var spf=txt(TX).filter(function(s){return/^v=spf1/i.test(s)}),dmarc=txt(DM).filter(function(s){return/^v=DMARC1/i.test(s)});
var mxs=(MX||[]).filter(function(x){return x.type===15}).map(function(x){return x.data.replace(/\\.$/,"")}),prov="unknown / self-hosted";var mj=mxs.join(" ").toLowerCase();
if(/google|googlemail/.test(mj))prov="Google Workspace / Gmail";else if(/outlook|protection\\.outlook|microsoft/.test(mj))prov="Microsoft 365";else if(/zoho/.test(mj))prov="Zoho";else if(/proton/.test(mj))prov="Proton";else if(/mimecast/.test(mj))prov="Mimecast";else if(/pphosted|proofpoint/.test(mj))prov="Proofpoint";else if(/secureserver/.test(mj))prov="GoDaddy";
var pol=dmarc.length?((dmarc[0].match(/p=([a-z]+)/i)||[])[1]||"?"):null,rows=[];
function R(k,v,c){rows.push("<tr><th>"+k+"</th><td class='"+(c||"")+"'>"+v+"</td></tr>")}
R("A records",A&&A.filter(function(x){return x.type===1}).length?esc(A.filter(function(x){return x.type===1}).map(function(x){return x.data}).join(", ")):"none found",A&&A.length?"":"warn");
R("Nameservers",NS&&NS.length?esc(NS.map(function(x){return x.data.replace(/\\.$/,"")}).join(", ")):"none found");
R("Mail (MX)",mxs.length?esc(mxs.join(", "))+"<br><span class='muted'>Looks like: "+prov+"</span>":"No MX record: this domain cannot receive email",mxs.length?"ok":"bad");
R("SPF",spf.length?esc(spf[0]):"No SPF record",spf.length?"ok":"warn");
R("DMARC",dmarc.length?esc(dmarc[0])+"<br><span class='muted'>Policy: "+esc(pol)+(pol==="none"?" (monitoring only)":"")+"</span>":"No DMARC record",dmarc.length&&pol!=="none"?"ok":"warn");
if(RD&&RD.events){var ev={};RD.events.forEach(function(e){ev[e.eventAction]=e.eventDate});var cr=ev.registration;if(cr){var yrs=((Date.now()-Date.parse(cr))/(365.25*864e5)).toFixed(1);R("Registered",esc(cr.slice(0,10))+" ("+yrs+" years ago)")}if(ev.expiration)R("Expires",esc(ev.expiration.slice(0,10)));
var reg=(RD.entities||[]).filter(function(e){return(e.roles||[]).indexOf("registrar")>-1})[0];if(reg&&reg.vcardArray){var fn=reg.vcardArray[1].filter(function(v){return v[0]==="fn"})[0];if(fn)R("Registrar",esc(fn[3]))}}else R("Registration (RDAP)","not available for this domain's registry","muted");
o.innerHTML="<table>"+rows.join("")+"</table><p class='muted'>Checked "+new Date().toISOString().slice(0,16).replace("T"," ")+" UTC.</p>"})}
$("d").addEventListener("keydown",function(e){if(e.key==="Enter")run()})'''
)

# 4 ---------------------------------------------------------------- job boards
T['ats-job-board-viewer'] = dict(
    title='Greenhouse, Lever and Ashby Job Board Viewer',
    desc='Enter a company board name and list its open jobs from the public Greenhouse, Lever or Ashby job board API, then filter and export to CSV.',
    body='''<p class="note">These three applicant tracking systems publish a free, key-free job board API that browsers may call directly. Paste a careers URL (boards.greenhouse.io/name, jobs.lever.co/name, jobs.ashbyhq.com/name) or pick a vendor and type the board name. Companies on Workday, iCIMS, Taleo and others are not covered here, and not every company uses these three.</p>
<div class="row"><div><label for="v">Vendor</label><select id="v"><option>greenhouse</option><option>lever</option><option>ashby</option></select></div><div><label for="b">Board name or careers URL</label><input id="b" placeholder="airbnb  or  https://jobs.lever.co/spotify"></div></div>
<button onclick="run()">List jobs</button><button class="alt" onclick="csv()">Download CSV</button><label for="f">Filter (title, location, team)</label><input id="f" placeholder="e.g. engineer, remote" oninput="draw()"><div id="out"></div>'''
          + scale_box(A, 'ats-open-roles', 'To pull jobs from hundreds of boards at once and keep them refreshed, '),
    js='''var jobs=[];
function parse(){var b=$("b").value.trim(),v=$("v").value,m;
if(m=b.match(/greenhouse\\.io\\/(?:embed\\/job_board\\?for=)?([\\w-]+)/i)){v="greenhouse";b=m[1]}else if(m=b.match(/lever\\.co\\/([\\w-]+)/i)){v="lever";b=m[1]}else if(m=b.match(/ashbyhq\\.com\\/([\\w%.-]+)/i)){v="ashby";b=m[1]}
$("v").value=v;return[v,b.replace(/[^\\w%.-]/g,"")]}
function run(){var p=parse(),v=p[0],b=p[1],o=$("out");if(!b){o.innerHTML='<p class="bad">Enter a board name.</p>';return}o.innerHTML="<p>Loading...</p>";jobs=[];
var u,map;if(v==="greenhouse"){u="https://boards-api.greenhouse.io/v1/boards/"+b+"/jobs";map=function(j){return(j.jobs||[]).map(function(x){return[x.title,(x.location||{}).name||"","",x.absolute_url,(x.updated_at||"").slice(0,10)]})}}
else if(v==="lever"){u="https://api.lever.co/v0/postings/"+b+"?mode=json";map=function(j){return j.map(function(x){return[x.text,(x.categories||{}).location||"",(x.categories||{}).team||"",x.hostedUrl,x.createdAt?new Date(x.createdAt).toISOString().slice(0,10):""]})}}
else{u="https://api.ashbyhq.com/posting-api/job-board/"+b;map=function(j){return(j.jobs||[]).map(function(x){return[x.title,x.location||"",x.department||x.team||"",x.jobUrl,(x.publishedAt||"").slice(0,10)]})}}
getJson(u).then(function(j){jobs=map(j);draw()}).catch(function(e){o.innerHTML='<p class="bad">Could not load board "'+esc(b)+'" on '+v+' ('+esc(e.message)+'). Check the spelling and vendor; the company may use a different ATS.</p>'})}
function draw(){var f=$("f").value.toLowerCase(),o=$("out");if(!jobs.length&&!f)return;var s=jobs.filter(function(j){return!f||j.join(" ").toLowerCase().indexOf(f)>-1});
o.innerHTML="<p>"+s.length+" of "+jobs.length+" jobs</p><table><tr><th>Title</th><th>Location</th><th>Team</th><th>Date</th></tr>"+s.slice(0,300).map(function(j){return"<tr><td><a href='"+esc(j[3])+"' rel='noopener'>"+esc(j[0])+"</a></td><td>"+esc(j[1])+"</td><td>"+esc(j[2])+"</td><td>"+esc(j[4])+"</td></tr>"}).join("")+"</table>"+(s.length>300?"<p class='muted'>Showing 300; download the CSV for all.</p>":"")}
function csv(){if(jobs.length)dl("jobs.csv",toCsv([["title","location","team","url","date"]].concat(jobs)))}'''
)

# 5 ---------------------------------------------------------------- seo audit
T['page-seo-audit-from-html'] = dict(
    title='On-Page SEO Audit from HTML',
    desc="Paste a page's HTML source and check title, description, headings, canonical, images, social tags and structured data in your browser.",
    body='''<p class="note">Browsers block one site from fetching another, so open the page, press Ctrl+U (View Source), copy everything and paste it here. It checks what is in the HTML you paste. It cannot measure speed, rankings, backlinks, or content rendered by JavaScript after load.</p>
<textarea id="in" placeholder="Paste the page source (starts with &lt;!doctype html&gt;)"></textarea><button onclick="run()">Audit</button><div id="out"></div>'''
          + scale_box(A, 'technical-seo-page-audit', 'To audit hundreds of URLs with the same checks plus status codes and redirects, '),
    js='''function run(){var x=$("in").value.trim(),o=$("out");if(!x){o.innerHTML="";return}var d=new DOMParser().parseFromString(x,"text/html"),R=[];
function add(k,v,s,n){R.push("<tr><th>"+k+"</th><td class='"+s+"'>"+v+"</td><td class='muted'>"+(n||"")+"</td></tr>")}
function meta(n,a){var e=d.querySelector('meta['+(a||"name")+'="'+n+'"]');return e?e.getAttribute("content")||"":null}
var t=(d.querySelector("title")||{}).textContent;t=t?t.trim():"";add("Title",t?esc(t)+" ("+t.length+" chars)":"Missing",t?(t.length>=30&&t.length<=60?"ok":"warn"):"bad","Aim for roughly 30-60 characters.");
var md=meta("description");add("Meta description",md?esc(md)+" ("+md.length+")":"Missing",md?(md.length>=70&&md.length<=160?"ok":"warn"):"warn","Aim for roughly 70-160 characters.");
var c=d.querySelector('link[rel="canonical"]');add("Canonical",c?esc(c.getAttribute("href")):"Missing",c?"ok":"warn");
var rb=meta("robots");add("Robots meta",rb?esc(rb):"none (indexable by default)",rb&&/noindex/i.test(rb)?"bad":"ok",rb&&/noindex/i.test(rb)?"Page asks not to be indexed.":"");
add("Language",d.documentElement.getAttribute("lang")?esc(d.documentElement.getAttribute("lang")):"Missing lang attribute",d.documentElement.getAttribute("lang")?"ok":"warn");
add("Viewport",meta("viewport")?"present":"Missing",meta("viewport")?"ok":"warn","Needed for mobile layouts.");
var h1=d.querySelectorAll("h1");add("H1 count",h1.length+(h1[0]?": "+esc(h1[0].textContent.trim().slice(0,80)):""),h1.length===1?"ok":"warn","One H1 is the usual convention.");
var hs=[].slice.call(d.querySelectorAll("h1,h2,h3,h4,h5,h6")),skip=0,last=0;hs.forEach(function(h){var n=+h.tagName[1];if(last&&n>last+1)skip++;last=n});add("Heading outline",hs.length+" headings"+(skip?", "+skip+" skipped level(s)":""),skip?"warn":"ok");
var im=[].slice.call(d.querySelectorAll("img")),na=im.filter(function(i){return!i.hasAttribute("alt")}).length;add("Images",im.length+" total, "+na+" without alt attribute",na?"warn":"ok");
var og=["og:title","og:description","og:image","og:url"].filter(function(p){return meta(p,"property")===null});add("Open Graph",og.length?"Missing: "+og.join(", "):"og:title, description, image, url present",og.length?"warn":"ok");
add("Twitter card",meta("twitter:card")?esc(meta("twitter:card")):"Missing",meta("twitter:card")?"ok":"warn");
var ld=[].slice.call(d.querySelectorAll('script[type="application/ld+json"]')),bad=0,types=[];ld.forEach(function(s){try{var j=JSON.parse(s.textContent);(Array.isArray(j)?j:[j]).forEach(function(z){if(z&&z["@type"])types.push(z["@type"])})}catch(e){bad++}});
add("Structured data (JSON-LD)",ld.length?ld.length+" block(s)"+(types.length?": "+esc(types.join(", ")):"")+(bad?", "+bad+" with invalid JSON":""):"None",bad?"bad":ld.length?"ok":"warn");
var a=[].slice.call(d.querySelectorAll("a[href]")),ext=a.filter(function(l){return/^https?:/.test(l.getAttribute("href"))}).length,nf=a.filter(function(l){return/nofollow/.test(l.getAttribute("rel")||"")}).length;add("Links",a.length+" total, "+ext+" absolute http(s), "+nf+" nofollow","ok");
var words=(d.body?d.body.textContent:"").trim().split(/\\s+/).filter(Boolean).length;add("Word count (HTML text)",String(words),words<150?"warn":"ok","Counts text present in the pasted source only.");
o.innerHTML="<table><tr><th>Check</th><th>Result</th><th>Note</th></tr>"+R.join("")+"</table>"}'''
)

# 6 ---------------------------------------------------------------- usaspending
T['federal-awards-by-recipient'] = dict(
    title='Federal Awards by Recipient',
    desc='Search US federal contracts or grants awarded to a company or organisation, using the free USAspending.gov API directly from your browser.',
    body='''<p class="note">Calls the public USAspending.gov API (no key needed) straight from your browser; nothing goes through our servers. Name matching is fuzzy and a company can appear under several legal names or subsidiaries, so check the recipient column. Shows the 25 largest awards that had activity in the period (the amount shown is the award's total, not just the period); it is not a complete audit and USAspending data can lag the source agencies.</p>
<div class="row"><div><label for="n">Recipient name</label><input id="n" placeholder="e.g. Lockheed Martin"></div><div><label for="k">Award kind</label><select id="k"><option value="c">Contracts</option><option value="g">Grants</option></select></div><div><label for="y">Activity period</label><select id="y"><option value="2024">Active since FY2024</option><option value="2022">Active since FY2022</option><option value="2020">Active since FY2020</option></select></div></div>
<button onclick="run()">Search</button><button class="alt" onclick="csv()">Download CSV</button><div id="out"></div>'''
          + scale_box(A, 'federal-grants-contracts', 'To pull open grant opportunities and award records across agencies on a schedule, '),
    js='''var rows=[];
function money(n){return n==null?"":"$"+Number(n).toLocaleString("en-US",{maximumFractionDigits:0})}
function run(){var n=$("n").value.trim(),o=$("out");if(n.length<3){o.innerHTML='<p class="bad">Enter at least 3 characters.</p>';return}o.innerHTML="<p>Searching USAspending...</p>";rows=[];
var y=+$("y").value,codes=$("k").value==="c"?["A","B","C","D"]:["02","03","04","05"];
var body={filters:{recipient_search_text:[n],award_type_codes:codes,time_period:[{start_date:(y-1)+"-10-01",end_date:new Date().toISOString().slice(0,10)}]},fields:["Award ID","Recipient Name","Award Amount","Awarding Agency","Start Date","End Date","Description"],sort:"Award Amount",order:"desc",limit:25,page:1};
getJson("https://api.usaspending.gov/api/v2/search/spending_by_award/",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body)}).then(function(j){var r=j.results||[];
if(!r.length){o.innerHTML="<p>No awards found for that name and period. Try a shorter name.</p>";return}
rows=r.map(function(x){return[x["Award ID"],x["Recipient Name"],x["Award Amount"],x["Awarding Agency"],x["Start Date"],x["End Date"],x["Description"]]});
o.innerHTML="<table><tr><th>Recipient</th><th>Amount</th><th>Agency</th><th>Start</th><th>Description</th></tr>"+rows.map(function(x){return"<tr><td>"+esc(x[1])+"<br><span class='muted'>"+esc(x[0])+"</span></td><td>"+money(x[2])+"</td><td>"+esc(x[3])+"</td><td>"+esc(x[4])+"</td><td>"+esc((x[6]||"").slice(0,140))+"</td></tr>"}).join("")+"</table><p class='muted'>Source: USAspending.gov, "+new Date().toISOString().slice(0,10)+".</p>"}).catch(function(e){o.innerHTML='<p class="bad">USAspending request failed ('+esc(e.message)+'). Try again.</p>'})}
function csv(){if(rows.length)dl("federal-awards.csv",toCsv([["award_id","recipient","amount","agency","start","end","description"]].concat(rows)))}
$("n").addEventListener("keydown",function(e){if(e.key==="Enter")run()})'''
)

# 7 ---------------------------------------------------------------- app store reviews
T['app-store-review-summary'] = dict(
    title='App Store Review Summary',
    desc="Enter an iPhone app ID and get its rating, the latest reviews, the rating split and the most common complaint words from Apple's public feed.",
    body='''<p class="note">Uses Apple's public iTunes lookup and customer-review RSS feeds, called from your browser (no key). The review feed returns only the most recent reviews per country (this page reads up to 250), not the full history, and Apple can change or remove the feed. App ID is the number in the App Store URL after "id", e.g. apps.apple.com/us/app/spotify/id<b>324684580</b>.</p>
<div class="row"><div><label for="a">App ID or App Store URL</label><input id="a" placeholder="324684580"></div><div><label for="c">Country</label><select id="c"><option>us</option><option>gb</option><option>ca</option><option>au</option><option>de</option><option>fr</option><option>in</option></select></div></div>
<button onclick="run()">Summarize</button><button class="alt" onclick="csv()">Download reviews CSV</button><div id="out"></div>'''
          + scale_box(A, 'app-store-reviews', 'To collect reviews and app details across many apps and countries on a schedule, '),
    js='''var rv=[];var STOP="the and for that this with have you was but not are they their all can its just app get has had from when out one been very would what will more about there which them than into also your like even only some how too any really use using still time".split(" ");
function run(){var s=$("a").value,m=s.match(/id(\\d{5,})/)||s.match(/^\\s*(\\d{5,})\\s*$/),o=$("out");if(!m){o.innerHTML='<p class="bad">Enter a numeric app ID or an App Store URL containing id123456.</p>';return}var id=m[1],c=$("c").value;o.innerHTML="<p>Loading...</p>";rv=[];
var pages=[];var chain=Promise.resolve();[1,2,3,4,5].forEach(function(p){chain=chain.then(function(){return getJson("https://itunes.apple.com/"+c+"/rss/customerreviews/page="+p+"/id="+id+"/sortby=mostrecent/json").catch(function(){return null}).then(function(j){pages.push(j)})})});
Promise.all([getJson("https://itunes.apple.com/lookup?id="+id+"&country="+c).catch(function(){return null}),chain.then(function(){return pages})]).then(function(r){var L=r[0]&&r[0].results&&r[0].results[0],h="";
if(L)h+="<div class='card'><b>"+esc(L.trackName)+"</b> by "+esc(L.sellerName)+"<br>Store rating "+(L.averageUserRating?L.averageUserRating.toFixed(2):"n/a")+" from "+(L.userRatingCount||0).toLocaleString()+" ratings (current version: "+(L.averageUserRatingForCurrentVersion?L.averageUserRatingForCurrentVersion.toFixed(2):"n/a")+"). Version "+esc(L.version)+".</div>";
r[1].forEach(function(j){if(!j||!j.feed||!j.feed.entry)return;var e=j.feed.entry;(Array.isArray(e)?e:[e]).forEach(function(x){if(!x["im:rating"])return;rv.push([x["im:rating"].label,(x.updated||{}).label?x.updated.label.slice(0,10):"",x.title.label,x.content.label,x.author?x.author.name.label:"",x["im:version"]?x["im:version"].label:""])})});
if(!rv.length){o.innerHTML=h+"<p>No reviews returned by the feed for this app and country.</p>";return}
var dist=[0,0,0,0,0,0],sum=0;rv.forEach(function(x){dist[+x[0]]++;sum+=+x[0]});var neg=rv.filter(function(x){return+x[0]<=2}),wc={};neg.forEach(function(x){(x[2]+" "+x[3]).toLowerCase().replace(/[^a-z\\s']/g," ").split(/\\s+/).forEach(function(w){if(w.length>3&&STOP.indexOf(w)<0)wc[w]=(wc[w]||0)+1})});var top=Object.keys(wc).sort(function(a,b){return wc[b]-wc[a]}).slice(0,12);
h+="<p>"+rv.length+" recent reviews fetched. Average of these: <b>"+(sum/rv.length).toFixed(2)+"</b></p><table><tr><th>Stars</th><th>Count</th><th>Share</th></tr>"+[5,4,3,2,1].map(function(s){return"<tr><td>"+s+"</td><td>"+dist[s]+"</td><td>"+Math.round(100*dist[s]/rv.length)+"%</td></tr>"}).join("")+"</table>";
if(top.length)h+="<p><b>Most common words in 1-2 star reviews ("+neg.length+" reviews):</b> "+top.map(function(w){return esc(w)+" ("+wc[w]+")"}).join(", ")+"</p><p class='muted'>Word counts are a crude pointer, read the reviews below for meaning.</p>";
h+="<h2>Latest reviews</h2><table><tr><th>Stars</th><th>Date</th><th>Review</th></tr>"+rv.slice(0,25).map(function(x){return"<tr><td>"+x[0]+"</td><td>"+esc(x[1])+"</td><td><b>"+esc(x[2])+"</b><br>"+esc(x[3].slice(0,300))+"</td></tr>"}).join("")+"</table>";o.innerHTML=h}).catch(function(e){o.innerHTML='<p class="bad">Failed: '+esc(e.message)+'</p>'})}
function csv(){if(rv.length)dl("app-reviews.csv",toCsv([["rating","date","title","review","author","version"]].concat(rv)))}
$("a").addEventListener("keydown",function(e){if(e.key==="Enter")run()})'''
)

if __name__ == '__main__':
    for slug, t in T.items():
        write(f'tools/{slug}.html', page(slug, t['title'], t['desc'], t['body'], 'tools', COMMON + t['js']))
    json_list = [{'slug': s, 'title': t['title'], 'desc': t['desc']} for s, t in T.items()]
    json.dump(json_list, open(os.path.join(ROOT, 'data', 'tools_new.json'), 'w'), indent=1)
