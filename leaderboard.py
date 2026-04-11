"""TriageFlow Benchmark Leaderboard — standalone page at GET /leaderboard."""

LEADERBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TriageFlow — Benchmark Leaderboard</title>
<meta name="description" content="Community benchmark results across all TriageFlow tasks">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#06080f;--bg-subtle:#0a0e1a;--surface:#111827;--surface2:#1e2740;--surface3:#283352;
  --border:rgba(139,92,246,.12);--border-bright:rgba(139,92,246,.2);
  --accent:#a78bfa;--accent-glow:rgba(139,92,246,.2);--accent-dim:rgba(139,92,246,.08);
  --blue:#60a5fa;--violet:#a78bfa;--rose:#fb7185;--amber:#fbbf24;--cyan:#22d3ee;--gold:#fbbf24;--silver:#94a3b8;--bronze:#d97706;
  --text:#f1f5f9;--text2:#94a3b8;--text3:#475569;
  --radius:16px;--radius-sm:10px;--radius-xs:6px;
}
html{font-size:14px}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
::selection{background:rgba(167,139,250,.25);color:#fff}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:4px}

@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes glow-breathe{0%,100%{box-shadow:0 0 20px rgba(139,92,246,.08)}50%{box-shadow:0 0 40px rgba(139,92,246,.25),0 0 80px rgba(139,92,246,.08)}}

.header{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:56px;background:rgba(6,8,15,.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header-left{display:flex;align-items:center;gap:12px}
.logo{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:-.3px;text-decoration:none;color:var(--text)}
.logo-icon{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#c084fc);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(139,92,246,.3);animation:glow-breathe 4s ease-in-out infinite}
.logo-icon .material-symbols-outlined{font-size:18px;color:var(--bg);font-variation-settings:'FILL' 1}
.nav-links{display:flex;gap:6px}
.nav-link{padding:6px 14px;border-radius:100px;font-size:12px;font-weight:600;color:var(--text2);text-decoration:none;border:1px solid transparent;transition:all .2s}
.nav-link:hover{color:var(--accent);border-color:var(--border)}
.nav-link.active{color:var(--accent);background:var(--accent-dim);border-color:rgba(139,92,246,.2)}
.badge-version{display:inline-flex;padding:3px 10px;border-radius:100px;font-size:10px;font-weight:700;background:rgba(148,163,184,.08);color:var(--text2);border:1px solid var(--border)}

.container{max-width:960px;margin:0 auto;padding:32px 24px}
.page-title{font-size:28px;font-weight:900;margin-bottom:6px;letter-spacing:-.5px}
.page-subtitle{color:var(--text3);font-size:14px;margin-bottom:28px}

/* TABS */
.tabs{display:flex;gap:6px;margin-bottom:20px}
.tab{padding:8px 20px;border-radius:100px;font-size:13px;font-weight:700;cursor:pointer;border:1px solid var(--border);background:var(--surface);color:var(--text2);transition:all .2s}
.tab:hover{border-color:var(--border-bright);color:var(--text)}
.tab.active{background:linear-gradient(135deg,#8b5cf6,#a78bfa);color:#fff;border-color:transparent;box-shadow:0 0 15px var(--accent-glow)}

/* TABLE */
.lb-table{width:100%;border-collapse:collapse;margin-bottom:32px}
.lb-table th{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;padding:10px 14px;border-bottom:1px solid var(--border);text-align:left}
.lb-table td{padding:12px 14px;border-bottom:1px solid rgba(139,92,246,.06);font-size:13px;transition:background .15s}
.lb-table tr:hover td{background:rgba(139,92,246,.03)}
.lb-table .rank{font-weight:800;font-family:'JetBrains Mono',monospace;width:50px;text-align:center}
.lb-table .model-name{font-weight:700}
.lb-table .score-cell{font-family:'JetBrains Mono',monospace;font-weight:700}
.lb-table tr.gold{border-left:3px solid var(--gold)}
.lb-table tr.silver{border-left:3px solid var(--silver)}
.lb-table tr.bronze{border-left:3px solid var(--bronze)}

/* Score bar inline */
.score-bar-wrap{display:flex;align-items:center;gap:8px}
.score-bar-track{width:100px;height:6px;background:var(--surface2);border-radius:3px;overflow:hidden}
.score-bar-fill{height:100%;border-radius:3px;transition:width .4s}

/* SUBMIT FORM */
.submit-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-top:8px}
.submit-card h3{font-size:16px;font-weight:800;margin-bottom:16px}
.form-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:12px}
.form-group{display:flex;flex-direction:column;gap:4px}
.form-label{font-size:9px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1px}
.form-input,.form-select{padding:10px 14px;background:rgba(6,8,15,.8);border:1px solid rgba(139,92,246,.12);border-radius:var(--radius-sm);color:var(--text);font-family:'Inter',sans-serif;font-size:13px;font-weight:500;outline:none;transition:all .25s;-webkit-appearance:none;appearance:none}
.form-input:focus,.form-select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(139,92,246,.12)}
.form-select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23a78bfa' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:32px;cursor:pointer}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 20px;border:none;border-radius:var(--radius-sm);font-family:'Inter',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:all .2s;letter-spacing:.3px}
.btn-accent{background:linear-gradient(135deg,#8b5cf6,#a78bfa);color:#fff;box-shadow:0 0 15px var(--accent-glow)}
.btn-accent:hover{filter:brightness(1.15);transform:translateY(-1px)}

.snackbar{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--surface2);color:#fff;padding:12px 28px;border-radius:var(--radius);font-size:13px;font-weight:600;z-index:200;transition:transform .3s;border:1px solid rgba(139,92,246,.3);box-shadow:0 12px 40px rgba(0,0,0,.5)}
.snackbar.show{transform:translateX(-50%) translateY(0)}
</style>
</head>
<body>

<header class="header">
  <div class="header-left">
    <a href="/" class="logo">
      <div class="logo-icon"><span class="material-symbols-outlined">bolt</span></div>
      TriageFlow
    </a>
    <span class="badge-version">v1.0.0</span>
  </div>
  <nav class="nav-links">
    <a href="/dashboard" class="nav-link">Dashboard</a>
    <a href="/replay" class="nav-link">Replay</a>
    <a href="/leaderboard" class="nav-link active">Leaderboard</a>
  </nav>
</header>

<div class="container">
  <h1 class="page-title">🏆 Benchmark Leaderboard</h1>
  <p class="page-subtitle">Community results across all TriageFlow tasks</p>

  <div class="tabs" id="tabs">
    <div class="tab active" data-task="ticket_classification" onclick="switchTab(this)">Easy</div>
    <div class="tab" data-task="ticket_routing" onclick="switchTab(this)">Medium</div>
    <div class="tab" data-task="policy_triage" onclick="switchTab(this)">Hard</div>
  </div>

  <table class="lb-table">
    <thead><tr>
      <th>Rank</th><th>Model</th><th>Score</th><th>Steps</th><th>Seed</th><th>Submitted</th>
    </tr></thead>
    <tbody id="lbBody"></tbody>
  </table>

  <div class="submit-card">
    <h3>📤 Submit Your Score</h3>
    <div class="form-row">
      <div class="form-group"><label class="form-label">Model Name</label><input class="form-input" id="fModel" placeholder="gpt-4o-mini"></div>
      <div class="form-group"><label class="form-label">Task</label>
        <select class="form-select" id="fTask">
          <option value="ticket_classification">Easy — Classification</option>
          <option value="ticket_routing">Medium — Routing</option>
          <option value="policy_triage">Hard — Policy Triage</option>
        </select></div>
      <div class="form-group"><label class="form-label">Score</label><input class="form-input" id="fScore" type="number" step="0.01" min="0" max="1" placeholder="0.85"></div>
      <div class="form-group"><label class="form-label">Steps</label><input class="form-input" id="fSteps" type="number" placeholder="10"></div>
      <div class="form-group"><label class="form-label">Seed</label><input class="form-input" id="fSeed" type="number" value="42"></div>
    </div>
    <button class="btn btn-accent" onclick="submitScore()">
      <span class="material-symbols-outlined" style="font-size:16px">upload</span> Submit Score
    </button>
  </div>
</div>

<div class="snackbar" id="snackbar"></div>

<script>
let lbData = [];
let activeTask = 'ticket_classification';

async function fetchLeaderboard() {
  try {
    const r = await fetch('/leaderboard_data');
    if (r.ok) lbData = await r.json();
  } catch {}
  renderTable();
}

function switchTab(el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  activeTask = el.dataset.task;
  renderTable();
}

function renderTable() {
  const filtered = lbData.filter(e => e.task_name === activeTask).sort((a,b) => b.score - a.score);
  const tbody = document.getElementById('lbBody');
  const MEDAL = ['gold','silver','bronze'];
  tbody.innerHTML = filtered.map((e, i) => {
    const cls = i < 3 ? MEDAL[i] : '';
    const pct = Math.min(100, e.score * 100);
    const col = e.score >= 0.7 ? '#a78bfa' : e.score >= 0.4 ? '#fbbf24' : '#fb7185';
    const ts = e.timestamp ? new Date(e.timestamp).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}) : '—';
    const rankIcon = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i+1);
    return `<tr class="${cls}"><td class="rank">${rankIcon}</td><td class="model-name">${e.model_name}</td><td class="score-cell"><div class="score-bar-wrap"><div class="score-bar-track"><div class="score-bar-fill" style="width:${pct}%;background:${col}"></div></div>${e.score.toFixed(2)}</div></td><td>${e.steps||'—'}</td><td style="font-family:'JetBrains Mono',monospace;color:var(--text3)">${e.seed||42}</td><td style="color:var(--text3);font-size:12px">${ts}</td></tr>`;
  }).join('');
}

async function submitScore() {
  const model = document.getElementById('fModel').value.trim();
  const score = parseFloat(document.getElementById('fScore').value);
  const steps = parseInt(document.getElementById('fSteps').value) || 0;
  const seed = parseInt(document.getElementById('fSeed').value) || 42;
  const task = document.getElementById('fTask').value;
  if (!model || isNaN(score)) { showSnack('Please fill in model name and score'); return; }
  try {
    const r = await fetch('/submit_score', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model_name:model,task_name:task,score,steps,seed,timestamp:new Date().toISOString()})});
    if (!r.ok) throw new Error('Submit failed');
    showSnack('Score submitted!');
    await fetchLeaderboard();
    activeTask = task;
    document.querySelectorAll('.tab').forEach(t => { t.classList.toggle('active', t.dataset.task === task); });
    renderTable();
  } catch(e) { showSnack('Error: '+e.message); }
}

let snackTimer;
function showSnack(msg) {
  const el = document.getElementById('snackbar');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(snackTimer);
  snackTimer = setTimeout(() => el.classList.remove('show'), 3000);
}

fetchLeaderboard();
</script>
</body>
</html>"""
