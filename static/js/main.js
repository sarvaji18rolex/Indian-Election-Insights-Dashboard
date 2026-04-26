/* ============================================================
   INDIA ELECTION DASHBOARD — main.js
   ============================================================ */

// ── Clock ─────────────────────────────────────────────────────
function updateClock() {
  const el = document.getElementById('live-clock');
  if (el) el.textContent = new Date().toLocaleString('en-IN', {
    dateStyle: 'medium', timeStyle: 'medium', hour12: true
  });
}
setInterval(updateClock, 1000);
updateClock();

// ── Helpers ───────────────────────────────────────────────────
function logoEl(logo, symbol, color, cls = '') {
  if (logo) {
    return `<img src="${logo}" class="${cls || 'ls-logo'}" alt="logo"
              onerror="this.outerHTML='<div class=\\'${cls || 'ls-logo-fb'}\\' style=\\'background:${color}20\\'>${symbol}</div>'">`;
  }
  return `<div class="${cls || 'ls-logo-fb'}" style="background:${color}20">${symbol}</div>`;
}

function allianceBadge(alliance, party) {
  if (!alliance || alliance === 'None') return '';
  const colors = { NDA: '#FF6B00', INDIA: '#19A84B', Independent: '#888' };
  return `<span class="sc-badge" style="background:${colors[alliance]||'#555'}">${alliance}</span>`;
}

// ── State filter state ────────────────────────────────────────
let allStates = [];
let currentRegion = 'All';

function filterRegion(region, btn) {
  currentRegion = region;
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderStates(allStates);
}

// ── Main data load ────────────────────────────────────────────
async function loadDashboard() {
  const res = await fetch('/api/dashboard');
  const data = await res.json();
  allStates = data.states;

  // Hero stats
  document.getElementById('hs-nda').textContent = data.nda_states;
  document.getElementById('hs-india').textContent = data.india_states;
  const minDays = Math.min(...data.upcoming.map(u => u.days));
  document.getElementById('hs-next').textContent = minDays;

  // PM days
  const pmEl = document.getElementById('pm-days');
  if (pmEl) {
    const since = new Date('2014-05-26');
    const diff = Math.floor((Date.now() - since) / 86400000);
    pmEl.textContent = diff.toLocaleString('en-IN');
  }

  renderLokSabha(data.lok_sabha);
  renderAlliances(data.lok_sabha);
  renderStates(allStates);
  renderTimeline(data.upcoming);
  renderDominance(data.tally);
}

// ── Lok Sabha ─────────────────────────────────────────────────
function renderLokSabha(ls) {
  const bar = document.getElementById('seat-bar');
  const cards = document.getElementById('ls-cards');
  if (!bar || !cards) return;

  const total = ls.reduce((a, b) => a + b.seats_won, 0);
  bar.innerHTML = ls.map(p => `
    <div style="width:${(p.seats_won/543*100).toFixed(1)}%;background:${p.color};
      title="${p.abbr}: ${p.seats_won}" min-width:40px">
      ${p.seats_won >= 30 ? `${p.abbr} ${p.seats_won}` : p.seats_won >= 10 ? p.seats_won : ''}
    </div>`).join('');

  cards.innerHTML = ls.slice(0, 8).map(p => `
    <div class="ls-card" style="border-left:4px solid ${p.color}">
      ${logoEl(p.logo, p.symbol || '🏛️', p.color)}
      <div class="ls-info">
        <div class="ls-name">${p.name}</div>
        <div class="ls-abbr">${p.abbr} · ${p.alliance || ''}</div>
      </div>
      <div>
        <div class="ls-seats" style="color:${p.color}">${p.seats_won}</div>
        <div class="ls-vote">${p.vote_share}% votes</div>
      </div>
    </div>`).join('');
}

// ── Alliances ─────────────────────────────────────────────────
function renderAlliances(ls) {
  let nda = 0, india = 0;
  const ndaP = [], indiaP = [];
  ls.forEach(p => {
    if (p.alliance === 'NDA') { nda += p.seats_won; ndaP.push(p); }
    if (p.alliance === 'INDIA') { india += p.seats_won; indiaP.push(p); }
  });
  const ndaEl = document.getElementById('nda-seats');
  const indiaEl = document.getElementById('india-seats');
  if (ndaEl) ndaEl.textContent = nda;
  if (indiaEl) indiaEl.textContent = india;

  const ndaPEl = document.getElementById('nda-parties');
  const indiaPEl = document.getElementById('india-parties');
  if (ndaPEl) ndaPEl.innerHTML = ndaP.map(p =>
    `<span class="ap-chip" style="background:${p.color}40;border-color:${p.color}60">${p.abbr} ${p.seats_won}</span>`
  ).join('');
  if (indiaPEl) indiaPEl.innerHTML = indiaP.map(p =>
    `<span class="ap-chip" style="background:${p.color}40;border-color:${p.color}60">${p.abbr} ${p.seats_won}</span>`
  ).join('');
}

