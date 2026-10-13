/* oda-chart: free embeddable SVG bar chart for Open Data Actors datasets.
   Usage: <script src="https://mamoo85.github.io/open-data-actors/widgets/oda-chart.js" async></script>
          <oda-chart dataset="warn-layoff-alerts"></oda-chart>
   Static: no cookies, no analytics, no tracking. Only fetches /api/<dataset>.json from the same site. */
(function () {
  var BASE = 'https://mamoo85.github.io/open-data-actors/';
  var STORE = 'https://apify.com/transparent_meteorite/';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function agg(rows, group, metric) {
    var m = {}, col = metric.indexOf('sum:') === 0 ? metric.slice(4) : null;
    rows.forEach(function (r) {
      var g = r[group]; if (g === '' || g == null) return;
      var k = String(g);
      if (!col) m[k] = (m[k] || 0) + 1;
      else { var x = parseFloat(r[col]); if (!isNaN(x)) m[k] = (m[k] || 0) + x; }
    });
    return Object.keys(m).map(function (k) { return [k, m[k]]; }).sort(function (a, b) { return b[1] - a[1]; });
  }
  function fmt(v) { return v >= 1e9 ? (v / 1e9).toFixed(1) + 'B' : v >= 1e6 ? (v / 1e6).toFixed(1) + 'M' : v >= 1e4 ? (v / 1e3).toFixed(0) + 'k' : String(Math.round(v * 10) / 10); }
  class OdaChart extends HTMLElement {
    connectedCallback() {
      var self = this, ds = this.getAttribute('dataset');
      if (!ds) return;
      var root = this.attachShadow ? (this.shadowRoot || this.attachShadow({ mode: 'open' })) : this;
      root.innerHTML = '<p style="font:14px system-ui,sans-serif">Loading chart...</p>';
      fetch(BASE + 'api/' + encodeURIComponent(ds) + '.json').then(function (r) { return r.json(); }).then(function (d) {
        var group = self.getAttribute('group') || d.chart.group, metric = self.getAttribute('metric') || d.chart.metric;
        var top = parseInt(self.getAttribute('top') || '10', 10);
        var title = self.getAttribute('title') || d.chart.title;
        var data = agg(d.rows, group, metric).slice(0, top);
        if (!data.length) { root.innerHTML = '<p style="font:14px system-ui,sans-serif">No data for this field.</p>'; return; }
        var W = 640, rowH = 26, L = 190, R = 60, H = data.length * rowH + 20, max = data[0][1] || 1;
        var s = '<style>:host{display:block;max-width:680px;font:14px system-ui,sans-serif;color:#1a1a1a}svg{width:100%;height:auto}text{fill:currentColor}.t{font-weight:600;margin:6px 0}.f{font-size:12px;color:#666;margin:6px 0}a{color:#1a56db}@media(prefers-color-scheme:dark){:host{color:#eee}.f{color:#aaa}a{color:#8ab4ff}}</style>';
        s += '<div class="t">' + esc(title) + '</div><svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(title) + '">';
        data.forEach(function (p, i) {
          var y = 10 + i * rowH, w = Math.max(2, (W - L - R) * p[1] / max), lab = p[0].length > 26 ? p[0].slice(0, 25) + '…' : p[0];
          s += '<text x="' + (L - 8) + '" y="' + (y + 15) + '" text-anchor="end" font-size="12">' + esc(lab) + '</text>';
          s += '<rect x="' + L + '" y="' + y + '" width="' + w.toFixed(1) + '" height="18" rx="3" fill="#2563eb"><title>' + esc(p[0]) + ': ' + p[1] + '</title></rect>';
          s += '<text x="' + (L + w + 6).toFixed(1) + '" y="' + (y + 14) + '" font-size="12">' + fmt(p[1]) + '</text>';
        });
        s += '</svg><div class="f">' + d.rowCount + '-row sample, updated ' + esc(d.generatedAt.slice(0, 10)) + '. Data: <a href="' + BASE + 'datasets/' + esc(ds) + '.html">dataset</a> from the Apify actor <a href="' + STORE + esc(ds) + '">' + esc(ds) + '</a>.</div>';
        root.innerHTML = s;
      }).catch(function () { root.innerHTML = '<p style="font:14px system-ui,sans-serif">Chart unavailable.</p>'; });
    }
  }
  if (!customElements.get('oda-chart')) customElements.define('oda-chart', OdaChart);
})();
