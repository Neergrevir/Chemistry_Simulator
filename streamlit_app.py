import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="화학 평형 시뮬레이터",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .stApp { background: #f4f8fb; }
      [data-testid="stHeader"] { display:none; }
      [data-testid="stToolbar"] { display:none; }
      [data-testid="stDecoration"] { display:none; }
      .block-container {
        padding-top: 0.25rem !important;
        padding-bottom: 0 !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 100% !important;
      }
      iframe { border-radius: 22px; }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>화학 평형 시뮬레이터</title>
<style>
  :root{
    --bg1:#f7fbfd;
    --bg2:#f4f2ff;
    --ink:#263248;
    --muted:#6b7890;
    --line:#dbe5ef;
    --card:rgba(255,255,255,.88);
    --blue:#8fc5ff;
    --blue2:#4b9cf5;
    --pink:#ff7f9c;
    --red:#df4a37;
    --orange:#f07a24;
    --yellow:#f7d64d;
    --green:#36b37e;
    --shadow:0 20px 45px rgba(38,50,72,.10);
  }
  *{ box-sizing:border-box; }
  html,body{ margin:0; height:100%; overflow:hidden; font-family: Pretendard, "Noto Sans KR", system-ui, -apple-system, Segoe UI, sans-serif; color:var(--ink); }
  body{
    background:
      radial-gradient(circle at 12% 4%, rgba(255,236,214,.80), transparent 28%),
      radial-gradient(circle at 80% 12%, rgba(220,245,255,.90), transparent 30%),
      linear-gradient(135deg,var(--bg1),var(--bg2));
  }
  .app{
    height:900px;
    min-height:900px;
    padding:18px 22px 22px;
    display:grid;
    grid-template-rows:74px 1fr;
    gap:14px;
  }
  .topbar{
    display:grid;
    grid-template-columns: 330px 1fr;
    gap:18px;
    align-items:stretch;
  }
  .title-card,.selector-card,.panel{
    background:var(--card);
    border:1px solid rgba(210,222,234,.82);
    border-radius:24px;
    box-shadow:var(--shadow);
    backdrop-filter: blur(12px);
  }
  .title-card{
    padding:16px 22px;
    display:flex;
    align-items:center;
    gap:14px;
  }
  .flask{ font-size:28px; filter: drop-shadow(0 4px 4px rgba(63,120,190,.18)); }
  h1{ margin:0; font-size:26px; letter-spacing:-.04em; line-height:1; }
  .subtitle{ margin-top:6px; font-size:13px; color:var(--muted); }
  .selector-card{
    padding:12px 16px;
    display:grid;
    grid-template-columns: 120px 1fr;
    gap:12px;
    align-items:center;
  }
  .label{ font-weight:800; font-size:14px; color:#43506a; }
  select, input[type="range"]{ width:100%; }
  select{
    height:42px;
    border:1px solid #d6e2ec;
    border-radius:12px;
    padding:0 12px;
    font-weight:800;
    background:#202431;
    color:#fff;
    outline:none;
  }
  .main{
    min-height:0;
    display:grid;
    grid-template-columns: 330px minmax(560px,1.2fr) minmax(500px,.95fr);
    gap:18px;
  }
  .panel{ min-height:0; padding:18px; overflow:hidden; }
  .left-panel{ display:flex; flex-direction:column; gap:12px; }
  .center-panel{ display:grid; grid-template-rows: 42px 1fr 110px; gap:10px; }
  .right-panel{ display:grid; grid-template-rows: 180px 185px 185px 1fr; gap:10px; }
  h2,h3{ margin:0; letter-spacing:-.035em; }
  h2{ font-size:22px; }
  h3{ font-size:16px; }
  .section-title{ font-weight:900; font-size:17px; margin-bottom:8px; }
  .reaction-box{
    border:1px solid #d9e4ee;
    border-radius:16px;
    padding:12px 14px;
    background:rgba(255,255,255,.72);
    font-weight:900;
    letter-spacing:-.02em;
  }
  .control-group{ padding:12px 0; border-bottom:1px solid #e1e9f1; }
  .control-group:last-child{ border-bottom:0; }
  .radio-row{ display:flex; align-items:flex-start; gap:8px; margin:8px 0; color:#334057; font-weight:700; font-size:14px; }
  .radio-row input{ accent-color:#ff596d; margin-top:3px; }
  .range-head{ display:flex; justify-content:space-between; align-items:baseline; margin:10px 0 3px; font-size:13px; }
  .range-value{ color:#f24b63; font-weight:900; }
  input[type="range"]{ accent-color:#ff596d; }
  .button-row{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-top:10px; }
  button{
    border:0;
    height:36px;
    border-radius:10px;
    background:#202431;
    color:#fff;
    font-weight:900;
    cursor:pointer;
    transition:.15s transform ease, .15s opacity ease;
  }
  button:hover{ transform:translateY(-1px); opacity:.9; }
  .ghost{ background:#edf4fb; color:#2f3c54; border:1px solid #d5e2ee; }
  .soft-note{ font-size:12px; line-height:1.55; color:#7d899d; }
  .legend{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
  .chip{
    display:inline-flex;
    align-items:center;
    gap:6px;
    padding:6px 10px;
    border-radius:999px;
    background:#eff6ff;
    color:#4b5c75;
    border:1px solid #dceaf8;
    font-size:12px;
    font-weight:800;
  }
  .dot{ width:8px; height:8px; border-radius:99px; display:inline-block; }
  .canvas-wrap{
    position:relative;
    border:1px solid #dce7f1;
    border-radius:24px;
    background:linear-gradient(145deg,rgba(253,254,255,.92),rgba(239,248,253,.82));
    overflow:hidden;
    min-height:0;
  }
  #simCanvas{ width:100%; height:100%; display:block; }
  .experiment-badge{
    position:absolute;
    left:22px;
    bottom:16px;
    display:flex;
    gap:8px;
    flex-wrap:wrap;
  }
  .badge{
    padding:8px 13px;
    border-radius:999px;
    background:rgba(255,255,255,.68);
    border:1px solid #d8e5ef;
    box-shadow:0 8px 22px rgba(43,66,94,.10);
    font-weight:900;
    color:#526073;
  }
  .status-card{
    border:1px solid #dce7f1;
    border-radius:18px;
    background:rgba(255,255,255,.74);
    padding:12px 14px;
    display:grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap:10px;
  }
  .metric-label{ color:#6e7a8e; font-size:12px; font-weight:800; }
  .metric-value{ font-size:21px; font-weight:950; margin-top:4px; letter-spacing:-.03em; }
  .result-summary{
    border:1px solid #dce7f1;
    border-radius:18px;
    background:rgba(255,255,255,.72);
    padding:13px 14px;
    display:grid;
    grid-template-columns: 1.05fr .95fr;
    gap:12px;
  }
  .pill{
    display:inline-block;
    padding:7px 11px;
    border-radius:999px;
    background:#e7f3ff;
    color:#1964a3;
    border:1px solid #c9e4fb;
    font-weight:900;
    margin:4px 4px 0 0;
    font-size:13px;
  }
  .formula{
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    white-space:pre-line;
    font-size:12px;
    line-height:1.55;
    color:#31405a;
    background:#f7f9fc;
    border-radius:14px;
    padding:11px 12px;
  }
  .chart-card{
    border:1px solid #dce7f1;
    border-radius:18px;
    background:rgba(255,255,255,.74);
    padding:12px;
    min-height:0;
  }
  .chart-title{ font-weight:950; font-size:14px; margin-bottom:5px; color:#2f3c54; }
  canvas.chart{ width:100%; height:126px; display:block; }
  .table-card{
    border:1px solid #dce7f1;
    border-radius:18px;
    background:rgba(255,255,255,.74);
    overflow:hidden;
    min-height:0;
  }
  table{ border-collapse:collapse; width:100%; font-size:12px; }
  th,td{ border-bottom:1px solid #e4edf5; padding:8px 10px; text-align:right; }
  th:first-child,td:first-child{ text-align:left; }
  th{ background:#f3f7fb; color:#526073; }
  .table-title{ font-weight:950; padding:10px 12px 4px; font-size:14px; }
  .hidden{ display:none !important; }
  .toggle-row{ display:flex; gap:10px; align-items:center; margin-top:6px; font-size:13px; font-weight:800; color:#556277; }
  .toggle-row input{ accent-color:#4b9cf5; }
  @media (max-width: 1300px){
    html,body{ overflow:auto; }
    .app{ height:auto; min-height:900px; }
    .main{ grid-template-columns: 310px minmax(520px,1fr); }
    .right-panel{ grid-column:1 / -1; grid-template-columns:1fr 1fr; grid-template-rows:auto auto; }
    .table-card{ grid-column:1 / -1; }
  }
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="title-card">
      <div class="flask">⚗️</div>
      <div>
        <h1>화학 평형 시뮬레이터</h1>
        <div class="subtitle">조건 변화에 따른 평형 이동, 색 변화, 속도 변화를 실시간으로 관찰합니다.</div>
      </div>
    </div>
    <div class="selector-card">
      <div class="label">실험 선택</div>
      <select id="reactionSelect">
        <option value="no2">이산화질소 ↔ 사산화이질소  |  2NO₂(g) ⇌ N₂O₄(g)</option>
        <option value="dichromate">다이크로메이트 ↔ 크로메이트  |  Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)</option>
      </select>
    </div>
  </div>

  <div class="main">
    <div class="panel left-panel">
      <h2>조건 변화</h2>
      <div class="reaction-box" id="leftReaction">2NO₂(g) ⇌ N₂O₄(g)</div>

      <div class="control-group" id="vesselGroup">
        <div class="section-title">용기</div>
        <label class="radio-row"><input type="radio" name="vessel" value="piston" checked> 외부 대기압과 일정하게 압력을 유지할 수 있는 피스톤 실린더</label>
        <label class="radio-row"><input type="radio" name="vessel" value="steel"> 부피가 일정한 강철용기</label>
      </div>

      <div class="control-group">
        <div class="range-head"><b>온도 조건 변화 (℃)</b><span class="range-value" id="tempValue">43</span></div>
        <input id="tempSlider" type="range" min="0" max="120" step="1" value="43">
        <div class="range-head"><b>압력 조건 변화 (atm)</b><span class="range-value" id="pressureValue">1.00</span></div>
        <input id="pressureSlider" type="range" min="0.35" max="3.00" step="0.01" value="1.00">
        <div class="range-head"><b>용기 기준 부피 (L)</b><span class="range-value" id="volumeValue">2.50</span></div>
        <input id="volumeSlider" type="range" min="0.80" max="3.40" step="0.01" value="2.50">
      </div>

      <div class="control-group">
        <div class="section-title">농도 / 물질 첨가·제거</div>
        <div class="label" style="margin-bottom:6px">대상 물질</div>
        <select id="substanceSelect"></select>
        <div class="range-head"><b>조작량 (상대값)</b><span class="range-value" id="amountValue">0.30</span></div>
        <input id="amountSlider" type="range" min="0.05" max="1.50" step="0.05" value="0.30">
        <div class="button-row">
          <button id="addBtn">첨가</button>
          <button id="removeBtn">제거</button>
          <button id="resetBtn" class="ghost">초기화</button>
        </div>
      </div>

      <div class="control-group">
        <div class="section-title">시각화 옵션</div>
        <label class="toggle-row"><input type="checkbox" id="motionToggle" checked> 분자 무작위 운동 애니메이션</label>
        <label class="toggle-row"><input type="checkbox" id="exaggerateToggle" checked> 변화 과장 표시</label>
        <p class="soft-note">교육용 시뮬레이션이라 실제 실험값과 완전히 같지는 않으며, 평형 이동과 색 변화가 잘 보이도록 시각 효과를 강화했습니다.</p>
      </div>
    </div>

    <div class="panel center-panel">
      <div>
        <h2 id="centerTitle">2NO₂(g) ⇌ N₂O₄(g)</h2>
        <div class="legend" id="legendRow"></div>
      </div>
      <div class="canvas-wrap">
        <canvas id="simCanvas"></canvas>
        <div class="experiment-badge" id="badgeRow">
          <span class="badge" id="badgePressure">1.00 atm</span>
          <span class="badge" id="badgeVolume">2.50 L</span>
          <span class="badge" id="badgeTemp">43℃</span>
        </div>
      </div>
      <div class="status-card">
        <div><div class="metric-label">주요 관찰</div><div class="metric-value" id="obsMetric">적갈색 진해짐</div></div>
        <div><div class="metric-label">분자 운동 속도</div><div class="metric-value" id="speedMetric">보통</div></div>
        <div><div class="metric-label">시각 색 변화</div><div class="metric-value" id="colorMetric">뚜렷함</div></div>
      </div>
    </div>

    <div class="panel right-panel">
      <div class="result-summary">
        <div>
          <h2>실험 결과</h2>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:10px">
            <div><div class="metric-label">평형상수 K</div><div class="metric-value" id="kMetric">4.24</div></div>
            <div><div class="metric-label">반응지수 Q</div><div class="metric-value" id="qMetric">3.68</div></div>
            <div><div class="metric-label">평형 이동</div><div class="metric-value" id="moveMetric">정반응</div></div>
            <div><div class="metric-label">현재 부피</div><div class="metric-value" id="volMetric">2.50 L</div></div>
          </div>
        </div>
        <div>
          <div id="explainPills">
            <span class="pill">Q &lt; K → 생성물 쪽 이동</span>
            <span class="pill">온도 상승 → NO₂ 증가</span>
          </div>
          <div class="formula" id="formulaBox" style="margin-top:10px"></div>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-title">Q와 K의 실시간 변화</div>
        <canvas class="chart" id="qkChart"></canvas>
      </div>
      <div class="chart-card">
        <div class="chart-title">정반응 속도와 역반응 속도</div>
        <canvas class="chart" id="rateChart"></canvas>
      </div>
      <div class="table-card">
        <div class="table-title">평형 농도 표</div>
        <table>
          <thead><tr><th>물질</th><th>현재</th><th>평형</th><th>농도</th></tr></thead>
          <tbody id="resultTable"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  const $ = (id)=>document.getElementById(id);
  const simCanvas = $('simCanvas');
  const ctx = simCanvas.getContext('2d');
  const qkCanvas = $('qkChart');
  const qkCtx = qkCanvas.getContext('2d');
  const rateCanvas = $('rateChart');
  const rateCtx = rateCanvas.getContext('2d');

  const state = {
    reaction:'no2', vessel:'piston', temp:43, pressure:1, baseVolume:2.5, amount:.3,
    no2:.80, n2o4:2.22,
    acid:.25, base:.15, water:1.00,
    motion:true, exaggerate:true,
    molecules:[],
    smooth:{K:4.24,Q:3.68,F:.38,R:.42, no2Frac:.42, chromateFrac:.50},
    targets:{K:4.24,Q:3.68,F:.38,R:.42, no2Frac:.42, chromateFrac:.50},
    history:[], lastHistory:0, t0:performance.now()
  };

  function setupCanvas(c){
    const rect = c.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    c.width = Math.max(2, Math.floor(rect.width*dpr));
    c.height = Math.max(2, Math.floor(rect.height*dpr));
    const context = c.getContext('2d');
    context.setTransform(dpr,0,0,dpr,0,0);
  }
  function resizeAll(){ setupCanvas(simCanvas); setupCanvas(qkCanvas); setupCanvas(rateCanvas); fitMolecules(); }
  window.addEventListener('resize', resizeAll);

  function fmt(n, d=2){ return Number(n).toFixed(d); }
  function clamp(x,a,b){ return Math.max(a, Math.min(b,x)); }
  function mix(a,b,t){ return a + (b-a)*t; }
  function sigmoid(x){ return 1/(1+Math.exp(-x)); }

  function actualVolume(){
    if(state.reaction==='dichromate') return state.baseVolume;
    if(state.vessel==='piston') return clamp(state.baseVolume / Math.sqrt(state.pressure), .72, 3.6);
    return state.baseVolume;
  }

  function solveNo2Equilibrium(K,V,no2,n2o4){
    no2 = Math.max(.02,no2); n2o4 = Math.max(.02,n2o4);
    const f = (x)=> ((n2o4+x)*V)/Math.pow(no2-2*x,2) - K;
    let lo = -n2o4 + .0001, hi = no2/2 - .0001;
    for(let i=0;i<80;i++){
      let mid = (lo+hi)/2;
      if(f(mid)>0) hi=mid; else lo=mid;
    }
    const x=(lo+hi)/2;
    return {no2:no2-2*x, n2o4:n2o4+x};
  }

  function computeTargets(){
    const V = actualVolume();
    if(state.reaction==='no2'){
      const tempEffect = Math.exp(-(state.temp-35)*0.045);
      const K = clamp(4.2 * tempEffect, .18, 38);
      const Q = clamp((Math.max(.02,state.n2o4)*V)/Math.pow(Math.max(.02,state.no2),2), .02, 90);
      const eq = solveNo2Equilibrium(K,V,state.no2,state.n2o4);
      const eqTotalUnits = eq.no2 + 2*eq.n2o4;
      let no2Frac = eq.no2 / Math.max(.01, eqTotalUnits);
      if(state.exaggerate) no2Frac = clamp(Math.pow(no2Frac, .55)*1.25, .04, .96);
      const F = clamp(.08 * Math.pow(Math.max(.02,state.no2)/V,2) * (1 + state.temp/75), .01, 4.5);
      const R = clamp(.18 * Math.max(.02,state.n2o4)/V * (1 + state.temp/120), .01, 4.5);
      state.targets={K,Q,F,R,no2Frac, chromateFrac:0};
      return {...state.targets, eq, V};
    }else{
      const acidStrength = clamp(state.acid - state.base*.85, -1.2, 1.8);
      const pH = clamp(7.2 + state.base*2.8 + (state.water-1)*.55 - state.acid*3.0, 1, 13);
      const tempNudge = (state.temp-25)/200;
      let chromateFrac = sigmoid((pH-6.7)*1.25 + tempNudge);
      if(state.exaggerate) chromateFrac = clamp(sigmoid((pH-6.7)*2.2 + tempNudge*2), .03, .97);
      const K = clamp(2.2 + (state.temp-25)*.012, .4, 7);
      const Q = clamp(K * (chromateFrac/(1.01-chromateFrac)) * (.82 + Math.max(0,acidStrength)*.24), .05, 25);
      const F = clamp(.12 + (1-chromateFrac)*.95 + state.temp/220, .02, 2.4);
      const R = clamp(.12 + chromateFrac*.95 + state.temp/240, .02, 2.4);
      state.targets={K,Q,F,R,no2Frac:0,chromateFrac};
      return {...state.targets, pH, V:state.baseVolume};
    }
  }

  function updateText(){
    const calc = computeTargets();
    $('tempValue').textContent = state.temp.toFixed(0);
    $('pressureValue').textContent = state.pressure.toFixed(2);
    $('volumeValue').textContent = state.baseVolume.toFixed(2);
    $('amountValue').textContent = state.amount.toFixed(2);
    $('badgeTemp').textContent = `${state.temp.toFixed(0)}℃`;
    $('badgePressure').textContent = state.reaction==='no2' ? `${state.pressure.toFixed(2)} atm` : `pH 약 ${calc.pH.toFixed(1)}`;
    $('badgeVolume').textContent = `${calc.V.toFixed(2)} L`;
    $('kMetric').textContent = fmt(state.smooth.K,2);
    $('qMetric').textContent = fmt(state.smooth.Q,2);
    $('volMetric').textContent = `${calc.V.toFixed(2)} L`;
    let move = '평형';
    if(state.smooth.Q < state.smooth.K*.96) move='정반응';
    if(state.smooth.Q > state.smooth.K*1.04) move='역반응';
    $('moveMetric').textContent = move;

    const speedWords = state.temp < 25 ? '느림' : state.temp < 70 ? '보통' : '빠름';
    $('speedMetric').textContent = speedWords;
    $('colorMetric').textContent = state.exaggerate ? '매우 뚜렷함' : '자연스러움';

    if(state.reaction==='no2'){
      $('leftReaction').innerHTML = '2NO₂(g) ⇌ N₂O₄(g)';
      $('centerTitle').innerHTML = '2NO₂(g) ⇌ N₂O₄(g)';
      $('vesselGroup').classList.remove('hidden');
      $('formulaBox').textContent = '2NO₂(g) ⇌ N₂O₄(g)\nK = [N₂O₄] / [NO₂]²\nQ = [N₂O₄]초기 / [NO₂]초기²';
      $('obsMetric').textContent = state.smooth.no2Frac>.58 ? '적갈색 진해짐' : state.smooth.no2Frac<.30 ? '색이 옅어짐' : '중간 색';
      $('explainPills').innerHTML = makePills([
        state.smooth.Q < state.smooth.K ? 'Q < K → 생성물 쪽 이동' : state.smooth.Q > state.smooth.K ? 'Q > K → 반응물 쪽 이동' : 'Q ≈ K → 평형 상태',
        state.temp > 50 ? '온도 상승 → NO₂ 증가' : '온도 하강 → N₂O₄ 증가',
        state.vessel==='piston' ? '피스톤이 압력 변화에 따라 이동' : '강철용기라 부피 일정'
      ]);
      const V=calc.V, eq=calc.eq;
      $('resultTable').innerHTML = `
        <tr><td>NO₂</td><td>${fmt(state.no2,3)}</td><td>${fmt(eq.no2,3)}</td><td>${fmt(eq.no2/V,3)} M</td></tr>
        <tr><td>N₂O₄</td><td>${fmt(state.n2o4,3)}</td><td>${fmt(eq.n2o4,3)}</td><td>${fmt(eq.n2o4/V,3)} M</td></tr>`;
      $('legendRow').innerHTML = '<span class="chip"><span class="dot" style="background:#d86528"></span>NO₂ 적갈색</span><span class="chip"><span class="dot" style="background:#c9d3dc;border:1px solid #758397"></span>N₂O₄ 무색</span>';
    }else{
      $('leftReaction').innerHTML = 'Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺';
      $('centerTitle').innerHTML = 'Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)';
      $('vesselGroup').classList.add('hidden');
      $('formulaBox').textContent = 'Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺\n산성: H⁺ 증가 → 왼쪽 이동\n염기성: H⁺ 감소 → 오른쪽 이동';
      $('obsMetric').textContent = state.smooth.chromateFrac>.60 ? '노란색 뚜렷함' : state.smooth.chromateFrac<.40 ? '주황색 뚜렷함' : '중간 색';
      $('explainPills').innerHTML = makePills([
        state.smooth.chromateFrac>.55 ? '염기성 → 크로메이트 증가' : '산성 → 다이크로메이트 증가',
        'HCl 첨가: H⁺ 증가',
        'NaOH 첨가: H⁺ 제거'
      ]);
      $('resultTable').innerHTML = `
        <tr><td>Cr₂O₇²⁻</td><td>${fmt(1-state.smooth.chromateFrac,3)}</td><td>${fmt(1-state.targets.chromateFrac,3)}</td><td>${fmt((1-state.targets.chromateFrac)/state.baseVolume,3)} M</td></tr>
        <tr><td>CrO₄²⁻</td><td>${fmt(state.smooth.chromateFrac,3)}</td><td>${fmt(state.targets.chromateFrac,3)}</td><td>${fmt(state.targets.chromateFrac/state.baseVolume,3)} M</td></tr>
        <tr><td>H⁺ 영향</td><td>${fmt(state.acid-state.base,3)}</td><td>pH ${calc.pH.toFixed(1)}</td><td>-</td></tr>`;
      $('legendRow').innerHTML = '<span class="chip"><span class="dot" style="background:#ef7b24"></span>Cr₂O₇²⁻ 주황색</span><span class="chip"><span class="dot" style="background:#f6df45"></span>CrO₄²⁻ 노란색</span>';
    }
  }
  function makePills(items){ return items.map(x=>`<span class="pill">${x}</span>`).join(''); }

  function updateSubstances(){
    const sel = $('substanceSelect');
    const before = sel.value;
    const opts = state.reaction==='no2'
      ? [['NO2','NO₂ 첨가 / 제거'],['N2O4','N₂O₄ 첨가 / 제거']]
      : [['HCl','HCl 첨가 / 제거'],['NaOH','NaOH 첨가 / 제거'],['H2O','H₂O 첨가 / 제거']];
    sel.innerHTML = opts.map(([v,t])=>`<option value="${v}">${t}</option>`).join('');
    if(opts.some(o=>o[0]===before)) sel.value=before;
  }

  function addOrRemove(sign){
    const s = $('substanceSelect').value;
    const a = state.amount * sign;
    if(state.reaction==='no2'){
      if(s==='NO2') state.no2 = clamp(state.no2 + a, .05, 6);
      if(s==='N2O4') state.n2o4 = clamp(state.n2o4 + a, .05, 6);
    }else{
      if(s==='HCl') state.acid = clamp(state.acid + a*.65, 0, 3);
      if(s==='NaOH') state.base = clamp(state.base + a*.65, 0, 3);
      if(s==='H2O') state.water = clamp(state.water + a*.55, .35, 3.5);
    }
    computeTargets();
    adaptMolecules(true);
    updateText();
  }
  function resetState(){
    state.no2=.80; state.n2o4=2.22; state.acid=.25; state.base=.15; state.water=1.00;
    state.temp=43; state.pressure=1; state.baseVolume=2.5; state.amount=.3;
    $('tempSlider').value=43; $('pressureSlider').value=1; $('volumeSlider').value=2.5; $('amountSlider').value=.3;
    state.history=[];
    computeTargets(); adaptMolecules(false); updateText();
  }

  function chamberGeometry(){
    const w = simCanvas.getBoundingClientRect().width;
    const h = simCanvas.getBoundingClientRect().height;
    const V = actualVolume();
    const cw = Math.min(360, Math.max(270, w*.43));
    const ch = Math.min(370, Math.max(280, h*.72));
    const x = Math.max(38, w*.10);
    const y = Math.max(52, h*.12);
    const bottom = y + ch;
    let pistonY = y + 32;
    if(state.vessel==='piston'){
      const t = (V-.72)/(3.6-.72);
      pistonY = mix(bottom-86, y+44, clamp(t,0,1));
    }else{
      pistonY = y + 18;
    }
    return {x,y,w:cw,h:ch,bottom,pistonY,gasTop:pistonY+20,gasBottom:bottom-18, gasLeft:x+18, gasRight:x+cw-18};
  }

  function fitMolecules(){
    const g = chamberGeometry();
    state.molecules.forEach(m=>{
      m.x = clamp(m.x, g.gasLeft+m.r, g.gasRight-m.r);
      m.y = clamp(m.y, g.gasTop+m.r, g.gasBottom-m.r);
    });
  }

  function adaptMolecules(keepExisting){
    if(state.reaction!=='no2') return;
    const frac = state.targets.no2Frac || .42;
    const total = state.exaggerate ? 42 : 30;
    const no2Count = clamp(Math.round(total*frac), 3, total-3);
    const n2o4Count = total - no2Count;
    const wanted = [];
    for(let i=0;i<no2Count;i++) wanted.push('NO2');
    for(let i=0;i<n2o4Count;i++) wanted.push('N2O4');
    const g = chamberGeometry();
    const newM=[];
    if(keepExisting){
      for(const type of wanted){
        const idx = state.molecules.findIndex(m=>m.type===type && !m.used);
        if(idx>=0){ const m=state.molecules[idx]; m.used=true; newM.push(m); continue; }
        newM.push(makeMolecule(type,g));
      }
      state.molecules.forEach(m=>delete m.used);
    }else{
      wanted.forEach(type=>newM.push(makeMolecule(type,g)));
    }
    state.molecules=newM;
    fitMolecules();
  }
  function makeMolecule(type,g){
    const r = type==='NO2' ? 8 : 10;
    const angle = Math.random()*Math.PI*2;
    const speed = type==='NO2' ? 1.2+Math.random()*.8 : .85+Math.random()*.55;
    return {
      type,r,
      x: mix(g.gasLeft+r, g.gasRight-r, Math.random()),
      y: mix(g.gasTop+r, g.gasBottom-r, Math.random()),
      vx: Math.cos(angle)*speed,
      vy: Math.sin(angle)*speed
    };
  }

  function drawRoundedRect(context,x,y,w,h,r,fill,stroke,lw=1){
    context.beginPath();
    context.moveTo(x+r,y); context.lineTo(x+w-r,y); context.quadraticCurveTo(x+w,y,x+w,y+r);
    context.lineTo(x+w,y+h-r); context.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    context.lineTo(x+r,y+h); context.quadraticCurveTo(x,y+h,x,y+h-r);
    context.lineTo(x,y+r); context.quadraticCurveTo(x,y,x+r,y); context.closePath();
    if(fill){ context.fillStyle=fill; context.fill(); }
    if(stroke){ context.strokeStyle=stroke; context.lineWidth=lw; context.stroke(); }
  }

  function drawSimulation(){
    const rect = simCanvas.getBoundingClientRect();
    const w = rect.width, h=rect.height;
    ctx.clearRect(0,0,w,h);
    if(state.reaction==='no2') drawNo2(w,h); else drawDichromate(w,h);
  }

  function drawNo2(w,h){
    const g = chamberGeometry();
    const frac = state.smooth.no2Frac;
    const brownAlpha = clamp(frac*.55 + (state.exaggerate? .16:0), .05, .72);
    const fill = `rgba(203,119,58,${brownAlpha})`;
    drawRoundedRect(ctx,g.x,g.y,g.w,g.h,36,fill,'#91c8ff',7);
    ctx.save();
    ctx.shadowColor='rgba(84,145,210,.16)'; ctx.shadowBlur=25;
    ctx.strokeStyle='rgba(118,180,245,.55)'; ctx.lineWidth=2;
    drawRoundedRect(ctx,g.x+12,g.y+12,g.w-24,g.h-24,28,null,'rgba(255,255,255,.75)',1.5);
    ctx.restore();

    if(state.vessel==='piston'){
      ctx.strokeStyle='#94a2b2'; ctx.lineWidth=12; ctx.lineCap='round';
      ctx.beginPath(); ctx.moveTo(g.x+g.w/2,g.y-50); ctx.lineTo(g.x+g.w/2,g.pistonY-14); ctx.stroke();
      drawRoundedRect(ctx,g.x+18,g.pistonY,g.w-36,25,10,'#bcc8d2','#7f8e9d',3);
      ctx.fillStyle='rgba(255,255,255,.72)';
      drawRoundedRect(ctx,g.x+g.w/2-48,g.pistonY-42,96,34,17,'rgba(255,255,255,.62)','#d7e3ee',1);
      ctx.fillStyle='#5d6a79'; ctx.font='800 14px system-ui'; ctx.textAlign='center';
      ctx.fillText('압력 조절',g.x+g.w/2,g.pistonY-20);
    }else{
      ctx.strokeStyle='#6f7b89'; ctx.lineWidth=10;
      drawRoundedRect(ctx,g.x,g.y,g.w,g.h,24,'rgba(226,232,238,.42)','#718091',10);
      ctx.fillStyle='rgba(113,128,145,.12)'; ctx.fillRect(g.x+12,g.y+12,g.w-24,g.h-24);
      ctx.fillStyle='#526073'; ctx.font='900 16px system-ui'; ctx.textAlign='center';
      ctx.fillText('부피 일정 강철용기',g.x+g.w/2,g.y+34);
    }

    const thermoX = Math.min(w-120, g.x+g.w+110);
    const thermoY = g.y+10;
    drawThermometer(thermoX,thermoY, state.temp);

    if(state.motion){
      const speedScale = .55 + state.temp/45;
      for(const m of state.molecules){
        m.x += m.vx*speedScale;
        m.y += m.vy*speedScale;
        if(m.x-m.r<g.gasLeft){m.x=g.gasLeft+m.r; m.vx=Math.abs(m.vx);}
        if(m.x+m.r>g.gasRight){m.x=g.gasRight-m.r; m.vx=-Math.abs(m.vx);}
        if(m.y-m.r<g.gasTop){m.y=g.gasTop+m.r; m.vy=Math.abs(m.vy);}
        if(m.y+m.r>g.gasBottom){m.y=g.gasBottom-m.r; m.vy=-Math.abs(m.vy);}
      }
    }
    for(const m of state.molecules) drawMolecule(m);

    ctx.fillStyle='rgba(255,255,255,.65)';
    drawRoundedRect(ctx,g.x+14,g.bottom-44,150,34,17,'rgba(255,255,255,.62)','#d8e5ef',1);
    ctx.fillStyle='#526073'; ctx.font='900 16px system-ui'; ctx.textAlign='center';
    ctx.fillText(`피스톤 실린더 · ${state.pressure.toFixed(2)} atm`,g.x+89,g.bottom-22);
  }

  function drawMolecule(m){
    ctx.save();
    ctx.translate(m.x,m.y);
    if(m.type==='NO2'){
      ctx.fillStyle='#d86d2f'; ctx.strokeStyle='rgba(156,76,35,.55)'; ctx.lineWidth=1.5;
      ctx.beginPath(); ctx.arc(0,0,m.r,0,Math.PI*2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(-m.r*.88,-m.r*.55,m.r*.55,0,Math.PI*2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(m.r*.88,-m.r*.55,m.r*.55,0,Math.PI*2); ctx.fill(); ctx.stroke();
    }else{
      ctx.fillStyle='rgba(246,249,252,.92)'; ctx.strokeStyle='#7f8ea0'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.arc(-m.r*.75,0,m.r*.75,0,Math.PI*2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(m.r*.75,0,m.r*.75,0,Math.PI*2); ctx.fill(); ctx.stroke();
    }
    ctx.restore();
  }

  function drawThermometer(x,y,temp){
    const height=245, tubeW=42;
    const t=clamp(temp/120,0,1);
    ctx.save();
    ctx.strokeStyle='#8996a6'; ctx.lineWidth=7;
    ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x,y+20); ctx.lineTo(x,y+height-58); ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.45)';
    ctx.beginPath(); ctx.arc(x,y+height-38,43,0,Math.PI*2); ctx.fill(); ctx.stroke();
    ctx.strokeStyle='#8996a6'; ctx.lineWidth=8;
    ctx.beginPath(); ctx.arc(x,y+height-38,43,0,Math.PI*2); ctx.stroke();
    const mercuryH = 42 + t*(height-80);
    ctx.strokeStyle='#ff718b'; ctx.lineWidth=24; ctx.beginPath(); ctx.moveTo(x,y+height-58); ctx.lineTo(x,y+height-mercuryH); ctx.stroke();
    ctx.fillStyle='#ff5c77'; ctx.beginPath(); ctx.arc(x,y+height-38,31,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#465366'; ctx.font='900 22px system-ui'; ctx.textAlign='center';
    ctx.fillText(`${temp.toFixed(0)}℃`,x,y+height+20);
    ctx.restore();
  }

  function drawDichromate(w,h){
    const centerX = w*.45, topY = h*.16, beakerW=Math.min(360,w*.52), beakerH=Math.min(380,h*.70);
    const frac = state.smooth.chromateFrac;
    const r = Math.round(mix(235,246,frac));
    const g = Math.round(mix(104,218,frac));
    const b = Math.round(mix(34,70,frac));
    ctx.save();
    ctx.fillStyle='rgba(255,255,255,.60)';
    drawRoundedRect(ctx, centerX-beakerW/2-18, topY-18, beakerW+36, beakerH+46,26,'rgba(255,255,255,.45)','#dbe7f1',1.5);
    ctx.strokeStyle='#8ea3b8'; ctx.lineWidth=6;
    ctx.beginPath();
    ctx.moveTo(centerX-beakerW/2, topY); ctx.lineTo(centerX-beakerW/2+26, topY+beakerH);
    ctx.lineTo(centerX+beakerW/2-26, topY+beakerH); ctx.lineTo(centerX+beakerW/2, topY);
    ctx.stroke();
    ctx.strokeStyle='#9fb0c2'; ctx.lineWidth=4;
    ctx.beginPath(); ctx.ellipse(centerX, topY, beakerW/2, 16,0,0,Math.PI*2); ctx.stroke();
    const liquidH = beakerH*.72;
    const liquidY = topY+beakerH-liquidH;
    const grd = ctx.createLinearGradient(0,liquidY,0,topY+beakerH);
    grd.addColorStop(0,`rgba(${r},${g},${b},.82)`);
    grd.addColorStop(1,`rgba(${Math.min(255,r+10)},${Math.min(255,g+12)},${Math.min(255,b+8)},.96)`);
    ctx.fillStyle=grd;
    ctx.beginPath();
    ctx.moveTo(centerX-beakerW/2+18,liquidY);
    ctx.bezierCurveTo(centerX-beakerW/4,liquidY-10,centerX+beakerW/4,liquidY+10,centerX+beakerW/2-18,liquidY);
    ctx.lineTo(centerX+beakerW/2-50,topY+beakerH-8);
    ctx.lineTo(centerX-beakerW/2+50,topY+beakerH-8);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.32)';
    ctx.beginPath(); ctx.ellipse(centerX,liquidY,beakerW*.42,14,0,0,Math.PI*2); ctx.fill();
    for(let i=0;i<22;i++){
      const x = centerX-beakerW*.34 + Math.random()*beakerW*.68;
      const y = liquidY + 22 + Math.random()*(liquidH-45);
      ctx.fillStyle = i/22 < frac ? 'rgba(255,238,80,.55)' : 'rgba(211,93,30,.55)';
      ctx.beginPath(); ctx.arc(x,y,3+Math.random()*2,0,Math.PI*2); ctx.fill();
    }
    ctx.fillStyle='#405066'; ctx.font='900 20px system-ui'; ctx.textAlign='center';
    const label = frac>.60 ? 'CrO₄²⁻ 증가 · 노란색' : frac<.40 ? 'Cr₂O₇²⁻ 증가 · 주황색' : '중간 평형 색';
    ctx.fillText(label,centerX,topY+beakerH+32);
    drawThermometer(Math.min(w-120, centerX+beakerW/2+120), topY+18, state.temp);
    ctx.restore();
  }

  function drawChart(c, context, series, labels, titleColors){
    const rect = c.getBoundingClientRect();
    const w=rect.width, h=rect.height;
    context.clearRect(0,0,w,h);
    const padL=44, padR=12, padT=10, padB=26;
    const plotW=w-padL-padR, plotH=h-padT-padB;
    context.strokeStyle='#e0e8f0'; context.lineWidth=1;
    context.font='11px system-ui'; context.fillStyle='#78859a';
    let max = 1, min = 0;
    series.forEach(s=>s.data.forEach(v=>{ if(isFinite(v)){ max=Math.max(max,v); min=Math.min(min,v); }}));
    if(min>0) min=0;
    if(max-min<.001) max=min+1;
    const span=max-min;
    max += span*.08;
    for(let i=0;i<=4;i++){
      const y=padT+plotH*(i/4);
      context.beginPath(); context.moveTo(padL,y); context.lineTo(w-padR,y); context.stroke();
      const val = max-(max-min)*(i/4);
      context.fillText(val.toFixed(max>10?1:2),6,y+4);
    }
    const n = Math.max(2, series[0].data.length);
    series.forEach((s,idx)=>{
      context.strokeStyle=s.color; context.lineWidth=2.8;
      context.beginPath();
      s.data.forEach((v,i)=>{
        const x=padL + plotW*(i/(n-1));
        const y=padT + plotH*(1-(v-min)/(max-min));
        if(i===0) context.moveTo(x,y); else context.lineTo(x,y);
      });
      context.stroke();
    });
    labels.forEach((l,i)=>{
      const x=padL + plotW*(i/(Math.max(1,labels.length-1)));
      if(i%Math.ceil(labels.length/6)===0){ context.fillStyle='#7d899d'; context.fillText(l,x-5,h-8); }
    });
    let lx=padL;
    series.forEach((s)=>{
      context.strokeStyle=s.color; context.lineWidth=4;
      context.beginPath(); context.moveTo(lx,h-8); context.lineTo(lx+16,h-8); context.stroke();
      context.fillStyle='#526073'; context.font='900 11px system-ui'; context.fillText(s.name,lx+22,h-5);
      lx += 90;
    });
  }

  function drawCharts(){
    const labels = state.history.map((_,i)=>String(i));
    drawChart(qkCanvas,qkCtx,[
      {name:'K', color:'#2176d2', data:state.history.map(p=>p.K)},
      {name:'Q', color:'#8fc5ff', data:state.history.map(p=>p.Q)}
    ], labels);
    drawChart(rateCanvas,rateCtx,[
      {name:'정반응', color:'#1e7bd8', data:state.history.map(p=>p.F)},
      {name:'역반응', color:'#74bfff', data:state.history.map(p=>p.R)}
    ], labels);
  }

  function frame(now){
    computeTargets();
    const s=state.smooth, t=state.targets;
    s.K += (t.K-s.K)*.055; s.Q += (t.Q-s.Q)*.055;
    s.F += (t.F-s.F)*.075; s.R += (t.R-s.R)*.075;
    s.no2Frac += (t.no2Frac-s.no2Frac)*.05;
    s.chromateFrac += (t.chromateFrac-s.chromateFrac)*.06;
    if(now-state.lastHistory>160){
      state.history.push({K:s.K,Q:s.Q,F:s.F,R:s.R});
      if(state.history.length>80) state.history.shift();
      state.lastHistory=now;
      updateText();
      if(state.reaction==='no2') adaptMolecules(true);
    }
    drawSimulation();
    drawCharts();
    requestAnimationFrame(frame);
  }

  function initEvents(){
    $('reactionSelect').addEventListener('change',e=>{
      state.reaction=e.target.value; updateSubstances(); state.history=[]; computeTargets(); adaptMolecules(false); updateText();
    });
    document.querySelectorAll('input[name="vessel"]').forEach(el=>el.addEventListener('change',e=>{ state.vessel=e.target.value; fitMolecules(); updateText(); }));
    $('tempSlider').addEventListener('input',e=>{ state.temp=Number(e.target.value); updateText(); });
    $('pressureSlider').addEventListener('input',e=>{ state.pressure=Number(e.target.value); fitMolecules(); updateText(); });
    $('volumeSlider').addEventListener('input',e=>{ state.baseVolume=Number(e.target.value); fitMolecules(); updateText(); });
    $('amountSlider').addEventListener('input',e=>{ state.amount=Number(e.target.value); updateText(); });
    $('addBtn').addEventListener('click',()=>addOrRemove(1));
    $('removeBtn').addEventListener('click',()=>addOrRemove(-1));
    $('resetBtn').addEventListener('click',resetState);
    $('motionToggle').addEventListener('change',e=>{ state.motion=e.target.checked; });
    $('exaggerateToggle').addEventListener('change',e=>{ state.exaggerate=e.target.checked; computeTargets(); adaptMolecules(true); updateText(); });
  }

  resizeAll();
  initEvents();
  updateSubstances();
  computeTargets();
  adaptMolecules(false);
  updateText();
  requestAnimationFrame(frame);
})();
</script>
</body>
</html>
"""

components.html(HTML, height=920, scrolling=False)
