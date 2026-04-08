"""TriageFlow Landing Page — premium cosmic-themed landing + login page."""

LANDING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TriageFlow — AI-Powered Ticket Triage</title>
<meta name="description" content="Supercharge your support workflow with AI-powered ticket triage. TriageFlow uses intelligent agents to classify, route, and resolve tickets in seconds.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
/* ═══════════════════════════════════════════════════════════════
   RESET & VARIABLES
═══════════════════════════════════════════════════════════════ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root {
  --bg-deep:    #06070D;
  --bg-dark:    #0B0D18;
  --bg-surface: #111325;
  --bg-card:    #161938;
  --border:     rgba(139,92,246,.12);
  --border-glow:rgba(139,92,246,.35);
  --primary:    #8B5CF6;
  --primary-lt: #A78BFA;
  --accent:     #C084FC;
  --accent2:    #E879F9;
  --blue:       #3B82F6;
  --cyan:       #22D3EE;
  --emerald:    #10B981;
  --amber:      #F59E0B;
  --rose:       #F43F5E;
  --text:       #F1F5F9;
  --text2:      #94A3B8;
  --text3:      #64748B;
  --radius:     16px;
  --radius-sm:  10px;
  --radius-xs:  6px;
  --glow:       0 0 40px rgba(139,92,246,.15), 0 0 80px rgba(139,92,246,.06);
  --glow-sm:    0 0 20px rgba(139,92,246,.12);
}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg-deep);color:var(--text);overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer;border:none;outline:none}
img{max-width:100%;display:block}

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════════════════════════════ */
@keyframes float{
  0%,100%{transform:translateY(0)}
  50%{transform:translateY(-12px)}
}
@keyframes glow-pulse{
  0%,100%{box-shadow:0 0 20px rgba(139,92,246,.2)}
  50%{box-shadow:0 0 40px rgba(139,92,246,.35)}
}
@keyframes shimmer{
  0%{background-position:-200% 0}
  100%{background-position:200% 0}
}
@keyframes fadeInUp{
  from{opacity:0;transform:translateY(30px)}
  to{opacity:1;transform:translateY(0)}
}
@keyframes fadeInScale{
  from{opacity:0;transform:scale(.95)}
  to{opacity:1;transform:scale(1)}
}
@keyframes rotate-slow{
  from{transform:rotate(0deg)}
  to{transform:rotate(360deg)}
}
@keyframes gradient-shift{
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}
@keyframes border-flow{
  0%{border-color:rgba(139,92,246,.2)}
  50%{border-color:rgba(139,92,246,.5)}
  100%{border-color:rgba(139,92,246,.2)}
}
@keyframes text-glow{
  0%,100%{text-shadow:0 0 20px rgba(139,92,246,.3)}
  50%{text-shadow:0 0 40px rgba(139,92,246,.6),0 0 80px rgba(200,132,252,.2)}
}
@keyframes star-twinkle{
  0%,100%{opacity:.3}
  50%{opacity:1}
}
.animate-in{opacity:0;transform:translateY(30px);transition:opacity .6s ease,transform .6s ease}
.animate-in.visible{opacity:1;transform:translateY(0)}

