"""TriageFlow Agent Replay Visualizer — standalone page at GET /replay."""

REPLAY_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TriageFlow — Agent Replay Visualizer</title>
<meta name="description" content="Step-by-step replay visualizer for TriageFlow agent inference logs">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#06080f;--bg-subtle:#0a0e1a;--surface:#111827;--surface2:#1e2740;--surface3:#283352;
  --border:rgba(139,92,246,.12);--border-bright:rgba(139,92,246,.2);
  --accent:#a78bfa;--accent-glow:rgba(139,92,246,.2);--accent-dim:rgba(139,92,246,.08);
  --blue:#60a5fa;--violet:#a78bfa;--rose:#fb7185;--amber:#fbbf24;--cyan:#22d3ee;
  --text:#f1f5f9;--text2:#94a3b8;--text3:#475569;
  --radius:16px;--radius-sm:10px;--radius-xs:6px;
}
html{font-size:14px}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
::selection{background:rgba(167,139,250,.25);color:#fff}
.mono{font-family:'JetBrains Mono',monospace}
::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:4px}

@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(139,92,246,.5)}100%{box-shadow:0 0 0 8px rgba(139,92,246,0)}}
@keyframes glow-breathe{0%,100%{box-shadow:0 0 20px rgba(139,92,246,.08)}50%{box-shadow:0 0 40px rgba(139,92,246,.25),0 0 80px rgba(139,92,246,.08)}}

