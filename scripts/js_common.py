COMMON = r"""
var $=function(i){return document.getElementById(i)};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function csvCell(v){v=String(v==null?'':v);return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v}
function toCsv(rows){return rows.map(function(r){return r.map(csvCell).join(',')}).join('\r\n')}
function dl(name,text){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'text/csv'}));a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
function getJson(url,opts){return fetch(url,opts).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status+' from '+new URL(url).host);return r.json()})}
function doh(name,type){return getJson('https://cloudflare-dns.com/dns-query?name='+encodeURIComponent(name)+'&type='+type,{headers:{accept:'application/dns-json'}}).then(function(j){return j.Answer||[]})}
"""