// ── States Grid ───────────────────────────────────────────────
function renderStates(states) {
  const grid = document.getElementById('states-grid');
  if (!grid) return;
  const filtered = currentRegion === 'All' ? states : states.filter(s => s.region === currentRegion);
  grid.innerHTML = filtered.map(s => `
    <a class="state-card" href="/state/${s.code}" style="--c:${s.color}; border-color:${s.color}30">
      <div style="position:absolute;top:0;left:0;right:0;height:4px;background:${s.color}"></div>
      <div class="sc-top">
        ${logoEl(s.logo, s.symbol || '🏛️', s.color, 'sc-logo')}
        <div>
          <div class="sc-name">${s.name}</div>
          <div class="sc-code">${s.code} · ${s.region}</div>
        </div>
        ${allianceBadge(s.alliance, s.party_name)}
      </div>
      <div class="sc-cm">CM: <strong>${s.cm}</strong></div>
      <div class="sc-cm" style="color:${s.color};font-weight:600">${s.party_name}</div>
      <div class="sc-stats">
        <div class="sc-stat">
          <div class="sc-stat-val">${s.years_ruling}y</div>
          <div class="sc-stat-lbl">In Power</div>
        </div>
        <div class="sc-stat">
          <div class="sc-stat-val">${s.seats}</div>
          <div class="sc-stat-lbl">Assembly Seats</div>
        </div>
        <div class="sc-stat">
          <div class="sc-stat-val">${s.days_ruling.toLocaleString('en-IN')}</div>
          <div class="sc-stat-lbl">Days Ruling</div>
        </div>
        <div class="sc-stat">
          <div class="sc-stat-val">${s.days_to_election > 0 ? s.days_to_election.toLocaleString('en-IN') : '—'}</div>
          <div class="sc-stat-lbl">Days to Election</div>
        </div>
      </div>
      <div class="sc-footer">
        <span class="sc-region">Pop: ${(s.population/1e7).toFixed(1)} Cr</span>
        <span class="sc-elect" style="color:${s.color}">Next: ${s.next_election.slice(0,7)}</span>
      </div>
    </a>`).join('');
}

// ── Timeline ──────────────────────────────────────────────────
function renderTimeline(upcoming) {
  const el = document.getElementById('timeline');
  if (!el) return;
  const max = upcoming[upcoming.length - 1]?.days || 1;
  el.innerHTML = upcoming.map((u, i) => `
    <div class="tl-item">
      <div class="tl-rank">${i + 1}</div>
      <div>
        <div class="tl-state">${u.state}</div>
        <div class="tl-party" style="color:${u.color}">${u.ruling}</div>
      </div>
      <div class="tl-bar">
        <div class="tl-fill" style="width:${Math.min(100, (u.days/max*100)).toFixed(0)}%;background:${u.color}"></div>
      </div>
      <div class="tl-date">${u.date.slice(0,7)}</div>
      <div class="tl-days">${u.days.toLocaleString('en-IN')}<small>days left</small></div>
    </div>`).join('');
}

// ── Dominance ─────────────────────────────────────────────────
function renderDominance(tally) {
  const el = document.getElementById('dominance');
  if (!el) return;
  const max = tally[0]?.states_ruled || 1;
  el.innerHTML = tally.map(p => `
    <div class="dom-row">
      ${logoEl(p.logo, p.symbol || '🏛️', p.color, 'dom-logo')}
      <div class="dom-name">
        <strong>${p.name}</strong>
        <span>${p.abbr} · ${p.alliance || '—'}</span>
      </div>
      <div class="dom-bar">
        <div class="dom-fill" style="width:${(p.states_ruled/max*100).toFixed(0)}%;background:${p.color}"></div>
      </div>
      <div>
        <div class="dom-count" style="color:${p.color}">${p.states_ruled}</div>
        <div class="dom-lbl">states</div>
      </div>
    </div>`).join('');
}

// ── Boot ──────────────────────────────────────────────────────
loadDashboard();
