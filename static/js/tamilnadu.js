/* Tamil Nadu detail page */
function updateClock() {
  const el = document.getElementById('live-clock');
  if (el) el.textContent = new Date().toLocaleString('en-IN', { dateStyle:'medium',timeStyle:'medium',hour12:true });
}
setInterval(updateClock, 1000); updateClock();

function logoEl(logo, sym, color, cls='') {
  if (logo) return `<img src="${logo}" class="${cls||'sc-logo'}" alt="" onerror="this.outerHTML='<div class=\\'${cls||'sc-logo-fb'}\\' style=\\'background:${color}20\\'>${sym}</div>'">`;
  return `<div class="${cls||'sc-logo-fb'}" style="background:${color}20">${sym}</div>`;
}

async function loadTN() {
  const res = await fetch('/api/tamilnadu');
  const d = await res.json();
  const s = d.state;

  // Quick stats
  document.getElementById('tn-quick').innerHTML = `
    <div class="tn-qs"><div class="tn-qs-val">${s.seats}</div><div class="tn-qs-lbl">Assembly Seats</div></div>
    <div class="tn-qs"><div class="tn-qs-val">${s.years_ruling}y</div><div class="tn-qs-lbl">DMK in Power</div></div>
    <div class="tn-qs"><div class="tn-qs-val">${s.days_ruling.toLocaleString('en-IN')}</div><div class="tn-qs-lbl">Days Ruling</div></div>
    <div class="tn-qs"><div class="tn-qs-val">${s.days_to_election.toLocaleString('en-IN')}</div><div class="tn-qs-lbl">Days to 2026 Election</div></div>
    <div class="tn-qs"><div class="tn-qs-val">${(s.population/1e7).toFixed(1)} Cr</div><div class="tn-qs-lbl">Population</div></div>
    <div class="tn-qs"><div class="tn-qs-val">${s.literacy}%</div><div class="tn-qs-lbl">Literacy Rate</div></div>`;

  // Govt card
  const cm = d.candidates.find(c => c.is_cm);
  document.getElementById('tn-govt').innerHTML = `
    <img src="${cm ? cm.image : ''}" style="width:100px;height:120px;object-fit:cover;border-radius:10px;border:3px solid #E60026"
      alt="${cm?.name}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(cm?.name||'CM')}&size=100&background=E60026&color=fff'">
    <div>
      <div style="color:#E60026;font-weight:700;font-size:12px;letter-spacing:2px;text-transform:uppercase">Chief Minister</div>
      <div style="font-family:'Cinzel',serif;font-size:28px;margin:4px 0">${cm?.name || s.cm}</div>
      <div style="color:var(--muted);font-size:14px;margin-bottom:12px">${cm?.position || ''} · ${cm?.constituency || ''}</div>
      <div style="display:flex;gap:24px;flex-wrap:wrap">
        <div><div style="font-size:22px;font-weight:700;color:#FFD700">${s.ruling_since}</div><div style="font-size:12px;color:var(--muted)">In Office Since</div></div>
        <div><div style="font-size:22px;font-weight:700;color:#FFD700">${s.next_election.slice(0,7)}</div><div style="font-size:12px;color:var(--muted)">Next Election</div></div>
        <div><div style="font-size:22px;font-weight:700;color:#FFD700">${s.days_ruling.toLocaleString('en-IN')}</div><div style="font-size:12px;color:var(--muted)">Days in Power</div></div>
      </div>
    </div>`;

  // Result bar 2021
  const r2021 = d.results.filter(r => r.year === 2021).sort((a,b) => b.seats_won - a.seats_won);
  const totalSeats = r2021.reduce((a,b) => a+b.seats_won, 0) || 234;
  document.getElementById('tn-result-bar').innerHTML = r2021.map(r =>
    `<div class="rb-seg" style="width:${(r.seats_won/234*100).toFixed(1)}%;background:${r.color};flex-shrink:0" title="${r.party_name}: ${r.seats_won}">
      ${r.seats_won >= 25 ? `${r.abbr} ${r.seats_won}` : r.seats_won >= 10 ? r.seats_won : ''}
    </div>`).join('');

  document.getElementById('tn-result-table').innerHTML = `
    <table class="rt"><thead><tr>
      <th>Party</th><th>Seats Won</th><th>Vote %</th><th>Alliance</th>
    </tr></thead><tbody>
    ${r2021.map(r => `<tr>
      <td><span class="party-dot" style="background:${r.color}"></span>${r.party_name}</td>
      <td><strong style="color:${r.color}">${r.seats_won}</strong></td>
      <td>${r.vote_share}%</td>
      <td>${r.abbr === 'DMK' ? 'INDIA' : r.abbr === 'AIADMK' ? 'NDA' : '—'}</td>
    </tr>`).join('')}
    </tbody></table>`;

  // History Chart
  const years = ['1989','1991','1996','2001','2006','2011','2016','2021'];
  new Chart(document.getElementById('tn-history-chart'), {
    type: 'line',
    data: {
      labels: years,
      datasets: d.history.map(h => ({
        label: h.party,
        data: years.map(y => h['y'+y]),
        borderColor: h.color,
        backgroundColor: h.color+'30',
        borderWidth: 3,
        pointRadius: 6,
        pointHoverRadius: 9,
        tension: 0.3,
        fill: false,
      }))
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#8892B0', font: { family: 'Rajdhani', size: 13 } } }
      },
      scales: {
        x: { ticks: { color: '#8892B0' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#8892B0' }, grid: { color: 'rgba(255,255,255,0.05)' },
          title: { display: true, text: 'Seats Won', color: '#8892B0' } }
      }
    }
  });

  // Candidates
  document.getElementById('tn-candidates').innerHTML = d.candidates.map(c => `
    <div class="cand-card" style="border-color:${c.color}40">
      <img src="${c.image}" class="cand-img" style="border-color:${c.color}"
        alt="${c.name}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(c.name)}&size=90&background=${c.color.slice(1)}&color=fff'">
      <div class="cand-name">${c.name}</div>
      <div class="cand-pos">${c.position}</div>
      <div class="cand-pos" style="color:var(--muted)">${c.constituency}</div>
      <span class="cand-party-chip" style="background:${c.color}">${c.party_name}</span>
    </div>`).join('');

  // Constituencies
  document.getElementById('tn-const').innerHTML = d.constituencies.map(c => `
    <div class="const-card" style="border-color:${c.color}30">
      <div>
        <div class="const-name">${c.name}</div>
        <div class="const-inc" style="color:${c.color}">${c.incumbent}</div>
      </div>
      <div style="text-align:right">
        <div class="const-status" style="background:${c.color}">${c.status}</div>
        <div class="const-margin" style="margin-top:4px">+${c.margin.toLocaleString('en-IN')}</div>
      </div>
    </div>`).join('');

  // Welfare
  document.getElementById('tn-welfare').innerHTML = d.welfare.map(w => `
    <div class="wf-card">
      <div class="wf-name">${w.name}</div>
      <div class="wf-stats">
        <span class="wf-ben">👥 ${w.beneficiaries}</span>
        <span class="wf-amt">${w.amount}</span>
      </div>
      <div class="wf-year">Launched: ${w.year}</div>
    </div>`).join('');

  // Predictions
  document.getElementById('tn-preds').innerHTML = d.predictions.map(p => `
    <div class="pred-tn" style="border-left-color:${p.color}">
      <div class="pred-tn-head">
        <div>
          <div class="pred-tn-party" style="color:${p.color}">${p.party_name}</div>
          <div style="font-size:13px;color:var(--muted)">Election Year: ${p.election_year}</div>
        </div>
        <div style="text-align:right">
          <div class="pred-tn-seats" style="color:${p.color}">${p.predicted_seats}</div>
          <div style="font-size:12px;color:var(--muted)">Predicted Seats</div>
        </div>
      </div>
      <div class="pred-conf-bar"><div class="pred-conf-fill" style="width:${p.confidence}%;background:${p.color}"></div></div>
      <div class="pred-conf-lbl">Confidence: ${p.confidence}%</div>
      <div class="pred-factors">${p.factors}</div>
    </div>`).join('');
}

loadTN();