/* ═══ HEADER ═══ */
.header{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:56px;background:rgba(6,8,15,.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header-left{display:flex;align-items:center;gap:12px}
.logo{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:-.3px;text-decoration:none;color:var(--text)}
.logo-icon{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#c084fc);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(139,92,246,.3);animation:glow-breathe 4s ease-in-out infinite}
.logo-icon .material-symbols-outlined{font-size:18px;color:var(--bg);font-variation-settings:'FILL' 1}
.nav-links{display:flex;gap:6px}
.nav-link{padding:6px 14px;border-radius:100px;font-size:12px;font-weight:600;color:var(--text2);text-decoration:none;border:1px solid transparent;transition:all .2s}
.nav-link:hover{color:var(--accent);border-color:var(--border)}
.nav-link.active{color:var(--accent);background:var(--accent-dim);border-color:rgba(139,92,246,.2)}
.badge{display:inline-flex;align-items:center;gap:3px;padding:3px 10px;border-radius:100px;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;white-space:nowrap}
.badge-version{background:rgba(148,163,184,.08);color:var(--text2);border:1px solid var(--border)}

/* ═══ CONTAINER ═══ */
.container{max-width:960px;margin:0 auto;padding:32px 24px}
.page-title{font-size:28px;font-weight:900;margin-bottom:6px;letter-spacing:-.5px}
.page-subtitle{color:var(--text3);font-size:14px;margin-bottom:28px}

/* ═══ INPUT AREA ═══ */
.input-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:24px}
.log-textarea{width:100%;height:200px;background:#030712;border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--accent);font-family:'JetBrains Mono',monospace;font-size:12px;padding:16px;resize:vertical;outline:none;line-height:1.6;transition:border-color .2s}
.log-textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(139,92,246,.1)}
.log-textarea::placeholder{color:var(--text3)}

.btn-row{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 20px;border:none;border-radius:var(--radius-sm);font-family:'Inter',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:all .2s;letter-spacing:.3px}
.btn-accent{background:linear-gradient(135deg,#8b5cf6,#a78bfa);color:#fff;box-shadow:0 0 15px var(--accent-glow)}
.btn-accent:hover{filter:brightness(1.15);transform:translateY(-1px);box-shadow:0 0 25px var(--accent-glow)}
.btn-ghost{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
.btn-rose{background:linear-gradient(135deg,#e11d48,#fb7185);color:#fff}
.btn-rose:hover{filter:brightness(1.1)}
.btn:disabled{opacity:.35;cursor:not-allowed;transform:none!important;filter:none!important}
.btn .material-symbols-outlined{font-size:16px}

/* ═══ STEP CARDS ═══ */
.step-timeline{display:flex;flex-direction:column;gap:10px;margin-top:24px}
.step-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px 20px;display:flex;align-items:center;gap:16px;animation:fadeUp .3s ease;transition:border-color .2s}
.step-card:hover{border-color:var(--border-bright)}
.step-card.hidden{display:none}
.step-num{width:36px;height:36px;border-radius:10px;background:var(--surface2);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:var(--text2);flex-shrink:0;font-family:'JetBrains Mono',monospace}
.step-icon{font-size:22px;color:var(--violet);flex-shrink:0}
.step-info{flex:1;min-width:0}
.step-action{font-size:14px;font-weight:700;margin-bottom:2px}
.step-meta{font-size:11px;color:var(--text3)}
.step-reward{font-size:16px;font-weight:800;font-family:'JetBrains Mono',monospace;flex-shrink:0}
.step-reward.pos{color:var(--accent)}.step-reward.neg{color:var(--rose)}
.step-error{font-size:11px;color:var(--rose);margin-top:4px}
.step-card.error-card{border-color:rgba(251,113,133,.3)}

/* ═══ CHART ═══ */
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-top:24px}
.chart-card .card-title{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.chart-card .card-title .material-symbols-outlined{font-size:14px;opacity:.5}

/* ═══ SUMMARY CARD ═══ */
.summary-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px;margin-top:24px;text-align:center}
.summary-card.success{border-color:rgba(139,92,246,.3);box-shadow:0 0 40px rgba(139,92,246,.06)}
.summary-card.fail{border-color:rgba(251,113,133,.2)}
.summary-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 18px;border-radius:100px;font-size:12px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;margin-bottom:12px}
.summary-badge.pass{background:rgba(139,92,246,.15);color:var(--accent);border:1px solid rgba(139,92,246,.3)}
.summary-badge.fail-badge{background:rgba(251,113,133,.12);color:var(--rose);border:1px solid rgba(251,113,133,.25)}
.final-score{font-size:64px;font-weight:900;letter-spacing:-3px;margin:8px 0}
.summary-stats{display:flex;justify-content:center;gap:32px;margin-top:12px;flex-wrap:wrap}
.stat-item{text-align:center}
.stat-value{font-size:20px;font-weight:800;font-family:'JetBrains Mono',monospace}
.stat-label{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.6px;margin-top:2px}
.sparkline-wrap{margin-top:16px}

/* ═══ EMPTY ═══ */
.empty-hint{text-align:center;color:var(--text3);padding:40px;font-size:13px}
.empty-hint .material-symbols-outlined{font-size:48px;display:block;margin-bottom:8px;opacity:.2}
</style>
</head>
<body>

<header class="header">
  <div class="header-left">
    <a href="/" class="logo">
      <div class="logo-icon"><span class="material-symbols-outlined">bolt</span></div>
      TriageFlow
    </a>
    <span class="badge badge-version">v1.0.0</span>
  </div>
  <nav class="nav-links">
    <a href="/dashboard" class="nav-link">Dashboard</a>
    <a href="/replay" class="nav-link active">Replay</a>
    <a href="/leaderboard" class="nav-link">Leaderboard</a>
  </nav>
</header>

<div class="container">
  <h1 class="page-title">🔁 Agent Replay Visualizer</h1>
  <p class="page-subtitle">Paste the raw stdout log from inference.py and watch the agent's episode play back step-by-step.</p>

  <div class="input-card">
    <textarea class="log-textarea" id="logInput" placeholder="Paste [START] [STEP] [END] log output here...

Example:
[START] task=ticket_classification env=triageflow model=gpt-4o
[STEP] step=1 action=classify reward=0.20 done=false error=null
[STEP] step=2 action=route reward=0.09 done=false error=null
[END] success=true steps=2 score=0.85 rewards=0.20,0.09"></textarea>
    <div class="btn-row">
      <button class="btn btn-accent" id="btnParse" onclick="parseAndRender()">
        <span class="material-symbols-outlined">play_arrow</span> Parse &amp; Replay
      </button>
      <button class="btn btn-ghost" id="btnStepThrough" onclick="enterStepMode()" disabled>
        <span class="material-symbols-outlined">skip_next</span> Step Through
      </button>
      <button class="btn btn-ghost" id="btnAutoPlay" onclick="toggleAutoPlay()" disabled>
        <span class="material-symbols-outlined">fast_forward</span> Auto Play
      </button>
      <button class="btn btn-ghost" id="btnShowAll" onclick="showAllSteps()" style="display:none">
        <span class="material-symbols-outlined">visibility</span> Show All
      </button>
      <button class="btn btn-ghost" id="btnReset" onclick="resetReplay()" style="display:none">
        <span class="material-symbols-outlined">restart_alt</span> Reset
      </button>
    </div>
  </div>

  <div id="replayOutput">
    <div class="empty-hint" id="emptyHint">
      <span class="material-symbols-outlined">replay</span>
      Paste a log above and click <strong>Parse &amp; Replay</strong> to visualize agent decisions.
    </div>
  </div>
</div>

<script>
const ACTION_ICONS = {classify:'label',route:'alt_route',request_info:'help_outline',escalate:'trending_up',resolve:'check_circle',skip:'skip_next',error:'error'};
let parsedSteps = [];
let parsedStart = null;
let parsedEnd = null;
let stepMode = false;
let stepIndex = 0;
let autoInterval = null;

function parseAndRender() {
  const raw = document.getElementById('logInput').value.trim();
  if (!raw) return;
  parsedSteps = [];
  parsedStart = null;
  parsedEnd = null;
  stepMode = false;
  stepIndex = 0;
  if (autoInterval) { clearInterval(autoInterval); autoInterval = null; }

  const lines = raw.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('[START]')) {
      const task = (trimmed.match(/task=(\S+)/) || [])[1] || '?';
      const model = (trimmed.match(/model=(\S+)/) || [])[1] || '?';
      parsedStart = { task, model };
    } else if (trimmed.startsWith('[STEP]')) {
      const step = parseInt((trimmed.match(/step=(\d+)/) || [])[1] || '0');
      const action = (trimmed.match(/action=(\S+)/) || [])[1] || '?';
      const reward = parseFloat((trimmed.match(/reward=([\-\d.]+)/) || [])[1] || '0');
      const done = (trimmed.match(/done=(\S+)/) || [])[1] === 'true';
      const errMatch = trimmed.match(/error=(\S+)/);
      const error = errMatch && errMatch[1] !== 'null' ? errMatch[1] : null;
      parsedSteps.push({ step, action, reward, done, error });
    } else if (trimmed.startsWith('[END]')) {
      const success = (trimmed.match(/success=(\S+)/) || [])[1] === 'true';
      const steps = parseInt((trimmed.match(/steps=(\d+)/) || [])[1] || '0');
      const score = parseFloat((trimmed.match(/score=([\-\d.]+)/) || [])[1] || '0');
      const rewardsStr = (trimmed.match(/rewards=([\S]+)/) || [])[1] || '';
      const rewards = rewardsStr ? rewardsStr.split(',').map(Number) : [];
      parsedEnd = { success, steps, score, rewards };
    }
  }

  renderFull();
  document.getElementById('btnStepThrough').disabled = false;
  document.getElementById('btnAutoPlay').disabled = false;
  document.getElementById('btnReset').style.display = '';
}

function renderFull() {
  const out = document.getElementById('replayOutput');
  let html = '';

  // Start info
  if (parsedStart) {
    html += `<div class="step-card" style="border-left:3px solid var(--accent)">
      <div class="step-num" style="background:linear-gradient(135deg,#8b5cf6,#c084fc);color:#fff">▶</div>
      <div class="step-info"><div class="step-action">Episode Start</div>
        <div class="step-meta">Task: <strong>${parsedStart.task.replace(/_/g,' ')}</strong> &nbsp;|&nbsp; Model: <strong>${parsedStart.model}</strong></div>
      </div></div>`;
  }

  // Chart
  if (parsedSteps.length > 0) {
    html += buildChart();
  }

  // Step cards
  html += '<div class="step-timeline" id="stepTimeline">';
  let cumulative = 0;
  parsedSteps.forEach((s, i) => {
    cumulative += s.reward;
    const icon = ACTION_ICONS[s.action] || 'radio_button_unchecked';
    const rClass = s.reward >= 0 ? 'pos' : 'neg';
    const rStr = (s.reward >= 0 ? '+' : '') + s.reward.toFixed(4);
    const errorHtml = s.error ? `<div class="step-error">⚠ ${s.error}</div>` : '';
    const errClass = s.error ? ' error-card' : '';
    html += `<div class="step-card${errClass}" data-step-idx="${i}">
      <div class="step-num">${s.step}</div>
      <span class="material-symbols-outlined step-icon">${icon}</span>
      <div class="step-info"><div class="step-action">${s.action.replace(/_/g,' ')}</div>
        <div class="step-meta">${s.done ? '✓ Terminal' : 'Continuing'} &nbsp;|&nbsp; Cumulative: ${cumulative.toFixed(4)}</div>
        ${errorHtml}</div>
      <div class="step-reward ${rClass}">${rStr}</div></div>`;
  });
  html += '</div>';

  // Summary
  if (parsedEnd) {
    const badge = parsedEnd.success
      ? '<span class="summary-badge pass"><span class="material-symbols-outlined" style="font-size:14px">check_circle</span>PASSED</span>'
      : '<span class="summary-badge fail-badge"><span class="material-symbols-outlined" style="font-size:14px">cancel</span>FAILED</span>';
    const col = parsedEnd.success ? 'var(--accent)' : 'var(--rose)';
    const sparkSvg = buildSparkline(parsedEnd.rewards, 400, 32);
    html += `<div class="summary-card ${parsedEnd.success ? 'success' : 'fail'}">
      ${badge}
      <div class="final-score" style="color:${col}">${parsedEnd.score.toFixed(4)}</div>
      <div class="summary-stats">
        <div class="stat-item"><div class="stat-value">${parsedEnd.steps}</div><div class="stat-label">Total Steps</div></div>
        <div class="stat-item"><div class="stat-value">${parsedEnd.rewards.length}</div><div class="stat-label">Rewards</div></div>
        <div class="stat-item"><div class="stat-value" style="color:${col}">${parsedEnd.rewards.reduce((a,b)=>a+b,0).toFixed(4)}</div><div class="stat-label">Total Reward</div></div>
      </div>
      <div class="sparkline-wrap">${sparkSvg}</div>
    </div>`;
  }

  out.innerHTML = html;
  document.getElementById('emptyHint').style.display = 'none';
}

function buildChart() {
  if (!parsedSteps.length) return '';
  const w = 900, h = 140, px = 40, py = 20;
  const iw = w - 2*px, ih = h - 2*py;
  let cum = 0;
  const pts = parsedSteps.map(s => { cum += s.reward; return cum; });
  const minY = Math.min(0, ...pts);
  const maxY = Math.max(0.1, ...pts);
  const rangeY = maxY - minY || 1;

  const toX = i => px + (i / Math.max(1, pts.length - 1)) * iw;
  const toY = v => py + ih - ((v - minY) / rangeY) * ih;

  let pathD = pts.map((v,i) => `${i===0?'M':'L'}${toX(i).toFixed(1)},${toY(v).toFixed(1)}`).join(' ');

  let dots = '';
  pts.forEach((v,i) => {
    const col = v >= 0 ? '#a78bfa' : '#fb7185';
    dots += `<circle cx="${toX(i).toFixed(1)}" cy="${toY(v).toFixed(1)}" r="4" fill="${col}" stroke="#06080f" stroke-width="2"/>`;
  });

  // zero line
  const zeroY = toY(0);
  const zeroLine = `<line x1="${px}" y1="${zeroY.toFixed(1)}" x2="${w-px}" y2="${zeroY.toFixed(1)}" stroke="var(--surface3)" stroke-width="1" stroke-dasharray="4,4"/>`;

  // axis labels
  let labels = '';
  parsedSteps.forEach((s,i) => {
    if (pts.length <= 20 || i % Math.ceil(pts.length/15) === 0)
      labels += `<text x="${toX(i).toFixed(1)}" y="${h-2}" text-anchor="middle" fill="var(--text3)" font-size="9" font-family="JetBrains Mono">${s.step}</text>`;
  });

  return `<div class="chart-card">
    <div class="card-title"><span class="material-symbols-outlined">show_chart</span>Cumulative Reward Over Time</div>
    <svg width="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet">
      ${zeroLine}
      <path d="${pathD}" fill="none" stroke="url(#chartGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <defs><linearGradient id="chartGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#c084fc"/></linearGradient></defs>
      ${dots}${labels}
    </svg></div>`;
}

function buildSparkline(rewards, w, h) {
  if (!rewards.length) return '';
  const px = 4;
  const iw = w - 2*px, ih = h - 8;
  const mn = Math.min(...rewards);
  const mx = Math.max(...rewards);
  const rng = mx - mn || 1;
  const toX = i => px + (i / Math.max(1, rewards.length - 1)) * iw;
  const toY = v => 4 + ih - ((v - mn) / rng) * ih;
  const d = rewards.map((v,i)=>`${i===0?'M':'L'}${toX(i).toFixed(1)},${toY(v).toFixed(1)}`).join(' ');
  return `<svg width="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="display:block">
    <path d="${d}" fill="none" stroke="var(--accent)" stroke-width="1.5" opacity=".6"/>
    ${rewards.map((v,i)=>`<circle cx="${toX(i).toFixed(1)}" cy="${toY(v).toFixed(1)}" r="2" fill="var(--accent)"/>`).join('')}
  </svg>`;
}

/* ═══ STEP-THROUGH MODE ═══ */
function enterStepMode() {
  stepMode = true;
  stepIndex = 0;
  const cards = document.querySelectorAll('#stepTimeline .step-card');
  cards.forEach(c => c.classList.add('hidden'));
  document.getElementById('btnStepThrough').disabled = true;
  document.getElementById('btnShowAll').style.display = '';
  // Show first
  advanceStep();
}

function advanceStep() {
  const cards = document.querySelectorAll('#stepTimeline .step-card');
  if (stepIndex < cards.length) {
    cards[stepIndex].classList.remove('hidden');
    cards[stepIndex].scrollIntoView({ behavior:'smooth', block:'center' });
    stepIndex++;
  }
  if (stepIndex >= cards.length && autoInterval) {
    clearInterval(autoInterval);
    autoInterval = null;
    document.getElementById('btnAutoPlay').innerHTML = '<span class="material-symbols-outlined">fast_forward</span> Auto Play';
  }
}

function toggleAutoPlay() {
  if (autoInterval) {
    clearInterval(autoInterval);
    autoInterval = null;
    document.getElementById('btnAutoPlay').innerHTML = '<span class="material-symbols-outlined">fast_forward</span> Auto Play';
  } else {
    if (!stepMode) enterStepMode();
    autoInterval = setInterval(() => {
      const cards = document.querySelectorAll('#stepTimeline .step-card');
      if (stepIndex >= cards.length) { clearInterval(autoInterval); autoInterval = null; return; }
      advanceStep();
    }, 1000);
    document.getElementById('btnAutoPlay').innerHTML = '<span class="material-symbols-outlined">pause</span> Pause';
  }
}

function showAllSteps() {
  stepMode = false;
  if (autoInterval) { clearInterval(autoInterval); autoInterval = null; }
  document.querySelectorAll('#stepTimeline .step-card').forEach(c => c.classList.remove('hidden'));
  document.getElementById('btnStepThrough').disabled = false;
  document.getElementById('btnShowAll').style.display = 'none';
  document.getElementById('btnAutoPlay').innerHTML = '<span class="material-symbols-outlined">fast_forward</span> Auto Play';
}

function resetReplay() {
  if (autoInterval) { clearInterval(autoInterval); autoInterval = null; }
  parsedSteps = []; parsedStart = null; parsedEnd = null; stepMode = false; stepIndex = 0;
  document.getElementById('replayOutput').innerHTML = '';
  document.getElementById('emptyHint').style.display = '';
  document.getElementById('btnStepThrough').disabled = true;
  document.getElementById('btnAutoPlay').disabled = true;
  document.getElementById('btnReset').style.display = 'none';
  document.getElementById('btnShowAll').style.display = 'none';
  document.getElementById('logInput').value = '';
}

// Keyboard shortcut: Space = next step, Enter = parse
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.code === 'Space' && stepMode) { e.preventDefault(); advanceStep(); }
});
</script>
</body>
</html>"""
