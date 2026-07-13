import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="화학 평형 시뮬레이터", page_icon="⚗️", layout="wide")

st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"] { background: #f7fbff; }
      .block-container { padding: 0.35rem 0.55rem 0.55rem 0.55rem !important; max-width: 100% !important; }
      header[data-testid="stHeader"] { display: none; }
      footer { display: none; }
      iframe { border-radius: 22px; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r'''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>화학 평형 시뮬레이터</title>
<style>
  :root{
    --bg:#f7fbff;
    --card:#ffffff;
    --line:#d9e5f2;
    --text:#253248;
    --muted:#6e7a8e;
    --blue:#7db7ff;
    --blue2:#e8f4ff;
    --pink:#ff5b73;
    --orange:#e88936;
    --yellow:#f7d84d;
    --dark:#172033;
    --shadow: 0 18px 42px rgba(89,114,148,.13);
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;background:var(--bg);font-family:Pretendard,Apple SD Gothic Neo,Malgun Gothic,Segoe UI,sans-serif;color:var(--text);overflow:hidden;}
  .app{width:100%;height:850px;padding:12px;display:flex;flex-direction:column;gap:10px;background:linear-gradient(120deg,#fffaf4 0%,#f2fbff 48%,#f8f7ff 100%);}
  .topbar{display:grid;grid-template-columns:minmax(330px,360px) minmax(460px,1fr);gap:10px;align-items:stretch;min-height:66px;}
  .title-card,.select-card,.panel,.stage-card,.result-card{background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);}
  .title-card{padding:13px 16px;display:flex;gap:10px;align-items:center;min-width:0;}
  .logo{font-size:28px;line-height:1;filter:drop-shadow(0 4px 8px rgba(98,160,210,.22));flex:0 0 auto;}
  h1{font-size:24px;margin:0;letter-spacing:-1.2px;line-height:1.1;white-space:nowrap;}
  .subtitle{display:none;}
  .select-card{padding:13px 15px;display:flex;align-items:center;gap:10px;min-width:0;}
  .select-label{font-weight:800;color:#334057;white-space:nowrap;}
  select,input[type=range],button{font-family:inherit;}
  .experiment-select{width:100%;height:38px;border:1px solid #d6e5f4;background:#202433;color:white;border-radius:10px;padding:0 12px;font-weight:700;outline:none;}
  .main{display:grid;grid-template-columns:minmax(300px,315px) minmax(430px,.95fr) minmax(540px,1.18fr);gap:10px;min-height:0;flex:1;}
  .panel{padding:14px 13px;overflow:hidden;min-width:0;}
  .panel-scroll{height:100%;overflow:auto;padding-right:3px;}
  .panel-scroll::-webkit-scrollbar{width:8px}.panel-scroll::-webkit-scrollbar-thumb{background:#d7e5f4;border-radius:20px}
  .panel h2,.result-card h2{margin:0 0 10px 0;font-size:21px;letter-spacing:-.8px;line-height:1.15;}
  .control-section{border:1px solid #dfe8f2;background:#fbfdff;border-radius:16px;padding:12px 11px;margin-bottom:10px;}
  .section-title{font-weight:900;margin-bottom:8px;color:#334057;font-size:13.5px;line-height:1.25;}
  .equation-pill{display:inline-flex;align-items:center;gap:6px;border:1px solid #d4e6fa;background:#fff;border-radius:12px;padding:8px 9px;font-weight:900;letter-spacing:-.5px;font-size:13.2px;line-height:1.25;max-width:100%;word-break:keep-all;}
  .radio-row{display:flex;flex-direction:column;gap:8px;margin:8px 0 10px;}
  label.radio{display:flex;align-items:center;gap:7px;font-size:13.4px;color:#3c4659;line-height:1.3;cursor:pointer;word-break:keep-all;}
  input[type=radio],input[type=checkbox]{accent-color:var(--pink);}
  .range-wrap{margin:12px 0;}
  .range-label{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;font-size:12.8px;color:#39465c;font-weight:700;gap:6px;}
  .range-value{color:var(--pink);font-weight:900;}
  input[type=range]{width:100%;height:6px;accent-color:var(--pink);}
  .inline-select{width:100%;height:36px;border:1px solid #d6e1ed;border-radius:10px;padding:0 8px;background:#f4f7fb;color:#263247;font-weight:700;outline:none;font-size:13px;}
  .button-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;}
  button{border:0;border-radius:11px;background:#151b2b;color:white;height:36px;font-weight:800;cursor:pointer;box-shadow:0 7px 15px rgba(21,27,43,.12);transition:transform .12s ease,opacity .12s ease;}
  button:hover{transform:translateY(-1px)} button.secondary{background:#edf5ff;color:#23649c;border:1px solid #cce4ff;box-shadow:none;}
  .note{display:none;}
  .stage-card{position:relative;padding:14px 14px 12px;overflow:hidden;display:flex;flex-direction:column;min-width:0;}
  .stage-head{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:8px;min-width:0;}
  .stage-title{font-weight:950;font-size:17px;letter-spacing:-.7px;line-height:1.24;word-break:keep-all;min-width:0;}
  .legend{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
  .legend-chip{font-size:11.2px;font-weight:800;padding:6px 8px;border-radius:999px;background:#f4f8fc;border:1px solid #d6e5f4;color:#5b6b80;white-space:nowrap;}
  .legend-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;vertical-align:middle;}
  .stage-canvas-wrap{position:relative;flex:1;min-height:455px;border:1px solid #dbe8f6;border-radius:24px;background:radial-gradient(circle at 35% 25%,rgba(255,255,255,.98),rgba(239,248,255,.78));overflow:hidden;}
  #stageCanvas{display:block;width:100%;height:100%;}
  .stage-caption{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);display:flex;gap:7px;flex-wrap:wrap;justify-content:center;max-width:92%;pointer-events:none;}
  .caption-pill{background:rgba(255,255,255,.80);backdrop-filter:blur(9px);border:1px solid #d5e6f7;border-radius:999px;padding:7px 11px;font-size:12.3px;font-weight:900;color:#4b5a70;box-shadow:0 7px 18px rgba(91,120,150,.08);white-space:nowrap;}
  .result-card{padding:14px;overflow:hidden;min-width:0;}
  .result-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;}
  .metric{border:1px solid #e2ebf5;background:#fbfdff;border-radius:15px;padding:9px 10px;min-width:0;}
  .metric .label{font-size:12px;color:#6f7e91;font-weight:800;margin-bottom:4px;}
  .metric .value{font-size:18px;font-weight:950;color:#263248;letter-spacing:-.6px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .badges{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 10px;}
  .badge{padding:7px 10px;border-radius:999px;background:#eaf5ff;border:1px solid #c9e3ff;color:#1e629a;font-size:12.3px;font-weight:900;line-height:1.2;white-space:nowrap;}
  .formula{border:1px solid #edf1f6;background:#fbfcff;border-radius:14px;padding:9px 10px;margin-bottom:9px;font-size:12.4px;line-height:1.5;color:#273246;word-break:keep-all;}
  .formula code{font-family:Consolas,Menlo,monospace;font-size:12.5px;color:#1c2b44;}
  .mini-table{width:100%;border-collapse:separate;border-spacing:0;margin-bottom:8px;font-size:12px;overflow:hidden;border:1px solid #e2ebf5;border-radius:13px;}
  .mini-table th,.mini-table td{padding:6px 7px;border-bottom:1px solid #edf2f7;text-align:right;background:white;white-space:nowrap;}
  .mini-table th:first-child,.mini-table td:first-child{text-align:left}.mini-table tr:last-child td{border-bottom:0}.mini-table th{background:#f7fbff;color:#617084;font-weight:900;}
  .chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  .chart-card{border:1px solid #e2ebf5;background:white;border-radius:16px;padding:8px 9px;min-width:0;}
  .chart-title{font-weight:950;font-size:13.5px;margin-bottom:2px;letter-spacing:-.45px;line-height:1.2;}
  .chart-sub{display:none;}
  canvas.chart{display:block;width:100%;height:154px;}
  .hidden{display:none !important;}
  .small-check{display:flex;gap:7px;align-items:flex-start;font-size:13px;color:#4e5c70;margin-top:8px;line-height:1.42;}
  .danger-text{color:var(--pink);font-weight:900;}
  .eq-mark{color:#0e74d4;font-weight:950;}
  @media (max-width:1200px){
    .app{height:auto;overflow:auto}.main{grid-template-columns:1fr}.topbar{grid-template-columns:1fr}.stage-canvas-wrap{min-height:430px}.chart-grid{grid-template-columns:1fr}.subtitle{white-space:normal;}
  }
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="title-card">
      <div class="logo">⚗️</div>
      <div>
        <h1>화학 평형 시뮬레이터</h1>
      </div>
    </div>
    <div class="select-card">
      <div class="select-label">실험 선택</div>
      <select id="experiment" class="experiment-select">
        <option value="gas">이산화질소 ↔ 사산화이질소  |  2NO₂(g) ⇌ N₂O₄(g)</option>
        <option value="chromate">다이크로메이트 ↔ 크로메이트  |  Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)</option>
      </select>
    </div>
  </div>

  <div class="main">
    <aside class="panel">
      <div class="panel-scroll">
        <h2>조건 변화</h2>
        <div class="control-section">
          <div id="leftEquation" class="equation-pill">2NO₂(g) ⇌ N₂O₄(g)</div>
          <div class="section-title" style="margin-top:12px;">용기</div>
          <div class="radio-row" id="vesselBox">
            <label class="radio"><input type="radio" name="vessel" value="cylinder" checked> 실린더</label>
            <label class="radio"><input type="radio" name="vessel" value="steel"> 강철용기</label>
          </div>
        </div>

        <div class="control-section">
          <div class="section-title">온도 · 압력 · 부피</div>
          <div class="range-wrap">
            <div class="range-label"><span>온도 조건 변화 (℃)</span><span id="tempVal" class="range-value">43</span></div>
            <input id="temp" type="range" min="0" max="120" step="1" value="43" />
          </div>
          <div id="pressureGroup" class="range-wrap">
            <div class="range-label"><span>압력 조건 변화 (atm)</span><span id="pressureVal" class="range-value">1.00</span></div>
            <input id="pressure" type="range" min="0.50" max="3.00" step="0.01" value="1.00" />
          </div>
          <div id="volumeGroup" class="range-wrap">
            <div class="range-label"><span>용기 부피 (L)</span><span id="volumeVal" class="range-value">2.50</span></div>
            <input id="volume" type="range" min="1.00" max="4.00" step="0.01" value="2.50" />
          </div>
          <div class="note" id="containerNote"></div>
        </div>

        <div id="gasControls" class="control-section">
          <div class="section-title">농도 / 물질 첨가·제거</div>
          <select id="gasAction" class="inline-select">
            <option value="addNO2">NO₂ 첨가</option>
            <option value="removeNO2">NO₂ 제거</option>
            <option value="addN2O4">N₂O₄ 첨가</option>
            <option value="removeN2O4">N₂O₄ 제거</option>
            <option value="addInert">H₂ 비활성 기체 첨가</option>
          </select>
          <div class="range-wrap">
            <div class="range-label"><span>조작량 (mol)</span><span id="gasAmountVal" class="range-value">0.30</span></div>
            <input id="gasAmount" type="range" min="0.05" max="1.00" step="0.05" value="0.30" />
          </div>
          <div class="button-row">
            <button id="applyGas">적용</button>
            <button id="resetGas" class="secondary">초기화</button>
          </div>
          <label class="small-check"><input type="checkbox" id="moleculeMotion" checked> NO₂·N₂O₄ 분자 운동 표시</label>
        </div>

        <div id="chromateControls" class="control-section hidden">
          <div class="section-title">농도 / 물질 첨가</div>
          <select id="chromateAction" class="inline-select">
            <option value="hcl">HCl 첨가</option>
            <option value="naoh">NaOH 첨가</option>
            <option value="water">H₂O 첨가</option>
          </select>
          <div class="range-wrap">
            <div class="range-label"><span>조작량</span><span id="chromateAmountVal" class="range-value">0.40</span></div>
            <input id="chromateAmount" type="range" min="0.10" max="1.00" step="0.05" value="0.40" />
          </div>
          <div class="button-row">
            <button id="applyChromate">적용</button>
            <button id="resetChromate" class="secondary">초기화</button>
          </div>
        </div>
      </div>
    </aside>

    <section class="stage-card">
      <div class="stage-head">
        <div id="stageTitle" class="stage-title">2NO₂(g) ⇌ N₂O₄(g)</div>
        <div id="legend" class="legend"></div>
      </div>
      <div class="stage-canvas-wrap">
        <canvas id="stageCanvas"></canvas>
        <div id="caption" class="stage-caption"></div>
      </div>
    </section>

    <aside class="result-card">
      <h2>실험 결과</h2>
      <div class="result-grid">
        <div class="metric"><div class="label">평형상수 K</div><div id="kVal" class="value">-</div></div>
        <div class="metric"><div class="label">반응지수 Q</div><div id="qVal" class="value">-</div></div>
        <div class="metric"><div class="label">평형 이동</div><div id="directionVal" class="value">-</div></div>
        <div class="metric"><div class="label">현재 부피</div><div id="currentVolVal" class="value">-</div></div>
      </div>
      <div id="badges" class="badges"></div>
      <div id="formula" class="formula"></div>
      <table class="mini-table">
        <thead><tr><th>물질</th><th>현재</th><th>평형</th><th>농도/상태</th></tr></thead>
        <tbody id="tableBody"></tbody>
      </table>
      <div class="chart-grid">
        <div class="chart-card">
          <div class="chart-title">Q와 K의 실시간 변화</div>
          
          <canvas id="qkChart" class="chart"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-title">정반응 속도와 역반응 속도</div>
          
          <canvas id="rateChart" class="chart"></canvas>
        </div>
      </div>
    </aside>
  </div>
</div>

<script>
(function(){
  const $ = (id)=>document.getElementById(id);
  const stage = $('stageCanvas');
  const ctx = stage.getContext('2d');
  const qkCtx = $('qkChart').getContext('2d');
  const rateCtx = $('rateChart').getContext('2d');

  const state = {
    experiment:'gas', vessel:'cylinder', temp:43, pressure:1.0, volume:2.5, displayVolume:2.5, inert:0.0,
    gas:{no2:0.80, n2o4:2.20},
    chromate:{balance:0.58, h:1.0, dilution:0.0},
    displayGas:{no2:0.80, n2o4:2.20},
    displayChromate:{balance:0.58, h:1.0},
    targetGas:{no2:0.80,n2o4:2.20},
    targetChromate:{balance:0.58,h:1.0},
    anim:null,
    volumeAnim:null,
    molecules:[],
    staticDots:[],
    lastTime:performance.now(),
    motion:true,
    chart:{qStart:1,qEnd:1,kStart:1,kEnd:1,rfStart:1,rfEnd:1,rrStart:1,rrEnd:1,start:performance.now(),duration:5000}
  };

  function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
  function lerp(a,b,t){return a+(b-a)*t;}
  function ease(t){return 1-Math.pow(1-clamp(t,0,1),3);}
  function fmt(v,d=2){ if(!isFinite(v)) return '-'; return Number(v).toFixed(d); }
  function pow10(v){ return Math.pow(10,v); }

  function resizeCanvas(c){
    const r = c.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(10, Math.floor(r.width*dpr));
    const h = Math.max(10, Math.floor(r.height*dpr));
    if(c.width!==w || c.height!==h){ c.width=w; c.height=h; }
    const g = c.getContext('2d');
    g.setTransform(dpr,0,0,dpr,0,0);
    return {w:r.width,h:r.height};
  }

  function effectiveVolume(){
    if(state.experiment==='chromate') return 3.40;
    if(state.vessel==='steel') return state.volume;
    return clamp(state.volume / Math.sqrt(state.pressure), .85, 4.30);
  }
  function visualEffectiveVolume(){
    const v = state.displayVolume ?? state.volume;
    if(state.experiment==='chromate') return 3.40;
    if(state.vessel==='steel') return v;
    return clamp(v / Math.sqrt(state.pressure), .85, 4.30);
  }
  function setVolumeAnimated(newVolume, duration=900){
    const from = state.displayVolume ?? state.volume;
    const to = clamp(newVolume, 1.00, 4.00);
    state.volume = to;
    $('volume').value = to;
    state.volumeAnim = {from, to, start:performance.now(), duration};
  }
  function animatePistonByEquilibrium(startGas,targetGas){
    if(state.experiment!=='gas' || state.vessel!=='cylinder') return;
    const startTotal = startGas.no2 + startGas.n2o4 + state.inert;
    const targetTotal = targetGas.no2 + targetGas.n2o4 + state.inert;
    const deltaMoles = targetTotal - startTotal;
    if(Math.abs(deltaMoles)<0.015) return;
    // 일정 압력 피스톤에서는 전체 기체 몰수 변화가 부피 변화로 이어지도록 시각화한다.
    // 정반응(2NO₂ -> N₂O₄)은 몰수가 줄어 피스톤이 내려가고, 역반응은 올라간다.
    const visualDelta = deltaMoles * 0.72;
    setVolumeAnimated(state.volume + visualDelta, 1700);
  }
  function gasK(temp=state.temp){
    // 2NO2 -> N2O4는 발열 반응이므로 온도가 높을수록 K가 작아지도록 설정한다.
    return clamp(4.4 * Math.exp((40-temp)/34), 0.18, 18.0);
  }
  function gasQ(g=state.displayGas, vol=effectiveVolume()){
    const cNO2 = Math.max(g.no2/vol, 1e-6);
    const cN2O4 = Math.max(g.n2o4/vol, 1e-6);
    return cN2O4/(cNO2*cNO2);
  }
  function solveGasEquilibrium(sourceGas){
    const V = effectiveVolume();
    const K = gasK();
    const total = Math.max(sourceGas.no2 + 2*sourceGas.n2o4, .08);
    let lo=0, hi=total/2-1e-5;
    for(let i=0;i<80;i++){
      const b=(lo+hi)/2;
      const a=Math.max(total-2*b,1e-7);
      const val = b*V/(a*a);
      if(val < K) lo=b; else hi=b;
    }
    const n2o4=(lo+hi)/2;
    return {no2:Math.max(total-2*n2o4,0.0001), n2o4:Math.max(n2o4,0.0001)};
  }
  function chromateK(){
    return clamp(2.4 + state.temp/45 + (state.chromate.dilution*0.35), 1.2, 7.2);
  }
  function chromateQ(ch=state.displayChromate){
    // 교육용 표현: 균형 비율을 Q값으로 대응시켜 K와 만나는 지점을 선명하게 보여준다.
    return 1.05 + ch.balance*5.7 + (ch.h-1)*0.35;
  }
  function solveChromateEquilibrium(source){
    const tempEffect = (state.temp-45)/85;
    const acidEffect = -(source.h-1.0)*0.42;
    const dilutionEffect = source.dilution*0.22;
    const raw = 0.56 + tempEffect + acidEffect + dilutionEffect;
    const balance = clamp(raw, 0.08, 0.94);
    return {balance, h:source.h};
  }

  function startTransition(target, reason='condition'){
    const now = performance.now();
    const duration = 5000;
    if(state.experiment==='gas'){
      const start = {...state.displayGas};
      state.targetGas = {...target};
      state.anim = {type:'gas', start, target:{...target}, startT:now, duration};
      const q0 = gasQ(start), k1 = gasK(), rf0 = rateForwardGas(start), rr0 = rateReverseGas(start);
      const rf1 = rateForwardGas(target), rr1 = rateReverseGas(target);
      state.chart = {qStart:q0, qEnd:k1, kStart:k1, kEnd:k1, rfStart:rf0, rfEnd:(rf1+rr1)/2, rrStart:rr0, rrEnd:(rf1+rr1)/2, start:now, duration};
      animatePistonByEquilibrium(start,target);
    } else {
      const start = {...state.displayChromate};
      state.targetChromate = {...target};
      state.anim = {type:'chromate', start, target:{...target}, startT:now, duration};
      const q0 = chromateQ(start), k1 = chromateK(), rf0 = rateForwardChromate(start), rr0 = rateReverseChromate(start);
      const mid = Math.max(0.18, (rf0+rr0)/2);
      state.chart = {qStart:q0, qEnd:k1, kStart:k1, kEnd:k1, rfStart:rf0, rfEnd:mid, rrStart:rr0, rrEnd:mid, start:now, duration};
    }
  }

  function applyConditionChange(){
    if(state.experiment==='gas') startTransition(solveGasEquilibrium(state.displayGas));
    else startTransition(solveChromateEquilibrium(state.chromate));
  }

  function rateForwardGas(g=state.displayGas){
    const c = Math.max(g.no2/effectiveVolume(),0.001);
    return clamp(0.11 + c*c*0.72 + state.temp/850, .03, 2.2);
  }
  function rateReverseGas(g=state.displayGas){
    const c = Math.max(g.n2o4/effectiveVolume(),0.001);
    return clamp(0.08 + c*0.32 + state.temp/1100, .03, 2.2);
  }
  function rateForwardChromate(ch=state.displayChromate){ return clamp(0.25 + (1-ch.balance)*0.65 + state.temp/580, .08, 1.4); }
  function rateReverseChromate(ch=state.displayChromate){ return clamp(0.22 + ch.balance*0.55 + ch.h*.08, .08, 1.4); }

  function directionFrom(q,k){
    if(Math.abs(q-k)/Math.max(k,0.1)<0.035) return '평형';
    if(state.experiment==='gas') return q<k ? '정반응' : '역반응';
    return q<k ? '정반응' : '역반응';
  }

  function makeMolecules(){
    state.molecules=[];
    for(let i=0;i<48;i++){
      state.molecules.push({
        kind: i%3===0?'n2o4':'no2',
        x: 150 + Math.random()*260,
        y: 230 + Math.random()*190,
        vx: (Math.random()*2-1)*(0.55+Math.random()*0.35),
        vy: (Math.random()*2-1)*(0.55+Math.random()*0.35),
        r: 7+Math.random()*2
      });
    }
  }
  function makeStaticDots(){
    state.staticDots=[];
    for(let i=0;i<24;i++){
      state.staticDots.push({x:Math.random(),y:Math.random(),kind:i%3});
    }
  }

  function pistonGeometry(W,H){
    const V = visualEffectiveVolume();
    const top = 62, bottom = H-68;
    const minY = top + 54, maxY = bottom - 118;
    const t = clamp((V-.85)/(4.3-.85),0,1);
    const pistonY = lerp(maxY,minY,t); // 부피가 커질수록 피스톤이 위로 이동
    return {x:70,y:top,w:Math.min(410,W*0.58),h:bottom-top,pistonY,gasTop:pistonY+16,gasBottom:bottom-8};
  }

  function drawGasMolecule(g,m,scale){
    if(m.kind==='no2'){
      g.fillStyle='#d97836'; g.strokeStyle='rgba(151,86,44,.35)'; g.lineWidth=1;
      g.beginPath(); g.arc(m.x,m.y,m.r*scale,0,Math.PI*2); g.fill(); g.stroke();
    } else if(m.kind==='h2'){
      g.strokeStyle='rgba(87,145,190,.55)'; g.lineWidth=1.8; g.fillStyle='#d8efff';
      g.beginPath(); g.arc(m.x-m.r*.42,m.y,m.r*.55*scale,0,Math.PI*2); g.fill(); g.stroke();
      g.beginPath(); g.arc(m.x+m.r*.42,m.y,m.r*.55*scale,0,Math.PI*2); g.fill(); g.stroke();
    } else {
      g.strokeStyle='#8090a3'; g.lineWidth=2; g.fillStyle='#f7fbff';
      g.beginPath(); g.arc(m.x-m.r*.72,m.y,m.r*.86*scale,0,Math.PI*2); g.fill(); g.stroke();
      g.beginPath(); g.arc(m.x+m.r*.72,m.y,m.r*.86*scale,0,Math.PI*2); g.fill(); g.stroke();
    }
  }

  function drawStage(){
    const {w:W,h:H}=resizeCanvas(stage);
    ctx.clearRect(0,0,W,H);
    if(state.experiment==='gas') drawGasStage(W,H); else drawChromateStage(W,H);
  }

  function drawRoundedRect(g,x,y,w,h,r,fill,stroke,lw=1){
    g.beginPath();
    g.moveTo(x+r,y); g.lineTo(x+w-r,y); g.quadraticCurveTo(x+w,y,x+w,y+r);
    g.lineTo(x+w,y+h-r); g.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    g.lineTo(x+r,y+h); g.quadraticCurveTo(x,y+h,x,y+h-r);
    g.lineTo(x,y+r); g.quadraticCurveTo(x,y,x+r,y);
    if(fill){g.fillStyle=fill;g.fill();}
    if(stroke){g.strokeStyle=stroke;g.lineWidth=lw;g.stroke();}
  }

  function drawThermometer(g,x,y,temp){
    const h=210, bulb=18, tubeW=16;
    const bulbCenterY = y+h-bulb+10;
    g.strokeStyle='#8f9dae';g.lineWidth=7;g.lineCap='round';
    g.beginPath();g.moveTo(x,y+h-bulb);g.lineTo(x,y+20);g.stroke();
    g.fillStyle='#ff5b73';
    const fillH = clamp(24 + temp/120*148, 24, 172);
    const tubeX = x-tubeW/2+4;
    const tubeY = y+h-bulb-fillH+22;
    g.beginPath();
    g.roundRect ? g.roundRect(tubeX,tubeY,tubeW-8,fillH,8) : g.rect(tubeX,tubeY,tubeW-8,fillH);
    g.fill();
    g.beginPath();g.arc(x,bulbCenterY,bulb,0,Math.PI*2);g.fill();
    g.strokeStyle='#8f9dae';g.lineWidth=5;g.beginPath();g.arc(x,bulbCenterY,bulb+5,0,Math.PI*2);g.stroke();

    // 온도 숫자는 온도계 아래에 작은 흰색 라벨로 표시해 배경과 겹치지 않게 한다.
    const label = Math.round(temp) + '°C';
    const labelY = bulbCenterY + bulb + 18;
    g.font='900 17px Segoe UI, sans-serif';
    g.textAlign='center';g.textBaseline='middle';
    const tw = g.measureText(label).width;
    drawRoundedRect(g,x-tw/2-10,labelY-14,tw+20,28,14,'rgba(255,255,255,.82)','#d6e5f4',1);
    g.fillStyle='#344156';
    g.fillText(label,x,labelY);
  }

  function drawGasStage(W,H){
    const pg = pistonGeometry(W,H);
    const no2Frac = state.displayGas.no2/(state.displayGas.no2+state.displayGas.n2o4+1e-6);
    const brownAlpha = clamp(.08 + no2Frac*.72, .08, .82);
    const vesselColor = `rgba(205,128,58,${brownAlpha})`;

    if(state.vessel==='cylinder'){
      // 실린더 외곽
      drawRoundedRect(ctx,pg.x,pg.y,pg.w,pg.h,38,'rgba(255,255,255,.34)','#92c8ff',7);
      // 기체 영역
      drawRoundedRect(ctx,pg.x+10,pg.gasTop,pg.w-20,pg.gasBottom-pg.gasTop,26,vesselColor,null,0);
      ctx.fillStyle='rgba(255,255,255,.30)';
      ctx.fillRect(pg.x+12,pg.gasTop,pg.w-24,10);
      // 피스톤 막대와 손잡이
      ctx.strokeStyle='#9eabb9';ctx.lineWidth=12;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(pg.x+pg.w/2,pg.pistonY-82);ctx.lineTo(pg.x+pg.w/2,pg.pistonY-12);ctx.stroke();
      drawRoundedRect(ctx,pg.x+28,pg.pistonY,pg.w-56,26,11,'#b9c4cf','#8190a0',3);
      // 피스톤 위 안내 문구는 작은 화면에서 글자가 잘려 보이므로 표시하지 않는다.
    } else {
      drawRoundedRect(ctx,pg.x+10,pg.y+8,pg.w-20,pg.h-18,36,'rgba(255,255,255,.34)','#778392',10);
      drawRoundedRect(ctx,pg.x+25,pg.y+28,pg.w-50,pg.h-58,24,vesselColor,null,0);
      ctx.fillStyle='rgba(37,48,72,.75)';ctx.font='900 16px Segoe UI, sans-serif';ctx.textAlign='center';
      ctx.fillText('부피 일정',pg.x+pg.w/2,pg.y+44);
    }

    // 분자 수와 색 비율을 눈에 띄게 반영
    const totalMoles = state.displayGas.no2 + state.displayGas.n2o4;
    const no2Need = Math.round(clamp(10 + no2Frac*32, 8, 42));
    const n2o4Need = Math.round(clamp(8 + (1-no2Frac)*22, 5, 30));
    const h2Need = Math.round(clamp(state.inert*9, 0, 20));
    let desired = no2Need + n2o4Need + h2Need;
    while(state.molecules.length<desired){
      state.molecules.push({kind:'no2',x:pg.x+45+Math.random()*(pg.w-90),y:pg.gasTop+25+Math.random()*(pg.gasBottom-pg.gasTop-50),vx:Math.random()*2-1,vy:Math.random()*2-1,r:7+Math.random()*2});
    }
    if(state.molecules.length>desired) state.molecules.length=desired;
    state.molecules.forEach((m,i)=>{m.kind = i<no2Need ? 'no2' : (i<no2Need+n2o4Need ? 'n2o4' : 'h2');});

    if(state.motion){
      const tempSpeed = lerp(.45,2.75,state.temp/120);
      for(const m of state.molecules){
        m.x += m.vx*tempSpeed;
        m.y += m.vy*tempSpeed;
        const left=pg.x+34, right=pg.x+pg.w-34, top=(state.vessel==='cylinder'?pg.gasTop+15:pg.y+45), bottom=pg.gasBottom-18;
        const rad = m.kind==='no2' ? m.r : (m.kind==='h2' ? m.r*.85 : m.r*1.7);
        if(m.x-rad<left){m.x=left+rad;m.vx=Math.abs(m.vx)}
        if(m.x+rad>right){m.x=right-rad;m.vx=-Math.abs(m.vx)}
        if(m.y-rad<top){m.y=top+rad;m.vy=Math.abs(m.vy)}
        if(m.y+rad>bottom){m.y=bottom-rad;m.vy=-Math.abs(m.vy)}
      }
    }
    for(const m of state.molecules) drawGasMolecule(ctx,m,1);

    const tx = Math.min(W-86, pg.x+pg.w+105);
    drawThermometer(ctx,tx,pg.y+46,state.temp);
  }

  function drawChromateStage(W,H){
    const centerX = W*.45, topY = H*.15, beakerW=Math.min(390,W*.58), beakerH=Math.min(365,H*.70);
    const x = centerX - beakerW/2;
    const b=state.displayChromate.balance;
    const r = Math.round(235*(1-b)+246*b), gg=Math.round(104*(1-b)+218*b), bb=Math.round(34*(1-b)+70*b);

    ctx.save();
    drawRoundedRect(ctx, centerX-beakerW/2-18, topY-18, beakerW+36, beakerH+46,26,'rgba(255,255,255,.45)','#dbe7f1',1.5);
    // 비커 외곽: v4 형태로 복원
    ctx.strokeStyle='#8ea3b8'; ctx.lineWidth=6; ctx.lineCap='round'; ctx.lineJoin='round';
    ctx.beginPath();
    ctx.moveTo(centerX-beakerW/2, topY);
    ctx.lineTo(centerX-beakerW/2+26, topY+beakerH);
    ctx.lineTo(centerX+beakerW/2-26, topY+beakerH);
    ctx.lineTo(centerX+beakerW/2, topY);
    ctx.stroke();
    ctx.strokeStyle='#9fb0c2'; ctx.lineWidth=4;
    ctx.beginPath(); ctx.ellipse(centerX, topY, beakerW/2, 16,0,0,Math.PI*2); ctx.stroke();

    // 용액: 예전 버전처럼 사다리꼴 형태 + 잔잔한 수면으로 표시
    const liquidH = beakerH*.72;
    const liquidY = topY+beakerH-liquidH;
    const grd = ctx.createLinearGradient(0,liquidY,0,topY+beakerH);
    grd.addColorStop(0,`rgba(${r},${gg},${bb},.82)`);
    grd.addColorStop(1,`rgba(${Math.min(255,r+10)},${Math.min(255,gg+12)},${Math.min(255,bb+8)},.96)`);
    ctx.fillStyle=grd;
    ctx.beginPath();
    ctx.moveTo(centerX-beakerW/2+18,liquidY);
    ctx.bezierCurveTo(centerX-beakerW/4,liquidY-10,centerX+beakerW/4,liquidY+10,centerX+beakerW/2-18,liquidY);
    ctx.lineTo(centerX+beakerW/2-50,topY+beakerH-8);
    ctx.lineTo(centerX-beakerW/2+50,topY+beakerH-8);
    ctx.closePath(); ctx.fill();
    // 용액 영역 클리핑 뒤 정지된 이온 점 표시
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(centerX-beakerW/2+18,liquidY);
    ctx.bezierCurveTo(centerX-beakerW/4,liquidY-10,centerX+beakerW/4,liquidY+10,centerX+beakerW/2-18,liquidY);
    ctx.lineTo(centerX+beakerW/2-50,topY+beakerH-8);
    ctx.lineTo(centerX-beakerW/2+50,topY+beakerH-8);
    ctx.closePath(); ctx.clip();
    for(const d of state.staticDots){
      const px = centerX-beakerW*.34 + d.x*beakerW*.68;
      const py = liquidY + 22 + d.y*(liquidH-45);
      ctx.globalAlpha=.56;
      ctx.fillStyle = d.kind===0?'rgba(211,93,30,.72)':'rgba(255,238,80,.72)';
      ctx.beginPath(); ctx.arc(px,py,3.7+d.kind*.6,0,Math.PI*2); ctx.fill();
      ctx.globalAlpha=1;
    }
    ctx.restore();
    ctx.fillStyle='rgba(255,255,255,.32)';
    ctx.beginPath(); ctx.ellipse(centerX,liquidY,beakerW*.42,14,0,0,Math.PI*2); ctx.fill();

    // 비커 아래 상태 문구를 예전 방식으로 복원한다. 단, '중간 평형 색'은 '중간색'으로 단순화한다.
    const label = b>.66 ? 'CrO₄²⁻ 증가 · 노란색' : (b<.38 ? 'Cr₂O₇²⁻ 증가 · 주황색' : '중간색');
    ctx.fillStyle='#405066'; ctx.font='900 19px Segoe UI, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(label,centerX,topY+beakerH+34);

    drawThermometer(ctx,Math.min(W-82, centerX+beakerW/2+112), topY+24, state.temp);
    ctx.restore();
  }

  function chartPoints(now){
    const t = clamp((now - state.chart.start)/state.chart.duration,0,1);
    const pts = [];
    const ratePts=[];
    const maxN = 70;
    const shown = Math.max(2, Math.floor(maxN*t));
    for(let i=0;i<shown;i++){
      const p = i/(maxN-1);
      const e = ease(p);
      pts.push({x:p*5, q:lerp(state.chart.qStart,state.chart.qEnd,e), k:lerp(state.chart.kStart,state.chart.kEnd,e)});
      ratePts.push({x:p*5, f:lerp(state.chart.rfStart,state.chart.rfEnd,e), r:lerp(state.chart.rrStart,state.chart.rrEnd,e)});
    }
    if(t>=.985){
      pts.push({x:5,q:state.chart.qEnd,k:state.chart.kEnd});
      ratePts.push({x:5,f:state.chart.rfEnd,r:state.chart.rrEnd});
    }
    return {pts,ratePts,progress:t};
  }

  function drawLineChart(canvasCtx, canvas, series, config){
    const {w,h}=resizeCanvas(canvas);
    const g=canvasCtx; g.clearRect(0,0,w,h);
    // 아래쪽 범례와 x축 숫자가 겹치지 않도록 범례를 그래프 위쪽으로 이동했다.
    const pad={l:38,r:14,t:28,b:28};
    const xs=series.flatMap(s=>s.data.map(p=>p.x));
    const ys=series.flatMap(s=>s.data.map(p=>p.y));
    const xmin=0, xmax=5;
    let ymin=Math.min(...ys,0), ymax=Math.max(...ys,1);
    if(!isFinite(ymin)||!isFinite(ymax)||ymax-ymin<.001){ymin=0;ymax=1;}
    const range=ymax-ymin; ymin-=range*.15; ymax+=range*.15;
    const X = x => pad.l + (x-xmin)/(xmax-xmin)*(w-pad.l-pad.r);
    const Y = y => h-pad.b - (y-ymin)/(ymax-ymin)*(h-pad.t-pad.b);
    g.strokeStyle='#e1e8f1';g.lineWidth=1;
    g.fillStyle='#7b8798';g.font='11px Segoe UI, sans-serif';g.textAlign='right';g.textBaseline='middle';
    for(let i=0;i<4;i++){
      const yy=pad.t+i*(h-pad.t-pad.b)/3;
      g.beginPath();g.moveTo(pad.l,yy);g.lineTo(w-pad.r,yy);g.stroke();
      const val=ymax-(ymax-ymin)*i/3;
      g.fillText(fmt(val,2),pad.l-8,yy);
    }
    g.textAlign='center';g.textBaseline='top';
    for(let i=0;i<=5;i+=1){
      const xx=X(i);g.fillText(String(i),xx,h-pad.b+8);
    }
    for(const s of series){
      g.strokeStyle=s.color;g.lineWidth=s.width||2.5;g.beginPath();
      s.data.forEach((p,i)=>{ if(i===0)g.moveTo(X(p.x),Y(p.y)); else g.lineTo(X(p.x),Y(p.y)); });
      g.stroke();
      if(s.data.length){ const p=s.data[s.data.length-1]; g.fillStyle=s.color; g.beginPath(); g.arc(X(p.x),Y(p.y),4,0,Math.PI*2); g.fill(); }
    }
    if(config && config.eq){
      g.strokeStyle='rgba(14,116,212,.23)';g.setLineDash([5,5]);
      g.beginPath();g.moveTo(X(5),pad.t);g.lineTo(X(5),h-pad.b);g.stroke();g.setLineDash([]);
      g.fillStyle='#0e74d4';g.font='900 11px Segoe UI, sans-serif';g.textAlign='right';
      g.fillText('평형',w-pad.r,h-pad.b-16);
    }
    // legend: 그래프 상단에 작게 표시해서 x축 숫자와 겹치지 않게 한다.
    g.textBaseline='middle';g.textAlign='left';g.font='900 11px Segoe UI, sans-serif';
    let lx=pad.l+4, ly=13;
    const legendWidth = Math.min(118, w-pad.l-pad.r-8);
    drawRoundedRect(g,lx-6,ly-10,legendWidth,20,10,'rgba(255,255,255,.78)','#edf2f7',1);
    for(const s of series){g.fillStyle=s.color;g.fillRect(lx,ly-4,10,3);g.fillStyle='#59677a';g.fillText(s.name,lx+14,ly);lx+=52;}
  }

  function drawCharts(){
    const now=performance.now();
    const {pts,ratePts}=chartPoints(now);
    drawLineChart(qkCtx,$('qkChart'),[
      {name:'K', color:'#0d73d9', width:3, data:pts.map(p=>({x:p.x,y:p.k}))},
      {name:'Q', color:'#88c7ff', width:3, data:pts.map(p=>({x:p.x,y:p.q}))}
    ],{eq:true});
    drawLineChart(rateCtx,$('rateChart'),[
      {name:'정반응', color:'#0d73d9', width:3, data:ratePts.map(p=>({x:p.x,y:p.f}))},
      {name:'역반응', color:'#88c7ff', width:3, data:ratePts.map(p=>({x:p.x,y:p.r}))}
    ],{eq:true});
  }

  function updateAnim(){
    if(state.volumeAnim){
      const vt = clamp((performance.now()-state.volumeAnim.start)/state.volumeAnim.duration,0,1);
      state.displayVolume = lerp(state.volumeAnim.from,state.volumeAnim.to,ease(vt));
      if(vt>=1){state.displayVolume=state.volumeAnim.to;state.volumeAnim=null;}
    } else if(state.experiment==='gas') {
      state.displayVolume = state.volume;
    }
    if(!state.anim) return;
    const t = clamp((performance.now()-state.anim.startT)/state.anim.duration,0,1);
    const e = ease(t);
    if(state.anim.type==='gas'){
      state.displayGas.no2 = lerp(state.anim.start.no2,state.anim.target.no2,e);
      state.displayGas.n2o4 = lerp(state.anim.start.n2o4,state.anim.target.n2o4,e);
      if(t>=1){ state.gas={...state.anim.target}; state.displayGas={...state.anim.target}; state.anim=null; }
    } else {
      state.displayChromate.balance = lerp(state.anim.start.balance,state.anim.target.balance,e);
      state.displayChromate.h = lerp(state.anim.start.h,state.anim.target.h,e);
      if(t>=1){ state.chromate.balance=state.anim.target.balance; state.chromate.h=state.anim.target.h; state.displayChromate={...state.anim.target}; state.anim=null; }
    }
  }

  function updateUI(){
    $('tempVal').textContent=Math.round(state.temp);
    $('pressureVal').textContent=fmt(state.pressure,2);
    $('volumeVal').textContent=fmt(state.volume,2);
    $('gasAmountVal').textContent=fmt(Number($('gasAmount').value),2);
    $('chromateAmountVal').textContent=fmt(Number($('chromateAmount').value),2);
    $('vesselBox').classList.toggle('hidden',state.experiment==='chromate');
    $('pressureGroup').classList.toggle('hidden',state.experiment==='chromate');
    $('volumeGroup').classList.toggle('hidden',state.experiment==='chromate');
    $('gasControls').classList.toggle('hidden',state.experiment!=='gas');
    $('chromateControls').classList.toggle('hidden',state.experiment!=='chromate');

    if(state.experiment==='gas'){
      $('leftEquation').textContent='2NO₂(g) ⇌ N₂O₄(g)';
      $('stageTitle').textContent='2NO₂(g) ⇌ N₂O₄(g)';
      $('containerNote').textContent='';
      $('legend').innerHTML='<span class="legend-chip"><span class="legend-dot" style="background:#d97836"></span>NO₂ 적갈색</span><span class="legend-chip"><span class="legend-dot" style="background:#eef5ff;border:1px solid #7d8ea1"></span>N₂O₄ 무색</span>' + (state.inert>0.01 ? '<span class="legend-chip"><span class="legend-dot" style="background:#d8efff;border:1px solid #5791be"></span>H₂ 비활성</span>' : '');
      const K=gasK(), Q=gasQ(), dir=directionFrom(Q,K), V=effectiveVolume();
      $('kVal').textContent=fmt(K,2); $('qVal').textContent=fmt(Q,2); $('directionVal').textContent=dir; $('currentVolVal').textContent=fmt(V,2)+' L';
      const no2Frac=state.displayGas.no2/(state.displayGas.no2+state.displayGas.n2o4+1e-6);
      $('badges').innerHTML=`<span class="badge">${dir==='정반응'?'N₂O₄ 생성 증가':dir==='역반응'?'NO₂ 생성 증가':'K = Q 평형'}</span><span class="badge">NO₂ 비율 ${(no2Frac*100).toFixed(0)}%</span>${state.inert>0.01?`<span class="badge">H₂ ${fmt(state.inert,2)} mol</span>`:''}`;
      $('formula').innerHTML='<b>계산식</b><br><code>2NO₂(g) ⇌ N₂O₄(g)</code><br><code>K = [N₂O₄] / [NO₂]²</code><br><code>Q = [N₂O₄]현재 / [NO₂]현재²</code>';
      const eq=state.targetGas; const rows=[
        ['NO₂', state.displayGas.no2, eq.no2, state.displayGas.no2/V], ['N₂O₄', state.displayGas.n2o4, eq.n2o4, state.displayGas.n2o4/V]
      ];
      $('tableBody').innerHTML=rows.map(r=>`<tr><td>${r[0]}</td><td>${fmt(r[1],3)} mol</td><td>${fmt(r[2],3)} mol</td><td>${fmt(r[3],3)} M</td></tr>`).join('') + (state.inert>0.01 ? `<tr><td>H₂</td><td>${fmt(state.inert,3)} mol</td><td>${fmt(state.inert,3)} mol</td><td>비활성</td></tr>` : '');
      $('caption').innerHTML='<span class="caption-pill">피스톤 위치가 조건 변화에 따라 이동합니다.</span>';
    } else {
      $('leftEquation').textContent='Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺';
      $('stageTitle').textContent='Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)';
      $('containerNote').textContent='';
      $('legend').innerHTML='<span class="legend-chip"><span class="legend-dot" style="background:#df7b32"></span>Cr₂O₇²⁻ 주황색</span><span class="legend-chip"><span class="legend-dot" style="background:#f7d84d"></span>CrO₄²⁻ 노란색</span>';
      const K=chromateK(), Q=chromateQ(), dir=directionFrom(Q,K), b=state.displayChromate.balance;
      $('kVal').textContent=fmt(K,2); $('qVal').textContent=fmt(Q,2); $('directionVal').textContent=dir; $('currentVolVal').textContent='비커';
      $('badges').innerHTML=`<span class="badge">${b>.66?'CrO₄²⁻ 증가':b<.38?'Cr₂O₇²⁻ 증가':'중간색'}</span>`;
      $('formula').innerHTML='<b>계산식</b><br><code>Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺</code><br><code>산성: H⁺ 증가 → 왼쪽 이동</code><br><code>염기성: H⁺ 감소 → 오른쪽 이동</code>';
      const orange=(1-b), yellow=b;
      $('tableBody').innerHTML=`<tr><td>Cr₂O₇²⁻</td><td>${fmt(orange,2)}</td><td>${fmt(1-state.targetChromate.balance,2)}</td><td>주황색</td></tr><tr><td>CrO₄²⁻</td><td>${fmt(yellow,2)}</td><td>${fmt(state.targetChromate.balance,2)}</td><td>노란색</td></tr><tr><td>H⁺</td><td>${fmt(state.displayChromate.h,2)}</td><td>${fmt(state.targetChromate.h,2)}</td><td>산성도</td></tr>`;
      $('caption').innerHTML='';
    }
  }

  function animate(){
    updateAnim();
    updateUI();
    drawStage();
    drawCharts();
    requestAnimationFrame(animate);
  }

  function resetGas(){
    state.temp=43;state.pressure=1;state.volume=2.5;state.displayVolume=2.5;state.inert=0;state.vessel='cylinder';
    state.gas={no2:.80,n2o4:2.20};state.displayGas={...state.gas};
    document.querySelector('input[name="vessel"][value="cylinder"]').checked=true;
    $('temp').value=state.temp;$('pressure').value=state.pressure;$('volume').value=state.volume;
    startTransition(solveGasEquilibrium(state.gas));
  }
  function resetChromate(){
    state.temp=43;state.chromate={balance:.58,h:1.0,dilution:0};state.displayChromate={balance:.58,h:1.0};
    $('temp').value=state.temp;
    startTransition(solveChromateEquilibrium(state.chromate));
  }

  $('experiment').addEventListener('change', e=>{
    state.experiment=e.target.value;
    if(state.experiment==='gas') startTransition(solveGasEquilibrium(state.displayGas));
    else startTransition(solveChromateEquilibrium(state.chromate));
  });
  document.querySelectorAll('input[name="vessel"]').forEach(r=>r.addEventListener('change',e=>{state.vessel=e.target.value;applyConditionChange();}));
  $('temp').addEventListener('input',e=>{state.temp=Number(e.target.value);applyConditionChange();});
  $('pressure').addEventListener('input',e=>{state.pressure=Number(e.target.value);applyConditionChange();});
  $('volume').addEventListener('input',e=>{state.volume=Number(e.target.value);state.displayVolume=state.volume;state.volumeAnim=null;applyConditionChange();});
  $('gasAmount').addEventListener('input',updateUI);
  $('chromateAmount').addEventListener('input',updateUI);
  $('moleculeMotion').addEventListener('change',e=>{state.motion=e.target.checked;});
  $('applyGas').addEventListener('click',()=>{
    const amt=Number($('gasAmount').value); const act=$('gasAction').value;
    let src={...state.displayGas};
    const beforeVol = state.volume;
    if(act==='addNO2') src.no2+=amt;
    if(act==='removeNO2') src.no2=Math.max(.04,src.no2-amt);
    if(act==='addN2O4') src.n2o4+=amt;
    if(act==='removeN2O4') src.n2o4=Math.max(.04,src.n2o4-amt);
    if(act==='addInert') state.inert=clamp(state.inert+amt,0,4.0);

    if(state.vessel==='cylinder'){
      let delta=0;
      if(act==='addNO2') delta=amt*.46;
      if(act==='addN2O4') delta=amt*.34;
      if(act==='addInert') delta=amt*.70;
      if(act==='removeNO2') delta=-amt*.34;
      if(act==='removeN2O4') delta=-amt*.25;
      if(delta!==0) setVolumeAnimated(beforeVol+delta);
    }
    state.gas={...src};state.displayGas={...src};
    startTransition(solveGasEquilibrium(src));
  });
  $('resetGas').addEventListener('click',resetGas);
  $('applyChromate').addEventListener('click',()=>{
    const amt=Number($('chromateAmount').value); const act=$('chromateAction').value;
    if(act==='hcl') state.chromate.h=clamp(state.chromate.h + amt*1.25,.15,2.8);
    if(act==='naoh') state.chromate.h=clamp(state.chromate.h - amt*1.35,.15,2.8);
    if(act==='water'){ state.chromate.h=clamp(state.chromate.h - amt*.18,.15,2.8); state.chromate.dilution=clamp(state.chromate.dilution+amt*.45,0,1.2); }
    startTransition(solveChromateEquilibrium(state.chromate));
  });
  $('resetChromate').addEventListener('click',resetChromate);

  if(!CanvasRenderingContext2D.prototype.roundRect){
    CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){
      this.beginPath();this.moveTo(x+r,y);this.lineTo(x+w-r,y);this.quadraticCurveTo(x+w,y,x+w,y+r);this.lineTo(x+w,y+h-r);this.quadraticCurveTo(x+w,y+h,x+w-r,y+h);this.lineTo(x+r,y+h);this.quadraticCurveTo(x,y+h,x,y+h-r);this.lineTo(x,y+r);this.quadraticCurveTo(x,y,x+r,y);return this;
    }
  }

  makeMolecules();makeStaticDots();
  window.addEventListener('resize',()=>{drawStage();drawCharts();});
  startTransition(solveGasEquilibrium(state.gas));
  animate();
})();
</script>
</body>
</html>
'''

components.html(APP_HTML, height=870, scrolling=False)
