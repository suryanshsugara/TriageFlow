"""TriageFlow Dashboard — single-page HTML dashboard served at GET /."""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TriageFlow — AI Ticket Triage Dashboard</title>
<meta name="description" content="OpenEnv-compliant benchmark dashboard for AI-powered support ticket triage">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Google+Sans+Display:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<script type="module" src="https://www.unpkg.com/@material/web/all.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0F172A;--surface:#1E293B;--surface2:#334155;--border:#334155;--primary:#3B82F6;--success:#10B981;--amber:#F59E0B;--rose:#F43F5E;--orange:#F97316;--text:#F8FAFC;--text2:#94A3B8;--text3:#64748B;--radius:12px;--radius-sm:8px;--radius-xs:6px}
html{font-size:14px}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
h1,h2,h3,h4{font-family:'Google Sans Display','Inter',sans-serif}
.mono{font-family:'JetBrains Mono','Courier New',monospace}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--surface2);border-radius:3px}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
.loading-sh{background:linear-gradient(90deg,var(--surface) 25%,var(--surface2) 50%,var(--surface) 75%)!important;background-size:200% 100%;animation:shimmer 1.5s infinite;color:transparent!important;pointer-events:none}
.loading-sh *{color:transparent!important}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
@keyframes dotpulse{0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,.7)}50%{box-shadow:0 0 0 6px rgba(16,185,129,0)}}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.fade-in{animation:fadeIn .15s ease}
.badge{display:inline-flex;align-items:center;padding:2px 10px;border-radius:100px;font-size:11px;font-weight:600;letter-spacing:.3px;white-space:nowrap}
.badge-low{background:#10B981;color:#fff}.badge-medium{background:#F59E0B;color:#000}.badge-high{background:#F97316;color:#fff}
.badge-critical{background:#F43F5E;color:#fff;animation:pulse 1s infinite}
.badge-pill{background:rgba(59,130,246,.15);color:#3B82F6;border:1px solid rgba(59,130,246,.3)}
.badge-version{background:rgba(148,163,184,.1);color:#94A3B8;border:1px solid rgba(148,163,184,.2)}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;transition:border-color .2s}
.card-title{font-size:12px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:8px 16px;border:none;border-radius:var(--radius-xs);font-family:'Inter',sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all .15s}
.btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:#2563EB;transform:translateY(-1px)}.btn-primary:active{transform:none}
.btn-sm{padding:6px 12px;font-size:12px}.btn:disabled{opacity:.5;cursor:not-allowed;transform:none!important}
.form-group{margin-bottom:8px}
.form-label{display:block;font-size:10px;font-weight:500;color:var(--text3);margin-bottom:3px;text-transform:uppercase;letter-spacing:.4px}
.form-select,.form-input{width:100%;padding:7px 10px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-xs);color:var(--text);font-family:'Inter',sans-serif;font-size:12px;outline:none;transition:border-color .15s}
.form-select:focus,.form-input:focus{border-color:var(--primary)}
.form-select option{background:var(--bg);color:var(--text)}

/* HEADER */
.header{display:flex;align-items:center;justify-content:space-between;padding:10px 24px;background:linear-gradient(135deg,#0F172A 0%,#1a2744 100%);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header-left{display:flex;align-items:center;gap:10px}
.logo{font-family:'Google Sans Display',sans-serif;font-size:20px;font-weight:700;color:#fff;display:flex;align-items:center;gap:8px}
.header-center{display:flex;gap:8px;flex-wrap:wrap}
.metric-chip{display:flex;align-items:center;gap:5px;padding:5px 12px;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:100px;font-size:11px;color:var(--text2)}
.metric-chip .val{color:#fff;font-weight:600}
.header-right{display:flex;align-items:center;gap:8px}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.status-dot.live{background:var(--success);animation:dotpulse 1.5s infinite}
.status-dot.offline{background:var(--rose)}
.status-label{font-size:12px;font-weight:600}

/* GRID */
.main{display:grid;grid-template-columns:270px 1fr 230px;gap:0;height:calc(100vh - 49px);overflow:hidden}
.sidebar-left{border-right:1px solid var(--border);overflow-y:auto;padding:14px}
.content{overflow-y:auto;padding:16px}
.sidebar-right{border-left:1px solid var(--border);overflow-y:auto;padding:14px}

/* TASK CARDS */
.task-card{padding:12px;border-radius:var(--radius-sm);background:var(--bg);border:1px solid var(--border);margin-bottom:8px;transition:all .15s}
.task-card:hover{border-color:rgba(59,130,246,.4)}
.task-card.active{border-color:var(--primary);background:rgba(59,130,246,.06)}
.task-card h4{font-size:13px;font-weight:600;margin-bottom:3px;display:flex;align-items:center;gap:6px}
.task-card p{font-size:11px;color:var(--text3);margin-bottom:4px;line-height:1.4}
.task-card .score-range{font-size:10px;color:var(--text3);margin-bottom:6px}

/* TICKET */
.ticket-id{font-family:'JetBrains Mono','Courier New',monospace;font-size:12px;color:var(--text3);float:right}
.ticket-subject{font-size:18px;font-weight:700;color:#fff;margin-bottom:8px}
.ticket-meta{display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.avatar{width:30px;height:30px;border-radius:50%;background:var(--primary);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;flex-shrink:0}
.ticket-body-box{font-size:13px;color:var(--text2);line-height:1.6;max-height:200px;overflow-y:auto;padding:14px;background:var(--bg);border-radius:var(--radius-sm);border:1px solid var(--border);margin-bottom:14px}
.ticket-badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.attachment-chip{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);border-radius:100px;font-size:11px;color:var(--primary)}

/* TIMELINE */
.timeline{max-height:170px;overflow-y:auto;margin-bottom:14px}
.timeline-item{display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:var(--radius-xs);transition:background .1s}
.timeline-item:hover{background:rgba(255,255,255,.03)}
.tl-step{font-size:11px;color:var(--text3);width:24px;flex-shrink:0;font-family:'JetBrains Mono',monospace}
.tl-icon{font-size:18px;color:var(--text2)}
.tl-action{font-size:12px;font-weight:500;flex:1}
.tl-reward{font-size:12px;font-weight:600;width:48px;text-align:right}
.tl-reward.pos{color:var(--success)}.tl-reward.neg{color:var(--rose)}

/* REWARD BARS */
.rbar-row{display:flex;align-items:center;gap:6px;margin-bottom:5px}
.rbar-label{font-size:10px;color:var(--text3);width:100px;text-align:right;flex-shrink:0}
.rbar-track{flex:1;height:12px;background:var(--bg);border-radius:6px;overflow:hidden}
.rbar-fill{height:100%;border-radius:6px;transition:width .4s ease;min-width:1px}
.rbar-val{font-size:11px;font-weight:600;width:36px;flex-shrink:0}
.reward-total{font-size:20px;font-weight:700;text-align:center;margin-top:6px}

/* GAUGE */
.gauge-wrap{display:flex;flex-direction:column;align-items:center;margin-bottom:16px}
.gauge-label{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.4px;margin-top:4px}

/* SCOREBOARD */
.score-row{margin-bottom:8px}
.score-row .sr-name{font-size:11px;color:var(--text2);margin-bottom:3px}
.sr-bar-wrap{display:flex;align-items:center;gap:6px}
.sr-track{flex:1;height:6px;background:var(--bg);border-radius:3px;overflow:hidden}
.sr-fill{height:100%;border-radius:3px;transition:width .4s ease}
.sr-val{font-size:11px;font-weight:600;width:32px;text-align:right}

/* TERMINAL */
.terminal{background:#0A0A0A;color:#22C55E;font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;padding:12px;border-radius:var(--radius-sm);height:200px;overflow-y:auto;border:1px solid #1F2937;line-height:1.5}

/* SNACKBAR */
.snackbar{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--rose);color:#fff;padding:10px 24px;border-radius:var(--radius-sm);font-size:13px;font-weight:500;z-index:200;transition:transform .25s ease;pointer-events:none;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.snackbar.show{transform:translateX(-50%) translateY(0);pointer-events:auto}

/* DIALOG */
.dialog-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:300;opacity:0;pointer-events:none;transition:opacity .2s}
.dialog-overlay.show{opacity:1;pointer-events:auto}
.dialog-box{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:32px;width:420px;max-width:90vw;text-align:center}
.dialog-box h2{font-size:18px;margin-bottom:6px}
.dialog-box .final-score{font-size:52px;font-weight:700;margin:12px 0}
.dialog-box table{width:100%;margin:12px 0;text-align:left;font-size:12px;border-collapse:collapse}
.dialog-box table td{padding:4px 8px}
.dialog-box table td:last-child{text-align:right;font-weight:600}
.section-title{font-size:11px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin:16px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--border)}
.empty-state{text-align:center;padding:40px 20px;color:var(--text3);font-size:13px}
.empty-state .material-symbols-outlined{font-size:48px;margin-bottom:8px;display:block;opacity:.3}
@media(max-width:768px){.header{flex-direction:column;gap:6px;padding:8px 12px}.header-center{flex-wrap:wrap;justify-content:center}.main{grid-template-columns:1fr;height:auto}.sidebar-left,.sidebar-right{border:none;border-bottom:1px solid var(--border)}}
</style>
</head>
<body>

<!-- HEADER -->
<header class="header" id="headerBar">
  <div class="header-left">
    <div class="logo">🎫 TriageFlow</div>
    <span class="badge badge-version">v1.0.0</span>
    <span class="badge badge-pill">OpenEnv Compliant</span>
  </div>
  <div class="header-center">
    <div class="metric-chip">Queue Depth: <span class="val" id="mcQueueDepth">—</span></div>
    <div class="metric-chip">Step: <span class="val" id="mcStep">—</span></div>
    <div class="metric-chip">Task: <span class="val" id="mcTask">—</span></div>
  </div>
  <div class="header-right">
    <span class="status-dot" id="statusDot"></span>
    <span class="status-label" id="statusLabel">—</span>
  </div>
</header>

<!-- MAIN GRID -->
<div class="main">

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar-left" id="sidebarLeft">
    <div class="section-title">Select Task</div>
    <div id="taskList"></div>
    <div class="section-title">Manual Action</div>
    <div class="form-group"><label class="form-label">Action Type</label><select class="form-select" id="fAction"><option value="classify">classify</option><option value="route">route</option><option value="request_info">request_info</option><option value="escalate">escalate</option><option value="resolve">resolve</option><option value="skip">skip</option></select></div>
    <div class="form-group"><label class="form-label">Urgency</label><select class="form-select" id="fUrgency"><option value="none">none</option><option value="low">low</option><option value="medium">medium</option><option value="high">high</option><option value="critical">critical</option></select></div>
    <div class="form-group"><label class="form-label">Category</label><select class="form-select" id="fCategory"><option value="none">none</option><option value="billing">billing</option><option value="technical">technical</option><option value="account">account</option><option value="policy">policy</option><option value="other">other</option></select></div>
    <div class="form-group"><label class="form-label">Assigned Team</label><select class="form-select" id="fTeam"><option value="none">none</option><option value="tier1">tier1</option><option value="tier2">tier2</option><option value="billing">billing</option><option value="security">security</option><option value="management">management</option></select></div>
    <div class="form-group"><label class="form-label">Resolution Note</label><input class="form-input" id="fNote" placeholder="Enter resolution note..."></div>
    <button class="btn btn-primary" style="width:100%;margin-top:6px" id="btnSubmit" disabled>
      <span class="material-symbols-outlined" style="font-size:16px">send</span> Submit Action
    </button>
  </aside>

  <!-- CENTER CONTENT -->
  <main class="content" id="contentArea">
    <div id="ticketViewer">
      <div class="empty-state" id="emptyState"><span class="material-symbols-outlined">confirmation_number</span>Select a task and load it to begin triage.</div>
      <!-- Ticket card injected here -->
      <div id="ticketCard" class="card fade-in" style="display:none">
        <span class="ticket-id" id="tvId"></span>
        <div class="ticket-subject" id="tvSubject"></div>
        <div class="ticket-meta">
          <div class="avatar" id="tvAvatar"></div>
          <div><span id="tvSender" style="font-weight:500"></span><span style="color:var(--text3);margin-left:8px;font-size:12px" id="tvTime"></span></div>
        </div>
        <div class="ticket-badges" id="tvBadges"></div>
        <div class="ticket-body-box" id="tvBody"></div>
        <div id="tvAttachments" style="margin-bottom:12px"></div>
      </div>

      <!-- Action history timeline -->
      <div id="timelineWrap" style="display:none">
        <div class="card-title" style="margin-top:14px">Action History</div>
        <div class="timeline" id="timeline"></div>
      </div>

      <!-- Reward breakdown -->
      <div id="rewardWrap" class="card" style="display:none;margin-top:14px">
        <div class="card-title">Reward Breakdown</div>
        <div id="rewardBars"></div>
        <div class="reward-total" id="rewardTotal">—</div>
      </div>
    </div>
  </main>

  <!-- RIGHT SIDEBAR -->
  <aside class="sidebar-right" id="sidebarRight">
    <!-- Score Gauge -->
    <div class="gauge-wrap">
      <svg width="120" height="120" viewBox="0 0 120 120" id="gaugesvg">
        <circle cx="60" cy="60" r="50" fill="none" stroke="#1E293B" stroke-width="8"/>
        <circle cx="60" cy="60" r="50" fill="none" stroke="var(--success)" stroke-width="8"
          stroke-dasharray="314.16" stroke-dashoffset="314.16" stroke-linecap="round"
          transform="rotate(-90 60 60)" id="gaugeArc" style="transition:stroke-dashoffset .4s ease,stroke .3s"/>
        <text x="60" y="60" text-anchor="middle" dominant-baseline="central"
          fill="#fff" font-size="22" font-weight="700" font-family="Inter" id="gaugeText">0.00</text>
      </svg>
      <div class="gauge-label">Episode Score</div>
    </div>

    <!-- Per-task scoreboard -->
    <div class="section-title">Task Scoreboard</div>
    <div id="scoreboard"></div>

    <!-- Terminal -->
    <div class="section-title">Step Log</div>
    <div class="terminal" id="terminalLog"></div>
  </aside>
</div>

<!-- Snackbar -->
<div class="snackbar" id="snackbar"></div>

<!-- Episode Complete Dialog -->
<div class="dialog-overlay" id="dialogOverlay">
  <div class="dialog-box">
    <h2>Episode Complete</h2>
    <p style="color:var(--text3);font-size:13px" id="dlgInfo"></p>
    <div class="final-score" id="dlgScore">0.00</div>
    <table id="dlgTable"></table>
    <button class="btn btn-primary" style="margin-top:12px;width:100%" id="btnPlayAgain">
      <span class="material-symbols-outlined" style="font-size:16px">replay</span> Play Again
    </button>
  </div>
</div>

<script>
/* ───────── STATE ───────── */
window.triageState = {
  online: false, tasks: [], activeTask: null, obs: null, lastReward: null,
  stepHistory: [], cumulativeReward: 0, episodeScore: 0, done: false,
  taskScores: JSON.parse(localStorage.getItem('tf_scores') || '{}'),
  logLines: [], submitting: false
};
const S = window.triageState;
const $ = (id) => document.getElementById(id);
const ACTION_ICONS = {classify:'label',route:'alt_route',request_info:'help_outline',escalate:'trending_up',resolve:'check_circle',skip:'skip_next'};
const SCORE_RANGES = {ticket_classification:'Agent: 0.85–0.95 | Random: 0.10–0.20',ticket_routing:'Agent: 0.70–0.85 | Random: 0.05–0.15',policy_triage:'Agent: 0.55–0.75 | Random: 0.02–0.10'};
const DIFF_BADGE = {easy:'badge-low',medium:'badge-medium',hard:'badge-critical'};

/* ───────── API ───────── */
async function api(method, path, body) {
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  if (!r.ok) { const e = await r.json().catch(()=>({})); throw new Error(e.detail || r.statusText); }
  return r.json();
}

/* ───────── SNACKBAR ───────── */
let snackTimer;
function showSnack(msg) {
  const el = $('snackbar'); el.textContent = msg; el.classList.add('show');
  clearTimeout(snackTimer); snackTimer = setTimeout(() => el.classList.remove('show'), 4000);
}

/* ───────── HEALTH ───────── */
async function checkHealth() {
  try { await api('GET','/health'); S.online=true; $('statusDot').className='status-dot live'; $('statusLabel').textContent='LIVE'; $('statusLabel').style.color='var(--success)';
  } catch { S.online=false; $('statusDot').className='status-dot offline'; $('statusLabel').textContent='OFFLINE'; $('statusLabel').style.color='var(--rose)'; }
}

/* ───────── TASKS ───────── */
async function loadTasks() {
  try {
    S.tasks = await api('GET','/tasks');
    const wrap = $('taskList'); wrap.innerHTML = '';
    S.tasks.forEach(t => {
      const div = document.createElement('div');
      div.className = 'task-card' + (S.activeTask === t.name ? ' active' : '');
      div.innerHTML = `<h4>${t.name.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())} <span class="badge ${DIFF_BADGE[t.difficulty]}">${t.difficulty.toUpperCase()}</span></h4>
        <p>${t.description}</p>
        <div class="score-range">${SCORE_RANGES[t.name]||''}</div>
        <button class="btn btn-primary btn-sm" data-task="${t.name}" style="width:100%">Load Task</button>`;
      div.querySelector('button').addEventListener('click', () => resetTask(t.name));
      wrap.appendChild(div);
    });
  } catch(e) { showSnack('Failed to load tasks: '+e.message); }
}

/* ───────── RESET ───────── */
async function resetTask(taskName) {
  try {
    $('sidebarLeft').querySelectorAll('.task-card').forEach(c=>c.classList.remove('active'));
    S.activeTask = taskName; S.done = false; S.stepHistory = []; S.cumulativeReward = 0; S.episodeScore = 0; S.lastReward = null;
    S.logLines = [];
    const obs = await api('POST','/reset',{task_name:taskName,seed:42});
    S.obs = obs;
    $('btnSubmit').disabled = false;
    renderTicket(); renderTimeline(); renderRewardBars(null); updateGauge(0);
    $('emptyState').style.display = 'none'; $('ticketCard').style.display = 'block';
    $('timelineWrap').style.display = 'block'; $('rewardWrap').style.display = 'block';
    addLog(`[START] task=${taskName} env=triageflow seed=42`);
    $('dialogOverlay').classList.remove('show');
    loadTasks(); // refresh active state
    pollState();
  } catch(e) { showSnack('Reset failed: '+e.message); }
}

/* ───────── STEP ───────── */
async function submitAction() {
  if (S.submitting || S.done || !S.obs) return;
  S.submitting = true; $('btnSubmit').disabled = true;
  $('ticketCard').classList.add('loading-sh');
  const body = { action_type: $('fAction').value };
  const u = $('fUrgency').value; if (u !== 'none') body.urgency = u;
  const c = $('fCategory').value; if (c !== 'none') body.category = c;
  const t = $('fTeam').value; if (t !== 'none') body.assigned_team = t;
  const n = $('fNote').value.trim(); if (n) body.resolution_note = n;
  try {
    const res = await api('POST','/step', body);
    S.obs = res.observation; S.lastReward = res.reward; S.done = res.done;
    S.cumulativeReward += res.reward.total;
    const stepNum = S.stepHistory.length + 1;
    S.stepHistory.push({step:stepNum, action:body.action_type, reward:res.reward, obs:res.observation});
    addLog(`[STEP] step=${stepNum} action=${body.action_type} reward=${res.reward.total.toFixed(2)} done=${res.done} error=null`);
    renderTicket(); renderTimeline(); renderRewardBars(res.reward);
    // Compute episode score from state
    try { const st = await api('GET','/state'); if(st.done && st.trajectory && st.trajectory.length) { const tr = st.trajectory; const tot = tr.reduce((s,x)=>s+x.reward.total,0); const tickets = st.total_tickets||1; S.episodeScore = Math.max(0,Math.min(1,tot/tickets)); } } catch{}
    if (!S.done) { const rawScore = Math.max(0, Math.min(1, S.cumulativeReward / Math.max(1, S.stepHistory.length * 0.2))); updateGauge(rawScore); }
    if (S.done) {
      const info = res.info || {};
      const finalScore = info.final_score !== undefined ? info.final_score : S.episodeScore;
      S.episodeScore = finalScore;
      updateGauge(finalScore);
      S.taskScores[S.activeTask] = finalScore;
      localStorage.setItem('tf_scores', JSON.stringify(S.taskScores));
      renderScoreboard();
      addLog(`[DONE] final_score=${finalScore.toFixed(4)} steps=${S.stepHistory.length} tickets_processed=${info.tickets_processed||'?'}/${info.total_tickets||'?'}`);
      showEpisodeDialog(finalScore, info);
      $('btnSubmit').disabled = true;
    } else { $('btnSubmit').disabled = false; }
  } catch(e) { showSnack('Step failed: '+e.message); $('btnSubmit').disabled = false;
  } finally { S.submitting = false; $('ticketCard').classList.remove('loading-sh'); }
}

/* ───────── RENDER: TICKET ───────── */
function renderTicket() {
  if (!S.obs) return;
  const o = S.obs;
  $('tvId').textContent = o.ticket_id;
  $('tvSubject').textContent = o.subject;
  const initials = (o.sender||'?').split(/[\s@]/).filter(Boolean).slice(0,2).map(w=>w[0].toUpperCase()).join('');
  $('tvAvatar').textContent = initials;
  $('tvSender').textContent = o.sender;
  const d = new Date(o.timestamp);
  $('tvTime').textContent = isNaN(d) ? o.timestamp : d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})+' at '+d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});
  $('tvBody').textContent = o.body;
  // Badges
  let bhtml = '';
  if (o.history) { const cls = o.history.find(h=>h.action_type==='classify');
    if(cls&&cls.urgency) bhtml += `<span class="badge badge-${cls.urgency}">${cls.urgency.toUpperCase()}</span>`;
    if(cls&&cls.category) bhtml += `<span class="badge badge-pill">${cls.category}</span>`;
  }
  $('tvBadges').innerHTML = bhtml;
  // Attachments
  let ahtml = '';
  if (o.attachments && o.attachments.length) { o.attachments.forEach(a => { ahtml += `<span class="attachment-chip"><span class="material-symbols-outlined" style="font-size:14px">attach_file</span>${a}</span>`; }); }
  $('tvAttachments').innerHTML = ahtml;
  // Update header metrics
  $('mcQueueDepth').textContent = o.queue_depth; $('mcStep').textContent = `${o.current_step}/${o.max_steps}`; $('mcTask').textContent = o.task_name ? o.task_name.replace(/_/g,' ') : '—';
  $('ticketCard').classList.add('fade-in'); setTimeout(()=>$('ticketCard').classList.remove('fade-in'),200);
}

/* ───────── RENDER: TIMELINE ───────── */
function renderTimeline() {
  const wrap = $('timeline'); wrap.innerHTML = '';
  S.stepHistory.forEach(h => {
    const icon = ACTION_ICONS[h.action] || 'radio_button_unchecked';
    const rw = h.reward.total; const rClass = rw >= 0 ? 'pos' : 'neg'; const rStr = (rw >= 0 ? '+' : '') + rw.toFixed(2);
    wrap.innerHTML += `<div class="timeline-item"><span class="tl-step">#${h.step}</span><span class="material-symbols-outlined tl-icon">${icon}</span><span class="tl-action">${h.action}</span><span class="tl-reward ${rClass}">${rStr}</span></div>`;
  });
  wrap.scrollTop = wrap.scrollHeight;
}

/* ───────── RENDER: REWARD BARS ───────── */
function renderRewardBars(reward) {
  const wrap = $('rewardBars'); wrap.innerHTML = '';
  if (!reward) { $('rewardTotal').textContent = '—'; return; }
  const components = [
    {label:'Correctness',val:reward.correctness,color:'var(--primary)'},
    {label:'Routing',val:reward.routing_score,color:'#8B5CF6'},
    {label:'Completeness',val:reward.completeness,color:'var(--success)'},
    {label:'Policy',val:reward.policy_compliance,color:'var(--amber)'},
    {label:'Step Penalty',val:reward.step_penalty,color:'var(--rose)'}
  ];
  components.forEach(c => {
    const pct = Math.min(100, Math.abs(c.val) * 500);
    const col = c.val < 0 ? 'var(--rose)' : c.color;
    wrap.innerHTML += `<div class="rbar-row"><span class="rbar-label">${c.label}</span><div class="rbar-track"><div class="rbar-fill" style="width:${pct}%;background:${col}"></div></div><span class="rbar-val" style="color:${col}">${c.val >= 0 ? '+' : ''}${c.val.toFixed(2)}</span></div>`;
  });
  const t = reward.total; const tc = t >= 0 ? 'var(--success)' : 'var(--rose)';
  $('rewardTotal').innerHTML = `<span style="color:${tc}">${t >= 0 ? '+' : ''}${t.toFixed(2)}</span>`;
}

/* ───────── GAUGE ───────── */
function updateGauge(score) {
  const circ = 314.16; const offset = circ * (1 - score);
  const arc = $('gaugeArc');
  arc.setAttribute('stroke-dashoffset', offset);
  arc.setAttribute('stroke', score >= 0.7 ? 'var(--success)' : score >= 0.4 ? 'var(--amber)' : 'var(--rose)');
  $('gaugeText').textContent = score.toFixed(2);
}

/* ───────── SCOREBOARD ───────── */
function renderScoreboard() {
  const wrap = $('scoreboard'); wrap.innerHTML = '';
  ['ticket_classification','ticket_routing','policy_triage'].forEach(tn => {
    const sc = S.taskScores[tn]; const val = sc !== undefined ? sc : null;
    const pct = val !== null ? (val * 100) : 0;
    const col = val === null ? 'var(--surface2)' : val >= 0.7 ? 'var(--success)' : val >= 0.4 ? 'var(--amber)' : 'var(--rose)';
    wrap.innerHTML += `<div class="score-row"><div class="sr-name">${tn.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}</div><div class="sr-bar-wrap"><div class="sr-track"><div class="sr-fill" style="width:${pct}%;background:${col}"></div></div><span class="sr-val" style="color:${col}">${val !== null ? val.toFixed(2) : '—'}</span></div></div>`;
  });
}

/* ───────── TERMINAL LOG ───────── */
function addLog(line) {
  S.logLines.push(line);
  if (S.logLines.length > 200) S.logLines.shift();
  const el = $('terminalLog');
  el.textContent = S.logLines.join('\n');
  el.scrollTop = el.scrollHeight;
}

/* ───────── EPISODE DIALOG ───────── */
function showEpisodeDialog(score, info) {
  const col = score >= 0.7 ? 'var(--success)' : score >= 0.4 ? 'var(--amber)' : 'var(--rose)';
  $('dlgScore').textContent = score.toFixed(2); $('dlgScore').style.color = col;
  $('dlgInfo').textContent = `Processed ${info.tickets_processed||'?'} of ${info.total_tickets||'?'} tickets in ${S.stepHistory.length} steps`;
  // Build reward breakdown table from last reward
  let thtml = '';
  if (S.stepHistory.length) {
    const totals = {correctness:0,routing_score:0,completeness:0,policy_compliance:0,step_penalty:0};
    S.stepHistory.forEach(h => { for (const k in totals) totals[k] += (h.reward[k]||0); });
    for (const [k,v] of Object.entries(totals)) {
      thtml += `<tr><td style="color:var(--text2)">${k.replace(/_/g,' ')}</td><td style="color:${v>=0?'var(--success)':'var(--rose)'}">${v>=0?'+':''}${v.toFixed(3)}</td></tr>`;
    }
  }
  $('dlgTable').innerHTML = thtml;
  $('dialogOverlay').classList.add('show');
}

/* ───────── POLL STATE ───────── */
async function pollState() {
  if (!S.activeTask || S.done) return;
  try {
    const st = await api('GET','/state');
    if (st.task_name) $('mcTask').textContent = st.task_name.replace(/_/g,' ');
    $('mcStep').textContent = `${st.current_step||0}/${st.max_steps||0}`;
    $('mcQueueDepth').textContent = st.total_tickets - (st.current_ticket_index||0);
  } catch {}
}

/* ───────── INIT ───────── */
async function init() {
  await checkHealth();
  await loadTasks();
  renderScoreboard();
  updateGauge(0);
  $('btnSubmit').addEventListener('click', submitAction);
  $('btnPlayAgain').addEventListener('click', () => { if(S.activeTask) resetTask(S.activeTask); });
  // Polling
  setInterval(async () => { await checkHealth(); if (S.activeTask && !S.done) await pollState(); }, 2000);
}
init();
</script>
</body>
</html>"""
