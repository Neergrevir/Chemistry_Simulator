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
  input[type=range]:disabled{opacity:.45;cursor:not-allowed;filter:grayscale(.35);}
  .fixed-control{opacity:.78;}
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

  /* 화면 폭이 충분한 태블릿 가로 화면에서는 PC처럼 조건·실험·결과를 동시에 보되, UI를 압축한다. */
  .mobile-tabs{display:none;gap:7px;grid-template-columns:1fr 1fr 1fr;}
  .mobile-tab{height:38px;border-radius:14px;background:#ffffff;color:#42516a;border:1px solid #d7e6f6;box-shadow:0 8px 18px rgba(89,114,148,.10);font-size:13px;font-weight:950;}
  .mobile-tab.active{background:#192235;color:#ffffff;border-color:#192235;}

  @media (min-width:900px) and (max-width:1200px) and (orientation:landscape) and (min-height:620px){
    html,body{overflow:hidden;touch-action:manipulation;}
    .app{height:860px;padding:8px;gap:7px;overflow:hidden;background:linear-gradient(160deg,#fffaf4 0%,#f2fbff 46%,#f8f7ff 100%);}
    .topbar{grid-template-columns:minmax(255px,300px) minmax(0,1fr);gap:8px;min-height:52px;}
    .title-card{padding:9px 11px;border-radius:18px;min-height:52px;}
    .logo{font-size:22px;}
    h1{font-size:20px;letter-spacing:-.95px;}
    .select-card{padding:8px 10px;border-radius:18px;gap:8px;}
    .select-label{font-size:12.3px;}
    .experiment-select{height:34px;border-radius:10px;font-size:11.5px;padding:0 8px;}
    .mobile-tabs{display:none !important;}
    .main{display:grid;grid-template-columns:minmax(218px,245px) minmax(0,1.02fr) minmax(0,1.12fr);gap:8px;flex:1;min-height:0;overflow:hidden;}
    .panel{padding:9px;overflow:hidden;border-radius:20px;}
    .stage-card{padding:9px;overflow:hidden;border-radius:20px;}
    .result-card{padding:9px;overflow:hidden;border-radius:20px;}
    .panel-scroll{height:100%;overflow:auto;padding-right:4px;}
    .panel h2,.result-card h2{font-size:18px;margin-bottom:7px;line-height:1.12;}
    .control-section{padding:8px;margin-bottom:7px;border-radius:14px;}
    .section-title{font-size:12.4px;margin-bottom:6px;}
    .equation-pill{font-size:11.7px;padding:6px 7px;border-radius:10px;}
    label.radio{font-size:12px;gap:5px;line-height:1.25;}
    .radio-row{gap:5px;margin:6px 0 7px;}
    .range-wrap{margin:8px 0;}
    .range-label{font-size:11.4px;margin-bottom:3px;}
    input[type=range]{height:22px;}
    .inline-select{height:34px;font-size:12px;border-radius:9px;}
    .button-row{gap:6px;margin-top:6px;}
    button{height:34px;font-size:12px;border-radius:10px;}
    .small-check{font-size:11.7px;margin-top:6px;line-height:1.3;}
    .stage-head{margin-bottom:6px;gap:5px;}
    .stage-title{font-size:14px;line-height:1.18;letter-spacing:-.55px;}
    .legend{gap:4px;}
    .legend-chip{font-size:9.8px;padding:4px 6px;}
    .legend-dot{width:7px;height:7px;margin-right:3px;}
    .stage-canvas-wrap{flex:1;min-height:0;border-radius:18px;}
    .stage-caption{bottom:7px;gap:5px;}
    .caption-pill{font-size:10.5px;padding:5px 8px;}
    .result-grid{grid-template-columns:1fr 1fr;gap:6px;margin-bottom:7px;}
    .metric{padding:7px;border-radius:12px;}
    .metric .label{font-size:10.7px;margin-bottom:3px;}
    .metric .value{font-size:14.5px;}
    .badges{gap:5px;margin:4px 0 7px;}
    .badge{font-size:10.6px;padding:5px 7px;}
    .formula{font-size:10.9px;line-height:1.35;padding:7px;margin-bottom:7px;border-radius:12px;}
    .formula code{font-size:10.6px;}
    .mini-table{font-size:10.5px;margin-bottom:7px;border-radius:11px;}
    .mini-table th,.mini-table td{padding:4px 4px;}
    .chart-grid{grid-template-columns:1fr;gap:7px;}
    .chart-card{padding:6px 7px;border-radius:13px;}
    .chart-title{font-size:11.8px;margin-bottom:1px;}
    canvas.chart{height:124px;}
  }

  /* 아이폰, 아이패드 세로 화면, 또는 높이가 낮은 가로 화면에서는 탭을 사용한다. */
  @media (max-width:899px), (min-width:900px) and (max-width:1200px) and (orientation:portrait), (max-width:1200px) and (max-height:619px){
    html,body{overflow:hidden;touch-action:manipulation;}
    .app{height:860px;padding:10px;gap:8px;overflow:hidden;background:linear-gradient(160deg,#fffaf4 0%,#f2fbff 46%,#f8f7ff 100%);}
    .topbar{grid-template-columns:1fr;gap:8px;min-height:0;}
    .title-card{padding:10px 12px;border-radius:18px;min-height:54px;}
    .logo{font-size:22px;}
    h1{font-size:21px;letter-spacing:-.9px;}
    .select-card{padding:9px 10px;border-radius:18px;display:grid;grid-template-columns:74px 1fr;align-items:center;gap:8px;}
    .select-label{font-size:12.5px;}
    .experiment-select{height:35px;border-radius:10px;font-size:11.7px;padding:0 8px;}
    .mobile-tabs{display:grid;}
    .main{display:block;flex:1;min-height:0;overflow:hidden;}
    .main > .panel,.main > .stage-card,.main > .result-card{height:100%;min-height:0;border-radius:20px;padding:10px;display:none;overflow:hidden;}
    .main[data-mobile-tab="control"] > .panel{display:block;}
    .main[data-mobile-tab="stage"] > .stage-card{display:flex;}
    .main[data-mobile-tab="result"] > .result-card{display:block;overflow:auto;}
    .panel-scroll{height:100%;overflow:auto;padding-right:4px;}
    .panel h2,.result-card h2{font-size:20px;margin-bottom:8px;}
    .control-section{padding:10px;margin-bottom:8px;border-radius:15px;}
    .equation-pill{font-size:12.5px;padding:7px 8px;}
    label.radio{font-size:13px;}
    .range-wrap{margin:10px 0;}
    .range-label{font-size:12.3px;}
    input[type=range]{height:26px;}
    .inline-select{height:38px;font-size:13px;}
    button{height:39px;font-size:13px;}
    .stage-head{margin-bottom:7px;}
    .stage-title{font-size:15.5px;}
    .legend{gap:5px;}
    .legend-chip{font-size:10.5px;padding:5px 7px;}
    .stage-canvas-wrap{height:calc(100% - 45px);min-height:0;border-radius:20px;}
    .result-grid{grid-template-columns:1fr 1fr;gap:7px;margin-bottom:8px;}
    .metric{padding:8px;border-radius:13px;}
    .metric .label{font-size:11.5px;}
    .metric .value{font-size:16px;}
    .badges{gap:6px;margin:5px 0 8px;}
    .badge{font-size:11.5px;padding:6px 8px;}
    .formula{font-size:11.8px;line-height:1.45;padding:8px;margin-bottom:8px;}
    .formula code{font-size:11.5px;}
    .mini-table{font-size:11.2px;margin-bottom:8px;}
    .mini-table th,.mini-table td{padding:5px 5px;}
    .chart-grid{grid-template-columns:1fr;gap:8px;}
    .chart-card{padding:7px 8px;border-radius:14px;}
    .chart-title{font-size:12.8px;}
    canvas.chart{height:132px;}
  }
  @media (max-width:430px){
    .app{height:850px;padding:7px;}
    .select-card{grid-template-columns:1fr;gap:5px;}
    .experiment-select{font-size:11px;}
    .mobile-tab{height:36px;font-size:12.5px;}
    .result-grid{grid-template-columns:1fr 1fr;}
    canvas.chart{height:122px;}
  }

  /* 화면 규칙
     - PC 넓은 화면: 기본 3단 레이아웃
     - 아이패드 가로: 축소 3단 레이아웃
     - 아이패드 세로 / 아이폰 / 낮은 가로 화면: 탭 레이아웃 */
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
        <option value="chromate">다이크로뮴산 ↔ 크로뮴산  |  Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)</option>
      </select>
    </div>
  </div>

  <div class="mobile-tabs" aria-label="모바일 화면 전환">
    <button type="button" class="mobile-tab" data-tab="control">조건</button>
    <button type="button" class="mobile-tab active" data-tab="stage">실험</button>
    <button type="button" class="mobile-tab" data-tab="result">결과</button>
  </div>

  <div class="main" id="main" data-mobile-tab="stage">
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
            <div class="range-label"><span>용기 부피 (L)</span><span id="volumeVal" class="range-value">2</span></div>
            <select id="volume" class="inline-select" aria-label="용기 부피 선택">
              <option value="1">1 L</option>
              <option value="2" selected>2 L</option>
              <option value="3">3 L</option>
              <option value="4">4 L</option>
            </select>
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
            <option value="addInert">헬륨(He) 첨가</option>
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
          <div id="hclConcGroup" class="range-wrap">
            <div class="range-label"><span>HCl 수용액 몰농도 (M)</span><span id="hclConcVal" class="range-value">1.00</span></div>
            <input id="hclConc" type="range" min="0.10" max="3.00" step="0.10" value="1.00" />
          </div>
          <div id="naohConcGroup" class="range-wrap">
            <div class="range-label"><span>NaOH 수용액 몰농도 (M)</span><span id="naohConcVal" class="range-value">1.00</span></div>
            <input id="naohConc" type="range" min="0.10" max="3.00" step="0.10" value="1.00" />
          </div>
          <div id="reagentVolumeInfo" class="range-wrap">
            <div class="range-label"><span>한 번에 첨가되는 수용액 부피</span><span class="range-value">0.10 L</span></div>
          </div>
          <div id="chromateAmountGroup" class="range-wrap hidden">
            <div class="range-label"><span id="chromateAmountLabel">첨가 물의 부피 (L)</span><span id="chromateAmountVal" class="range-value">0.10</span></div>
            <input id="chromateAmount" type="range" min="0.05" max="0.50" step="0.05" value="0.10" />
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


  function setMobileTab(tab){
    const main = $('main');
    if(!main) return;
    main.setAttribute('data-mobile-tab', tab);
    document.querySelectorAll('.mobile-tab').forEach(btn=>{
      btn.classList.toggle('active', btn.dataset.tab===tab);
    });
    // 숨겨져 있던 캔버스는 다시 보이는 순간 크기를 다시 읽어야 선명하게 그려진다.
    setTimeout(()=>{ drawStage(); drawCharts(); }, 60);
  }
  document.querySelectorAll('.mobile-tab').forEach(btn=>{
    btn.addEventListener('click',()=>setMobileTab(btn.dataset.tab));
  });

  const state = {
    experiment:'gas', vessel:'cylinder', temp:43, pressure:1.0, volume:2.0, displayVolume:2.0, inert:0.0, displayInert:0.0, inertAnim:null, hePistonAnim:null, pistonVisualVolume:null,
    gas:{no2:0.80, n2o4:2.20},
    chromate:{balance:0.58, h:1.0, dilution:0.0, netAcid:0.05, solutionVolume:1.00},
    displayGas:{no2:0.80, n2o4:2.20},
    displayChromate:{balance:0.58, h:1.0, dilution:0.0, netAcid:0.05, solutionVolume:1.00},
    targetGas:{no2:0.80,n2o4:2.20},
    targetChromate:{balance:0.58,h:1.0,dilution:0.0,netAcid:0.05,solutionVolume:1.00},
    anim:null,
    volumeAnim:null,
    volumePulse:null,
    steelResetUntil:0,
    referenceGasTotal:3.00,
    referenceTempK:273 + 43,
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

  const INITIAL_GAS_TOTAL = 3.00;
  const BASE_TEMP_K = 273 + 43;
  const PISTON_VISUAL_GAIN_HE = 4.8;
  const PISTON_VISUAL_GAIN_EQUILIBRIUM = 5.6;
  function activeGasTotal(g=state.displayGas, inertAmount=(state.displayInert ?? state.inert)){
    return Math.max(0.05, g.no2 + g.n2o4 + inertAmount);
  }
  function effectiveVolume(g=state.displayGas, rawVolume=state.volume, inertAmount=(state.displayInert ?? state.inert)){
    if(state.experiment==='chromate') return 3.40;
    if(state.vessel==='steel') return rawVolume;
    // 일정 외부 압력의 실린더에서는 V ∝ nT/P이다.
    // He는 반응식에는 들어가지 않지만 전체 기체 몰수에는 포함되므로,
    // 첨가량만큼 부피가 자연스럽게 증가한다.
    const reference = Math.max(0.05, state.referenceGasTotal || INITIAL_GAS_TOTAL);
    const molFactor = activeGasTotal(g, inertAmount) / reference;
    const tempFactor = (273 + state.temp) / Math.max(1,state.referenceTempK || BASE_TEMP_K);
    const pressureFactor = Math.max(0.25, state.pressure);
    return clamp(rawVolume * molFactor * tempFactor / pressureFactor, .55, 4.60);
  }
  function visualEffectiveVolume(){
    const v = state.displayVolume ?? state.volume;
    if(state.experiment==='chromate') return 3.40;
    if(state.vessel==='steel') return v;

    // He 첨가 직후의 1차 팽창과, 이후 역반응으로 인한 2차 팽창을 분리해서 보여준다.
    // 계산에 쓰이는 실제 부피는 effectiveVolume()을 그대로 사용하고,
    // 피스톤 그림에만 즉시 팽창 부피 → 최종 평형 부피 보간값을 사용한다.
    if(state.hePistonAnim){
      const t=clamp((performance.now()-state.hePistonAnim.start)/state.hePistonAnim.duration,0,1);
      const shown=lerp(state.hePistonAnim.from,state.hePistonAnim.to,ease(t));
      if(t>=1){
        state.pistonVisualVolume=state.hePistonAnim.to;
        state.hePistonAnim=null;
      }
      return shown;
    }
    if(Number.isFinite(state.pistonVisualVolume)) return state.pistonVisualVolume;
    return effectiveVolume(state.displayGas, v, state.displayInert ?? state.inert);
  }
  function setVolumeAnimated(newVolume, duration=900){
    const from = state.displayVolume ?? state.volume;
    const to = clamp(newVolume, 1.00, 4.00);
    state.volume = to;
    $('volume').value = to;
    state.volumeAnim = {from, to, start:performance.now(), duration};
  }
  function triggerGasDensityPulse(compressionSignal, duration=1650, maxAmount=.15){
    if(state.experiment!=='gas') return;
    if(!Number.isFinite(compressionSignal) || Math.abs(compressionSignal)<0.0001) return;
    // compressionSignal > 0 : 압축/압력 증가 → NO₂ 농도 순간 증가 → 잠깐 진해짐
    // compressionSignal < 0 : 팽창/압력 감소 → NO₂ 농도 순간 감소 → 잠깐 옅어짐
    // 슬라이더가 0.01 단위로 움직여도 눈에 보이도록 제곱근으로 감도를 높인다.
    // 순간 색 변화는 실제 농도 변화의 느낌만 주도록 작게 제한한다.
    const signedStrength = Math.sign(compressionSignal) * clamp(Math.sqrt(Math.abs(compressionSignal)), 0, 1);
    state.volumePulse = {amount:signedStrength*maxAmount, start:performance.now(), duration};
  }
  function animatePistonByEquilibrium(startGas,targetGas){
    if(state.experiment!=='gas' || state.vessel!=='cylinder') return;
    // 평형 이동에 따른 피스톤 움직임은 state.volume을 직접 바꾸지 않는다.
    // state.volume을 바꿔 버리면 이미 계산한 평형 조성과 다른 부피가 적용되어 K와 Q가 어긋난다.
    // 대신 drawStage → visualEffectiveVolume()이 displayGas의 전체 몰수 변화를 읽어
    // V ∝ nT/P 방식으로 피스톤 위치를 자연스럽게 움직이게 한다.
  }
  function gasK(temp=state.temp){
    // 2NO2 -> N2O4는 발열 반응이므로 온도가 높을수록 K가 작아지도록 설정한다.
    return clamp(4.4 * Math.exp((40-temp)/34), 0.18, 18.0);
  }
  function gasQ(g=state.displayGas, vol=null, inertAmount=(state.displayInert ?? state.inert)){
    if(vol===null) vol=effectiveVolume(g,state.volume,inertAmount);
    const cNO2 = Math.max(g.no2/vol, 1e-6);
    const cN2O4 = Math.max(g.n2o4/vol, 1e-6);
    return cN2O4/(cNO2*cNO2);
  }
  function solveGasEquilibriumAtFixedVolume(sourceGas, fixedVolume){
    const K = gasK();
    const total = Math.max(sourceGas.no2 + 2*sourceGas.n2o4, .08);
    let lo=0, hi=total/2-1e-5;
    for(let i=0;i<90;i++){
      const b=(lo+hi)/2;
      const a=Math.max(total-2*b,1e-7);
      const val = b*fixedVolume/(a*a);
      if(val < K) lo=b; else hi=b;
    }
    const n2o4=(lo+hi)/2;
    return {no2:Math.max(total-2*n2o4,0.0001), n2o4:Math.max(n2o4,0.0001)};
  }

  function solveGasEquilibrium(sourceGas){
    const K = gasK();
    const total = Math.max(sourceGas.no2 + 2*sourceGas.n2o4, .08);
    let lo=0, hi=total/2-1e-5;
    for(let i=0;i<90;i++){
      const b=(lo+hi)/2;
      const a=Math.max(total-2*b,1e-7);
      // 피스톤 용기에서는 부피가 최종 평형 조성의 전체 몰수에 따라 달라진다.
      // 따라서 sourceGas의 부피를 고정해서 풀면 최종 표시 Q가 K와 달라질 수 있다.
      const trialGas = {no2:a, n2o4:b};
      const V = effectiveVolume(trialGas, state.volume, state.inert);
      const val = b*V/(a*a);
      if(val < K) lo=b; else hi=b;
    }
    const n2o4=(lo+hi)/2;
    return {no2:Math.max(total-2*n2o4,0.0001), n2o4:Math.max(n2o4,0.0001)};
  }
  function acidityIndex(netAcid, solutionVolume){
    const v=Math.max(0.05,solutionVolume||1);
    const netConc=netAcid/v;
    // 양수면 산성, 0이면 중성 부근, 음수면 염기성이다.
    return clamp(1 + netConc/0.20, 0.05, 2.80);
  }
  function chromateSpecies(ch=state.displayChromate){
    const net=Number.isFinite(ch.netAcid)?ch.netAcid:0;
    return {hMol:Math.max(net,0), ohMol:Math.max(-net,0)};
  }

  // balance가 1만큼 증가하는 것은 정반응 진행량의 시각적 지표이다.
  // 정반응 1회마다 H⁺가 2 mol 생성되므로 H⁺/OH⁻ 몰수도 함께 바뀐다.
  const CHROMATE_REACTION_POOL = 0.25;

  function chromateK(){
    // 평형상수 K는 온도가 같으면 일정해야 한다.
    // H₂O, HCl, NaOH 첨가는 Q와 조성만 바꾸고 K 자체는 바꾸지 않는다.
    return clamp(2.4 + state.temp/45, 1.2, 8.4);
  }
  function chromateHFactor(){ return 1.30; }
  function chromateDilutionFactor(){ return 1.05; }
  function chromateQ(ch=state.displayChromate){
    // 교육용 표현: HCl/NaOH/H₂O로 H⁺ 또는 희석 정도가 변하면 Q가 먼저 달라지고,
    // 이후 balance가 이동하면서 같은 온도의 K와 다시 만나도록 맞춘다.
    const dilution = Number.isFinite(ch.dilution) ? ch.dilution : (state.chromate.dilution || 0);
    return 1.05 + ch.balance*5.7 + (ch.h-1)*chromateHFactor() - dilution*chromateDilutionFactor();
  }
  function solveChromateEquilibrium(source){
    // 평형 이동에 따라 크로메이트/다이크로메이트 조성뿐 아니라 H⁺도 함께 변한다.
    // 정반응이면 H⁺가 생성되고 역반응이면 H⁺가 소비된다.
    const K = chromateK();
    const dilution = Number.isFinite(source.dilution) ? source.dilution : (state.chromate.dilution || 0);
    const volume = Math.max(0.05, source.solutionVolume || 1);
    const startBalance = clamp(source.balance,0.08,0.94);
    const startNetAcid = Number.isFinite(source.netAcid) ? source.netAcid : 0;

    function candidateAt(balance){
      const reactionExtent = (balance-startBalance)*CHROMATE_REACTION_POOL;
      const netAcid = startNetAcid + 2*reactionExtent;
      const h = acidityIndex(netAcid,volume);
      const candidate={balance,h,dilution,netAcid,solutionVolume:volume};
      return {candidate,q:chromateQ(candidate)};
    }

    let lo=0.08, hi=0.94;
    for(let i=0;i<90;i++){
      const mid=(lo+hi)/2;
      const {q}=candidateAt(mid);
      if(q<K) lo=mid; else hi=mid;
    }
    return candidateAt((lo+hi)/2).candidate;
  }

  function startTransition(target, reason='condition'){
    const now = performance.now();
    const duration = 5000;
    if(state.experiment==='gas'){
      const start = {...state.displayGas};
      state.targetGas = {...target};
      state.anim = {type:'gas', reason, start, target:{...target}, startT:now, duration};
      const q0 = gasQ(start), k1 = gasK(), q1 = gasQ(target,null,state.inert), rf0 = rateForwardGas(start), rr0 = rateReverseGas(start);
      const rf1 = rateForwardGas(target,state.inert), rr1 = rateReverseGas(target,state.inert);
      state.chart = {qStart:q0, qEnd:q1, kStart:k1, kEnd:k1, rfStart:rf0, rfEnd:(rf1+rr1)/2, rrStart:rr0, rrEnd:(rf1+rr1)/2, start:now, duration};
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
    if(state.experiment==='gas' && !state.hePistonAnim) state.pistonVisualVolume=null;
    if(state.experiment==='gas') startTransition(solveGasEquilibrium(state.displayGas));
    else startTransition(solveChromateEquilibrium(state.chromate));
  }

  function rateForwardGas(g=state.displayGas, inertAmount=(state.displayInert ?? state.inert)){
    const c = Math.max(g.no2/effectiveVolume(g,state.volume,inertAmount),0.001);
    return clamp(0.11 + c*c*0.72 + state.temp/850, .03, 2.2);
  }
  function rateReverseGas(g=state.displayGas, inertAmount=(state.displayInert ?? state.inert)){
    const c = Math.max(g.n2o4/effectiveVolume(g,state.volume,inertAmount),0.001);
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
    } else if(m.kind==='he'){
      // 헬륨은 단원자 기체이므로 원자 하나로 표시한다.
      g.strokeStyle='rgba(87,145,190,.62)'; g.lineWidth=1.8; g.fillStyle='#d8efff';
      g.beginPath(); g.arc(m.x,m.y,m.r*.72*scale,0,Math.PI*2); g.fill(); g.stroke();
      g.fillStyle='rgba(255,255,255,.72)';
      g.beginPath(); g.arc(m.x-m.r*.20,m.y-m.r*.20,m.r*.16*scale,0,Math.PI*2); g.fill();
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

  function drawColorScaleBelowThermometer(g,cx,y,w,t,mode){
    const value=clamp(t,0,1);
    const isGas=mode==='gas';
    const leftColor=isGas ? '#f7fbff' : '#df7b32';
    const rightColor=isGas ? '#9f5e35' : '#f8dc55';
    const leftLabel=isGas ? '옅음' : '주황색';
    const rightLabel=isGas ? '진함' : '노란색';
    const stateLabel=isGas
      ? (value<.34 ? '옅은 갈색' : value<.67 ? '갈색' : '진한 갈색')
      : (value<.35 ? '주황색' : value<.65 ? '중간색' : '노란색');
    const h=13;
    const x=cx-w/2;
    const markerX=x+w*value;

    g.save();
    g.textAlign='center';
    g.textBaseline='middle';
    drawRoundedRect(g,x-12,y-20,w+24,62,15,'rgba(255,255,255,.88)','#d6e5f4',1);

    g.font='900 11.5px Segoe UI, sans-serif';
    g.fillStyle='#253248';
    g.fillText(stateLabel,cx,y-8);

    const grad=g.createLinearGradient(x,0,x+w,0);
    grad.addColorStop(0,leftColor);
    grad.addColorStop(1,rightColor);
    drawRoundedRect(g,x,y+4,w,h,7,grad,'#8f9dae',1.7);

    // 현재 색 위치 표시선. 원형 표식은 쓰지 않는다.
    g.strokeStyle='#253248';
    g.lineWidth=3;
    g.lineCap='round';
    g.beginPath();
    g.moveTo(markerX,y+1);
    g.lineTo(markerX,y+h+7);
    g.stroke();

    // 하단 글자는 흰 배경에서도 잘 보이도록 진한 색으로 고정한다.
    g.font='800 10.5px Segoe UI, sans-serif';
    g.fillStyle='#253248';
    g.fillText(leftLabel,x+8,y+31);
    g.fillText(rightLabel,x+w-8,y+31);
    g.restore();
  }

  function drawGasStage(W,H){
    const pg = pistonGeometry(W,H);
    const no2Frac = state.displayGas.no2/(state.displayGas.no2+state.displayGas.n2o4+1e-6);
    const VforColor = Math.max(effectiveVolume(state.displayGas), .5);
    const no2Conc = state.displayGas.no2 / VforColor;
    // 색은 단순 몰분율만이 아니라 부피 변화로 생기는 압력/농도 변화도 함께 반영한다.
    // 부피 감소 직후에는 NO₂ 농도 증가로 잠깐 더 진해지고,
    // 시간이 지나 평형이 오른쪽으로 이동하면 NO₂ 비율 감소가 반영되어 다시 옅어진다.
    const equilibriumBrown = .03 + Math.pow(clamp(no2Frac,0,1), .72) * .92;
    const concentrationBrown = .05 + clamp(no2Conc / 1.05, 0, 1) * .34;
    let pulseBrown = 0;
    if(state.volumePulse){
      const pt = clamp((performance.now()-state.volumePulse.start)/state.volumePulse.duration,0,1);
      pulseBrown = state.volumePulse.amount * 0.85 * (1-ease(pt));
      if(pt>=1) state.volumePulse=null;
    }
    const rawBrownAlpha = equilibriumBrown*.78 + concentrationBrown*.22 + pulseBrown;
    // NO₂ 색 변화가 눈에 더 잘 보이도록 색 표현만 약 30% 강화한다.
    // K, Q, 농도 계산에는 영향을 주지 않는다.
    const brownAlpha = clamp(.08 + (rawBrownAlpha-.08)*1.30, .06, .90);
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
    const amountScale = clamp((activeGasTotal(state.displayGas)/Math.max(state.referenceGasTotal,0.05))*(state.volume/2), .28, 2.25);
    const no2Need = Math.round(clamp((10 + no2Frac*32)*amountScale, 3, 72));
    const n2o4Need = Math.round(clamp((8 + (1-no2Frac)*22)*amountScale, 2, 55));
    const heNeed = Math.round(clamp((state.displayInert ?? state.inert)*14*amountScale, 0, 42));
    let desired = no2Need + n2o4Need + heNeed;
    while(state.molecules.length<desired){
      state.molecules.push({kind:'no2',x:pg.x+45+Math.random()*(pg.w-90),y:pg.gasTop+25+Math.random()*(pg.gasBottom-pg.gasTop-50),vx:Math.random()*2-1,vy:Math.random()*2-1,r:7+Math.random()*2});
    }
    if(state.molecules.length>desired) state.molecules.length=desired;
    state.molecules.forEach((m,i)=>{m.kind = i<no2Need ? 'no2' : (i<no2Need+n2o4Need ? 'n2o4' : 'he');});

    if(state.motion){
      const tempSpeed = lerp(.45,2.75,state.temp/120);
      for(const m of state.molecules){
        m.x += m.vx*tempSpeed;
        m.y += m.vy*tempSpeed;
        const left=pg.x+34, right=pg.x+pg.w-34, top=(state.vessel==='cylinder'?pg.gasTop+15:pg.y+45), bottom=pg.gasBottom-18;
        const rad = m.kind==='no2' ? m.r : (m.kind==='he' ? m.r*.75 : m.r*1.7);
        if(m.x-rad<left){m.x=left+rad;m.vx=Math.abs(m.vx)}
        if(m.x+rad>right){m.x=right-rad;m.vx=-Math.abs(m.vx)}
        if(m.y-rad<top){m.y=top+rad;m.vy=Math.abs(m.vy)}
        if(m.y+rad>bottom){m.y=bottom-rad;m.vy=-Math.abs(m.vy)}
      }
    }
    for(const m of state.molecules) drawGasMolecule(ctx,m,1);

    const tx = Math.min(W-86, pg.x+pg.w+105);
    drawThermometer(ctx,tx,pg.y+46,state.temp);
    const gasScale = clamp((brownAlpha-.06)/(.90-.06),0,1);
    const gasScaleY = Math.min(H-52, pg.y+330);
    drawColorScaleBelowThermometer(ctx,tx,gasScaleY,96,gasScale,'gas');
  }

  function drawChromateStage(W,H){
    const centerX = W*.45, topY = H*.15, beakerW=Math.min(390,W*.58), beakerH=Math.min(365,H*.70);
    const b=state.displayChromate.balance;
    // 노란색 영역이 탁하게 묻히지 않도록 크로메이트 비율을 시각적으로 약간 강조한다.
    // 계산에 쓰이는 balance, K, Q는 그대로이며 캔버스 색 혼합에만 적용된다.
    const visualB=clamp(Math.pow(b,0.84),0,1);
    const r = Math.round(235*(1-visualB)+250*visualB), gg=Math.round(104*(1-visualB)+226*visualB), bb=Math.round(34*(1-visualB)+62*visualB);

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

    // 용액: 사다리꼴 형태 + 흔들리는 수면 애니메이션
    const liquidH = beakerH*.72;
    const liquidY = topY+beakerH-liquidH;
    const leftTop = centerX-beakerW/2+18;
    const rightTop = centerX+beakerW/2-18;
    const bottomRight = centerX+beakerW/2-50;
    const bottomLeft = centerX-beakerW/2+50;
    const bottomY = topY+beakerH-8;
    const now = performance.now();
    const transitionT = state.anim && state.anim.type==='chromate' ? clamp((now-state.anim.startT)/state.anim.duration,0,1) : 1;
    const settling = state.anim && state.anim.type==='chromate' ? (1-transitionT) : .18;
    const waveAmp = 3.2 + settling*6.5 + (state.temp/120)*1.6;
    const waveTime = now*.0028;
    function surfaceY(px){
      const u = (px-leftTop)/(rightTop-leftTop);
      return liquidY
        + Math.sin(u*Math.PI*2.15 + waveTime)*waveAmp
        + Math.sin(u*Math.PI*4.5 - waveTime*1.05)*(waveAmp*.32);
    }
    function liquidPath(){
      ctx.beginPath();
      ctx.moveTo(leftTop, surfaceY(leftTop));
      const steps=42;
      for(let i=1;i<=steps;i++){
        const px = leftTop + (rightTop-leftTop)*i/steps;
        ctx.lineTo(px, surfaceY(px));
      }
      ctx.lineTo(bottomRight,bottomY);
      ctx.lineTo(bottomLeft,bottomY);
      ctx.closePath();
    }

    const grd = ctx.createLinearGradient(0,liquidY,0,topY+beakerH);
    grd.addColorStop(0,`rgba(${r},${gg},${bb},.82)`);
    grd.addColorStop(1,`rgba(${Math.min(255,r+10)},${Math.min(255,gg+12)},${Math.min(255,bb+8)},.96)`);
    ctx.fillStyle=grd;
    liquidPath();
    ctx.fill();

    // 용액 영역 클리핑 뒤 정지된 이온 점 표시
    ctx.save();
    liquidPath();
    ctx.clip();
    for(const d of state.staticDots){
      const px = centerX-beakerW*.34 + d.x*beakerW*.68;
      const py = liquidY + 28 + d.y*(liquidH-55);
      ctx.globalAlpha=.56;
      ctx.fillStyle = d.kind===0?'rgba(211,93,30,.72)':'rgba(255,238,80,.72)';
      ctx.beginPath(); ctx.arc(px,py,3.7+d.kind*.6,0,Math.PI*2); ctx.fill();
      ctx.globalAlpha=1;
    }
    ctx.restore();

    // 수면 하이라이트: 실제 흔들림이 눈에 보이도록 밝은 선과 얇은 반사광 추가
    ctx.save();
    ctx.strokeStyle='rgba(255,255,255,.58)'; ctx.lineWidth=2.2; ctx.lineCap='round';
    ctx.beginPath();
    ctx.moveTo(leftTop+8, surfaceY(leftTop+8));
    const steps=38;
    for(let i=1;i<=steps;i++){
      const px = leftTop+8 + (rightTop-leftTop-16)*i/steps;
      ctx.lineTo(px, surfaceY(px));
    }
    ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.24)'; ctx.lineWidth=1.2;
    ctx.beginPath();
    for(let i=0;i<=steps;i++){
      const px = leftTop+24 + (rightTop-leftTop-48)*i/steps;
      const py = surfaceY(px)+11+Math.sin(i*.5+waveTime*.85)*1.8;
      if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }
    ctx.stroke();
    ctx.restore();

    // 비커 아래에는 색 이름 대신, 평형 이동 중 증가하는 이온과 이동 방향을 표시한다.
    // 애니메이션이 끝나면 간단히 '평형'만 표시한다.
    ctx.fillStyle='#405066';
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    if(state.anim && state.anim.type==='chromate') {
      const deltaBalance = state.anim.target.balance - state.anim.start.balance;
      let ionText = '변화 없음';
      let directionText = '평형 이동 없음';
      if(deltaBalance > 0.002) {
        ionText = '증가하는 이온: CrO₄²⁻';
        directionText = '평형 이동: 정반응 →';
      } else if(deltaBalance < -0.002) {
        ionText = '증가하는 이온: Cr₂O₇²⁻';
        directionText = '평형 이동: ← 역반응';
      }
      ctx.font='900 17px Segoe UI, sans-serif';
      ctx.fillText(ionText,centerX,topY+beakerH+27);
      ctx.font='800 15px Segoe UI, sans-serif';
      ctx.fillText(directionText,centerX,topY+beakerH+50);
    } else {
      ctx.font='900 20px Segoe UI, sans-serif';
      ctx.fillText('평형',centerX,topY+beakerH+36);
    }

    const chromateThermX = Math.min(W-82, centerX+beakerW/2+112);
    drawThermometer(ctx,chromateThermX, topY+24, state.temp);
    const chromateScaleY = Math.min(H-52, topY+308);
    drawColorScaleBelowThermometer(ctx,chromateThermX,chromateScaleY,96,visualB,'chromate');
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
    // He는 버튼을 누르는 순간 지정한 몰수만큼 모두 들어간 것으로 처리한다.
    // He로 인한 부피 증가는 즉시 나타나고, 이후에는 평형 조성 변화만 애니메이션된다.
    state.displayInert=state.inert;
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
      state.displayChromate.netAcid = lerp(state.anim.start.netAcid ?? 0,state.anim.target.netAcid ?? 0,e);
      state.displayChromate.solutionVolume = lerp(state.anim.start.solutionVolume ?? 1,state.anim.target.solutionVolume ?? 1,e);
      state.displayChromate.dilution = lerp(state.anim.start.dilution ?? 0,state.anim.target.dilution ?? 0,e);
      if(t>=1){ state.chromate={...state.anim.target}; state.displayChromate={...state.anim.target}; state.anim=null; }
    }
  }

  function updateUI(){
    $('tempVal').textContent=Math.round(state.temp);
    $('pressureVal').textContent=fmt(state.pressure,2);
    $('volumeVal').textContent=String(Math.round(state.volume));
    $('gasAmountVal').textContent=fmt(Number($('gasAmount').value),2);
    $('chromateAmountVal').textContent=fmt(Number($('chromateAmount').value),2);
    $('hclConcVal').textContent=fmt(Number($('hclConc').value),2);
    $('naohConcVal').textContent=fmt(Number($('naohConc').value),2);
    const chromateAct=$('chromateAction').value;
    $('hclConcGroup').classList.toggle('hidden',chromateAct!=='hcl');
    $('naohConcGroup').classList.toggle('hidden',chromateAct!=='naoh');
    $('reagentVolumeInfo').classList.toggle('hidden',chromateAct==='water');
    $('chromateAmountGroup').classList.toggle('hidden',chromateAct!=='water');
    $('chromateAmountLabel').textContent='첨가 물의 부피 (L)';
    const steelPressureFixed = state.experiment==='gas' && state.vessel==='steel';
    $('pressure').disabled = steelPressureFixed;
    $('pressureGroup').classList.toggle('fixed-control',steelPressureFixed);
    if(steelPressureFixed){
      state.pressure=1.00;
      $('pressure').value='1.00';
      $('pressureVal').textContent='1.00 (고정)';
    }
    $('vesselBox').classList.toggle('hidden',state.experiment==='chromate');
    $('pressureGroup').classList.toggle('hidden',state.experiment==='chromate');
    $('volumeGroup').classList.toggle('hidden',state.experiment==='chromate');
    $('gasControls').classList.toggle('hidden',state.experiment!=='gas');
    $('chromateControls').classList.toggle('hidden',state.experiment!=='chromate');

    if(state.experiment==='gas'){
      $('leftEquation').textContent='2NO₂(g) ⇌ N₂O₄(g)';
      $('stageTitle').textContent='2NO₂(g) ⇌ N₂O₄(g)';
      $('containerNote').textContent=state.vessel==='steel'
        ? '강철용기는 압력 조건을 1.00 atm으로 고정합니다. 부피 선택은 새 실험으로 초기화됩니다.'
        : '용기 부피는 1·2·3·4 L 중 하나를 선택하며, 변경하면 새 실험으로 초기화됩니다.';
      $('legend').innerHTML='<span class="legend-chip"><span class="legend-dot" style="background:#d97836"></span>NO₂ 적갈색</span><span class="legend-chip"><span class="legend-dot" style="background:#eef5ff;border:1px solid #7d8ea1"></span>N₂O₄ 무색</span>' + (state.inert>0.01 ? '<span class="legend-chip"><span class="legend-dot" style="background:#d8efff;border:1px solid #5791be"></span>He 헬륨</span>' : '');
      const K=gasK(), Q=gasQ(), dir=directionFrom(Q,K), V=effectiveVolume(state.displayGas);
      $('kVal').textContent=fmt(K,2); $('qVal').textContent=fmt(Q,2); $('directionVal').textContent=dir; $('currentVolVal').textContent=fmt(V,2)+' L';
      const no2Frac=state.displayGas.no2/(state.displayGas.no2+state.displayGas.n2o4+1e-6);
      $('badges').innerHTML=`<span class="badge">${dir==='정반응'?'N₂O₄ 생성 증가':dir==='역반응'?'NO₂ 생성 증가':'K = Q 평형'}</span><span class="badge">NO₂ 비율 ${(no2Frac*100).toFixed(0)}%</span>${state.inert>0.01?`<span class="badge">He ${fmt(state.inert,2)} mol</span>`:''}`;
      $('formula').innerHTML='<b>화학 반응 정보</b><br><code>정반응: 발열반응 / 분자 수 감소</code><br><code>역반응: 흡열반응 / 분자 수 증가</code>';
      const eq=state.targetGas; const rows=[
        ['NO₂', state.displayGas.no2, eq.no2, state.displayGas.no2/V], ['N₂O₄', state.displayGas.n2o4, eq.n2o4, state.displayGas.n2o4/V]
      ];
      $('tableBody').innerHTML=rows.map(r=>`<tr><td>${r[0]}</td><td>${fmt(r[1],3)} mol</td><td>${fmt(r[2],3)} mol</td><td>${fmt(r[3],3)} M</td></tr>`).join('') + (state.inert>0.01 ? `<tr><td>He</td><td>${fmt(state.inert,3)} mol</td><td>${fmt(state.inert,3)} mol</td><td>비활성</td></tr>` : '');
      if(performance.now()<state.steelResetUntil){
        $('caption').innerHTML='<span class="caption-pill">선택한 부피의 새 용기로 실험을 시작했습니다. 압력 1.00 atm · Q = K</span>';
      } else if(state.vessel==='cylinder'){
        $('caption').innerHTML='<span class="caption-pill">부피 선택은 새 실험으로 초기화되며, 압력 변화에는 피스톤이 움직입니다.</span>';
      } else {
        $('caption').innerHTML='';
      }
    } else {
      $('leftEquation').textContent='Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺';
      $('stageTitle').textContent='Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)';
      $('containerNote').textContent='';
      $('legend').innerHTML='<span class="legend-chip"><span class="legend-dot" style="background:#df7b32"></span>Cr₂O₇²⁻ 주황색</span><span class="legend-chip"><span class="legend-dot" style="background:#f7d84d"></span>CrO₄²⁻ 노란색</span>';
      const K=chromateK(), Q=chromateQ(), dir=directionFrom(Q,K), b=state.displayChromate.balance;
      $('kVal').textContent=fmt(K,2); $('qVal').textContent=fmt(Q,2); $('directionVal').textContent=dir; $('currentVolVal').textContent=fmt(state.displayChromate.solutionVolume,3)+' L';
      if(state.anim && state.anim.type==='chromate') {
        const deltaBalance = state.anim.target.balance - state.anim.start.balance;
        const status = deltaBalance > 0.002
          ? 'CrO₄²⁻ 증가 · 정반응 →'
          : deltaBalance < -0.002
            ? 'Cr₂O₇²⁻ 증가 · ← 역반응'
            : '평형 이동 없음';
        $('badges').innerHTML=`<span class="badge">${status}</span>`;
      } else {
        $('badges').innerHTML='<span class="badge">평형</span>';
      }
      const species=chromateSpecies(state.displayChromate);
      const targetSpecies=chromateSpecies(state.targetChromate);
      const acidBaseLabel=species.hMol>1e-6?'산성':species.ohMol>1e-6?'염기성':'중성 부근';
      $('formula').innerHTML='<b>화학 반응 정보</b><br><code>정반응: 흡열반응</code><br><code>역반응: 발열반응</code><br><code>산/염기 수용액 첨가: H⁺이온 수 변화 + 전체 용액 부피 증가에 따른 몰농도 변화</code><br><code>물 첨가: 전체 용액 부피 증가에 따른 몰농도 변화</code>';
      const orange=(1-b), yellow=b;
      $('tableBody').innerHTML=`<tr><td>Cr₂O₇²⁻</td><td>${fmt(orange,2)}</td><td>${fmt(1-state.targetChromate.balance,2)}</td><td>주황색</td></tr><tr><td>CrO₄²⁻</td><td>${fmt(yellow,2)}</td><td>${fmt(state.targetChromate.balance,2)}</td><td>노란색</td></tr><tr><td>H⁺</td><td>${fmt(species.hMol,3)} mol</td><td>${fmt(targetSpecies.hMol,3)} mol</td><td>${acidBaseLabel}</td></tr><tr><td>OH⁻</td><td>${fmt(species.ohMol,3)} mol</td><td>${fmt(targetSpecies.ohMol,3)} mol</td><td>${acidBaseLabel}</td></tr><tr><td>용액 부피</td><td>${fmt(state.displayChromate.solutionVolume,3)} L</td><td>${fmt(state.targetChromate.solutionVolume,3)} L</td><td>시약 용액 포함</td></tr>`;
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

  function setGasEquilibriumImmediately(sourceGas){
    const eq=solveGasEquilibrium(sourceGas);
    state.gas={...eq};
    state.displayGas={...eq};
    state.targetGas={...eq};
    state.anim=null;

    const now=performance.now();
    const k=gasK();
    const q=gasQ(eq, effectiveVolume(eq, state.volume));
    const forward=rateForwardGas(eq);
    const reverse=rateReverseGas(eq);
    const rate=(forward+reverse)/2;
    state.chart={qStart:q,qEnd:q,kStart:k,kEnd:k,rfStart:rate,rfEnd:rate,rrStart:rate,rrEnd:rate,start:now,duration:5000};
  }

  function startNewGasExperiment(nextVolume, showMessage=true){
    // 용기 부피 선택은 진행 중인 실험의 압축·팽창 조작이 아니다.
    // 1, 2, 3, 4 L 중 선택한 새 용기로 실험을 처음부터 다시 시작한다.
    state.volume=clamp(Math.round(nextVolume),1,4);
    state.displayVolume=state.volume;
    state.pressure=1.00;
    state.inert=0; state.displayInert=0; state.inertAnim=null; state.hePistonAnim=null; state.pistonVisualVolume=null;
    state.volumeAnim=null;
    state.volumePulse=null;
    state.anim=null;

    $('volume').value=String(state.volume);
    $('pressure').value=String(state.pressure);

    // 2 L 기준 시료의 몰수를 선택 부피에 비례해 조정한다.
    // 예: 1 L 새 실험은 2 L 실험의 절반 몰수로 시작하므로, 온도와 압력이 같을 때
    // 농도와 부분압력이 유지되어 1 atm이라는 설정이 납득 가능하다.
    const scale=state.volume/2;
    const source={no2:.80*scale,n2o4:2.20*scale};
    const eq=solveGasEquilibriumAtFixedVolume(source,state.volume);
    state.referenceGasTotal=Math.max(0.05,eq.no2+eq.n2o4);
    state.referenceTempK=273+state.temp;
    state.gas={...eq};
    state.displayGas={...eq};
    state.targetGas={...eq};
    state.anim=null;
    const now=performance.now();
    const k=gasK();
    const q=gasQ(eq,state.volume);
    const forward=rateForwardGas(eq), reverse=rateReverseGas(eq);
    const rate=(forward+reverse)/2;
    state.chart={qStart:q,qEnd:q,kStart:k,kEnd:k,rfStart:rate,rfEnd:rate,rrStart:rate,rrEnd:rate,start:now,duration:5000};
    state.steelResetUntil=showMessage ? performance.now()+1800 : 0;
    makeMolecules();
    updateUI();
  }

  function resetGas(){
    state.temp=43;
    state.vessel='cylinder';
    document.querySelector('input[name="vessel"][value="cylinder"]').checked=true;
    $('temp').value=state.temp;
    startNewGasExperiment(2,false);
  }
  function resetChromate(){
    state.temp=43;
    state.chromate={balance:.58,h:acidityIndex(.05,1.00),dilution:0,netAcid:.05,solutionVolume:1.00};
    state.displayChromate={...state.chromate};
    state.targetChromate={...state.chromate};
    $('temp').value=state.temp;
    startTransition(solveChromateEquilibrium(state.chromate));
  }

  $('experiment').addEventListener('change', e=>{
    state.experiment=e.target.value;
    if(state.experiment==='gas') startTransition(solveGasEquilibrium(state.displayGas));
    else startTransition(solveChromateEquilibrium(state.chromate));
  });
  document.querySelectorAll('input[name="vessel"]').forEach(r=>r.addEventListener('change',e=>{
    state.vessel=e.target.value;
    state.pressure=1.00;
    $('pressure').value='1.00';
    startNewGasExperiment(state.volume,true);
  }));
  $('temp').addEventListener('input',e=>{state.temp=Number(e.target.value);applyConditionChange();});
  $('pressure').addEventListener('input',e=>{
    if(state.vessel==='steel'){
      state.pressure=1.00;
      e.target.value='1.00';
      updateUI();
      return;
    }
    const nextPressure=Number(e.target.value);
    const prevPressure=state.pressure;
    state.pressure=nextPressure;
    if(state.experiment==='gas'){
      // 압력 증가: 순간 압축으로 NO₂ 농도가 커져 잠깐 진해진 뒤,
      // 평형 이동 과정에서 N₂O₄ 쪽으로 이동하며 다시 옅어진다.
      // 압력 감소는 반대로 순간적으로 옅어진 뒤 NO₂ 쪽으로 이동한다.
      triggerGasDensityPulse((nextPressure-prevPressure)*0.85, 1550, .14);
    }
    applyConditionChange();
  });
  $('volume').addEventListener('change',e=>{
    const nextVolume=Number(e.target.value);
    if(state.experiment==='gas'){
      // 실린더와 강철용기 모두 부피 선택을 새 실험으로 처리한다.
      // 압력은 1.00 atm으로 초기화되고, 선택 부피에서 Q=K인 상태로 즉시 시작한다.
      startNewGasExperiment(nextVolume,true);
    }
  });
  $('gasAmount').addEventListener('input',updateUI);
  $('chromateAmount').addEventListener('input',updateUI);
  $('hclConc').addEventListener('input',updateUI);
  $('naohConc').addEventListener('input',updateUI);
  $('chromateAction').addEventListener('change',updateUI);
  $('moleculeMotion').addEventListener('change',e=>{state.motion=e.target.checked;});
  $('applyGas').addEventListener('click',()=>{
    const amt=Number($('gasAmount').value); const act=$('gasAction').value;
    let src={...state.displayGas};
    state.hePistonAnim=null;
    if(act!=='addInert') state.pistonVisualVolume=null;
    if(act==='addNO2') src.no2+=amt;
    if(act==='removeNO2') src.no2=Math.max(.04,src.no2-amt);
    if(act==='addN2O4') src.n2o4+=amt;
    if(act==='removeN2O4') src.n2o4=Math.max(.04,src.n2o4-amt);
    if(act==='addInert'){
      state.inert=clamp(state.inert+amt,0,4.0);
      // He는 사용자가 지정한 몰수만큼 한 번에 첨가한다.
      // 따라서 displayInert도 즉시 최종값으로 바뀌고, 피스톤은 먼저 한 번에 팽창한다.
      // 그 직후부터 반응 기체 조성만 5초 동안 새 평형으로 이동한다.
      state.displayInert=state.inert;
      state.inertAnim=null;
      state.volumePulse=null;
    }

    state.gas={...src};state.displayGas={...src};
    if(act==='addInert' && state.vessel==='steel'){
      const q=gasQ(state.displayGas,state.volume,state.inert);
      const k=gasK();
      const forward=rateForwardGas(state.displayGas,state.inert);
      const reverse=rateReverseGas(state.displayGas,state.inert);
      state.targetGas={...state.displayGas};
      state.anim=null;
      state.chart={qStart:q,qEnd:q,kStart:k,kEnd:k,rfStart:forward,rfEnd:forward,rrStart:reverse,rrEnd:reverse,start:performance.now(),duration:5000};
      updateUI();
    } else {
      if(act==='addInert' && state.vessel==='cylinder'){
        // 1단계: He 전량 첨가 직후의 부피는 즉시 반영한다.
        const beforeHeVolume=effectiveVolume(src,state.volume,state.inert-amt);
        const immediateVolume=effectiveVolume(src,state.volume,state.inert);

        // 실제 계산값은 그대로 두되, 피스톤 그림만 교육적으로 더 크게 움직인다.
        // 1차: He 첨가에 따른 즉시 팽창을 약 2.4배 강조한다.
        const visualImmediate=clamp(
          beforeHeVolume + (immediateVolume-beforeHeVolume)*PISTON_VISUAL_GAIN_HE,
          .55, 4.60
        );

        // 2차: 역반응으로 총 기체 몰수가 늘어나는 추가 팽창을 약 2.8배 강조한다.
        const target=solveGasEquilibrium(src);
        const finalVolume=effectiveVolume(target,state.volume,state.inert);
        const visualFinal=clamp(
          visualImmediate + (finalVolume-immediateVolume)*PISTON_VISUAL_GAIN_EQUILIBRIUM,
          .55, 4.60
        );
        state.pistonVisualVolume=visualImmediate;
        state.hePistonAnim={
          from:visualImmediate,
          to:visualFinal,
          start:performance.now(),
          duration:5000
        };
        startTransition(target,'helium-expansion');
      } else {
        startTransition(solveGasEquilibrium(src),'condition');
      }
    }  });
  $('resetGas').addEventListener('click',resetGas);
  $('applyChromate').addEventListener('click',()=>{
    const waterAmount=Number($('chromateAmount').value);
    const act=$('chromateAction').value;
    const current={...state.displayChromate};
    state.chromate={...current};
    const reagentVolume=0.10; // HCl·NaOH 수용액은 매번 0.10 L씩 첨가

    if(act==='hcl'){
      const concentration=Math.max(.01,Number($('hclConc').value));
      const addedMoles=concentration*reagentVolume;
      state.chromate.netAcid=(state.chromate.netAcid||0)+addedMoles;
      state.chromate.solutionVolume=(state.chromate.solutionVolume||1)+reagentVolume;
    }
    if(act==='naoh'){
      const concentration=Math.max(.01,Number($('naohConc').value));
      const addedMoles=concentration*reagentVolume;
      // OH⁻와 H⁺는 1:1로 중화되며, 남는 OH⁻는 netAcid의 음수로 저장한다.
      state.chromate.netAcid=(state.chromate.netAcid||0)-addedMoles;
      state.chromate.solutionVolume=(state.chromate.solutionVolume||1)+reagentVolume;
    }
    if(act==='water'){
      state.chromate.solutionVolume=(state.chromate.solutionVolume||1)+waterAmount;
      state.chromate.dilution=clamp((state.chromate.dilution||0)+waterAmount*.70,0,2.5);
    }
    // HCl·NaOH 수용액도 용매를 포함하므로 첨가할수록 전체 용액 부피가 증가한다.
    // 따라서 H⁺가 이미 모두 중화된 뒤에도 추가 NaOH 수용액의 희석 효과가 Q를 낮추고
    // 크로메이트 생성 방향(정반응)으로 평형을 계속 이동시킨다.
    const addedVolume = Math.max(0, (state.chromate.solutionVolume||1) - 1.00);
    state.chromate.dilution=clamp(addedVolume*.70,0,2.5);
    state.chromate.h=acidityIndex(state.chromate.netAcid||0,state.chromate.solutionVolume||1);
    state.displayChromate={...current,h:state.chromate.h,netAcid:state.chromate.netAcid,solutionVolume:state.chromate.solutionVolume,dilution:state.chromate.dilution};
    startTransition(solveChromateEquilibrium(state.chromate));
  });
  $('resetChromate').addEventListener('click',resetChromate);

  if(!CanvasRenderingContext2D.prototype.roundRect){
    CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){
      this.beginPath();this.moveTo(x+r,y);this.lineTo(x+w-r,y);this.quadraticCurveTo(x+w,y,x+w,y+r);this.lineTo(x+w,y+h-r);this.quadraticCurveTo(x+w,y+h,x+w-r,y+h);this.lineTo(x+r,y+h);this.quadraticCurveTo(x,y+h,x,y+h-r);this.lineTo(x,y+r);this.quadraticCurveTo(x,y,x+r,y);return this;
    }
  }

  state.chromate.h=acidityIndex(state.chromate.netAcid,state.chromate.solutionVolume);
  state.displayChromate={...state.chromate};
  state.targetChromate={...state.chromate};
  makeMolecules();makeStaticDots();
  window.addEventListener('resize',()=>{drawStage();drawCharts();});
  startNewGasExperiment(2,false);
  animate();
})();
</script>
</body>
</html>
'''

components.html(APP_HTML, height=900, scrolling=False)
