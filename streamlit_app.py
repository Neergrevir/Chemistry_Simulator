import math
import random
from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# 화학 평형 시뮬레이터
# - 교육용 단순화 모델입니다.
# - 실제 정량 실험값과 완전히 일치시키기보다, 르샤틀리에 원리와
#   Q/K 비교를 직관적으로 보여주는 데 초점을 두었습니다.
# ============================================================

st.set_page_config(
    page_title="화학 평형 시뮬레이터",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------
# CSS 디자인
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #fff7f0 0%, #f2fbff 48%, #f6f2ff 100%);
    }

    .main-title {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.85);
        border-radius: 24px;
        padding: 18px 22px;
        box-shadow: 0 12px 35px rgba(80, 70, 120, 0.10);
        margin-bottom: 10px;
    }

    .main-title h1 {
        margin: 0;
        font-size: 2.25rem;
        font-weight: 800;
        color: #384152;
        letter-spacing: -0.04em;
    }

    .main-title p {
        margin: 6px 0 0 0;
        color: #6b7280;
        font-size: 0.98rem;
    }

    .panel {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.92);
        border-radius: 24px;
        padding: 18px 18px 20px 18px;
        box-shadow: 0 14px 35px rgba(80, 70, 120, 0.10);
        min-height: 640px;
    }

    .panel h3 {
        margin-top: 0;
        color: #374151;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .soft-card {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 18px;
        padding: 13px 14px;
        margin-bottom: 13px;
    }

    .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #eef2ff;
        color: #4338ca;
        font-weight: 700;
        font-size: 0.85rem;
        margin: 4px 4px 4px 0;
    }

    .formula-box {
        background: #f8fafc;
        border-left: 5px solid #a5b4fc;
        border-radius: 14px;
        padding: 12px 13px;
        color: #334155;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    .result-good {
        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #166534;
        border-radius: 14px;
        padding: 11px 13px;
        font-weight: 700;
    }

    .result-warn {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        border-radius: 14px;
        padding: 11px 13px;
        font-weight: 700;
    }

    .result-info {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        border-radius: 14px;
        padding: 11px 13px;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.70);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 12px 14px;
    }

    .small-note {
        color: #64748b;
        font-size: 0.86rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# 공통 유틸리티
# -----------------------------
EPS = 1e-9
R = 8.314  # J/(mol K)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.strip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{int(clamp(v, 0, 255)):02x}" for v in rgb)


def mix_color(c1: str, c2: str, t: float):
    """c1에서 c2로 t만큼 선형 보간."""
    t = clamp(t, 0, 1)
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))


def safe_div(a, b):
    return a / b if abs(b) > EPS else float("inf")


