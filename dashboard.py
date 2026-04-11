"""TriageFlow Dashboard — premium single-page HTML dashboard served at GET /dashboard."""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TriageFlow — AI Ticket Triage Dashboard</title>
<meta name="description" content="OpenEnv-compliant benchmark dashboard for AI-powered support ticket triage">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
/* ═══ NAV LINKS ═══ */
.nav-link{padding:5px 12px;border-radius:100px;font-size:11px;font-weight:600;color:var(--text2);text-decoration:none;border:1px solid transparent;transition:all .2s}
.nav-link:hover{color:var(--accent);border-color:var(--border)}
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
::selection{background:rgba(163,230,53,.25);color:#fff}
.mono{font-family:'JetBrains Mono',monospace}
::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:4px}::-webkit-scrollbar-thumb:hover{background:var(--text3)}

/* ───── ANIMATIONS ───── */
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(139,92,246,.5)}100%{box-shadow:0 0 0 8px rgba(139,92,246,0)}}
@keyframes glow-breathe{0%,100%{box-shadow:0 0 20px rgba(139,92,246,.08)}50%{box-shadow:0 0 40px rgba(139,92,246,.25),0 0 80px rgba(139,92,246,.08)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes float{0%,100%{transform:translateY(0px)}50%{transform:translateY(-6px)}}
.fade-up{animation:fadeUp .25s ease}
.loading-sh{background:linear-gradient(90deg,var(--surface) 25%,var(--surface2) 50%,var(--surface) 75%)!important;background-size:200% 100%;animation:shimmer 1.5s infinite;color:transparent!important;pointer-events:none}
.loading-sh *{color:transparent!important}

/* ───── BADGES ───── */
.badge{display:inline-flex;align-items:center;gap:3px;padding:3px 10px;border-radius:100px;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;white-space:nowrap}
.badge-low{background:rgba(16,185,129,.15);color:#34d399;border:1px solid rgba(16,185,129,.25)}
.badge-medium{background:rgba(251,191,36,.12);color:#fbbf24;border:1px solid rgba(251,191,36,.25)}
.badge-high{background:rgba(249,115,22,.12);color:#fb923c;border:1px solid rgba(249,115,22,.25)}
.badge-critical{background:rgba(251,113,133,.12);color:#fb7185;border:1px solid rgba(251,113,133,.3);animation:pulse-ring 2s infinite}
.badge-pill{background:rgba(96,165,250,.1);color:#60a5fa;border:1px solid rgba(96,165,250,.2)}
.badge-accent{background:var(--accent-dim);color:var(--accent);border:1px solid rgba(163,230,53,.2)}
.badge-version{background:rgba(148,163,184,.08);color:var(--text2);border:1px solid var(--border)}

/* ───── CARDS ───── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;transition:all .2s ease}
.card:hover{border-color:var(--border-bright)}
.card-glass{background:rgba(17,24,39,.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius)}
.card-title{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-bottom:14px;display:flex;align-items:center;gap:6px}

/* ───── BUTTONS ───── */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:9px 16px;border:none;border-radius:var(--radius-sm);font-family:'Inter',sans-serif;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;letter-spacing:.3px}
.btn-accent{background:var(--accent);color:var(--bg);box-shadow:0 0 15px var(--accent-glow)}
.btn-accent:hover{filter:brightness(1.1);transform:translateY(-1px);box-shadow:0 0 30px var(--accent-glow)}
.btn-accent:active{transform:translateY(0)}
.btn-ghost{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
.btn-sm{padding:6px 12px;font-size:11px}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none!important;filter:none!important}

/* ───── FORMS ───── */
.form-group{margin-bottom:12px}
.form-label{display:block;font-size:9px;font-weight:700;color:var(--accent);margin-bottom:5px;text-transform:uppercase;letter-spacing:1px}
.form-select,.form-input{width:100%;padding:10px 14px;background:rgba(6,8,15,.8);border:1px solid rgba(139,92,246,.12);border-radius:var(--radius-sm);color:var(--text);font-family:'Inter',sans-serif;font-size:13px;font-weight:500;outline:none;transition:all .25s cubic-bezier(.4,0,.2,1);-webkit-appearance:none;appearance:none}
.form-select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23a78bfa' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:32px;cursor:pointer}
.form-select:hover,.form-input:hover{border-color:rgba(139,92,246,.3);background:rgba(11,13,26,.9)}
.form-select:focus,.form-input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(139,92,246,.12),0 0 20px rgba(139,92,246,.06);background:rgba(11,13,26,.95)}
.form-select option{background:#0f1225;color:var(--text);padding:8px;font-weight:500}
.form-input::placeholder{color:var(--text3);font-weight:400}

/* ═══════ HEADER ═══════ */
.header{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:56px;background:rgba(6,8,15,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header-left{display:flex;align-items:center;gap:12px}
.logo{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:800;letter-spacing:-.3px}
.logo-icon{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#c084fc);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(139,92,246,.3);animation:glow-breathe 4s ease-in-out infinite}
.logo-icon .material-symbols-outlined{font-size:18px;color:var(--bg);font-variation-settings:'FILL' 1}
.header-center{display:flex;gap:6px}
.chip{display:flex;align-items:center;gap:5px;padding:5px 14px;background:var(--surface);border:1px solid var(--border);border-radius:100px;font-size:11px;color:var(--text2);font-weight:500}
.chip .val{color:var(--text);font-weight:700;font-family:'JetBrains Mono',monospace;font-size:11px}
.header-right{display:flex;align-items:center;gap:10px}
.status-pill{display:flex;align-items:center;gap:6px;padding:4px 12px;border-radius:100px;font-size:11px;font-weight:700;letter-spacing:.3px}
.status-pill.live{background:rgba(163,230,53,.1);color:var(--accent);border:1px solid rgba(163,230,53,.2)}
.status-pill.offline{background:rgba(251,113,133,.1);color:var(--rose);border:1px solid rgba(251,113,133,.2)}
.status-dot{width:6px;height:6px;border-radius:50%}
.status-pill.live .status-dot{background:var(--accent);animation:pulse-ring 2s infinite}
.status-pill.offline .status-dot{background:var(--rose)}

/* ═══════ GRID LAYOUT ═══════ */
.main{display:grid;grid-template-columns:280px 1fr 260px;gap:0;height:calc(100vh - 56px);overflow:hidden}
.sidebar-left{border-right:1px solid var(--border);overflow-y:auto;padding:16px;background:var(--bg-subtle)}
.content{overflow-y:auto;padding:20px;position:relative}
.sidebar-right{border-left:1px solid var(--border);overflow-y:auto;padding:16px;background:var(--bg-subtle)}

/* Ambient glow in content area */
.content::before{content:'';position:absolute;top:-100px;right:-100px;width:400px;height:400px;background:radial-gradient(circle,rgba(163,230,53,.04) 0%,transparent 70%);pointer-events:none}
.content::after{content:'';position:absolute;bottom:-100px;left:-100px;width:350px;height:350px;background:radial-gradient(circle,rgba(96,165,250,.03) 0%,transparent 70%);pointer-events:none}

/* ═══════ SECTION TITLES ═══════ */
.section-title{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin:18px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:6px}
.section-title .material-symbols-outlined{font-size:14px;opacity:.5}

/* ═══════ TASK CARDS ═══════ */
.task-card{padding:14px;border-radius:var(--radius-sm);background:var(--surface);border:1px solid var(--border);margin-bottom:8px;transition:all .2s;cursor:pointer}
.task-card:hover{border-color:rgba(163,230,53,.3);background:rgba(163,230,53,.02)}
.task-card.active{border-color:var(--accent);background:rgba(163,230,53,.05);box-shadow:0 0 20px var(--accent-dim)}
.task-card h4{font-size:13px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px}
.task-card p{font-size:11px;color:var(--text3);margin-bottom:4px;line-height:1.5}
.task-card .score-range{font-size:10px;color:var(--text3);margin-bottom:8px;font-family:'JetBrains Mono',monospace}

/* ═══════ TICKET VIEWER ═══════ */
.ticket-header{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px}
.ticket-id{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text3);padding:3px 8px;background:var(--surface2);border-radius:var(--radius-xs)}
.ticket-subject{font-size:20px;font-weight:800;color:#fff;margin-bottom:10px;line-height:1.3;letter-spacing:-.2px}
.ticket-meta{display:flex;align-items:center;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.avatar{width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#c084fc);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0}
.sender-info{display:flex;flex-direction:column;gap:1px}
.sender-info .name{font-weight:600;font-size:13px}
.sender-info .time{color:var(--text3);font-size:11px}
.ticket-body-box{font-size:13px;color:var(--text2);line-height:1.7;max-height:180px;overflow-y:auto;padding:16px;background:var(--bg);border-radius:var(--radius-sm);border:1px solid var(--border);margin-bottom:14px;position:relative}
.ticket-body-box::after{content:'';position:absolute;bottom:0;left:0;right:0;height:30px;background:linear-gradient(transparent,var(--bg));pointer-events:none}
.ticket-badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.attachment-chip{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.15);border-radius:100px;font-size:11px;color:var(--blue);font-weight:500}

/* ═══════ TIMELINE ═══════ */
.timeline{max-height:200px;overflow-y:auto;margin-bottom:14px}
.timeline-item{display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:var(--radius-xs);transition:all .15s;border:1px solid transparent}
.timeline-item:hover{background:rgba(255,255,255,.02);border-color:var(--border)}
.tl-step{font-size:10px;color:var(--text3);width:24px;flex-shrink:0;font-family:'JetBrains Mono',monospace;font-weight:700}
.tl-icon{font-size:16px;color:var(--text2)}
.tl-action{font-size:12px;font-weight:600;flex:1}
.tl-reward{font-size:12px;font-weight:700;width:50px;text-align:right;font-family:'JetBrains Mono',monospace}
.tl-reward.pos{color:var(--accent)}.tl-reward.neg{color:var(--rose)}

/* ═══════ REWARD BARS ═══════ */
.rbar-row{display:flex;align-items:center;gap:8px;margin-bottom:6px}
.rbar-label{font-size:10px;color:var(--text3);width:90px;text-align:right;flex-shrink:0;font-weight:500}
.rbar-track{flex:1;height:8px;background:var(--bg);border-radius:4px;overflow:hidden}
.rbar-fill{height:100%;border-radius:4px;transition:width .5s cubic-bezier(.4,0,.2,1);min-width:2px}
.rbar-val{font-size:11px;font-weight:700;width:42px;flex-shrink:0;font-family:'JetBrains Mono',monospace}
.reward-total{font-size:22px;font-weight:800;text-align:center;margin-top:8px;letter-spacing:-.3px}

/* ═══════ GAUGE ═══════ */
.gauge-wrap{display:flex;flex-direction:column;align-items:center;padding:16px 0;position:relative}
.gauge-wrap::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:140px;height:140px;border-radius:50%;background:var(--accent-dim);filter:blur(30px);opacity:.3;transition:opacity .3s}
.gauge-label{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-top:8px;font-weight:600}

/* ═══════ SCOREBOARD ═══════ */
.score-row{margin-bottom:10px}
.score-row .sr-name{font-size:11px;color:var(--text2);margin-bottom:4px;font-weight:500}
.sr-bar-wrap{display:flex;align-items:center;gap:8px}
.sr-track{flex:1;height:5px;background:var(--surface2);border-radius:3px;overflow:hidden}
.sr-fill{height:100%;border-radius:3px;transition:width .5s cubic-bezier(.4,0,.2,1)}
.sr-val{font-size:11px;font-weight:700;width:34px;text-align:right;font-family:'JetBrains Mono',monospace}

/* ═══════ TERMINAL ═══════ */
.terminal{background:#030712;color:#a78bfa;font-family:'JetBrains Mono',monospace;font-size:10px;padding:12px;border-radius:var(--radius-sm);height:200px;overflow-y:auto;border:1px solid var(--border);line-height:1.6;position:relative}
.terminal::before{content:'CONSOLE';position:absolute;top:6px;right:8px;font-size:8px;color:var(--text3);letter-spacing:1px;opacity:.5}

/* ═══════ SNACKBAR ═══════ */
.snackbar{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(100px);background:var(--surface2);color:#fff;padding:12px 28px;border-radius:var(--radius);font-size:13px;font-weight:600;z-index:200;transition:transform .3s cubic-bezier(.4,0,.2,1);pointer-events:none;box-shadow:0 12px 40px rgba(0,0,0,.5);border:1px solid var(--border)}
.snackbar.show{transform:translateX(-50%) translateY(0);pointer-events:auto}
.snackbar.error{border-color:rgba(251,113,133,.3)}
.snackbar.success{border-color:rgba(163,230,53,.3)}

/* ═══════ DIALOG ═══════ */
.dialog-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;z-index:300;opacity:0;pointer-events:none;transition:opacity .25s}
.dialog-overlay.show{opacity:1;pointer-events:auto}
.dialog-box{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:36px;width:440px;max-width:90vw;text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.5)}
.dialog-box h2{font-size:20px;font-weight:800;margin-bottom:6px}
.dialog-box .final-score{font-size:56px;font-weight:900;margin:16px 0;letter-spacing:-2px}
.dialog-box table{width:100%;margin:16px 0;text-align:left;font-size:12px;border-collapse:collapse}
.dialog-box table td{padding:6px 10px}
.dialog-box table td:last-child{text-align:right;font-weight:700;font-family:'JetBrains Mono',monospace}
.dialog-box table tr:hover{background:rgba(255,255,255,.02)}

/* ═══════ EMPTY STATE ═══════ */
.empty-state{text-align:center;padding:60px 20px;color:var(--text3);font-size:13px}
.empty-state .material-symbols-outlined{font-size:56px;margin-bottom:12px;display:block;opacity:.2;font-variation-settings:'FILL' 0,'wght' 300}
.empty-state p{margin-top:4px;font-size:12px;color:var(--text3);max-width:240px;margin-inline:auto;line-height:1.5}

/* ═══════ RESPONSIVE ═══════ */
/* ═══════ FULL-WIDTH SECTIONS ═══════ */
.full-section{padding:24px 28px;border-top:1px solid var(--border)}
.full-section-title{font-size:18px;font-weight:800;margin-bottom:16px;display:flex;align-items:center;gap:10px;letter-spacing:-.3px}

/* Agent Runner */
.runner-grid{display:grid;grid-template-columns:320px 1fr;gap:20px}
.runner-config{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.runner-output{background:#030712;border:1px solid var(--border);border-radius:var(--radius);padding:16px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent);min-height:300px;max-height:400px;overflow-y:auto;position:relative;line-height:1.6}
.runner-output::before{content:'LIVE OUTPUT';position:absolute;top:6px;right:8px;font-size:8px;color:var(--text3);letter-spacing:1px;opacity:.5}
.runner-score{font-size:48px;font-weight:900;text-align:center;margin-top:12px;letter-spacing:-2px}
.btn-run{background:linear-gradient(135deg,#3B82F6,#60a5fa);color:#fff;width:100%;margin-top:12px;padding:12px}
.btn-run:hover{filter:brightness(1.15);transform:translateY(-1px)}
.btn-stop{background:linear-gradient(135deg,#e11d48,#fb7185);color:#fff;width:100%;margin-top:8px;padding:10px}
.btn-download{margin-top:8px;width:100%}

/* Heatmap */
.heatmap-container{position:relative}
.heatmap-tooltip{position:absolute;background:var(--surface2);border:1px solid var(--border-bright);border-radius:var(--radius-xs);padding:10px 14px;font-size:11px;pointer-events:none;opacity:0;transition:opacity .15s;z-index:10;white-space:nowrap;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.heatmap-tooltip.visible{opacity:1}
.legend-bar{height:12px;border-radius:6px;margin-top:12px}
.legend-labels{display:flex;justify-content:space-between;font-size:10px;color:var(--text3);margin-top:4px}

@media(max-width:1024px){.main{grid-template-columns:1fr;height:auto}.sidebar-left,.sidebar-right{border:none;border-bottom:1px solid var(--border)}.header-center{display:none}.runner-grid{grid-template-columns:1fr}}
</style>
</head>
<body>

<!-- HEADER -->
<header class="header" id="headerBar">
  <div class="header-left">
    <div class="logo">
      <div class="logo-icon"><span class="material-symbols-outlined">bolt</span></div>
      TriageFlow
    </div>
    <span class="badge badge-version">v1.0.0</span>
    <span class="badge badge-accent">OpenEnv</span>
  </div>
  <div class="header-center">
    <div class="chip"><span class="material-symbols-outlined" style="font-size:14px">inbox</span>Queue: <span class="val" id="mcQueueDepth">—</span></div>
    <div class="chip"><span class="material-symbols-outlined" style="font-size:14px">footsteps</span>Step: <span class="val" id="mcStep">—</span></div>
    <div class="chip"><span class="material-symbols-outlined" style="font-size:14px">task</span>Task: <span class="val" id="mcTask">—</span></div>
  </div>
  <div class="header-right">
    <a href="/replay" class="nav-link">🔁 Replay</a>
    <a href="/leaderboard" class="nav-link">🏆 Leaderboard</a>
    <div class="status-pill" id="statusPill">
      <span class="status-dot"></span>
      <span id="statusLabel">—</span>
    </div>
  </div>
</header>

<!-- MAIN GRID -->
<div class="main">

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar-left" id="sidebarLeft">
    <div class="section-title"><span class="material-symbols-outlined">view_list</span>Select Task</div>
    <div id="taskList"></div>

    <div class="section-title"><span class="material-symbols-outlined">gamepad</span>Manual Action</div>
    <div class="form-group"><label class="form-label">Action Type</label><select class="form-select" id="fAction"><option value="classify">🏷️ Classify</option><option value="route">🔀 Route</option><option value="request_info">❓ Request Info</option><option value="escalate">⬆️ Escalate</option><option value="resolve">✅ Resolve</option><option value="skip">⏭️ Skip</option></select></div>
    <div class="form-group"><label class="form-label">Urgency</label><select class="form-select" id="fUrgency"><option value="none">— Select —</option><option value="low">🟢 Low</option><option value="medium">🟡 Medium</option><option value="high">🟠 High</option><option value="critical">🔴 Critical</option></select></div>
    <div class="form-group"><label class="form-label">Category</label><select class="form-select" id="fCategory"><option value="none">— Select —</option><option value="billing">💳 Billing</option><option value="technical">🔧 Technical</option><option value="account">👤 Account</option><option value="policy">📋 Policy</option><option value="other">📦 Other</option></select></div>
    <div class="form-group"><label class="form-label">Assigned Team</label><select class="form-select" id="fTeam"><option value="none">— Select —</option><option value="tier1">Tier 1 — General</option><option value="tier2">Tier 2 — Specialist</option><option value="billing">Billing Team</option><option value="security">Security Team</option><option value="management">Management</option></select></div>
    <div class="form-group"><label class="form-label">Missing Fields</label><input class="form-input" id="fMissing" placeholder="e.g. order_id, account_number"></div>
    <div class="form-group"><label class="form-label">Resolution Note</label><input class="form-input" id="fNote" placeholder="Describe the resolution (min. 20 chars)"></div>
    <div class="form-group"><label class="form-label">Escalation Reason</label><input class="form-input" id="fEscalation" placeholder="Reason for escalation..."></div>
    <button class="btn btn-accent" style="width:100%;margin-top:8px" id="btnSubmit" disabled>
      <span class="material-symbols-outlined" style="font-size:16px">send</span> Submit Action
    </button>
  </aside>

  <!-- CENTER CONTENT -->
  <main class="content" id="contentArea">
    <div id="ticketViewer">
      <div class="empty-state" id="emptyState">
        <span class="material-symbols-outlined">confirmation_number</span>
        <strong>No Active Episode</strong>
        <p>Select a task from the sidebar and load it to begin triaging tickets.</p>
      </div>
      <!-- Ticket card -->
      <div id="ticketCard" class="card fade-up" style="display:none">
        <div class="ticket-header">
          <div class="ticket-badges" id="tvBadges"></div>
          <span class="ticket-id" id="tvId"></span>
        </div>
        <div class="ticket-subject" id="tvSubject"></div>
        <div class="ticket-meta">
          <div class="avatar" id="tvAvatar"></div>
          <div class="sender-info">
            <span class="name" id="tvSender"></span>
            <span class="time" id="tvTime"></span>
          </div>
        </div>
        <div class="ticket-body-box" id="tvBody"></div>
        <div id="tvAttachments" style="margin-bottom:12px"></div>
      </div>

      <!-- Action history timeline -->
      <div id="timelineWrap" style="display:none">
        <div class="card-title" style="margin-top:16px"><span class="material-symbols-outlined" style="font-size:14px">history</span>Action History</div>
        <div class="timeline" id="timeline"></div>
      </div>

      <!-- Reward breakdown -->
      <div id="rewardWrap" class="card" style="display:none;margin-top:16px">
        <div class="card-title"><span class="material-symbols-outlined" style="font-size:14px">analytics</span>Reward Breakdown</div>
        <div id="rewardBars"></div>
        <div class="reward-total" id="rewardTotal">—</div>
      </div>
    </div>
  </main>

  <!-- RIGHT SIDEBAR -->
  <aside class="sidebar-right" id="sidebarRight">
    <!-- Score Gauge -->
    <div class="gauge-wrap">
      <svg width="130" height="130" viewBox="0 0 130 130" id="gaugesvg">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#a78bfa"/>
            <stop offset="100%" stop-color="#c084fc"/>
          </linearGradient>
        </defs>
        <circle cx="65" cy="65" r="52" fill="none" stroke="var(--surface2)" stroke-width="6"/>
        <circle cx="65" cy="65" r="52" fill="none" stroke="url(#gaugeGrad)" stroke-width="6"
          stroke-dasharray="326.73" stroke-dashoffset="326.73" stroke-linecap="round"
          transform="rotate(-90 65 65)" id="gaugeArc" style="transition:stroke-dashoffset .6s cubic-bezier(.4,0,.2,1)"/>
        <text x="65" y="62" text-anchor="middle" dominant-baseline="central"
          fill="#fff" font-size="24" font-weight="800" font-family="Inter" id="gaugeText">0.00</text>
        <text x="65" y="82" text-anchor="middle" fill="var(--text3)" font-size="9" font-weight="600" font-family="Inter" letter-spacing="1">SCORE</text>
      </svg>
      <div class="gauge-label">Episode Score</div>
    </div>

    <!-- Per-task scoreboard -->
    <div class="section-title"><span class="material-symbols-outlined">leaderboard</span>Task Scoreboard</div>
    <div id="scoreboard"></div>

    <!-- Terminal -->
    <div class="section-title"><span class="material-symbols-outlined">terminal</span>Step Log</div>
    <div class="terminal" id="terminalLog"></div>
  </aside>
</div>

<!-- ═══════ LIVE AGENT RUNNER ═══════ -->
<div class="full-section">
  <div class="full-section-title">🤖 Live Agent Runner</div>
  <div class="runner-grid">
    <div class="runner-config">
      <div class="card-title"><span class="material-symbols-outlined" style="font-size:14px">settings</span>Agent Configuration</div>
      <div class="form-group"><label class="form-label">API Base URL</label><input class="form-input" id="raUrl" placeholder="https://api.openai.com/v1" value="https://api.openai.com/v1"></div>
      <div class="form-group"><label class="form-label">Model Name</label><input class="form-input" id="raModel" placeholder="gpt-4o-mini" value="gpt-4o-mini"></div>
      <div class="form-group"><label class="form-label">API Key</label><input class="form-input" id="raKey" type="password" placeholder="sk-..."></div>
      <div class="form-group"><label class="form-label">Task</label>
        <div style="display:flex;flex-direction:column;gap:6px;margin-top:4px">
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer"><input type="radio" name="raTask" value="ticket_classification" checked style="accent-color:var(--accent)"> 🟢 Easy — Classification</label>
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer"><input type="radio" name="raTask" value="ticket_routing" style="accent-color:var(--accent)"> 🟡 Medium — Routing</label>
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer"><input type="radio" name="raTask" value="policy_triage" style="accent-color:var(--accent)"> 🔴 Hard — Policy Triage</label>
        </div>
      </div>
      <div class="form-group"><label class="form-label">Seed</label><input class="form-input" id="raSeed" type="number" value="42"></div>
      <button class="btn btn-run" id="btnRunAgent" onclick="runAgent()"><span class="material-symbols-outlined" style="font-size:16px">play_arrow</span> Run Agent</button>
      <button class="btn btn-stop" id="btnStopAgent" onclick="stopAgent()" style="display:none"><span class="material-symbols-outlined" style="font-size:16px">stop</span> Stop</button>
      <button class="btn btn-ghost btn-download" id="btnDownloadLog" onclick="downloadLog()" style="display:none"><span class="material-symbols-outlined" style="font-size:16px">download</span> Download Log</button>
    </div>
    <div>
      <div class="runner-output" id="runnerOutput"></div>
      <div class="runner-score" id="runnerScore" style="display:none"></div>
    </div>
  </div>
</div>

<!-- ═══════ TICKET DIFFICULTY HEATMAP ═══════ -->
<div class="full-section">
  <div class="full-section-title"><span class="material-symbols-outlined" style="font-size:20px;opacity:.6">grid_view</span> Agent Difficulty Matrix</div>
  <p style="color:var(--text3);font-size:12px;margin:-8px 0 16px;max-width:600px">Estimated resolution difficulty per category–urgency combination. Hover for routing guidance.</p>
  <div class="heatmap-container" id="heatmapContainer"></div>
  <div class="heatmap-tooltip" id="heatmapTooltip"></div>
</div>

<!-- Snackbar -->
<div class="snackbar" id="snackbar"></div>

<!-- Episode Complete Dialog -->
<div class="dialog-overlay" id="dialogOverlay">
  <div class="dialog-box">
    <span class="material-symbols-outlined" style="font-size:40px;color:var(--accent);margin-bottom:8px;display:block;font-variation-settings:'FILL' 1">emoji_events</span>
    <h2>Episode Complete</h2>
    <p style="color:var(--text3);font-size:13px" id="dlgInfo"></p>
    <div class="final-score" id="dlgScore">0.00</div>
    <table id="dlgTable"></table>
    <button class="btn btn-accent" style="margin-top:16px;width:100%" id="btnPlayAgain">
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
function showSnack(msg, type='error') {
  const el = $('snackbar'); el.textContent = msg; el.className = 'snackbar show ' + type;
  clearTimeout(snackTimer); snackTimer = setTimeout(() => el.classList.remove('show'), 4000);
}

/* ───────── HEALTH ───────── */
async function checkHealth() {
  try {
    await api('GET','/health');
    S.online=true;
    $('statusPill').className='status-pill live';
    $('statusLabel').textContent='LIVE';
  } catch {
    S.online=false;
    $('statusPill').className='status-pill offline';
    $('statusLabel').textContent='OFFLINE';
  }
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
        <button class="btn btn-accent btn-sm" data-task="${t.name}" style="width:100%">Load Task</button>`;
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
    showSnack('Episode started — ' + obs.queue_depth + ' tickets loaded', 'success');
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
  const m = $('fMissing').value.trim(); if (m) body.missing_fields = m.split(',').map(s=>s.trim()).filter(Boolean);
  const esc = $('fEscalation').value.trim(); if (esc) body.escalation_reason = esc;
  try {
    const res = await api('POST','/step', body);
    S.obs = res.observation; S.lastReward = res.reward; S.done = res.done;
    S.cumulativeReward += res.reward.total;
    const stepNum = S.stepHistory.length + 1;
    S.stepHistory.push({step:stepNum, action:body.action_type, reward:res.reward, obs:res.observation});
    addLog(`[STEP] step=${stepNum} action=${body.action_type} reward=${res.reward.total.toFixed(2)} done=${res.done} error=null`);
    renderTicket(); renderTimeline(); renderRewardBars(res.reward);
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
      addLog(`[END] success=${finalScore>=0.5} steps=${S.stepHistory.length} score=${finalScore.toFixed(2)} rewards=${S.stepHistory.map(h=>h.reward.total.toFixed(2)).join(',')}`);
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
  let bhtml = '';
  if (o.history) { const cls = o.history.find(h=>h.action_type==='classify');
    if(cls&&cls.urgency) bhtml += `<span class="badge badge-${cls.urgency}">${cls.urgency.toUpperCase()}</span>`;
    if(cls&&cls.category) bhtml += `<span class="badge badge-pill">${cls.category}</span>`;
  }
  $('tvBadges').innerHTML = bhtml;
  let ahtml = '';
  if (o.attachments && o.attachments.length) { o.attachments.forEach(a => { ahtml += `<span class="attachment-chip"><span class="material-symbols-outlined" style="font-size:14px">attach_file</span>${a}</span>`; }); }
  $('tvAttachments').innerHTML = ahtml;
  $('mcQueueDepth').textContent = o.queue_depth; $('mcStep').textContent = `${o.current_step}/${o.max_steps}`; $('mcTask').textContent = o.task_name ? o.task_name.replace(/_/g,' ') : '—';
  $('ticketCard').classList.add('fade-up'); setTimeout(()=>$('ticketCard').classList.remove('fade-up'),300);
}

/* ───────── RENDER: TIMELINE ───────── */
function renderTimeline() {
  const wrap = $('timeline'); wrap.innerHTML = '';
  S.stepHistory.forEach(h => {
    const icon = ACTION_ICONS[h.action] || 'radio_button_unchecked';
    const rw = h.reward.total; const rClass = rw >= 0 ? 'pos' : 'neg'; const rStr = (rw >= 0 ? '+' : '') + rw.toFixed(3);
    wrap.innerHTML += `<div class="timeline-item"><span class="tl-step">#${h.step}</span><span class="material-symbols-outlined tl-icon">${icon}</span><span class="tl-action">${h.action}</span><span class="tl-reward ${rClass}">${rStr}</span></div>`;
  });
  wrap.scrollTop = wrap.scrollHeight;
}

/* ───────── RENDER: REWARD BARS ───────── */
function renderRewardBars(reward) {
  const wrap = $('rewardBars'); wrap.innerHTML = '';
  if (!reward) { $('rewardTotal').textContent = '—'; return; }
  const components = [
    {label:'Correctness',val:reward.correctness,color:'var(--blue)'},
    {label:'Routing',val:reward.routing_score,color:'var(--violet)'},
    {label:'Completeness',val:reward.completeness,color:'var(--accent)'},
    {label:'Policy',val:reward.policy_compliance,color:'var(--amber)'},
    {label:'Step Penalty',val:reward.step_penalty,color:'var(--rose)'}
  ];
  components.forEach(c => {
    const pct = Math.min(100, Math.abs(c.val) * 500);
    const col = c.val < 0 ? 'var(--rose)' : c.color;
    wrap.innerHTML += `<div class="rbar-row"><span class="rbar-label">${c.label}</span><div class="rbar-track"><div class="rbar-fill" style="width:${pct}%;background:${col}"></div></div><span class="rbar-val" style="color:${col}">${c.val >= 0 ? '+' : ''}${c.val.toFixed(3)}</span></div>`;
  });
  const t = reward.total; const tc = t >= 0 ? 'var(--accent)' : 'var(--rose)';
  $('rewardTotal').innerHTML = `<span style="color:${tc}">${t >= 0 ? '+' : ''}${t.toFixed(3)}</span>`;
}

/* ───────── GAUGE ───────── */
function updateGauge(score) {
  const circ = 326.73; const offset = circ * (1 - score);
  $('gaugeArc').setAttribute('stroke-dashoffset', offset);
  $('gaugeText').textContent = score.toFixed(2);
}

/* ───────── SCOREBOARD ───────── */
function renderScoreboard() {
  const wrap = $('scoreboard'); wrap.innerHTML = '';
  ['ticket_classification','ticket_routing','policy_triage'].forEach(tn => {
    const sc = S.taskScores[tn]; const val = sc !== undefined ? sc : null;
    const pct = val !== null ? (val * 100) : 0;
    const col = val === null ? 'var(--surface3)' : val >= 0.7 ? 'var(--accent)' : val >= 0.4 ? 'var(--amber)' : 'var(--rose)';
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
  const col = score >= 0.7 ? 'var(--accent)' : score >= 0.4 ? 'var(--amber)' : 'var(--rose)';
  $('dlgScore').textContent = score.toFixed(2); $('dlgScore').style.color = col;
  $('dlgInfo').textContent = `Processed ${info.tickets_processed||'?'} of ${info.total_tickets||'?'} tickets in ${S.stepHistory.length} steps`;
  let thtml = '';
  if (S.stepHistory.length) {
    const totals = {correctness:0,routing_score:0,completeness:0,policy_compliance:0,step_penalty:0};
    S.stepHistory.forEach(h => { for (const k in totals) totals[k] += (h.reward[k]||0); });
    for (const [k,v] of Object.entries(totals)) {
      thtml += `<tr><td style="color:var(--text2)">${k.replace(/_/g,' ')}</td><td style="color:${v>=0?'var(--accent)':'var(--rose)'}">${v>=0?'+':''}${v.toFixed(3)}</td></tr>`;
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
  setInterval(async () => { await checkHealth(); if (S.activeTask && !S.done) await pollState(); }, 2000);
  renderHeatmap();
}
init();

/* ═══════ LIVE AGENT RUNNER ═══════ */
let agentController = null;
let agentLogLines = [];

async function runAgent() {
  const url = $('raUrl').value.trim();
  const model = $('raModel').value.trim();
  const key = $('raKey').value.trim();
  const task = document.querySelector('input[name="raTask"]:checked').value;
  const seed = parseInt($('raSeed').value) || 42;
  if (!url || !model || !key) { showSnack('Please fill in API URL, model, and key'); return; }
  $('btnRunAgent').style.display = 'none';
  $('btnStopAgent').style.display = '';
  $('btnDownloadLog').style.display = 'none';
  $('runnerScore').style.display = 'none';
  $('runnerOutput').textContent = '';
  agentLogLines = [];
  agentController = new AbortController();
  try {
    const resp = await fetch('/run_agent', {
      method:'POST', signal:agentController.signal,
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({api_base_url:url,model_name:model,api_key:key,task_name:task,seed})
    });
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, {stream:true});
      const parts = buffer.split('\n\n');
      buffer = parts.pop();
      for (const part of parts) {
        if (part.startsWith('data: ')) {
          const line = part.slice(6);
          agentLogLines.push(line);
          $('runnerOutput').textContent += line + '\n';
          $('runnerOutput').scrollTop = $('runnerOutput').scrollHeight;
          if (line.startsWith('[END]')) {
            const scoreM = line.match(/score=([\d.]+)/);
            if (scoreM) {
              const sc = parseFloat(scoreM[1]);
              const col = sc >= 0.5 ? 'var(--accent)' : 'var(--rose)';
              $('runnerScore').style.display = '';
              $('runnerScore').style.color = col;
              $('runnerScore').textContent = sc.toFixed(4);
            }
          }
        }
      }
    }
  } catch(e) { if (e.name !== 'AbortError') showSnack('Agent run error: ' + e.message); }
  $('btnRunAgent').style.display = '';
  $('btnStopAgent').style.display = 'none';
  if (agentLogLines.length) $('btnDownloadLog').style.display = '';
}

function stopAgent() {
  if (agentController) agentController.abort();
  $('btnRunAgent').style.display = '';
  $('btnStopAgent').style.display = 'none';
}

function downloadLog() {
  const task = document.querySelector('input[name="raTask"]:checked').value;
  const model = $('raModel').value.trim() || 'agent';
  const ts = new Date().toISOString().replace(/[:.]/g,'-');
  const blob = new Blob([agentLogLines.join('\n')], {type:'text/plain'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `triageflow_${task}_${model}_${ts}.txt`;
  a.click();
}

/* ═══════ AGENT DIFFICULTY MATRIX ═══════ */
function renderHeatmap() {
  const categories = ['Billing','Technical','Account','Policy','Other'];
  const urgencies = ['Critical','High','Medium','Low'];
  const diffMap = {
    'Technical-Critical':0.95,'Policy-High':0.88,'Billing-Critical':0.82,
    'Technical-High':0.79,'Policy-Critical':0.85,'Policy-Medium':0.71,
    'Account-Critical':0.72,'Account-High':0.65,'Account-Medium':0.58,
    'Billing-High':0.68,'Billing-Medium':0.55,'Technical-Medium':0.60,
    'Technical-Low':0.42,'Billing-Low':0.38,'Account-Low':0.31,
    'Policy-Low':0.45,'Other-Critical':0.35,'Other-High':0.28,
    'Other-Medium':0.25,'Other-Low':0.20
  };
  const recs = d => d>=0.8 ? 'Recommend immediate escalation to Tier 2' : d>=0.6 ? 'Route with caution; verify SLA compliance' : d>=0.4 ? 'Standard routing procedures apply' : 'Tier 1 resolution generally sufficient';
  const cellW=80, cellH=36, padL=70, padT=36, padB=44, gap=3;
  const w = padL + categories.length*(cellW+gap) + 10;
  const h = padT + urgencies.length*(cellH+gap) + padB;

  let svg = `<svg width="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="display:block;max-width:580px">`;
  // Column headers
  categories.forEach((c,i) => {
    svg += `<text x="${padL+i*(cellW+gap)+cellW/2}" y="${padT-10}" text-anchor="middle" fill="var(--text3)" font-size="10" font-weight="600" font-family="Inter" letter-spacing=".3">${c}</text>`;
  });
  // Row headers
  urgencies.forEach((u,j) => {
    svg += `<text x="${padL-8}" y="${padT+j*(cellH+gap)+cellH/2+3}" text-anchor="end" fill="var(--text3)" font-size="10" font-weight="500" font-family="Inter">${u}</text>`;
  });
  // Cells — subtle opacity-based tint on a single hue
  urgencies.forEach((u,j) => {
    categories.forEach((c,i) => {
      const key = `${c}-${u}`;
      const d = diffMap[key] !== undefined ? diffMap[key] : 0.5;
      // Low difficulty = subtle surface, High = vivid violet-rose
      const opacity = 0.12 + d * 0.55;
      const hue = Math.round(280 - d * 60); // violet(280) → rose-ish(220)
      const sat = Math.round(40 + d * 40);
      const fill = `hsla(${hue},${sat}%,60%,${opacity.toFixed(2)})`;
      const txtCol = d > 0.55 ? 'rgba(241,245,249,.9)' : 'rgba(148,163,184,.8)';
      const x = padL + i*(cellW+gap), y = padT + j*(cellH+gap);
      svg += `<rect x="${x}" y="${y}" width="${cellW}" height="${cellH}" rx="6" fill="${fill}" stroke="rgba(139,92,246,.08)" stroke-width="1" style="cursor:pointer;transition:opacity .15s" data-cat="${c}" data-urg="${u}" data-diff="${d.toFixed(2)}" data-rec="${recs(d)}"
        onmouseenter="showHeatTip(evt)" onmouseleave="hideHeatTip()" onmouseover="this.style.opacity=1;this.style.strokeWidth=1.5;this.style.stroke='rgba(167,139,250,.4)'" onmouseout="this.style.opacity='';this.style.strokeWidth=1;this.style.stroke='rgba(139,92,246,.08)'"/>`;
      svg += `<text x="${x+cellW/2}" y="${y+cellH/2+3.5}" text-anchor="middle" fill="${txtCol}" font-size="11" font-weight="600" font-family="JetBrains Mono" pointer-events="none">${d.toFixed(2)}</text>`;
    });
  });
  svg += '</svg>';
  // Compact legend
  svg += `<div style="max-width:260px;margin:8px 0 0"><div class="legend-bar" style="background:linear-gradient(90deg,hsla(280,40%,60%,.15),hsla(220,80%,60%,.65));height:6px;border-radius:3px"></div><div class="legend-labels" style="font-size:9px;margin-top:2px"><span>Low difficulty</span><span>High difficulty</span></div></div>`;
  $('heatmapContainer').innerHTML = svg;
}

function showHeatTip(evt) {
  const el = evt.target;
  const tip = $('heatmapTooltip');
  tip.innerHTML = `<div style="margin-bottom:4px"><strong>${el.dataset.cat}</strong> · ${el.dataset.urg} urgency</div><div style="color:var(--text2)">Difficulty index: <strong style="color:var(--text)">${el.dataset.diff}</strong></div><div style="color:var(--text3);margin-top:3px;font-style:italic">${el.dataset.rec}</div>`;
  tip.classList.add('visible');
  const rect = el.getBoundingClientRect();
  const container = $('heatmapContainer').getBoundingClientRect();
  tip.style.left = Math.max(0, rect.left - container.left + rect.width/2 - tip.offsetWidth/2) + 'px';
  tip.style.top = (rect.top - container.top - tip.offsetHeight - 6) + 'px';
}
function hideHeatTip() { $('heatmapTooltip').classList.remove('visible'); }

</script>
</body>
</html>"""