/* ═══════════════════════════════════════════════════════════════
   STARS BACKGROUND
═══════════════════════════════════════════════════════════════ */
.stars-layer{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.star{position:absolute;width:2px;height:2px;background:#fff;border-radius:50%;animation:star-twinkle var(--dur) ease-in-out infinite;opacity:.3}

/* ═══════════════════════════════════════════════════════════════
   NAVBAR
═══════════════════════════════════════════════════════════════ */
.navbar{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 40px;
  background:rgba(6,7,13,.65);
  backdrop-filter:blur(20px) saturate(1.3);
  -webkit-backdrop-filter:blur(20px) saturate(1.3);
  border-bottom:1px solid rgba(139,92,246,.08);
  transition:all .3s ease;
}
.navbar.scrolled{
  background:rgba(6,7,13,.92);
  border-bottom-color:rgba(139,92,246,.15);
  box-shadow:0 4px 30px rgba(0,0,0,.4);
}
.nav-brand{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;letter-spacing:-.3px}
.nav-brand .brand-icon{
  width:36px;height:36px;
  background:linear-gradient(135deg,var(--primary),var(--accent2));
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:18px;color:#fff;
  box-shadow:0 0 20px rgba(139,92,246,.3);
}
.nav-links{display:flex;align-items:center;gap:6px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  border-radius:100px;padding:4px;
}
.nav-links a{
  padding:8px 18px;border-radius:100px;
  font-size:14px;font-weight:500;color:var(--text2);
  transition:all .2s ease;
}
.nav-links a:hover{color:#fff;background:rgba(139,92,246,.1)}
.nav-links a.active{color:#fff;background:rgba(139,92,246,.15)}
.nav-actions{display:flex;align-items:center;gap:12px}
.btn-ghost{
  padding:9px 20px;border-radius:10px;
  font-size:14px;font-weight:600;color:var(--text2);
  background:transparent;transition:all .2s;
}
.btn-ghost:hover{color:#fff}
.btn-cta{
  padding:9px 22px;border-radius:10px;
  font-size:14px;font-weight:600;color:#fff;
  background:linear-gradient(135deg,var(--primary),#7C3AED);
  box-shadow:0 0 20px rgba(139,92,246,.25);
  transition:all .25s ease;
  position:relative;overflow:hidden;
}
.btn-cta:hover{
  transform:translateY(-1px);
  box-shadow:0 4px 30px rgba(139,92,246,.4);
}
.btn-cta::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,transparent,rgba(255,255,255,.1),transparent);
  transform:translateX(-100%);transition:transform .5s;
}
.btn-cta:hover::after{transform:translateX(100%)}

/* ═══════════════════════════════════════════════════════════════
   HERO
═══════════════════════════════════════════════════════════════ */
.hero{
  position:relative;min-height:100vh;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:120px 24px 80px;overflow:hidden;
}
.hero-cosmic{
  position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:900px;height:900px;
  background:radial-gradient(ellipse at center,
    rgba(139,92,246,.18) 0%,
    rgba(139,92,246,.08) 25%,
    rgba(99,49,196,.04) 50%,
    transparent 70%
  );
  border-radius:50%;pointer-events:none;
  filter:blur(40px);
  animation:float 8s ease-in-out infinite;
}
.hero-cosmic-ring{
  position:absolute;top:50%;left:50%;
  width:650px;height:650px;
  border:1px solid rgba(139,92,246,.08);
  border-radius:50%;transform:translate(-50%,-50%);
  pointer-events:none;
  animation:rotate-slow 120s linear infinite;
}
.hero-cosmic-ring::before{
  content:'';position:absolute;top:-4px;left:50%;
  width:8px;height:8px;border-radius:50%;
  background:var(--primary);
  box-shadow:0 0 12px var(--primary);
}
.hero-badge{
  display:inline-flex;align-items:center;gap:8px;
  padding:6px 16px 6px 8px;
  background:rgba(139,92,246,.08);
  border:1px solid rgba(139,92,246,.2);
  border-radius:100px;font-size:13px;font-weight:500;
  color:var(--primary-lt);margin-bottom:28px;
  animation:fadeInUp .6s ease;
  animation:border-flow 3s ease infinite;
}
.hero-badge .badge-dot{
  width:8px;height:8px;border-radius:50%;
  background:var(--emerald);
  box-shadow:0 0 8px rgba(16,185,129,.6);
  animation:glow-pulse 2s ease infinite;
}
.hero-title{
  font-size:clamp(40px,6vw,72px);font-weight:900;
  letter-spacing:-2px;line-height:1.08;
  max-width:800px;margin-bottom:20px;
  background:linear-gradient(135deg,#fff 0%,#C4B5FD 40%,#A78BFA 60%,#E9D5FF 100%);
  background-size:200% 200%;
  animation:gradient-shift 6s ease infinite;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  animation:fadeInUp .7s ease .1s both, gradient-shift 6s ease infinite;
}
.hero-subtitle{
  font-size:clamp(16px,2vw,19px);color:var(--text2);
  max-width:540px;line-height:1.6;margin-bottom:36px;
  animation:fadeInUp .7s ease .2s both;
}
.hero-actions{
  display:flex;align-items:center;gap:14px;
  animation:fadeInUp .7s ease .3s both;
  flex-wrap:wrap;justify-content:center;
}
.btn-hero{
  padding:14px 32px;border-radius:14px;
  font-size:16px;font-weight:700;color:#fff;
  background:linear-gradient(135deg,var(--primary),#7C3AED);
  box-shadow:0 0 30px rgba(139,92,246,.3),0 8px 32px rgba(0,0,0,.3);
  transition:all .3s ease;position:relative;overflow:hidden;
}
.btn-hero:hover{
  transform:translateY(-2px);
  box-shadow:0 0 50px rgba(139,92,246,.45),0 12px 40px rgba(0,0,0,.4);
}
.btn-hero::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,transparent,rgba(255,255,255,.1),transparent);
  transform:translateX(-100%);transition:transform .6s;
}
.btn-hero:hover::after{transform:translateX(100%)}
.btn-hero-outline{
  padding:14px 32px;border-radius:14px;
  font-size:16px;font-weight:600;color:var(--text);
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  transition:all .3s ease;
}
.btn-hero-outline:hover{
  background:rgba(255,255,255,.08);
  border-color:rgba(139,92,246,.3);
  transform:translateY(-2px);
}

/* HERO APP PREVIEW */
.hero-preview{
  position:relative;
  margin-top:60px;
  max-width:920px;width:100%;
  animation:fadeInScale .8s ease .4s both;
}
.preview-glow{
  position:absolute;inset:-40px;
  background:radial-gradient(ellipse at center,rgba(139,92,246,.15),transparent 60%);
  border-radius:30px;pointer-events:none;
  filter:blur(30px);
}
.preview-frame{
  position:relative;
  background:var(--bg-surface);
  border:1px solid rgba(139,92,246,.15);
  border-radius:20px;
  overflow:hidden;
  box-shadow:0 20px 80px rgba(0,0,0,.5),0 0 40px rgba(139,92,246,.08);
}
.preview-titlebar{
  display:flex;align-items:center;gap:8px;
  padding:14px 18px;
  background:rgba(0,0,0,.3);
  border-bottom:1px solid rgba(255,255,255,.05);
}
.preview-dot{width:12px;height:12px;border-radius:50%}
.preview-dot.r{background:#F43F5E}.preview-dot.y{background:#F59E0B}.preview-dot.g{background:#10B981}
.preview-titlebar .url-bar{
  flex:1;margin:0 40px;padding:6px 14px;
  background:rgba(255,255,255,.05);border-radius:8px;
  font-size:12px;color:var(--text3);text-align:center;
  font-family:'JetBrains Mono',monospace;
}
.preview-body{
  display:grid;grid-template-columns:220px 1fr 200px;
  min-height:380px;
}
.preview-sidebar{padding:16px;border-right:1px solid rgba(255,255,255,.05)}
.preview-sidebar .ps-item{
  display:flex;align-items:center;gap:8px;
  padding:8px 12px;border-radius:8px;
  font-size:13px;color:var(--text2);
  margin-bottom:4px;transition:all .15s;
}
.preview-sidebar .ps-item:hover{background:rgba(139,92,246,.08);color:#fff}
.preview-sidebar .ps-item.active{background:rgba(139,92,246,.12);color:var(--primary-lt)}
.preview-sidebar .ps-item .material-symbols-outlined{font-size:18px}
.preview-center{padding:20px;border-right:1px solid rgba(255,255,255,.05)}
.preview-center .ticket-mock{
  background:rgba(0,0,0,.2);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:16px;margin-bottom:12px;
}
.preview-center .ticket-mock h4{font-size:14px;font-weight:600;margin-bottom:6px;color:#fff}
.preview-center .ticket-mock p{font-size:12px;color:var(--text3);line-height:1.5}
.preview-center .ticket-mock .mock-badge{
  display:inline-block;padding:2px 8px;border-radius:100px;
  font-size:10px;font-weight:600;margin-top:8px;
}
.preview-right-bar{padding:16px}
.preview-right-bar .gauge-mock{
  width:80px;height:80px;border-radius:50%;
  border:4px solid rgba(139,92,246,.2);
  border-top-color:var(--primary);
  display:flex;align-items:center;justify-content:center;
  margin:0 auto 12px;font-size:18px;font-weight:700;
  animation:rotate-slow 3s linear infinite;
}
.preview-right-bar .gauge-mock span{animation:rotate-slow 3s linear infinite reverse}
.preview-right-bar .sb-row{margin-bottom:8px}
.preview-right-bar .sb-row .sb-label{font-size:10px;color:var(--text3);margin-bottom:3px}
.preview-right-bar .sb-track{height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden}
.preview-right-bar .sb-fill{height:100%;border-radius:3px;transition:width 1s ease}

/* ═══════════════════════════════════════════════════════════════
   FEATURES
═══════════════════════════════════════════════════════════════ */
.features{
  padding:100px 40px;max-width:1200px;margin:0 auto;
  position:relative;z-index:1;
}
.section-header{text-align:center;margin-bottom:64px}
.section-header .overline{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:600;color:var(--primary-lt);
  text-transform:uppercase;letter-spacing:1.5px;
  margin-bottom:16px;
}
.section-header h2{
  font-size:clamp(28px,4vw,44px);font-weight:800;
  letter-spacing:-1px;margin-bottom:14px;
  background:linear-gradient(to right,#fff,#C4B5FD);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.section-header p{font-size:17px;color:var(--text2);max-width:540px;margin:0 auto;line-height:1.6}
.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.feature-card{
  padding:28px 24px;
  background:rgba(17,19,37,.6);
  border:1px solid rgba(139,92,246,.08);
  border-radius:var(--radius);
  transition:all .3s ease;
  position:relative;overflow:hidden;
}
.feature-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--primary),transparent);
  opacity:0;transition:opacity .3s;
}
.feature-card:hover{
  border-color:rgba(139,92,246,.2);
  transform:translateY(-4px);
  box-shadow:var(--glow);
}
.feature-card:hover::before{opacity:1}
.feature-icon{
  width:48px;height:48px;
  background:rgba(139,92,246,.1);
  border:1px solid rgba(139,92,246,.15);
  border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  margin-bottom:18px;
}
.feature-icon .material-symbols-outlined{font-size:24px;color:var(--primary-lt)}
.feature-card h3{font-size:16px;font-weight:700;margin-bottom:8px;color:#fff}
.feature-card p{font-size:14px;color:var(--text2);line-height:1.6}

/* ═══════════════════════════════════════════════════════════════
   STATS BAR
═══════════════════════════════════════════════════════════════ */
.stats-bar{
  display:flex;justify-content:center;gap:60px;
  padding:50px 40px;
  position:relative;z-index:1;
}
.stat-item{text-align:center}
.stat-number{
  font-size:42px;font-weight:800;
  background:linear-gradient(135deg,var(--primary-lt),var(--accent));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;letter-spacing:-1px;
}
.stat-label{font-size:14px;color:var(--text3);margin-top:4px;font-weight:500}

/* ═══════════════════════════════════════════════════════════════
   HOW IT WORKS
═══════════════════════════════════════════════════════════════ */
.how-it-works{
  padding:80px 40px 100px;max-width:1000px;margin:0 auto;
  position:relative;z-index:1;
}
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-top:64px}
.step-card{text-align:center;position:relative}
.step-number{
  width:56px;height:56px;border-radius:50%;
  background:linear-gradient(135deg,var(--primary),var(--accent2));
  display:flex;align-items:center;justify-content:center;
  font-size:22px;font-weight:800;color:#fff;
  margin:0 auto 20px;
  box-shadow:0 0 30px rgba(139,92,246,.25);
}
.step-card h3{font-size:17px;font-weight:700;margin-bottom:8px}
.step-card p{font-size:14px;color:var(--text2);line-height:1.6}
.step-connector{
  position:absolute;top:28px;left:calc(50% + 36px);
  width:calc(100% - 72px);height:2px;
  background:linear-gradient(90deg,rgba(139,92,246,.3),rgba(139,92,246,.1));
}
.step-card:last-child .step-connector{display:none}

/* ═══════════════════════════════════════════════════════════════
   CTA SECTION
═══════════════════════════════════════════════════════════════ */
.cta-section{
  padding:80px 40px;text-align:center;
  position:relative;z-index:1;
}
.cta-box{
  max-width:700px;margin:0 auto;
  padding:60px 40px;
  background:linear-gradient(135deg,rgba(139,92,246,.08),rgba(99,49,196,.04));
  border:1px solid rgba(139,92,246,.15);
  border-radius:24px;
  position:relative;overflow:hidden;
}
.cta-box::before{
  content:'';position:absolute;inset:-1px;
  background:linear-gradient(135deg,rgba(139,92,246,.3),transparent,rgba(200,132,252,.2));
  border-radius:24px;z-index:-1;
  filter:blur(40px);
}
.cta-box h2{
  font-size:32px;font-weight:800;letter-spacing:-1px;margin-bottom:14px;
  background:linear-gradient(to right,#fff,#C4B5FD);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.cta-box p{font-size:16px;color:var(--text2);margin-bottom:28px;line-height:1.6}

/* ═══════════════════════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════════════════════ */
.footer{
  padding:40px;text-align:center;
  border-top:1px solid rgba(139,92,246,.08);
  color:var(--text3);font-size:13px;
  position:relative;z-index:1;
}
.footer a{color:var(--primary-lt);transition:color .2s}
.footer a:hover{color:#fff}

/* ═══════════════════════════════════════════════════════════════
   LOGIN PAGE
═══════════════════════════════════════════════════════════════ */
.login-page{display:none}
.login-wrapper{
  min-height:100vh;
  display:flex;align-items:center;justify-content:center;
  padding:40px 20px;
  position:relative;
}
.login-glow{
  position:absolute;top:30%;left:50%;transform:translate(-50%,-50%);
  width:600px;height:600px;
  background:radial-gradient(ellipse at center,rgba(139,92,246,.12),transparent 60%);
  pointer-events:none;filter:blur(60px);
}
.login-card{
  width:100%;max-width:420px;
  background:rgba(17,19,37,.7);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border:1px solid rgba(139,92,246,.12);
  border-radius:24px;
  padding:44px 36px;
  box-shadow:0 20px 60px rgba(0,0,0,.4),var(--glow-sm);
  position:relative;z-index:2;
  animation:fadeInScale .5s ease;
}
.login-card .brand-row{
  display:flex;align-items:center;justify-content:center;gap:10px;
  margin-bottom:8px;
}
.login-card .brand-row .brand-icon{
  width:40px;height:40px;
  background:linear-gradient(135deg,var(--primary),var(--accent2));
  border-radius:12px;display:flex;align-items:center;justify-content:center;
  font-size:20px;color:#fff;box-shadow:0 0 20px rgba(139,92,246,.3);
}
.login-card .brand-row span{font-size:22px;font-weight:800;letter-spacing:-.3px}
.login-card .login-subtitle{text-align:center;color:var(--text2);font-size:14px;margin-bottom:32px}
.form-field{margin-bottom:18px}
.form-field label{
  display:block;font-size:12px;font-weight:600;
  color:var(--text2);margin-bottom:6px;
  text-transform:uppercase;letter-spacing:.5px;
}
.form-field .input-wrap{
  position:relative;display:flex;align-items:center;
}
.form-field .input-wrap .material-symbols-outlined{
  position:absolute;left:14px;font-size:18px;color:var(--text3);
}
.form-field input{
  width:100%;padding:13px 14px 13px 44px;
  background:rgba(0,0,0,.3);
  border:1px solid rgba(139,92,246,.1);
  border-radius:12px;color:#fff;
  font-size:14px;font-family:'Inter',sans-serif;
  outline:none;transition:all .2s;
}
.form-field input::placeholder{color:var(--text3)}
.form-field input:focus{
  border-color:var(--primary);
  box-shadow:0 0 0 3px rgba(139,92,246,.12);
}
.form-field .toggle-pw{
  position:absolute;right:14px;
  background:none;border:none;color:var(--text3);
  font-size:18px;cursor:pointer;padding:0;
}
.form-field .toggle-pw:hover{color:var(--text2)}
.form-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}
.form-row .remember{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text2)}
.form-row .remember input[type="checkbox"]{
  width:16px;height:16px;accent-color:var(--primary);
  border-radius:4px;cursor:pointer;
}
.form-row .forgot{font-size:13px;color:var(--primary-lt);font-weight:500;transition:color .2s}
.form-row .forgot:hover{color:#fff}
.btn-login{
  width:100%;padding:14px;border-radius:14px;
  font-size:15px;font-weight:700;color:#fff;
  background:linear-gradient(135deg,var(--primary),#7C3AED);
  box-shadow:0 0 24px rgba(139,92,246,.25);
  transition:all .25s ease;
  position:relative;overflow:hidden;
}
.btn-login:hover{
  transform:translateY(-1px);
  box-shadow:0 4px 30px rgba(139,92,246,.4);
}
.btn-login::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,transparent,rgba(255,255,255,.1),transparent);
  transform:translateX(-100%);transition:transform .5s;
}
.btn-login:hover::after{transform:translateX(100%)}
.divider{
  display:flex;align-items:center;gap:16px;
  margin:24px 0;color:var(--text3);font-size:12px;
}
.divider::before,.divider::after{
  content:'';flex:1;height:1px;
  background:rgba(255,255,255,.08);
}
.social-btns{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.btn-social{
  display:flex;align-items:center;justify-content:center;gap:8px;
  padding:11px 16px;border-radius:12px;
  font-size:13px;font-weight:600;color:var(--text);
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  transition:all .2s;
}
.btn-social:hover{background:rgba(255,255,255,.08);border-color:rgba(139,92,246,.2)}
.btn-social svg{width:18px;height:18px}
.signup-link{
  text-align:center;margin-top:24px;
  font-size:14px;color:var(--text2);
}
.signup-link a{color:var(--primary-lt);font-weight:600;transition:color .2s}
.signup-link a:hover{color:#fff}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════════════ */
@media(max-width:1024px){
  .features-grid{grid-template-columns:repeat(2,1fr)}
  .preview-body{grid-template-columns:1fr}
  .preview-sidebar,.preview-right-bar{display:none}
  .stats-bar{gap:30px;flex-wrap:wrap}
}
@media(max-width:768px){
  .navbar{padding:12px 20px}
  .nav-links{display:none}
  .hero{padding:100px 20px 60px}
  .features-grid{grid-template-columns:1fr}
  .steps-grid{grid-template-columns:1fr;gap:40px}
  .step-connector{display:none!important}
  .stats-bar{flex-direction:column;gap:24px}
  .login-card{padding:32px 24px}
}
@media(max-width:480px){
  .hero-title{font-size:32px;letter-spacing:-1px}
  .stat-number{font-size:32px}
}
</style>
</head>
<body>

<!-- STARS -->
<div class="stars-layer" id="starsLayer"></div>

<!-- ═══════ LANDING PAGE ═══════ -->
<div class="landing-page" id="landingPage">

<!-- NAVBAR -->
<nav class="navbar" id="navbar">
  <a href="#" class="nav-brand" onclick="showPage('landing');return false">
    <div class="brand-icon">🎫</div>
    TriageFlow
  </a>
  <div class="nav-links">
    <a href="#features" class="active">Features</a>
    <a href="#how-it-works">How It Works</a>
    <a href="#stats">Benchmarks</a>
    <a href="/dashboard" id="dashboardLink">Dashboard</a>
  </div>
  <div class="nav-actions">
    <button class="btn-ghost" id="navLoginBtn" onclick="showPage('login')">Login</button>
    <button class="btn-cta" onclick="showPage('login')">Start free trial</button>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-cosmic"></div>
  <div class="hero-cosmic-ring"></div>
  <div class="hero-badge">
    <span class="badge-dot"></span>
    OpenEnv Compliant Benchmark
  </div>
  <h1 class="hero-title">Triage smarter with TriageFlow</h1>
  <p class="hero-subtitle">Never miss a critical ticket, routing decision, or escalation. AI-powered triage that learns your workflow and acts in seconds.</p>
  <div class="hero-actions">
    <button class="btn-hero" onclick="showPage('login')">
      <span style="display:flex;align-items:center;gap:8px">
        Get Started <span class="material-symbols-outlined" style="font-size:18px">arrow_forward</span>
      </span>
    </button>
    <button class="btn-hero-outline" onclick="window.location.href='/dashboard'">
      <span style="display:flex;align-items:center;gap:8px">
        <span class="material-symbols-outlined" style="font-size:18px">play_circle</span> Live Demo
      </span>
    </button>
  </div>

  <!-- APP PREVIEW -->
  <div class="hero-preview">
    <div class="preview-glow"></div>
    <div class="preview-frame">
      <div class="preview-titlebar">
        <span class="preview-dot r"></span>
        <span class="preview-dot y"></span>
        <span class="preview-dot g"></span>
        <div class="url-bar">localhost:7860/dashboard</div>
      </div>
      <div class="preview-body">
        <div class="preview-sidebar">
          <div class="ps-item"><span class="material-symbols-outlined">label</span> Daily Notes</div>
          <div class="ps-item active"><span class="material-symbols-outlined">confirmation_number</span> Ticket Queue</div>
          <div class="ps-item"><span class="material-symbols-outlined">task_alt</span> Tasks</div>
          <div class="ps-item"><span class="material-symbols-outlined">analytics</span> Analytics</div>
          <div class="ps-item"><span class="material-symbols-outlined">map</span> Workflow Map</div>
        </div>
        <div class="preview-center">
          <div class="ticket-mock">
            <h4>🔴 Payment gateway returning 503 errors</h4>
            <p>Hi team, our checkout process has been failing intermittently since the last deployment. Customers are reporting payment timeouts...</p>
            <span class="mock-badge" style="background:rgba(244,63,94,.15);color:#F43F5E">CRITICAL</span>
            <span class="mock-badge" style="background:rgba(59,130,246,.15);color:#3B82F6;margin-left:6px">billing</span>
          </div>
          <div class="ticket-mock">
            <h4>🟡 Update user profile throws validation error</h4>
            <p>When attempting to update a user's display name with special characters, the API returns a 422 validation error...</p>
            <span class="mock-badge" style="background:rgba(245,158,11,.15);color:#F59E0B">MEDIUM</span>
            <span class="mock-badge" style="background:rgba(59,130,246,.15);color:#3B82F6;margin-left:6px">technical</span>
          </div>
          <div class="ticket-mock">
            <h4>🟢 Request for API documentation update</h4>
            <p>Could you update the REST API docs to include the new v3 endpoints? The current documentation only covers v2...</p>
            <span class="mock-badge" style="background:rgba(16,185,129,.15);color:#10B981">LOW</span>
            <span class="mock-badge" style="background:rgba(59,130,246,.15);color:#3B82F6;margin-left:6px">other</span>
          </div>
        </div>
        <div class="preview-right-bar">
          <div class="gauge-mock"><span>0.87</span></div>
          <div style="font-size:10px;color:var(--text3);text-align:center;margin-bottom:16px;text-transform:uppercase;letter-spacing:.4px">Episode Score</div>
          <div class="sb-row"><div class="sb-label">Classification</div><div class="sb-track"><div class="sb-fill" style="width:92%;background:var(--emerald)"></div></div></div>
          <div class="sb-row"><div class="sb-label">Routing</div><div class="sb-track"><div class="sb-fill" style="width:78%;background:var(--primary)"></div></div></div>
          <div class="sb-row"><div class="sb-label">Policy</div><div class="sb-track"><div class="sb-fill" style="width:64%;background:var(--amber)"></div></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="features" id="features">
  <div class="section-header animate-in">
    <div class="overline"><span class="material-symbols-outlined" style="font-size:16px">auto_awesome</span> Features</div>
    <h2>Everything you need for AI triage</h2>
    <p>A complete benchmark environment for developing and evaluating intelligent ticket triage agents.</p>
  </div>
  <div class="features-grid">
    <div class="feature-card animate-in">
      <div class="feature-icon"><span class="material-symbols-outlined">bolt</span></div>
      <h3>Built for speed</h3>
      <p>Deterministic graders evaluate agent actions in microseconds. No waiting, no bottlenecks. Pure performance.</p>
    </div>
    <div class="feature-card animate-in">
      <div class="feature-icon"><span class="material-symbols-outlined">hub</span></div>
      <h3>Networked scoring</h3>
      <p>Multi-dimensional reward signals cover correctness, routing, completeness, policy compliance, and step efficiency.</p>
    </div>
    <div class="feature-card animate-in">
      <div class="feature-icon"><span class="material-symbols-outlined">devices</span></div>
      <h3>REST API interface</h3>
      <p>OpenEnv-compliant HTTP endpoints. Connect any agent — Python, JavaScript, or any language with HTTP support.</p>
    </div>
    <div class="feature-card animate-in">
      <div class="feature-icon"><span class="material-symbols-outlined">lock</span></div>
      <h3>Reproducible benchmarks</h3>
      <p>Seeded task generation ensures deterministic, repeatable experiments for fair agent comparison.</p>
    </div>
  </div>
</section>

<!-- STATS -->
<div class="stats-bar" id="stats">
  <div class="stat-item animate-in">
    <div class="stat-number" id="statTasks">5</div>
    <div class="stat-label">Reward Dimensions</div>
  </div>
  <div class="stat-item animate-in">
    <div class="stat-number" id="statTickets">3</div>
    <div class="stat-label">Task Types</div>
  </div>
  <div class="stat-item animate-in">
    <div class="stat-number" id="statActions">6</div>
    <div class="stat-label">Action Types</div>
  </div>
  <div class="stat-item animate-in">
    <div class="stat-number" id="statScore">100%</div>
    <div class="stat-label">OpenEnv Compliant</div>
  </div>
</div>

<!-- HOW IT WORKS -->
<section class="how-it-works" id="how-it-works">
  <div class="section-header animate-in">
    <div class="overline"><span class="material-symbols-outlined" style="font-size:16px">route</span> Workflow</div>
    <h2>How TriageFlow works</h2>
    <p>Three simple steps to benchmark your AI triage agent.</p>
  </div>
  <div class="steps-grid">
    <div class="step-card animate-in">
      <div class="step-connector"></div>
      <div class="step-number">1</div>
      <h3>Load a task</h3>
      <p>Choose from classification, routing, or policy triage tasks with configurable difficulty levels.</p>
    </div>
    <div class="step-card animate-in">
      <div class="step-connector"></div>
      <div class="step-number">2</div>
      <h3>Triage tickets</h3>
      <p>Your agent reads tickets and takes actions — classify urgency, route to teams, escalate, or resolve.</p>
    </div>
    <div class="step-card animate-in">
      <div class="step-number">3</div>
      <h3>Get scored</h3>
      <p>Receive dense reward signals after each action.  Track cumulative scores across entire episodes.</p>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="cta-box animate-in">
    <h2>Ready to benchmark?</h2>
    <p>Start evaluating your AI triage agents in minutes. Open source, deterministic, and endlessly extensible.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <button class="btn-hero" onclick="showPage('login')">Get Started Free</button>
      <button class="btn-hero-outline" onclick="window.open('https://github.com','_blank')">
        <span style="display:flex;align-items:center;gap:8px">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          View on GitHub
        </span>
      </button>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <p>© 2026 TriageFlow · AI-Powered Support Ticket Triage Benchmark · Built with <a href="#">FastAPI</a> + <a href="#">OpenEnv</a></p>
</footer>

</div><!-- end landing page -->


<!-- ═══════ LOGIN PAGE ═══════ -->
<div class="login-page" id="loginPage">
<nav class="navbar scrolled" id="loginNav">
  <a href="#" class="nav-brand" onclick="showPage('landing');return false">
    <div class="brand-icon">🎫</div>
    TriageFlow
  </a>
  <div class="nav-actions">
    <button class="btn-ghost" onclick="showPage('landing')">← Back to Home</button>
  </div>
</nav>
<div class="login-wrapper">
  <div class="login-glow"></div>
  <div class="login-card">
    <div class="brand-row">
      <div class="brand-icon">🎫</div>
      <span>TriageFlow</span>
    </div>
    <p class="login-subtitle">Sign in to access your triage dashboard</p>
    <form id="loginForm" onsubmit="handleLogin(event)">
      <div class="form-field">
        <label for="loginEmail">Email Address</label>
        <div class="input-wrap">
          <span class="material-symbols-outlined">mail</span>
          <input type="email" id="loginEmail" placeholder="you@company.com" required autocomplete="email">
        </div>
      </div>
      <div class="form-field">
        <label for="loginPassword">Password</label>
        <div class="input-wrap">
          <span class="material-symbols-outlined">lock</span>
          <input type="password" id="loginPassword" placeholder="Enter your password" required autocomplete="current-password">
          <button type="button" class="toggle-pw" onclick="togglePassword()" aria-label="Toggle password visibility">
            <span class="material-symbols-outlined" id="pwIcon">visibility</span>
          </button>
        </div>
      </div>
      <div class="form-row">
        <label class="remember">
          <input type="checkbox" id="rememberMe"> Remember me
        </label>
        <a href="#" class="forgot" onclick="return false">Forgot password?</a>
      </div>
      <button type="submit" class="btn-login" id="loginSubmitBtn">
        Sign in to Dashboard
      </button>
    </form>
    <div class="divider">or continue with</div>
    <div class="social-btns">
      <button type="button" class="btn-social" onclick="handleSocialLogin('google')">
        <svg viewBox="0 0 24 24" fill="none"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
        Google
      </button>
      <button type="button" class="btn-social" onclick="handleSocialLogin('github')">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
        GitHub
      </button>
    </div>
    <div class="signup-link">
      Don't have an account? <a href="#" onclick="return false">Create one</a>
    </div>
  </div>
</div>
</div><!-- end login page -->


<canvas id="particleCanvas" style="position:fixed;inset:0;z-index:0;pointer-events:none"></canvas>
<script>
/* ═══════ INTERACTIVE PARTICLE SYSTEM ═══════ */
(function(){
  const c=document.getElementById('particleCanvas'),ctx=c.getContext('2d');
  let W,H,mx=0,my=0,particles=[];
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight}
  window.addEventListener('resize',resize);resize();
  document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY});
  class P{
    constructor(){this.reset()}
    reset(){this.x=Math.random()*W;this.y=Math.random()*H;this.r=Math.random()*1.8+.3;this.vx=(Math.random()-.5)*.3;this.vy=(Math.random()-.5)*.3;this.o=Math.random()*.5+.1;this.life=Math.random()*200+100}
    update(){
      const dx=mx-this.x,dy=my-this.y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<200){this.vx+=dx*.00003;this.vy+=dy*.00003;this.o=Math.min(.8,.1+(.2*(200-d)/200))}
      this.x+=this.vx;this.y+=this.vy;this.life--;
      if(this.x<0||this.x>W||this.y<0||this.y>H||this.life<=0)this.reset();
    }
    draw(){ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=`rgba(139,92,246,${this.o})`;ctx.fill()}
  }
  for(let i=0;i<120;i++)particles.push(new P());
  function loop(){
    ctx.clearRect(0,0,W,H);
    particles.forEach(p=>{p.update();p.draw()});
    // draw lines between nearby particles
    for(let i=0;i<particles.length;i++)for(let j=i+1;j<particles.length;j++){
      const dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y,d=dx*dx+dy*dy;
      if(d<12000){ctx.strokeStyle=`rgba(139,92,246,${.06*(1-d/12000)})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);ctx.stroke()}
    }
    requestAnimationFrame(loop);
  }
  loop();
})();

/* ═══════ PARALLAX MOUSE on HERO ═══════ */
(function(){
  const cosmic=document.querySelector('.hero-cosmic');
  const ring=document.querySelector('.hero-cosmic-ring');
  document.addEventListener('mousemove',e=>{
    const cx=window.innerWidth/2,cy=window.innerHeight/2;
    const dx=(e.clientX-cx)/cx,dy=(e.clientY-cy)/cy;
    if(cosmic)cosmic.style.transform=`translateX(calc(-50% + ${dx*30}px)) translateY(${dy*20}px)`;
    if(ring)ring.style.transform=`translate(calc(-50% + ${dx*-15}px),calc(-50% + ${dy*-10}px))`;
  });
})();

/* ═══════ STAGGERED SCROLL REVEAL ═══════ */
const animateObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const delay = e.target.dataset.delay || 0;
      setTimeout(() => e.target.classList.add('visible'), delay);
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.animate-in').forEach((el, i) => {
  el.dataset.delay = (i % 4) * 100;
  animateObserver.observe(el);
});

/* ═══════ ANIMATED NUMBER COUNTERS ═══════ */
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting || e.target.dataset.counted) return;
    e.target.dataset.counted = '1';
    const text = e.target.textContent;
    const isPercent = text.includes('%');
    const target = parseInt(text);
    let current = 0;
    const step = Math.max(1, Math.floor(target / 40));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      e.target.textContent = current + (isPercent ? '%' : '');
    }, 30);
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-number').forEach(el => counterObserver.observe(el));

/* ═══════ MAGNETIC BUTTON HOVER ═══════ */
document.querySelectorAll('.btn-hero, .btn-cta, .btn-hero-outline').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
    btn.style.transition = 'transform .4s cubic-bezier(.4,0,.2,1)';
    setTimeout(() => btn.style.transition = '', 400);
  });
});

/* ═══════ TILT EFFECT on PREVIEW FRAME ═══════ */
const preview = document.querySelector('.preview-frame');
if (preview) {
  preview.addEventListener('mousemove', e => {
    const rect = preview.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - .5;
    const y = (e.clientY - rect.top) / rect.height - .5;
    preview.style.transform = `perspective(1000px) rotateY(${x*6}deg) rotateX(${-y*6}deg)`;
  });
  preview.addEventListener('mouseleave', () => {
    preview.style.transform = '';
    preview.style.transition = 'transform .6s cubic-bezier(.4,0,.2,1)';
    setTimeout(() => preview.style.transition = 'all .3s ease', 600);
  });
}

/* ═══════ NAVBAR SCROLL ═══════ */
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  if (nav) nav.classList.toggle('scrolled', window.scrollY > 40);
});

/* ═══════ PAGE SWITCHING ═══════ */
function showPage(page) {
  const landing = document.getElementById('landingPage');
  const login = document.getElementById('loginPage');
  if (page === 'login') {
    landing.style.display = 'none';
    login.style.display = 'block';
    login.querySelector('.login-card').style.animation = 'none';
    requestAnimationFrame(() => {
      login.querySelector('.login-card').style.animation = 'fadeInScale .5s ease';
    });
    window.scrollTo(0, 0);
  } else {
    login.style.display = 'none';
    landing.style.display = 'block';
    window.scrollTo(0, 0);
  }
}

/* ═══════ LOGIN HANDLING ═══════ */
function handleLogin(e) {
  e.preventDefault();
  const btn = document.getElementById('loginSubmitBtn');
  btn.textContent = 'Signing in...';
  btn.style.opacity = '0.7';
  btn.disabled = true;
  setTimeout(() => { window.location.href = '/dashboard'; }, 800);
}
function togglePassword() {
  const pw = document.getElementById('loginPassword'), icon = document.getElementById('pwIcon');
  if (pw.type === 'password') { pw.type = 'text'; icon.textContent = 'visibility_off'; }
  else { pw.type = 'password'; icon.textContent = 'visibility'; }
}
function handleSocialLogin(provider) { window.location.href = '/dashboard'; }

/* ═══════ SMOOTH SCROLL ═══════ */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});
</script>
</body>
</html>"""
