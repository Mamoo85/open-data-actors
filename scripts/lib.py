"""Shared helpers for the generated free tools / calculator / quiz pages."""
import json, os, re, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BASE = 'https://mamoo85.github.io/open-data-actors/'
USER = 'transparent_meteorite'

CSS = ('body{font:16px/1.55 system-ui,sans-serif;max-width:760px;margin:0 auto;padding:24px 16px;color:#1a1a1a;background:#fff}'
 'textarea,input,select{width:100%;box-sizing:border-box;font:inherit;padding:8px;border:1px solid #999;border-radius:6px}'
 'textarea{min-height:140px;font-family:ui-monospace,monospace;font-size:14px}'
 'button,.btn{font:inherit;padding:8px 16px;border:0;border-radius:6px;background:#1a56db;color:#fff;cursor:pointer;margin:8px 8px 8px 0;display:inline-block;text-decoration:none}'
 'button.alt{background:#555}'
 'table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}td,th{border:1px solid #ccc;padding:6px 8px;text-align:left;vertical-align:top}'
 '.ok{color:#116611}.bad{color:#a11}.warn{color:#8a5a00}.muted{color:#666;font-size:13px}'
 '.note{background:#f4f4f4;padding:12px;border-radius:6px;font-size:14px}'
 '.row{display:flex;gap:12px;flex-wrap:wrap}.row>*{flex:1 1 200px}'
 '.card{border:1px solid #ccc;border-radius:8px;padding:12px;margin:12px 0}'
 'label{display:block;font-size:14px;margin:8px 0 2px}'
 'a{color:#1a56db}pre{background:#f4f4f4;padding:10px;border-radius:6px;overflow-x:auto;font-size:13px}'
 '@media(prefers-color-scheme:dark){body{background:#111;color:#eee}.note,pre{background:#222}textarea,input,select{background:#1b1b1b;color:#eee;border-color:#555}'
 'td,th,.card{border-color:#444}a{color:#8ab4ff}.ok{color:#6c6}.bad{color:#f88}.warn{color:#eb6}.muted{color:#aaa}}')


def load_actors():
    p = json.load(open(os.path.join(ROOT, 'data', 'pricing.json'), encoding='utf-8'))
    out = {}
    for a in p['actors']:
        s = a['slug']
        d = ''
        f = os.path.join(ROOT, s + '.html')
        if os.path.exists(f):
            m = re.search(r'<meta name="description" content="([^"]*)"', open(f, encoding='utf-8').read())
            if m: d = html.unescape(m.group(1))
        a['desc'] = d
        a['page'] = BASE + s + '.html'
        out[s] = a
    return out, p['generated']


def esc(s):
    return html.escape(str(s), quote=True)


def page(slug, title, desc, body, folder='tools', script=''):
    canon = f'{BASE}{folder}/{slug}.html' if folder else f'{BASE}{slug}.html'
    up = '../' if folder else ''
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">'
            f'<style>{CSS}</style></head><body><p><a href="{BASE}">Open Data Actors</a> / '
            f'{"free tools" if folder == "tools" else "guides"}</p><h1>{esc(title)}</h1><p>{esc(desc)}</p>{body}'
            f'<p class="muted">Disclosure: we build and maintain the Apify actors linked here. This page is free, has no tracking or analytics, '
            f'and does not store anything; inputs stay in your browser except where the page says it calls a named public API.</p>'
            f'<script>{script}</script></body></html>')


def scale_box(actors, slug, text):
    a = actors[slug]
    return (f'<h2>Need this at scale?</h2><p>{text} <a href="{a["url"]}">{esc(slug)} on the Apify Store</a> '
            f'(<a href="{a["page"]}">details and free sample CSV</a>) does it in bulk and returns structured data. '
            f'Estimate the cost first with the <a href="{BASE}cost-calculator.html">pay-per-event cost calculator</a>.</p>')


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(content)
    print('wrote', path, len(content))
