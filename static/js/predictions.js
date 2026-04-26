function updateClock() {
  const el = document.getElementById('live-clock');
  if (el) el.textContent = new Date().toLocaleString('en-IN',{dateStyle:'medium',timeStyle:'medium',hour12:true});
}
setInterval(updateClock,1000); updateClock();

async function loadPredictions() {
  const res = await fetch('/api/predictions');
  const d = await res.json();

  const statePreds = d.predictions.filter(p => p.state_id);
  const ls29 = d.predictions.filter(p => !p.state_id);

  document.getElementById('pred-grid').innerHTML = statePreds.map(p => `
    <div class="pred-card" style="border-left-color:${p.color}">
      <div class="pred-head">
        <div>
          <div class="pred-party" style="color:${p.color}">${p.party_name}</div>
          <div class="pred-state">${p.state_name || 'National'} (${p.state_code || 'IND'})</div>
        </div>
        <div class="pred-year">${p.election_year}</div>
      </div>
      <div class="pred-seats" style="color:${p.color}">${p.predicted_seats}
        <span style="font-size:16px;color:var(--muted)"> seats</span>
      </div>
      <div class="pred-conf-bar"><div class="pred-conf-fill" style="width:${p.confidence}%;background:${p.color}"></div></div>
      <div class="pred-conf-lbl">Confidence Score: <strong>${p.confidence}%</strong></div>
      <div class="pred-factors">${p.factors}</div>
    </div>`).join('');

  document.getElementById('ls29-wrap').innerHTML = `
    <h3 style="font-family:'Cinzel',serif;color:var(--gold);margin-bottom:20px">Lok Sabha 2029 — Seat Projections</h3>
    <div style="display:flex;flex-direction:column;gap:14px">
    ${ls29.map(p => `
      <div style="display:flex;align-items:center;gap:16px;background:var(--glass);border:1px solid ${p.color}30;border-radius:12px;padding:16px 20px">
        <div style="min-width:160px">
          <div style="font-size:16px;font-weight:700;color:${p.color}">${p.party_name}</div>
          <div style="font-size:12px;color:var(--muted)">Confidence: ${p.confidence}%</div>
        </div>
        <div style="flex:1;height:10px;background:rgba(255,255,255,.08);border-radius:5px;overflow:hidden">
          <div style="width:${(p.predicted_seats/543*100).toFixed(0)}%;height:100%;background:${p.color};border-radius:5px"></div>
        </div>
        <div style="font-size:28px;font-weight:900;color:${p.color};min-width:60px;text-align:right">${p.predicted_seats}</div>
      </div>`).join('')}
    </div>
    <div style="margin-top:16px;padding:12px 16px;background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.2);border-radius:8px;font-size:13px;color:var(--muted)">
      ⚠️ Projections are AI-generated estimates based on historical trends, alliance dynamics, and governance data. Not official forecasts. Actual results may vary significantly.
    </div>`;
}

loadPredictions();