# -----------------------------
# 세션 상태 초기화
# -----------------------------
def init_state():
    defaults = {
        "no2_moles": 1.45,
        "n2o4_moles": 0.20,
        "last_action": "초기 상태",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# -----------------------------
# NO2/N2O4 평형 계산
# -----------------------------
def k_no2_n2o4(temp_c: float):
    """2NO2(g) -> N2O4(g)의 교육용 Kc 계산.
    기준: 298.15 K에서 Kc≈6.9 M^-1, 정반응 발열(ΔH≈-57.2 kJ/mol)로 단순화.
    """
    t_ref = 298.15
    k_ref = 6.9
    delta_h = -57_200.0
    temp_k = temp_c + 273.15
    return k_ref * math.exp((-delta_h / R) * (1 / t_ref - 1 / temp_k))


def solve_no2_equilibrium(n_no2_init: float, n_n2o4_init: float, volume_l: float, k_value: float):
    """2NO2 ⇌ N2O4, K = [N2O4]/[NO2]^2.
    x: 정반응 진행량. n_NO2 = n_NO2_init - 2x, n_N2O4 = n_N2O4_init + x.
    """
    volume_l = max(volume_l, EPS)
    lower = -n_n2o4_init + EPS
    upper = n_no2_init / 2 - EPS

    def f(x):
        no2 = max(n_no2_init - 2 * x, EPS)
        n2o4 = max(n_n2o4_init + x, EPS)
        return volume_l * n2o4 / (no2 ** 2) - k_value

    # 이 구간에서 f는 대체로 증가 함수이므로 이분법 사용
    lo, hi = lower, upper
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    x_eq = (lo + hi) / 2
    n_no2_eq = max(n_no2_init - 2 * x_eq, EPS)
    n_n2o4_eq = max(n_n2o4_init + x_eq, EPS)

    q_initial = safe_div((n_n2o4_init / volume_l), (n_no2_init / volume_l) ** 2)
    q_final = safe_div((n_n2o4_eq / volume_l), (n_no2_eq / volume_l) ** 2)

    if abs(q_initial - k_value) / max(k_value, EPS) < 0.025:
        direction = "거의 평형 상태"
    elif q_initial < k_value:
        direction = "정반응 쪽으로 이동"
    else:
        direction = "역반응 쪽으로 이동"

    return {
        "x_eq": x_eq,
        "no2_eq": n_no2_eq,
        "n2o4_eq": n_n2o4_eq,
        "no2_init": n_no2_init,
        "n2o4_init": n_n2o4_init,
        "q_initial": q_initial,
        "q_final": q_final,
        "direction": direction,
        "volume": volume_l,
        "k": k_value,
    }


def no2_time_series(result, steps=70):
    t = np.linspace(0, 1, steps)
    # 지수적으로 평형에 접근하는 교육용 곡선
    relax = 1 - np.exp(-4.5 * t)
    no2 = result["no2_init"] + (result["no2_eq"] - result["no2_init"]) * relax
    n2o4 = result["n2o4_init"] + (result["n2o4_eq"] - result["n2o4_init"]) * relax
    volume = result["volume"]
    c_no2 = no2 / volume
    c_n2o4 = n2o4 / volume
    q = c_n2o4 / np.maximum(c_no2 ** 2, EPS)
    # 속도는 교육용: v_forward = kf[NO2]^2, v_reverse = kr[N2O4]
    kf = 1.0
    kr = kf / max(result["k"], EPS)
    v_forward = kf * c_no2 ** 2
    v_reverse = kr * c_n2o4
    return pd.DataFrame(
        {
            "시간": t,
            "[NO₂]": c_no2,
            "[N₂O₄]": c_n2o4,
            "Q": q,
            "K": np.full_like(t, result["k"]),
            "정반응 속도": v_forward,
            "역반응 속도": v_reverse,
        }
    )


# -----------------------------
# 크로메이트/다이크로메이트 평형 계산
# -----------------------------
def solve_chromate_equilibrium(hcl: float, naoh: float, water: float, chromium_total: float = 1.0):
    """Cr2O7^2- + H2O ⇌ 2CrO4^2- + 2H+
    K = [CrO4]^2 [H+]^2 / [Cr2O7]
    전체 크롬 보존: 2[D] + [C] = T
    """
    # 산/염기/희석 효과를 pH로 단순화
    ph = 4.2 - 2.2 * hcl + 2.7 * naoh + 0.8 * water
    ph = clamp(ph, 1.0, 13.0)
    h = 10 ** (-ph)
    k_value = 1.0e-8

    # 2*h^2*C^2 + K*C - K*T = 0
    a = 2 * h * h
    b = k_value
    c = -k_value * chromium_total
    discriminant = max(b * b - 4 * a * c, 0)
    chromate = (-b + math.sqrt(discriminant)) / max(2 * a, EPS)
    chromate = clamp(chromate, EPS, chromium_total - EPS)
    dichromate = max((chromium_total - chromate) / 2, EPS)
    q_initial = None
    q_final = safe_div((chromate ** 2) * (h ** 2), dichromate)

    if hcl > naoh and hcl > 0.05:
        direction = "역반응 쪽으로 이동"
        reason = "HCl을 넣으면 H⁺가 증가하므로 H⁺를 소비하는 왼쪽, 즉 다이크로메이트 쪽이 유리해집니다."
    elif naoh > hcl and naoh > 0.05:
        direction = "정반응 쪽으로 이동"
        reason = "NaOH를 넣으면 OH⁻가 H⁺를 제거하므로, H⁺를 다시 만들기 위해 오른쪽 크로메이트 쪽이 유리해집니다."
    elif water > 0.05:
        direction = "정반응 쪽으로 이동"
        reason = "물을 넣으면 용액이 희석되고 H⁺ 농도가 낮아진 것으로 볼 수 있어 노란색 크로메이트 쪽이 상대적으로 유리해집니다."
    else:
        direction = "초기 조건에 가까움"
        reason = "산이나 염기를 거의 넣지 않아 뚜렷한 평형 이동이 크지 않습니다."

    return {
        "chromate": chromate,
        "dichromate": dichromate,
        "h": h,
        "ph": ph,
        "k": k_value,
        "q_final": q_final,
        "direction": direction,
        "reason": reason,
        "hcl": hcl,
        "naoh": naoh,
        "water": water,
        "chromium_total": chromium_total,
    }


def chromate_time_series(result, steps=70):
    t = np.linspace(0, 1, steps)
    relax = 1 - np.exp(-4.5 * t)

    # 초기값은 중성에 가까운 혼합 상태로 설정하고 평형값으로 접근시킨다.
    c0 = 0.48 + 0.20 * result["naoh"] - 0.20 * result["hcl"] + 0.08 * result["water"]
    c0 = clamp(c0, 0.05, 0.95)
    d0 = max((result["chromium_total"] - c0) / 2, EPS)
    c_eq = result["chromate"]
    d_eq = result["dichromate"]

    chromate = c0 + (c_eq - c0) * relax
    dichromate = d0 + (d_eq - d0) * relax
    h = result["h"]
    q = (chromate ** 2) * (h ** 2) / np.maximum(dichromate, EPS)

    # 교육용 속도: v_forward = kf[D], v_reverse = kr[C]^2[H]^2
    kf = 1.0
    kr = kf / max(result["k"], EPS)
    v_forward = kf * dichromate
    v_reverse = kr * (chromate ** 2) * (h ** 2)

    return pd.DataFrame(
        {
            "시간": t,
            "[CrO₄²⁻]": chromate,
            "[Cr₂O₇²⁻]": dichromate,
            "Q": q,
            "K": np.full_like(t, result["k"]),
            "정반응 속도": v_forward,
            "역반응 속도": v_reverse,
        }
    )


# -----------------------------
# SVG / HTML 시각화
# -----------------------------
def cylinder_svg(color: str, volume_factor: float, container_type: str, no2_ratio: float):
    piston_y = int(60 + (volume_factor - 0.45) / (1.70 - 0.45) * 105)
    piston_y = clamp(piston_y, 55, 170)
    gas_y = piston_y + 10
    gas_h = 245 - gas_y
    opacity = 0.35 + 0.55 * no2_ratio

    if container_type == "피스톤 실린더":
        piston = f"""
        <rect x="70" y="{piston_y}" width="160" height="14" rx="7" fill="#94a3b8" />
        <rect x="140" y="22" width="20" height="{piston_y - 12}" rx="8" fill="#cbd5e1" />
        <circle cx="150" cy="24" r="18" fill="#e2e8f0" stroke="#94a3b8" stroke-width="3" />
        <text x="150" y="29" text-anchor="middle" font-size="18">↕</text>
        """
        title = "피스톤 실린더"
    else:
        piston = """
        <rect x="60" y="42" width="180" height="222" rx="26" fill="none" stroke="#64748b" stroke-width="10" opacity="0.65" />
        <path d="M70 52 L230 254" stroke="#94a3b8" stroke-width="3" opacity="0.35" />
        <path d="M230 52 L70 254" stroke="#94a3b8" stroke-width="3" opacity="0.35" />
        """
        title = "부피 일정 강철용기"
        gas_y = 56
        gas_h = 196

    svg = f"""
    <svg width="100%" viewBox="0 0 300 310" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#64748b" flood-opacity="0.22"/>
        </filter>
        <linearGradient id="glass" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75" />
          <stop offset="100%" stop-color="#e0f2fe" stop-opacity="0.28" />
        </linearGradient>
      </defs>
      <rect x="35" y="10" width="230" height="285" rx="28" fill="#ffffff" opacity="0.44" />
      <rect x="70" y="48" width="160" height="215" rx="26" fill="url(#glass)" stroke="#93c5fd" stroke-width="4" filter="url(#shadow)"/>
      <rect x="79" y="{gas_y}" width="142" height="{gas_h}" rx="22" fill="{color}" opacity="{opacity}"/>
      <circle cx="112" cy="{gas_y + 45}" r="8" fill="#b45309" opacity="0.72" />
      <circle cx="185" cy="{gas_y + 80}" r="6" fill="#b45309" opacity="0.65" />
      <circle cx="151" cy="{gas_y + 128}" r="9" fill="#f8fafc" opacity="0.9" stroke="#94a3b8" />
      {piston}
      <text x="150" y="288" text-anchor="middle" fill="#475569" font-size="18" font-weight="700">{title}</text>
    </svg>
    """
    return svg


def beaker_svg(color: str, chromate_ratio: float):
    liquid_opacity = 0.62 + 0.25 * chromate_ratio
    svg = f"""
    <svg width="100%" viewBox="0 0 300 310" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="10" stdDeviation="7" flood-color="#64748b" flood-opacity="0.2"/>
        </filter>
        <linearGradient id="glass" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8" />
          <stop offset="100%" stop-color="#dbeafe" stop-opacity="0.28" />
        </linearGradient>
      </defs>
      <rect x="42" y="18" width="216" height="272" rx="28" fill="#ffffff" opacity="0.43" />
      <path d="M78 58 L222 58 L205 258 Q201 275 184 275 L116 275 Q99 275 95 258 Z" fill="url(#glass)" stroke="#93c5fd" stroke-width="4" filter="url(#shadow)"/>
      <path d="M95 150 L205 150 L194 256 Q191 263 182 263 L118 263 Q109 263 106 256 Z" fill="{color}" opacity="{liquid_opacity}"/>
      <ellipse cx="150" cy="150" rx="55" ry="10" fill="#ffffff" opacity="0.25" />
      <line x1="105" y1="95" x2="132" y2="95" stroke="#94a3b8" stroke-width="2" />
      <line x1="105" y1="125" x2="124" y2="125" stroke="#94a3b8" stroke-width="2" />
      <line x1="105" y1="155" x2="132" y2="155" stroke="#94a3b8" stroke-width="2" />
      <line x1="105" y1="185" x2="124" y2="185" stroke="#94a3b8" stroke-width="2" />
      <circle cx="132" cy="192" r="7" fill="#fde68a" opacity="0.65" />
      <circle cx="170" cy="218" r="8" fill="#f59e0b" opacity="0.45" />
      <text x="150" y="295" text-anchor="middle" fill="#475569" font-size="18" font-weight="700">비커 속 평형 색 변화</text>
    </svg>
    """
    return svg


def thermometer_svg(temp_c: float):
    fill_h = int(30 + (temp_c - 0) / 100 * 160)
    fill_h = clamp(fill_h, 25, 185)
    y = 235 - fill_h
    svg = f"""
    <svg width="100%" viewBox="0 0 100 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="36" y="28" width="28" height="196" rx="14" fill="#ffffff" stroke="#94a3b8" stroke-width="4"/>
      <circle cx="50" cy="235" r="26" fill="#ffffff" stroke="#94a3b8" stroke-width="4"/>
      <rect x="43" y="{y}" width="14" height="{fill_h}" rx="7" fill="#fb7185"/>
      <circle cx="50" cy="235" r="17" fill="#fb7185"/>
      <text x="50" y="18" text-anchor="middle" font-size="13" fill="#475569" font-weight="700">온도</text>
      <text x="50" y="270" text-anchor="middle" font-size="15" fill="#475569" font-weight="700">{temp_c:.0f}℃</text>
    </svg>
    """
    return svg


def molecule_animation_html(no2_count=20, n2o4_count=7, gas_color="#c08457"):
    # iframe 내부에서만 동작하는 간단한 Canvas 애니메이션
    # Streamlit과 양방향 통신하지는 않지만, 현재 평형 상태를 반영해 분자 수를 갱신한다.
    no2_count = int(clamp(no2_count, 4, 45))
    n2o4_count = int(clamp(n2o4_count, 2, 24))
    html = f"""
    <div style="width:100%; height:300px; border-radius:22px; overflow:hidden; background:rgba(255,255,255,0.72); border:1px solid rgba(203,213,225,0.75);">
      <canvas id="molCanvas" width="760" height="300" style="width:100%; height:300px;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('molCanvas');
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    const particles = [];
    const no2N = {no2_count};
    const n2o4N = {n2o4_count};

    function rand(a, b) {{ return a + Math.random() * (b - a); }}

    for (let i = 0; i < no2N; i++) {{
      particles.push({{type:'NO2', x:rand(45,W-45), y:rand(45,H-45), vx:rand(-1.2,1.2), vy:rand(-1.2,1.2), r:9}});
    }}
    for (let i = 0; i < n2o4N; i++) {{
      particles.push({{type:'N2O4', x:rand(55,W-55), y:rand(55,H-55), vx:rand(-0.9,0.9), vy:rand(-0.9,0.9), r:13}});
    }}

    function drawNO2(p) {{
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.fillStyle = '#b45309';
      ctx.beginPath(); ctx.arc(0,0,8,0,Math.PI*2); ctx.fill();
      ctx.fillStyle = '#f97316';
      ctx.beginPath(); ctx.arc(-10,-8,5,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(10,-8,5,0,Math.PI*2); ctx.fill();
      ctx.fillStyle = '#334155'; ctx.font='11px sans-serif'; ctx.fillText('NO₂', -12, 22);
      ctx.restore();
    }}

    function drawN2O4(p) {{
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.strokeStyle = '#64748b'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(-12, 0); ctx.lineTo(12, 0); ctx.stroke();
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath(); ctx.arc(-12,0,9,0,Math.PI*2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(12,0,9,0,Math.PI*2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#334155'; ctx.font='11px sans-serif'; ctx.fillText('N₂O₄', -18, 26);
      ctx.restore();
    }}

    function step() {{
      ctx.clearRect(0, 0, W, H);
      const grad = ctx.createLinearGradient(0,0,W,H);
      grad.addColorStop(0, 'rgba(255,255,255,0.78)');
      grad.addColorStop(1, '{gas_color}22');
      ctx.fillStyle = grad;
      ctx.fillRect(0,0,W,H);

      ctx.strokeStyle = 'rgba(148,163,184,0.35)';
      ctx.lineWidth = 3;
      ctx.strokeRect(18, 18, W-36, H-36);

      for (const p of particles) {{
        p.x += p.vx; p.y += p.vy;
        if (p.x < 35 || p.x > W - 35) p.vx *= -1;
        if (p.y < 35 || p.y > H - 35) p.vy *= -1;
        if (p.type === 'NO2') drawNO2(p); else drawN2O4(p);
      }}
      requestAnimationFrame(step);
    }}
    step();
    </script>
    """
    return html


# -----------------------------
# 상단부
# -----------------------------
top_left, top_right = st.columns([1.35, 1.65])
with top_left:
    st.markdown(
        """
        <div class="main-title">
          <h1>⚗️ 화학 평형 시뮬레이터</h1>
          <p>조건을 바꾸면 Q, K, 색 변화, 반응 속도 그래프가 함께 변합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
    experiment = st.selectbox(
        "실험 선택",
        [
            "이산화질소 ↔ 사산화이질소  |  2NO₂(g) ⇌ N₂O₄(g)",
            "다이크로메이트 ↔ 크로메이트  |  Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)",
        ],
        label_visibility="visible",
    )
    st.markdown("</div>", unsafe_allow_html=True)

is_gas = experiment.startswith("이산화질소")


# -----------------------------
# 좌/중/우 레이아웃
# -----------------------------
left, center, right = st.columns([1.05, 1.65, 1.35], gap="large")


# -----------------------------
# 좌측부: 조건 설정
# -----------------------------
with left:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### 조건 변화")

    if is_gas:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("**반응식**")
        st.latex(r"2NO_2(g) \rightleftharpoons N_2O_4(g)")
        st.markdown("<span class='pill'>NO₂: 적갈색</span><span class='pill'>N₂O₄: 무색</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        container_type = st.radio(
            "용기 선택",
            ["피스톤 실린더", "부피 일정 강철용기"],
            help="피스톤 실린더는 압력 변화가 부피 변화로 이어지는 상황을 단순화해 표현합니다.",
        )

        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("**농도: 반응물/생성물 첨가·제거**")
        target = st.selectbox("물질 선택", ["NO₂ 첨가/제거", "N₂O₄ 첨가/제거"])
        amount = st.slider("변화량", 0.05, 0.50, 0.10, 0.05)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("첨가", use_container_width=True):
                if target.startswith("NO₂"):
                    st.session_state.no2_moles += amount
                    st.session_state.last_action = f"NO₂ {amount:.2f} mol 첨가"
                else:
                    st.session_state.n2o4_moles += amount
                    st.session_state.last_action = f"N₂O₄ {amount:.2f} mol 첨가"
        with b2:
            if st.button("제거", use_container_width=True):
                if target.startswith("NO₂"):
                    st.session_state.no2_moles = max(0.05, st.session_state.no2_moles - amount)
                    st.session_state.last_action = f"NO₂ {amount:.2f} mol 제거"
                else:
                    st.session_state.n2o4_moles = max(0.02, st.session_state.n2o4_moles - amount)
                    st.session_state.last_action = f"N₂O₄ {amount:.2f} mol 제거"
        with b3:
            if st.button("초기화", use_container_width=True):
                st.session_state.no2_moles = 1.45
                st.session_state.n2o4_moles = 0.20
                st.session_state.last_action = "초기화"
        st.caption(f"최근 조작: {st.session_state.last_action}")
        st.markdown("</div>", unsafe_allow_html=True)

        if container_type == "피스톤 실린더":
            pressure = st.slider("압력 조건 변화", 0.60, 2.40, 1.00, 0.05, help="값이 클수록 압축된 상태로 가정합니다.")
            volume_factor = 1 / pressure
            volume_l = 1.00 * volume_factor
        else:
            pressure = st.slider("외부 압력 표시", 0.60, 2.40, 1.00, 0.05, disabled=True)
            volume_factor = 1.00
            volume_l = 1.00
            st.caption("강철용기는 부피가 일정하므로 외부 압력을 바꿔도 용기 부피가 직접 변하지 않는 것으로 처리했습니다.")

        temp_c = st.slider("온도 조건 변화", 0, 100, 25, 1)
        show_animation = st.checkbox("NO₂ / N₂O₄ 분자 운동 애니메이션", value=True)

        k_value = k_no2_n2o4(temp_c)
        result = solve_no2_equilibrium(
            st.session_state.no2_moles,
            st.session_state.n2o4_moles,
            volume_l,
            k_value,
        )
        df = no2_time_series(result)

    else:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("**반응식**")
        st.latex(r"Cr_2O_7^{2-}(aq)+H_2O(l) \rightleftharpoons 2CrO_4^{2-}(aq)+2H^+(aq)")
        st.markdown("<span class='pill'>Cr₂O₇²⁻: 주황색</span><span class='pill'>CrO₄²⁻: 노란색</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("**첨가 가능 물질**")
        hcl = st.slider("HCl 추가량", 0.0, 1.0, 0.25, 0.05, help="H⁺를 증가시켜 다이크로메이트 쪽을 유리하게 합니다.")
        naoh = st.slider("NaOH 추가량", 0.0, 1.0, 0.10, 0.05, help="H⁺를 제거해 크로메이트 쪽을 유리하게 합니다.")
        water = st.slider("H₂O 추가량", 0.0, 1.0, 0.20, 0.05, help="희석 효과를 단순화해 반영했습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

        temp_c = st.slider("온도 인터페이스", 0, 100, 25, 1, help="이 실험에서는 산·염기 조건 변화가 중심이므로 온도는 시각 인터페이스 위주로 표시합니다.")
        container_type = "비커"
        show_animation = False
        result = solve_chromate_equilibrium(hcl, naoh, water)
        df = chromate_time_series(result)

    st.markdown("<div class='small-note'>※ 이 앱은 교육용 시뮬레이터입니다. 실제 실험에서는 온도, 용매, 이온세기, 농도 범위에 따라 정량값이 달라질 수 있습니다.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 중앙부: 실험 진행/시각화
# -----------------------------
with center:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### 실험 진행")

    if is_gas:
        no2_conc = result["no2_eq"] / result["volume"]
        n2o4_conc = result["n2o4_eq"] / result["volume"]
        no2_ratio = clamp(no2_conc / (no2_conc + n2o4_conc + EPS), 0, 1)
        gas_color = mix_color("#f8fafc", "#9a3412", no2_ratio)

        c1, c2 = st.columns([1.6, 0.55])
        with c1:
            st.markdown(cylinder_svg(gas_color, volume_factor, container_type, no2_ratio), unsafe_allow_html=True)
        with c2:
            st.markdown(thermometer_svg(temp_c), unsafe_allow_html=True)
            st.metric("부피", f"{result['volume']:.2f} L")
            if container_type == "피스톤 실린더":
                st.metric("상대 압력", f"{pressure:.2f} atm")

        if show_animation:
            st.markdown("**분자 무작위 운동 애니메이션**")
            no2_count = 8 + int(30 * no2_ratio)
            n2o4_count = 4 + int(18 * (1 - no2_ratio))
            components.html(molecule_animation_html(no2_count, n2o4_count, gas_color), height=318)
        else:
            st.info("분자 운동 애니메이션이 꺼져 있습니다.")

    else:
        chromate_ratio = clamp(result["chromate"] / (result["chromate"] + 2 * result["dichromate"] + EPS), 0, 1)
        liquid_color = mix_color("#f97316", "#fde047", chromate_ratio)

        c1, c2 = st.columns([1.6, 0.55])
        with c1:
            st.markdown(beaker_svg(liquid_color, chromate_ratio), unsafe_allow_html=True)
        with c2:
            st.markdown(thermometer_svg(temp_c), unsafe_allow_html=True)
            st.metric("예상 pH", f"{result['ph']:.2f}")
            st.metric("[H⁺]", f"{result['h']:.2e} M")

        st.markdown(
            f"""
            <div class="formula-box">
            <b>색 변화 해석</b><br>
            주황색이 강할수록 Cr₂O₇²⁻ 비율이 크고, 노란색이 강할수록 CrO₄²⁻ 비율이 큽니다.<br>
            현재 예측 색상은 <b>{'노란색에 가까움' if chromate_ratio > 0.55 else '주황색에 가까움'}</b>입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 우측부: 결과/계산식/그래프
# -----------------------------
with right:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("### 실험 결과 도출 및 시각화")

    if is_gas:
        if result["direction"] == "정반응 쪽으로 이동":
            box_class = "result-info"
        elif result["direction"] == "역반응 쪽으로 이동":
            box_class = "result-warn"
        else:
            box_class = "result-good"

        st.markdown(f"<div class='{box_class}'>평형 이동: {result['direction']}</div>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.metric("K", f"{result['k']:.3g}")
            st.metric("Q 초기", f"{result['q_initial']:.3g}")
        with m2:
            st.metric("[NO₂] 평형", f"{result['no2_eq']/result['volume']:.3g} M")
            st.metric("[N₂O₄] 평형", f"{result['n2o4_eq']/result['volume']:.3g} M")

        st.markdown(
            """
            <div class="formula-box">
            <b>계산식</b><br>
            2NO₂(g) ⇌ N₂O₄(g)<br>
            K = [N₂O₄] / [NO₂]²<br>
            Q &lt; K이면 정반응, Q &gt; K이면 역반응으로 이동합니다.<br>
            정반응은 발열 반응으로 단순화했기 때문에 온도를 높이면 NO₂ 쪽이 상대적으로 유리해집니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        table = pd.DataFrame(
            {
                "물질": ["NO₂", "N₂O₄"],
                "초기 mol": [result["no2_init"], result["n2o4_init"]],
                "평형 mol": [result["no2_eq"], result["n2o4_eq"]],
                "평형 농도(M)": [result["no2_eq"] / result["volume"], result["n2o4_eq"] / result["volume"]],
            }
        )
        st.dataframe(table, use_container_width=True, hide_index=True)

        explanation = []
        if container_type == "피스톤 실린더" and pressure > 1.05:
            explanation.append("압력을 높여 부피가 줄어든 상황이므로, 기체 몰수가 더 적은 N₂O₄ 쪽이 유리합니다.")
        elif container_type == "피스톤 실린더" and pressure < 0.95:
            explanation.append("압력을 낮춰 부피가 커진 상황이므로, 기체 몰수가 더 많은 NO₂ 쪽이 유리합니다.")
        if temp_c > 35:
            explanation.append("온도가 높아져 발열 방향인 N₂O₄ 생성보다 흡열 방향인 NO₂ 생성이 상대적으로 유리합니다.")
        elif temp_c < 15:
            explanation.append("온도가 낮아져 발열 방향인 N₂O₄ 생성이 상대적으로 유리합니다.")
        if not explanation:
            explanation.append("현재 조건에서는 Q와 K의 비교에 따라 평형 이동 방향이 결정됩니다.")
        st.write(" ".join(explanation))

    else:
        if result["direction"] == "정반응 쪽으로 이동":
            box_class = "result-info"
        elif result["direction"] == "역반응 쪽으로 이동":
            box_class = "result-warn"
        else:
            box_class = "result-good"

        st.markdown(f"<div class='{box_class}'>평형 이동: {result['direction']}</div>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.metric("K", f"{result['k']:.1e}")
            st.metric("Q 평형", f"{result['q_final']:.1e}")
        with m2:
            st.metric("[CrO₄²⁻]", f"{result['chromate']:.3g} M")
            st.metric("[Cr₂O₇²⁻]", f"{result['dichromate']:.3g} M")

        st.markdown(
            """
            <div class="formula-box">
            <b>계산식</b><br>
            Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺<br>
            K = [CrO₄²⁻]²[H⁺]² / [Cr₂O₇²⁻]<br>
            HCl을 넣으면 H⁺ 증가 → 왼쪽, NaOH를 넣으면 H⁺ 감소 → 오른쪽입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        table = pd.DataFrame(
            {
                "물질": ["CrO₄²⁻", "Cr₂O₇²⁻", "H⁺"],
                "예상 농도(M)": [result["chromate"], result["dichromate"], result["h"]],
                "색/역할": ["노란색", "주황색", "산성도 결정"],
            }
        )
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.write(result["reason"])

    # Q와 K 그래프
    st.markdown("#### 반응지수 Q와 평형상수 K")
    q_chart = df.set_index("시간")[["Q", "K"]].copy()
    st.line_chart(q_chart, height=255, use_container_width=True)

    # 정반응/역반응 속도 그래프
    st.markdown("#### 정반응 속도와 역반응 속도")
    v_chart = df.set_index("시간")[["정반응 속도", "역반응 속도"]].copy()
    st.line_chart(v_chart, height=255, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 하단 안내
# -----------------------------
st.markdown(
    """
    <div class="soft-card small-note">
    <b>활용 팁</b> — 발표할 때는 왼쪽에서 조건을 바꾼 뒤, 중앙의 색 변화와 오른쪽의 Q/K 그래프가 동시에 변한다는 점을 보여주면 좋습니다.
    특히 Q와 K의 관계를 먼저 설명한 다음, 르샤틀리에 원리로 결과를 해석하면 과학적 설명이 자연스럽게 이어집니다.
    </div>
    """,
    unsafe_allow_html=True,
)
