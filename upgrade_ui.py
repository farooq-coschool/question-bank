#!/usr/bin/env python3
"""Replace the CSS block in question_bank_generator_4.html with an upgraded UI."""

NEW_CSS = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --bg:        #080a10;
    --surface:   #0e1118;
    --surface2:  #141820;
    --surface3:  #1c2130;
    --border:    #232b3d;
    --border2:   #2e3a52;

    --accent:    #4f8cff;
    --accent2:   #8b5cf6;
    --accent3:   #06d6b0;
    --warn:      #f59e0b;
    --danger:    #f43f5e;
    --success:   #10d9a0;

    --text:      #e2e8f8;
    --text2:     #7f8ea8;
    --text3:     #3d4d66;

    --glow-blue: rgba(79,140,255,0.25);
    --glow-purple: rgba(139,92,246,0.25);
    --glow-green: rgba(16,217,160,0.2);

    --radius:    14px;
    --radius-sm: 9px;
    --radius-xs: 6px;

    --ease: cubic-bezier(.4,0,.2,1);
    --spring: cubic-bezier(.34,1.56,.64,1);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  /* ── TOPBAR ─────────────────────────────────────────── */
  .app { display: flex; flex-direction: column; min-height: 100vh; }

  .topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 32px;
    background: rgba(14,17,24,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
  }
  .logo { display: flex; align-items: center; gap: 12px; }
  .logo-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 18px var(--glow-blue);
  }
  .logo-text { font-size: 17px; font-weight: 700; letter-spacing: -0.4px; }
  .logo-sub  { font-size: 11.5px; color: var(--text2); font-weight: 400; }
  .api-status { display: flex; align-items: center; gap: 8px; }
  .api-badge {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px;
    background: var(--surface2); border: 1px solid var(--border);
    font-size: 13px; color: var(--text2);
    cursor: pointer; transition: all .2s var(--ease);
  }
  .api-badge:hover { border-color: var(--accent); color: var(--text); box-shadow: 0 0 12px var(--glow-blue); }
  .api-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--text3); }
  .api-dot.active { background: var(--success); box-shadow: 0 0 10px var(--glow-green); animation: pulseDot 2s infinite; }
  @keyframes pulseDot { 0%,100%{box-shadow:0 0 10px var(--glow-green)} 50%{box-shadow:0 0 18px var(--success)} }

  /* ── MAIN LAYOUT ────────────────────────────────────── */
  .main { flex: 1; display: flex; }

  /* ── SIDEBAR ────────────────────────────────────────── */
  .sidebar {
    width: 256px; min-width: 256px;
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 28px 14px;
    display: flex; flex-direction: column; gap: 3px;
    position: sticky; top: 67px; height: calc(100vh - 67px);
    overflow-y: auto;
  }
  .sidebar-title {
    font-size: 10.5px; font-weight: 700; color: var(--text3);
    text-transform: uppercase; letter-spacing: 1.2px;
    padding: 4px 14px 14px;
  }
  .step-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: var(--radius-sm);
    cursor: pointer; transition: all .2s var(--ease);
    color: var(--text2); font-size: 13.5px; font-weight: 500;
    position: relative; overflow: hidden;
  }
  .step-item::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(90deg, var(--glow-blue), transparent);
    opacity: 0; transition: opacity .2s;
  }
  .step-item:hover { background: var(--surface2); color: var(--text); }
  .step-item:hover::before { opacity: 1; }
  .step-item.active {
    background: rgba(79,140,255,0.1);
    color: var(--accent);
    border: 1px solid rgba(79,140,255,0.25);
    box-shadow: inset 0 0 20px rgba(79,140,255,0.06);
  }
  .step-item.active::before { opacity: 1; }
  .step-item.completed { color: var(--success); }
  .step-item.completed:hover { background: rgba(16,217,160,0.07); }
  .step-item.disabled { opacity: 0.35; pointer-events: none; }
  .step-num {
    width: 23px; height: 23px; border-radius: 50%; flex-shrink: 0;
    border: 1.5px solid currentColor;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
    transition: all .2s;
  }
  .step-item.active .step-num { background: var(--accent); border-color: var(--accent); color: #fff; box-shadow: 0 0 12px var(--glow-blue); }
  .step-item.completed .step-num { background: var(--success); border-color: var(--success); color: #000; box-shadow: 0 0 10px var(--glow-green); }

  /* ── CONTENT AREA ───────────────────────────────────── */
  .content { flex: 1; padding: 36px 40px; overflow-y: auto; max-width: 940px; }

  /* ── CARDS ──────────────────────────────────────────── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 30px;
    margin-bottom: 20px;
    position: relative; overflow: hidden;
    transition: border-color .25s var(--ease), box-shadow .25s var(--ease);
  }
  .card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0; transition: opacity .3s;
  }
  .card:hover { border-color: var(--border2); box-shadow: 0 8px 40px rgba(0,0,0,0.35); }
  .card:hover::before { opacity: 0.6; }

  .card-title { font-size: 18px; font-weight: 700; margin-bottom: 6px; letter-spacing: -0.3px; }
  .card-sub   { font-size: 13.5px; color: var(--text2); margin-bottom: 26px; }

  /* ── FORM ELEMENTS ──────────────────────────────────── */
  .form-row        { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
  .form-row.single { grid-template-columns: 1fr; }
  .form-row.triple { grid-template-columns: 1fr 1fr 1fr; }
  .form-group      { display: flex; flex-direction: column; gap: 6px; }

  label          { font-size: 12.5px; font-weight: 600; color: var(--text2); letter-spacing: 0.1px; }
  label .req     { color: var(--danger); margin-left: 2px; }

  input[type="text"], input[type="number"], select, textarea {
    background: var(--surface2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    color: var(--text);
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    outline: none;
    transition: border-color .2s var(--ease), box-shadow .2s var(--ease), background .2s;
    width: 100%;
  }
  input:hover, select:hover, textarea:hover { border-color: var(--border2); }
  input:focus, select:focus, textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(79,140,255,0.12);
    background: var(--surface3);
  }
  textarea { resize: vertical; min-height: 80px; }
  select option { background: var(--surface2); }

  /* ── SUBJECT GRID ───────────────────────────────────── */
  .subject-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
    gap: 10px; margin-bottom: 16px;
  }
  .subject-card {
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px;
    cursor: pointer;
    transition: all .22s var(--ease);
    display: flex; flex-direction: column; gap: 6px;
    background: var(--surface2);
    position: relative; overflow: hidden;
  }
  .subject-card::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, var(--glow-blue), transparent);
    opacity: 0; transition: opacity .25s;
  }
  .subject-card:hover {
    border-color: var(--accent);
    background: rgba(79,140,255,0.07);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(79,140,255,0.12);
  }
  .subject-card:hover::after { opacity: 1; }
  .subject-card.selected {
    border-color: var(--accent);
    background: rgba(79,140,255,0.12);
    box-shadow: 0 0 0 3px rgba(79,140,255,0.15), 0 8px 24px rgba(79,140,255,0.15);
    transform: translateY(-2px);
  }
  .subject-card.selected::after { opacity: 1; }
  .subject-card.disabled { opacity: 0.3; pointer-events: none; }
  .subject-icon { font-size: 24px; z-index: 1; position: relative; }
  .subject-name { font-size: 13px; font-weight: 700; z-index: 1; position: relative; }
  .subject-tag  { font-size: 11px; color: var(--text2); z-index: 1; position: relative; }

  /* ── CURRICULUM PILLS ───────────────────────────────── */
  .pill-group { display: flex; gap: 8px; flex-wrap: wrap; }
  .pill {
    padding: 8px 20px; border-radius: 22px;
    border: 1.5px solid var(--border);
    font-size: 13px; font-weight: 600;
    cursor: pointer; transition: all .2s var(--ease);
    background: var(--surface2); color: var(--text2);
    letter-spacing: 0.1px;
  }
  .pill:hover {
    border-color: var(--accent); color: var(--text);
    box-shadow: 0 0 14px var(--glow-blue);
    transform: translateY(-1px);
  }
  .pill.selected {
    border-color: var(--accent);
    background: linear-gradient(135deg, rgba(79,140,255,0.2), rgba(139,92,246,0.15));
    color: var(--accent);
    box-shadow: 0 0 18px var(--glow-blue);
  }
  .pill.disabled { opacity: 0.3; pointer-events: none; }

  /* ── BUTTONS ────────────────────────────────────────── */
  .btn {
    padding: 10px 22px; border-radius: var(--radius-sm);
    border: none; cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-size: 13.5px; font-weight: 600;
    transition: all .22s var(--spring);
    display: inline-flex; align-items: center; gap: 8px;
    position: relative; overflow: hidden; letter-spacing: 0.1px;
  }
  .btn::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(rgba(255,255,255,0.07), rgba(255,255,255,0));
    opacity: 0; transition: opacity .2s;
    border-radius: inherit;
  }
  .btn:hover::after { opacity: 1; }

  .btn-primary {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #fff;
    box-shadow: 0 4px 18px rgba(79,140,255,0.3);
  }
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(79,140,255,0.45);
    filter: brightness(1.08);
  }
  .btn-primary:active { transform: translateY(0); box-shadow: 0 3px 12px rgba(79,140,255,0.3); }
  .btn-primary:disabled { opacity: 0.45; pointer-events: none; box-shadow: none; }

  .btn-secondary {
    background: var(--surface2);
    border: 1.5px solid var(--border2);
    color: var(--text);
  }
  .btn-secondary:hover {
    border-color: var(--accent); color: var(--accent);
    box-shadow: 0 4px 16px var(--glow-blue);
    transform: translateY(-1px);
  }

  .btn-success {
    background: rgba(16,217,160,0.12);
    border: 1.5px solid rgba(16,217,160,0.4);
    color: var(--success);
  }
  .btn-success:hover {
    background: rgba(16,217,160,0.2);
    box-shadow: 0 4px 16px var(--glow-green);
    transform: translateY(-1px);
  }

  .btn-danger {
    background: rgba(244,63,94,0.1);
    border: 1.5px solid rgba(244,63,94,0.35);
    color: var(--danger);
  }
  .btn-danger:hover {
    background: rgba(244,63,94,0.18);
    box-shadow: 0 4px 16px rgba(244,63,94,0.25);
    transform: translateY(-1px);
  }

  .btn-sm  { padding: 6px 14px; font-size: 12.5px; }
  .btn-lg  { padding: 13px 30px; font-size: 15px; border-radius: 10px; }
  .btn-row { display: flex; gap: 10px; align-items: center; margin-top: 26px; flex-wrap: wrap; }

  /* ── INFO BOXES ─────────────────────────────────────── */
  .info-box {
    background: rgba(79,140,255,0.07);
    border: 1px solid rgba(79,140,255,0.22);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-sm);
    padding: 14px 16px;
    font-size: 13px; color: var(--text2);
    margin-bottom: 16px;
    display: flex; gap: 10px;
  }
  .info-box.warn    { background: rgba(245,158,11,0.07); border-color: rgba(245,158,11,0.22); border-left-color: var(--warn); }
  .info-box.success { background: rgba(16,217,160,0.07); border-color: rgba(16,217,160,0.22); border-left-color: var(--success); color: var(--success); }

  /* ── CHAPTER STRUCTURE PREVIEW ──────────────────────── */
  .struct-preview {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px; max-height: 320px;
    overflow-y: auto; white-space: pre-wrap;
    word-break: break-word; color: var(--text); line-height: 1.8;
  }
  .struct-ch { color: var(--accent); font-weight: 700; }
  .struct-st { color: var(--success); padding-left: 18px; }
  .struct-nc { color: var(--warn); padding-left: 36px; }

  /* ── COUNTS TABLE ───────────────────────────────────── */
  .counts-table { width: 100%; border-collapse: collapse; font-size: 13.5px; margin-top: 8px; }
  .counts-table th {
    text-align: left; padding: 9px 14px;
    background: var(--surface3); color: var(--text2);
    font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px;
    border-bottom: 1px solid var(--border);
  }
  .counts-table td { padding: 9px 14px; border-bottom: 1px solid var(--border); }
  .counts-table tr:last-child td { border-bottom: none; }
  .counts-table tr:hover td { background: var(--surface3); }
  .counts-table input[type="number"] { width: 72px; padding: 5px 9px; font-size: 13px; }

  .level-badge { display: inline-flex; align-items: center; padding: 3px 9px; border-radius: 5px; font-size: 11px; font-weight: 700; letter-spacing: 0.2px; }
  .level-factual       { background: rgba(79,140,255,0.15); color: var(--accent); }
  .level-understanding { background: rgba(16,217,160,0.12); color: var(--success); }
  .level-application   { background: rgba(139,92,246,0.15); color: #a78bfa; }
  .diff-easy   { color: #68d391; }
  .diff-medium { color: var(--warn); }
  .diff-hard   { color: var(--danger); }

  /* ── PROGRESS TRACK ─────────────────────────────────── */
  .progress-track { margin: 24px 0; }
  .progress-step {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 13px 0; border-bottom: 1px solid var(--border);
    transition: background .15s;
  }
  .progress-step:last-child { border-bottom: none; }
  .p-icon {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; margin-top: 1px;
  }
  .p-icon.pending  { background: var(--surface3); color: var(--text3); }
  .p-icon.running  { background: rgba(79,140,255,0.18); color: var(--accent); animation: spinPulse 1.4s infinite; box-shadow: 0 0 14px var(--glow-blue); }
  .p-icon.done     { background: rgba(16,217,160,0.18); color: var(--success); box-shadow: 0 0 12px var(--glow-green); }
  .p-icon.skipped  { background: var(--surface3); color: var(--text3); }
  .p-icon.error    { background: rgba(244,63,94,0.18); color: var(--danger); }
  @keyframes spinPulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.6;transform:scale(0.92)} }

  .p-info  { flex: 1; }
  .p-name  { font-size: 13.5px; font-weight: 600; }
  .p-status{ font-size: 12px; color: var(--text2); margin-top: 2px; }
  .p-log {
    font-family: 'JetBrains Mono', monospace; font-size: 11.5px;
    color: var(--text2); background: var(--surface2);
    border-radius: 6px; padding: 9px 13px; margin-top: 8px;
    max-height: 90px; overflow-y: auto; white-space: pre-wrap;
    border: 1px solid var(--border);
  }

  /* ── OUTPUT / FILE TREE ─────────────────────────────── */
  .output-section { margin-top: 26px; }
  .output-section h3 { font-size: 14px; font-weight: 700; margin-bottom: 12px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }
  .file-tree {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 18px;
    font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
    line-height: 1.9;
  }
  .ft-folder { color: var(--accent); }
  .ft-json   { color: var(--warn); }
  .ft-txt    { color: var(--success); }

  .download-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin-top: 12px; }
  .dl-card {
    background: var(--surface2); border: 1.5px solid var(--border);
    border-radius: var(--radius-sm); padding: 14px;
    display: flex; flex-direction: column; gap: 8px;
    transition: all .2s var(--ease);
    cursor: default;
  }
  .dl-card:hover { border-color: var(--border2); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
  .dl-name { font-size: 13px; font-weight: 600; word-break: break-all; }
  .dl-size { font-size: 11px; color: var(--text2); }

  /* ── MODAL ──────────────────────────────────────────── */
  .modal-overlay {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.75); backdrop-filter: blur(8px);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000; padding: 20px;
  }
  .modal-overlay.hidden { display: none; }
  .modal {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 18px; padding: 36px;
    width: 100%; max-width: 480px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
    animation: modalIn .2s var(--spring);
  }
  @keyframes modalIn { from{opacity:0;transform:scale(.95) translateY(12px)} to{opacity:1;transform:none} }
  .modal h2 { font-size: 20px; margin-bottom: 8px; font-weight: 700; }
  .modal p  { font-size: 14px; color: var(--text2); margin-bottom: 22px; }
  .modal input { margin-bottom: 16px; font-family: 'JetBrains Mono', monospace; font-size: 13px; }

  /* ── PAGE SECTIONS ──────────────────────────────────── */
  .page { display: none; }
  .page.active { display: block; }

  /* ── TOGGLE ─────────────────────────────────────────── */
  .toggle-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
  .toggle {
    width: 42px; height: 24px; border-radius: 12px;
    background: var(--surface3); border: 1.5px solid var(--border);
    cursor: pointer; position: relative; transition: all .25s var(--ease);
  }
  .toggle.on { background: var(--accent); border-color: var(--accent); box-shadow: 0 0 12px var(--glow-blue); }
  .toggle::after {
    content: ''; position: absolute; top: 2px; left: 2px;
    width: 16px; height: 16px; border-radius: 50%;
    background: white; transition: left .2s var(--spring);
    box-shadow: 0 1px 4px rgba(0,0,0,0.35);
  }
  .toggle.on::after { left: 22px; }
  .toggle-label { font-size: 13px; font-weight: 500; }

  /* ── STAT BOXES ─────────────────────────────────────── */
  .stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 22px; }
  .stat-box {
    flex: 1; min-width: 120px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 16px;
    text-align: center;
    transition: all .2s var(--ease);
  }
  .stat-box:hover { border-color: var(--border2); box-shadow: 0 4px 20px rgba(0,0,0,0.25); }
  .stat-num { font-size: 30px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--accent); line-height: 1; }
  .stat-lbl { font-size: 11.5px; color: var(--text2); margin-top: 4px; font-weight: 500; }

  /* ── IMAGE UPLOAD ───────────────────────────────────── */
  .img-upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 36px 24px; text-align: center;
    cursor: pointer; transition: all .2s var(--ease);
    background: var(--surface2); position: relative;
  }
  .img-upload-area:hover { border-color: var(--accent); background: rgba(79,140,255,0.05); box-shadow: 0 0 24px var(--glow-blue); }
  .img-upload-area.drag-over { border-color: var(--success); background: rgba(16,217,160,0.06); box-shadow: 0 0 24px var(--glow-green); }
  .img-upload-icon { font-size: 42px; margin-bottom: 10px; }
  .img-upload-text { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 5px; }
  .img-upload-sub  { font-size: 12px; color: var(--text2); }

  /* ── TAGS / BADGES ──────────────────────────────────── */
  .tag { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px; border-radius: 5px; font-size: 11px; font-weight: 700; }
  .tag-icse { background: rgba(79,140,255,0.14); color: var(--accent); }
  .tag-cbse { background: rgba(16,217,160,0.12); color: var(--success); }

  /* ── MISC ───────────────────────────────────────────── */
  .error-msg      { color: var(--danger); font-size: 12px; margin-top: 4px; font-weight: 500; }
  .section-divider{ height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 22px 0; }

  .loading-dots::after { content: ''; animation: dots 1.5s infinite; }
  @keyframes dots { 0%{content:''}33%{content:'.'}66%{content:'..'}100%{content:'...'} }

  /* ── SCROLLBAR ──────────────────────────────────────── */
  ::-webkit-scrollbar { width: 5px; height: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--text3); }

  /* ── RESPONSIVE ─────────────────────────────────────── */
  @media (max-width: 768px) {
    .sidebar { display: none; }
    .content { padding: 20px 16px; }
    .topbar  { padding: 12px 16px; }
    .form-row, .form-row.triple { grid-template-columns: 1fr; }
  }
</style>"""

OLD_STYLE_START = '<style>\n  @import url(\'https://fonts.googleapis.com/css2?family=DM+Sans'
OLD_STYLE_END   = '</style>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip'

with open('question_bank_generator_4.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find(OLD_STYLE_START)
assert start != -1, "Could not find <style> block start"
end = html.find(OLD_STYLE_END, start)
assert end != -1, "Could not find </style> end"
end_pos = end + len('</style>')

html = html[:start] + NEW_CSS + '\n' + html[end_pos:]

# Also update font references in inline styles that use DM Sans / DM Mono
html = html.replace("font-family: 'DM Sans', sans-serif", "font-family: 'Inter', sans-serif")
html = html.replace("font-family: 'DM Mono', monospace", "font-family: 'JetBrains Mono', monospace")
html = html.replace("'DM Sans'", "'Inter'")
html = html.replace("'DM Mono'", "'JetBrains Mono'")

with open('question_bank_generator_4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("UI upgrade applied successfully.")
