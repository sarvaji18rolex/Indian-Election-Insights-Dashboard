function updateClock() {
  const el = document.getElementById('live-clock');
  if (el) el.textContent = new Date().toLocaleString('en-IN',{dateStyle:'medium',timeStyle:'medium',hour12:true});
}
setInterval(updateClock,1000); updateClock();

function logoEl(logo, sym, color, cls='') {
  if (logo) return `<img src="${logo}" class="${cls||'sc-logo'}" alt="" onerror="this.outerHTML='<div style=\\'background:${color}20;width:50px;height:50px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:24px\\'>${sym}</div>'">`;
  return `<div style="background:${color}20;width:50px;height:50px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:24px">${sym}</div>`;
}

async function loadState() {
  const res = await fetch(`/api/state/${STATE_CODE}`);
  if (!res.ok) { document.getElementById('state-content').innerHTML='<div class="loading-spinner">State not found.</div>'; return; }
  const d = await res.json();
  const s = d.state;

  document.title = `${s.name} | India Election Dashboard`;

  document.getElementById('state-content').innerHTML = `
    <div style="text-align:center;padding:60px 0 40px">
      <div style="font-size:48px;margin-bottom:8px">${s.symbol||'🏛️'}</div>
      <h1 style="font-family:'Cinzel',serif;font-size:48px;color:#fff">${s.name}</h1>
      <div style="color:${s.color};font-size:16px;font-weight:600;margin:8px 0">${s.party_name} · ${s.alliance||'—'}</div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:40px">
      ${[
        ['CM', s.cm], ['Ruling Since', s.ruling_since], ['Seats', s.seats],
        ['Years Ruling', s.years_ruling+'y'], ['Days Ruling', s.days_ruling.toLocaleString('en-IN')],
        ['Next Election', s.next_election.slice(0,7)], ['Days Left', s.days_to_election.toLocaleString('en-IN')],
        ['Population', (s.population/1e7).toFixed(1)+' Cr'], ['Literacy', s.literacy+'%'], ['Region', s.region]
      ].map(([l,v]) => `<div class="sc-stat"><div class="sc-stat-val" style="font-size:20px;color:${s.color}">${v}</div><div class="sc-stat-lbl">${l}</div></div>`).join('')}
    </div>

    ${d.candidates.length ? `
    <h2 style="font-family:'Cinzel',serif;color:var(--gold);margin-bottom:20px">Key Leaders</h2>
    <div class="candidates-grid" style="margin-bottom:40px">
      ${d.candidates.map(c => `
        <div class="cand-card" style="border-color:${c.color}40">
          <img src="${c.image}" class="cand-img" style="border-color:${c.color}"
            alt="${c.name}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(c.name)}&size=90&background=${c.color.slice(1)}&color=fff'">
          <div class="cand-name">${c.name}</div>
          <div class="cand-pos">${c.position}</div>
          <span class="cand-party-chip" style="background:${c.color}">${c.party_name}</span>
        </div>`).join('')}
    </div>` : ''}

    ${d.results.length ? `
    <h2 style="font-family:'Cinzel',serif;color:var(--gold);margin-bottom:20px">Election Results</h2>
    <div class="result-table" style="margin-bottom:40px">
      <table class="rt"><thead><tr><th>Party</th><th>Year</th><th>Seats</th><th>Vote %</th></tr></thead>
      <tbody>${d.results.map(r=>`<tr>
        <td><span class="party-dot" style="background:${r.color}"></span>${r.party_name}</td>
        <td>${r.year}</td>
        <td><strong style="color:${r.color}">${r.seats_won}</strong></td>
        <td>${r.vote_share}%</td>
      </tr>`).join('')}</tbody></table>
    </div>` : ''}

    ${d.predictions.length ? `
    <h2 style="font-family:'Cinzel',serif;color:var(--gold);margin-bottom:20px">🔮 Election Predictions</h2>
    <div class="pred-grid">
      ${d.predictions.map(p=>`
        <div class="pred-card" style="border-left-color:${p.color}">
          <div class="pred-head">
            <div class="pred-party" style="color:${p.color}">${p.party_name}</div>
            <div class="pred-year">${p.election_year}</div>
          </div>
          <div class="pred-seats" style="color:${p.color}">${p.predicted_seats} <span style="font-size:16px;color:var(--muted)">seats</span></div>
          <div class="pred-conf-bar"><div class="pred-conf-fill" style="width:${p.confidence}%;background:${p.color}"></div></div>
          <div class="pred-conf-lbl">Confidence: ${p.confidence}%</div>
          <div class="pred-factors">${p.factors}</div>
        </div>`).join('')}
    </div>` : ''}

    <div style="margin-top:40px;text-align:center">
      <a href="/" style="color:var(--gold);font-size:15px;font-weight:600;text-decoration:none">← Back to Dashboard</a>
    </div>`;
}

loadState();
