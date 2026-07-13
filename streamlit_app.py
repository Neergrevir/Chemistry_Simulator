import math
import random
from html import escape

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="화학 평형 시뮬레이터",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 1.6rem;
        max-width: 1500px;
    }
    div[data-testid="stVerticalBlock"] { gap: 0.75rem; }
    .hero-card {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(147, 179, 214, 0.22);
        border-radius: 26px;
        padding: 1.45rem 1.75rem;
        box-shadow: 0 18px 45px rgba(130, 160, 190, 0.13);
    }
    .hero-title {
        font-size: 2.15rem;
        line-height: 1.15;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #2d3448;
        margin: 0 0 0.45rem 0;
    }
    .hero-subtitle {
        color: #63708a;
        font-size: 1.02rem;
        margin: 0;
    }
    .section-card {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(147, 179, 214, 0.22);
        border-radius: 24px;
        padding: 1.15rem 1.2rem;
        box-shadow: 0 18px 45px rgba(130, 160, 190, 0.11);
        min-height: 100px;
    }
    .small-note {
        color: #6a768e;
        font-size: 0.88rem;
        line-height: 1.55;
    }
    .reaction-box {
        background: linear-gradient(135deg, #f7fbff 0%, #fff8f2 100%);
        border: 1px solid rgba(127, 182, 244, 0.26);
        border-radius: 18px;
        padding: 0.8rem 0.95rem;
        color: #34405a;
        font-weight: 700;
    }
    .status-pill {
        display: inline-block;
        padding: 0.33rem 0.7rem;
        border-radius: 999px;
        background: #edf6ff;
        color: #35648f;
        border: 1px solid #cfe8ff;
        font-weight: 700;
        margin: 0.12rem 0.12rem 0.12rem 0;
        font-size: 0.86rem;
    }
    div.stButton > button {
        border-radius: 14px;
        font-weight: 800;
        border: 1px solid rgba(100, 140, 190, 0.22);
        background: linear-gradient(135deg, #f4f9ff, #fff8f3);
        color: #2d3448;
    }
    div.stButton > button:hover {
        border-color: #7fb6f4;
        color: #24517d;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state
# -----------------------------
GAS_DEFAULTS = {
    "gas_no2": 0.80,
    "gas_n2o4": 0.22,
    "gas_volume_fixed": 1.00,
}
CHROMATE_DEFAULTS = {
    "cr2o7": 0.035,
    "cro4": 0.020,
    "hplus": 0.060,
    "solution_volume": 1.00,
}

for key, value in {**GAS_DEFAULTS, **CHROMATE_DEFAULTS}.items():
    if key not in st.session_state:
        st.session_state[key] = value
if "history" not in st.session_state:
    st.session_state.history = []
if "last_signature" not in st.session_state:
    st.session_state.last_signature = None

# -----------------------------
# Utility functions
# -----------------------------
def clamp(value, low, high):
    return max(low, min(high, value))


def bisect_monotonic(func, low, high, iterations=90):
    f_low = func(low)
    f_high = func(high)
    if not (math.isfinite(f_low) and math.isfinite(f_high)):
        return 0.0
    if abs(f_low) < 1e-12:
        return low
    if abs(f_high) < 1e-12:
        return high
    if f_low * f_high > 0:
        return low if abs(f_low) < abs(f_high) else high
    for _ in range(iterations):
        mid = (low + high) / 2
        f_mid = func(mid)
        if abs(f_mid) < 1e-10:
            return mid
        if f_low * f_mid <= 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
    return (low + high) / 2


def gas_k(temp_c):
    # 2NO2(g) -> N2O4(g) is exothermic. Lower temperature makes K larger.
    t = temp_c + 273.15
    t_ref = 298.15
    k_ref = 6.9
    return k_ref * math.exp(2550 * (1 / t - 1 / t_ref))


def gas_volume(vessel, pressure_atm, temp_c, fixed_volume):
    if vessel.startswith("외부"):
        # Piston vessel: pressure is externally controlled, so volume responds qualitatively to P and T.
        return clamp(1.00 * ((temp_c + 273.15) / 298.15) / max(pressure_atm, 0.15), 0.28, 2.80)
    return fixed_volume


def gas_equilibrium(no2, n2o4, volume_l, k_value):
    no2 = max(no2, 1e-8)
    n2o4 = max(n2o4, 1e-8)
    volume_l = max(volume_l, 1e-8)

    c_no2_initial = no2 / volume_l
    c_n2o4_initial = n2o4 / volume_l
    q_initial = c_n2o4_initial / max(c_no2_initial ** 2, 1e-12)

    low = -n2o4 + 1e-8
    high = no2 / 2 - 1e-8

    def f(x):
        n_no2 = max(no2 - 2 * x, 1e-10)
        n_n2o4 = max(n2o4 + x, 1e-10)
        c_no2 = n_no2 / volume_l
        c_n2o4 = n_n2o4 / volume_l
        return c_n2o4 / max(c_no2 ** 2, 1e-14) - k_value

    extent = bisect_monotonic(f, low, high)
    eq_no2 = max(no2 - 2 * extent, 0)
    eq_n2o4 = max(n2o4 + extent, 0)
    return {
        "q_initial": q_initial,
        "extent": extent,
        "eq_no2": eq_no2,
        "eq_n2o4": eq_n2o4,
        "c_no2_eq": eq_no2 / volume_l,
        "c_n2o4_eq": eq_n2o4 / volume_l,
    }


def gas_path(no2, n2o4, eq_no2, eq_n2o4, volume_l, k_value, temp_c):
    rows = []
    k_forward = 0.55 * math.exp((temp_c - 25) / 58)
    k_reverse = k_forward / max(k_value, 1e-8)
    for t in np.linspace(0, 12, 80):
        alpha = 1 - math.exp(-t / 2.6)
        n_no2 = no2 + (eq_no2 - no2) * alpha
        n_n2o4 = n2o4 + (eq_n2o4 - n2o4) * alpha
        c_no2 = max(n_no2 / volume_l, 1e-8)
        c_n2o4 = max(n_n2o4 / volume_l, 1e-8)
        q = c_n2o4 / max(c_no2 ** 2, 1e-12)
        rows.append(
            {
                "시간": round(float(t), 2),
                "Q": q,
                "K": k_value,
                "정반응 속도": k_forward * c_no2 ** 2,
                "역반응 속도": k_reverse * c_n2o4,
                "[NO₂]": c_no2,
                "[N₂O₄]": c_n2o4,
            }
        )
    return pd.DataFrame(rows)


def chromate_k(temp_c):
    # Educational simplified constant. Slight temperature dependence only.
    return 0.0065 * math.exp((temp_c - 25) / 85)


def chromate_equilibrium(cr2o7, cro4, hplus, volume_l, k_value):
    cr2o7 = max(cr2o7, 1e-8)
    cro4 = max(cro4, 1e-8)
    hplus = max(hplus, 1e-8)
    volume_l = max(volume_l, 1e-8)

    c_d = cr2o7 / volume_l
    c_c = cro4 / volume_l
    c_h = hplus / volume_l
    q_initial = (c_c ** 2 * c_h ** 2) / max(c_d, 1e-12)

    low = -min(cro4 / 2, hplus / 2) + 1e-8
    high = cr2o7 - 1e-8

    def f(x):
        n_d = max(cr2o7 - x, 1e-10)
        n_c = max(cro4 + 2 * x, 1e-10)
        n_h = max(hplus + 2 * x, 1e-10)
        c_d2 = n_d / volume_l
        c_c2 = n_c / volume_l
        c_h2 = n_h / volume_l
        return (c_c2 ** 2 * c_h2 ** 2) / max(c_d2, 1e-14) - k_value

    extent = bisect_monotonic(f, low, high)
    eq_d = max(cr2o7 - extent, 0)
    eq_c = max(cro4 + 2 * extent, 0)
    eq_h = max(hplus + 2 * extent, 0)
    return {
        "q_initial": q_initial,
        "extent": extent,
        "eq_cr2o7": eq_d,
        "eq_cro4": eq_c,
        "eq_hplus": eq_h,
        "c_cr2o7_eq": eq_d / volume_l,
        "c_cro4_eq": eq_c / volume_l,
        "c_hplus_eq": eq_h / volume_l,
    }


def chromate_path(cr2o7, cro4, hplus, eq_d, eq_c, eq_h, volume_l, k_value, temp_c):
    rows = []
    k_forward = 0.42 * math.exp((temp_c - 25) / 70)
    k_reverse = k_forward / max(k_value, 1e-8)
    for t in np.linspace(0, 12, 80):
        alpha = 1 - math.exp(-t / 2.35)
        n_d = cr2o7 + (eq_d - cr2o7) * alpha
        n_c = cro4 + (eq_c - cro4) * alpha
        n_h = hplus + (eq_h - hplus) * alpha
        c_d = max(n_d / volume_l, 1e-8)
        c_c = max(n_c / volume_l, 1e-8)
        c_h = max(n_h / volume_l, 1e-8)
        q = (c_c ** 2 * c_h ** 2) / max(c_d, 1e-12)
        rows.append(
            {
                "시간": round(float(t), 2),
                "Q": q,
                "K": k_value,
                "정반응 속도": k_forward * c_d,
                "역반응 속도": k_reverse * (c_c ** 2) * (c_h ** 2),
                "[Cr₂O₇²⁻]": c_d,
                "[CrO₄²⁻]": c_c,
                "[H⁺]": c_h,
            }
        )
    return pd.DataFrame(rows)


def direction_text(q, k):
    if q < k * 0.97:
        return "정반응", "Q < K 이므로 생성물 쪽으로 평형이 이동합니다."
    if q > k * 1.03:
        return "역반응", "Q > K 이므로 반응물 쪽으로 평형이 이동합니다."
    return "평형", "Q ≈ K 이므로 거의 평형 상태입니다."


def append_history(signature, label, q, k, forward_rate, reverse_rate):
    if st.session_state.last_signature != signature:
        st.session_state.history.append(
            {
                "순서": len(st.session_state.history) + 1,
                "실험": label,
                "Q": float(q),
                "K": float(k),
                "정반응 속도": float(forward_rate),
                "역반응 속도": float(reverse_rate),
            }
        )
        st.session_state.history = st.session_state.history[-60:]
        st.session_state.last_signature = signature


def particles_html(no2_count, n2o4_count, animate=True, seed=7):
    rng = random.Random(seed)
    pieces = []
    animation_state = "running" if animate else "paused"
    for i in range(no2_count):
        left = rng.uniform(13, 82)
        top = rng.uniform(22, 76)
        size = rng.uniform(15, 22)
        duration = rng.uniform(3.2, 7.0)
        delay = rng.uniform(-4.0, 0.0)
        pieces.append(
            f'<div class="particle no2" title="NO₂" style="left:{left:.1f}%; top:{top:.1f}%; width:{size:.1f}px; height:{size:.1f}px; animation-duration:{duration:.2f}s; animation-delay:{delay:.2f}s; animation-play-state:{animation_state};"></div>'
        )
    for i in range(n2o4_count):
        left = rng.uniform(13, 78)
        top = rng.uniform(22, 76)
        duration = rng.uniform(4.0, 8.5)
        delay = rng.uniform(-4.0, 0.0)
        pieces.append(
            f'<div class="particle n2o4" title="N₂O₄" style="left:{left:.1f}%; top:{top:.1f}%; animation-duration:{duration:.2f}s; animation-delay:{delay:.2f}s; animation-play-state:{animation_state};"><span></span><span></span></div>'
        )
    return "\n".join(pieces)


def gas_visual_html(vessel, temp_c, pressure_atm, volume_l, c_no2_eq, c_n2o4_eq, animate=True):
    no2_count = int(clamp(6 + c_no2_eq * 8, 3, 34))
    n2o4_count = int(clamp(5 + c_n2o4_eq * 4, 2, 24))
    no2_ratio = clamp(c_no2_eq / max(c_no2_eq + c_n2o4_eq, 1e-8), 0, 1)
    brown_alpha = 0.08 + 0.30 * no2_ratio
    piston_top = clamp(12 + (2.8 - volume_l) / 2.52 * 40, 10, 52)
    is_piston = vessel.startswith("외부")
    vessel_label = "피스톤 실린더" if is_piston else "부피 일정 강철용기"
    vessel_class = "piston-vessel" if is_piston else "steel-vessel"
    piston_html = ""
    if is_piston:
        piston_html = f"""
        <div class="piston-rod"></div>
        <div class="piston-head" style="top:{piston_top:.1f}%;"></div>
        <div class="piston-handle" style="top:{piston_top - 9:.1f}%;">압력 조절</div>
        """
    particles = particles_html(no2_count, n2o4_count, animate, seed=int(temp_c * 11 + pressure_atm * 100 + volume_l * 41))
    return f"""
    <html>
    <head>
    <style>
    body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color:#2d3448; }}
    .stage {{
        height: 520px;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(246,251,255,.96), rgba(255,248,242,.95));
        border: 1px solid rgba(127,182,244,.25);
        box-shadow: inset 0 1px 0 rgba(255,255,255,.8), 0 18px 45px rgba(130,160,190,.16);
        position: relative;
        overflow: hidden;
    }}
    .stage-title {{ position:absolute; left:24px; top:18px; font-weight:900; font-size:20px; color:#34405a; }}
    .legend {{ position:absolute; left:24px; top:54px; display:flex; gap:10px; font-size:13px; color:#63708a; }}
    .chip {{ background:rgba(255,255,255,.75); border:1px solid rgba(127,182,244,.24); border-radius:999px; padding:6px 10px; }}
    .vessel-wrap {{ position:absolute; left:8%; top:16%; width:58%; height:70%; }}
    .vessel {{
        position:absolute; left:8%; top:3%; width:78%; height:82%;
        background: rgba(180, 94, 40, {brown_alpha:.2f});
        border: 9px solid #98caff;
        box-shadow: inset 0 0 24px rgba(255,255,255,.55), 0 18px 50px rgba(137, 174, 210, .20);
        overflow:hidden;
    }}
    .piston-vessel {{ border-radius: 42px 42px 58px 58px; }}
    .steel-vessel {{ border-radius: 42px; border-color:#8c99aa; background: linear-gradient(135deg, rgba(210,220,230,.36), rgba(255,255,255,.52)), rgba(180, 94, 40, {brown_alpha:.2f}); }}
    .piston-head {{
        position:absolute; left:4%; width:92%; height:20px;
        background: linear-gradient(180deg, #cfd8e6, #aeb9c8);
        border: 3px solid #8794a5;
        border-radius: 14px;
        z-index: 3;
        box-shadow: 0 6px 14px rgba(80,95,120,.17);
    }}
    .piston-rod {{ position:absolute; left:47%; top:-10%; height:22%; width:12px; background:#98a5b5; border-radius:999px; z-index:4; }}
    .piston-handle {{
        position:absolute; left:35%; transform:translateY(-100%);
        z-index:5; font-size:12px; color:#526075; background:rgba(255,255,255,.85);
        padding:5px 10px; border-radius:999px; border:1px solid rgba(120,150,180,.22);
    }}
    .particle {{ position:absolute; z-index:2; transform:translate(-50%,-50%); animation-name: drift; animation-iteration-count: infinite; animation-direction: alternate; animation-timing-function: ease-in-out; }}
    .no2 {{ border-radius:50%; background: radial-gradient(circle at 35% 35%, #ffb179 0%, #d87938 44%, #a44c1f 100%); box-shadow: 0 0 0 2px rgba(255,255,255,.55); }}
    .n2o4 {{ width:42px; height:24px; }}
    .n2o4 span {{ position:absolute; width:20px; height:20px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #ffffff 0%, #dfe8f3 45%, #8c99aa 100%); border:3px solid #7c8999; box-sizing:border-box; }}
    .n2o4 span:first-child {{ left:0; top:2px; }}
    .n2o4 span:last-child {{ left:17px; top:2px; }}
    @keyframes drift {{
        0% {{ transform: translate(-50%,-50%) translate(-9px, 7px) rotate(-8deg); }}
        50% {{ transform: translate(-50%,-50%) translate(12px, -11px) rotate(7deg); }}
        100% {{ transform: translate(-50%,-50%) translate(-5px, 14px) rotate(13deg); }}
    }}
    .thermo {{ position:absolute; right:8%; top:8%; width:18%; height:78%; display:flex; align-items:center; justify-content:center; }}
    .thermo-body {{ position:relative; width:54px; height:330px; border:9px solid #8d99a8; border-radius:999px; background:rgba(255,255,255,.68); }}
    .thermo-fill {{ position:absolute; left:12px; bottom:16px; width:30px; height:{clamp(55 + temp_c * 2.35, 45, 287):.1f}px; background:linear-gradient(180deg,#ff8da1,#ff5f78); border-radius:999px; }}
    .thermo-bulb {{ position:absolute; bottom:-28px; left:-20px; width:94px; height:94px; border-radius:50%; background:#ff627c; border:9px solid #8d99a8; box-sizing:border-box; }}
    .thermo-label {{ position:absolute; right:8%; bottom:7%; width:18%; text-align:center; font-size:24px; font-weight:900; color:#4b5568; }}
    .volume-card {{ position:absolute; right:6%; bottom:18%; background:rgba(255,255,255,.78); border:1px solid rgba(130,160,190,.22); border-radius:18px; padding:12px 18px; min-width:124px; text-align:center; font-weight:900; color:#526075; }}
    .bottom-label {{ position:absolute; left:11%; bottom:5%; font-weight:900; color:#4b5568; background:rgba(255,255,255,.72); border:1px solid rgba(130,160,190,.20); border-radius:999px; padding:8px 14px; }}
    </style>
    </head>
    <body>
        <div class="stage">
            <div class="stage-title">2NO₂(g) ⇌ N₂O₄(g)</div>
            <div class="legend"><span class="chip">● NO₂ 적갈색</span><span class="chip">○ N₂O₄ 무색</span></div>
            <div class="vessel-wrap">
                <div class="vessel {vessel_class}">
                    {piston_html}
                    {particles}
                </div>
                <div class="bottom-label">{escape(vessel_label)} · {pressure_atm:.2f} atm</div>
            </div>
            <div class="thermo">
                <div class="thermo-body"><div class="thermo-fill"></div><div class="thermo-bulb"></div></div>
            </div>
            <div class="thermo-label">{temp_c:.0f}°C</div>
            <div class="volume-card">{volume_l:.2f} L</div>
        </div>
    </body>
    </html>
    """


def solution_color(cr2o7_m, cro4_m):
    total = max(cr2o7_m + cro4_m, 1e-8)
    yellow_ratio = clamp(cro4_m / total, 0, 1)
    # RGB interpolation from dichromate orange to chromate yellow
    r = int(238 + 14 * yellow_ratio)
    g = int(133 + 74 * yellow_ratio)
    b = int(40 + 12 * yellow_ratio)
    return f"rgb({r},{g},{b})", yellow_ratio


def chromate_visual_html(temp_c, cr2o7_m, cro4_m, hplus_m, volume_l):
    color, yellow_ratio = solution_color(cr2o7_m, cro4_m)
    level = clamp(58 + (volume_l - 1.0) * 20, 42, 76)
    bubbles = []
    rng = random.Random(int(temp_c * 9 + cr2o7_m * 10000 + cro4_m * 10000))
    for i in range(26):
        left = rng.uniform(18, 82)
        top = rng.uniform(24, 78)
        size = rng.uniform(5, 14)
        alpha = rng.uniform(0.18, 0.45)
        bubbles.append(f'<span style="left:{left:.1f}%; top:{top:.1f}%; width:{size:.1f}px; height:{size:.1f}px; opacity:{alpha:.2f};"></span>')
    bubbles_html = "".join(bubbles)
    return f"""
    <html>
    <head>
    <style>
    body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color:#2d3448; }}
    .stage {{
        height: 520px;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(246,251,255,.96), rgba(255,248,242,.95));
        border: 1px solid rgba(127,182,244,.25);
        box-shadow: inset 0 1px 0 rgba(255,255,255,.8), 0 18px 45px rgba(130,160,190,.16);
        position: relative;
        overflow: hidden;
    }}
    .stage-title {{ position:absolute; left:24px; top:18px; font-weight:900; font-size:19px; color:#34405a; }}
    .legend {{ position:absolute; left:24px; top:54px; display:flex; gap:10px; font-size:13px; color:#63708a; }}
    .chip {{ background:rgba(255,255,255,.75); border:1px solid rgba(127,182,244,.24); border-radius:999px; padding:6px 10px; }}
    .beaker-wrap {{ position:absolute; left:9%; top:16%; width:60%; height:70%; }}
    .beaker {{
        position:absolute; left:12%; top:2%; width:66%; height:86%;
        border-left: 8px solid #95a3b4; border-right: 8px solid #95a3b4; border-bottom: 8px solid #95a3b4;
        border-radius: 0 0 54px 54px;
        background:rgba(255,255,255,.35); overflow:hidden;
        box-shadow: inset 0 0 24px rgba(255,255,255,.8), 0 20px 50px rgba(137,174,210,.19);
    }}
    .rim {{ position:absolute; left:8%; top:2%; width:74%; height:22px; border:7px solid #95a3b4; border-radius:50%; background:rgba(255,255,255,.65); z-index:3; }}
    .solution {{ position:absolute; left:0; bottom:0; width:100%; height:{level:.1f}%; background:{color}; opacity:.86; }}
    .surface {{ position:absolute; left:0; top:{100-level:.1f}%; width:100%; height:18px; background:rgba(255,255,255,.42); border-radius:50%; z-index:2; }}
    .bubble span {{ position:absolute; border:2px solid rgba(255,255,255,.72); border-radius:50%; z-index:2; }}
    .info {{ position:absolute; left:13%; bottom:5%; background:rgba(255,255,255,.78); border:1px solid rgba(130,160,190,.22); border-radius:999px; padding:8px 14px; font-weight:900; color:#4b5568; }}
    .thermo {{ position:absolute; right:8%; top:8%; width:18%; height:78%; display:flex; align-items:center; justify-content:center; }}
    .thermo-body {{ position:relative; width:54px; height:330px; border:9px solid #8d99a8; border-radius:999px; background:rgba(255,255,255,.68); }}
    .thermo-fill {{ position:absolute; left:12px; bottom:16px; width:30px; height:{clamp(55 + temp_c * 2.35, 45, 287):.1f}px; background:linear-gradient(180deg,#ffcf77,#ff8560); border-radius:999px; }}
    .thermo-bulb {{ position:absolute; bottom:-28px; left:-20px; width:94px; height:94px; border-radius:50%; background:#ff9a62; border:9px solid #8d99a8; box-sizing:border-box; }}
    .thermo-label {{ position:absolute; right:8%; bottom:7%; width:18%; text-align:center; font-size:24px; font-weight:900; color:#4b5568; }}
    .color-card {{ position:absolute; right:6%; bottom:18%; background:rgba(255,255,255,.78); border:1px solid rgba(130,160,190,.22); border-radius:18px; padding:12px 18px; min-width:132px; text-align:center; font-weight:900; color:#526075; }}
    </style>
    </head>
    <body>
        <div class="stage">
            <div class="stage-title">Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺</div>
            <div class="legend"><span class="chip">Cr₂O₇²⁻ 주황</span><span class="chip">CrO₄²⁻ 노랑</span></div>
            <div class="beaker-wrap">
                <div class="rim"></div>
                <div class="beaker">
                    <div class="solution"></div>
                    <div class="surface"></div>
                    <div class="bubble">{bubbles_html}</div>
                </div>
                <div class="info">용액 부피 {volume_l:.2f} L</div>
            </div>
            <div class="thermo">
                <div class="thermo-body"><div class="thermo-fill"></div><div class="thermo-bulb"></div></div>
            </div>
            <div class="thermo-label">{temp_c:.0f}°C</div>
            <div class="color-card">노란색 비율 {yellow_ratio*100:.0f}%</div>
        </div>
    </body>
    </html>
    """

# -----------------------------
# Header and experiment selector
# -----------------------------
header_col, select_col = st.columns([0.44, 0.56], vertical_alignment="center")
with header_col:
    st.markdown(
        """
        <div class="hero-card">
          <div class="hero-title">⚗️ 화학 평형 시뮬레이터</div>
          <p class="hero-subtitle">조건을 바꾸면 Q, K, 색 변화, 반응 속도 그래프가 함께 변합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with select_col:
    st.write("")
    experiment = st.selectbox(
        "실험 선택",
        [
            "이산화질소 ↔ 사산화이질소  |  2NO₂(g) ⇌ N₂O₄(g)",
            "다이크로메이트 ↔ 크로메이트  |  Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)",
        ],
        label_visibility="collapsed",
    )

left, center, right = st.columns([0.92, 1.50, 1.12], gap="large")

# -----------------------------
# Gas experiment
# -----------------------------
if experiment.startswith("이산화질소"):
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("조건 변화")
        st.markdown('<div class="reaction-box">2NO₂(g) ⇌ N₂O₄(g)</div>', unsafe_allow_html=True)
        vessel = st.radio(
            "용기",
            ["외부 대기압과 일정하게 압력 유지할 수 있는 피스톤이 달린 실린더", "부피가 일정한 강철용기"],
            index=0,
        )
        temp_c = st.slider("온도 조건 변화 (°C)", 0, 100, 25, 1)
        pressure_atm = st.slider("압력 조건 변화 (atm)", 0.20, 3.00, 1.00, 0.05)
        fixed_volume = st.slider("강철용기 부피 (L)", 0.50, 2.50, float(st.session_state.gas_volume_fixed), 0.05)
        st.session_state.gas_volume_fixed = fixed_volume
        st.divider()
        st.write("농도 / 물질 첨가·제거")
        material = st.selectbox("대상 물질", ["NO₂ 첨가 / 제거", "N₂O₄ 첨가 / 제거"])
        amount = st.slider("조작량 (mol)", 0.01, 0.50, 0.10, 0.01)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("첨가", use_container_width=True):
                if material.startswith("NO₂"):
                    st.session_state.gas_no2 += amount
                else:
                    st.session_state.gas_n2o4 += amount
        with c2:
            if st.button("제거", use_container_width=True):
                if material.startswith("NO₂"):
                    st.session_state.gas_no2 = max(0.01, st.session_state.gas_no2 - amount)
                else:
                    st.session_state.gas_n2o4 = max(0.01, st.session_state.gas_n2o4 - amount)
        with c3:
            if st.button("초기화", use_container_width=True):
                st.session_state.gas_no2 = GAS_DEFAULTS["gas_no2"]
                st.session_state.gas_n2o4 = GAS_DEFAULTS["gas_n2o4"]
                st.session_state.history = []
                st.session_state.last_signature = None
        molecule_motion = st.checkbox("NO₂, N₂O₄ 분자 무작위 운동 애니메이션", value=True)
        live_history = st.checkbox("조건 변화 기록을 그래프에 누적", value=True)
        st.markdown('<p class="small-note">피스톤은 중앙 실린더 안에 통합했습니다. 슬라이더를 움직이면 실린더, 온도계, 색, 그래프가 함께 갱신됩니다.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    volume_l = gas_volume(vessel, pressure_atm, temp_c, fixed_volume)
    k_value = gas_k(temp_c)
    eq = gas_equilibrium(st.session_state.gas_no2, st.session_state.gas_n2o4, volume_l, k_value)
    direction, direction_sentence = direction_text(eq["q_initial"], k_value)
    path = gas_path(
        st.session_state.gas_no2,
        st.session_state.gas_n2o4,
        eq["eq_no2"],
        eq["eq_n2o4"],
        volume_l,
        k_value,
        temp_c,
    )
    signature = (
        "gas",
        round(st.session_state.gas_no2, 3),
        round(st.session_state.gas_n2o4, 3),
        vessel,
        round(temp_c, 1),
        round(pressure_atm, 2),
        round(volume_l, 3),
    )
    if live_history:
        append_history(signature, "NO₂/N₂O₄", eq["q_initial"], k_value, path["정반응 속도"].iloc[0], path["역반응 속도"].iloc[0])

    with center:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        components.html(
            gas_visual_html(vessel, temp_c, pressure_atm, volume_l, eq["c_no2_eq"], eq["c_n2o4_eq"], molecule_motion),
            height=540,
            scrolling=False,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("실험 결과")
        m1, m2 = st.columns(2)
        m1.metric("평형상수 K", f"{k_value:.4g}")
        m2.metric("초기 반응지수 Q", f"{eq['q_initial']:.4g}")
        m3, m4 = st.columns(2)
        m3.metric("평형 이동", direction)
        m4.metric("부피", f"{volume_l:.2f} L")
        st.markdown(
            f"""
            <span class="status-pill">{escape(direction_sentence)}</span>
            <span class="status-pill">NO₂가 많을수록 적갈색이 진해집니다.</span>
            """,
            unsafe_allow_html=True,
        )
        st.write("계산식")
        st.code("2NO₂(g) ⇌ N₂O₄(g)\nK = [N₂O₄] / [NO₂]²\nQ = [N₂O₄]초기 / [NO₂]초기²", language="text")
        table = pd.DataFrame(
            [
                ["NO₂", st.session_state.gas_no2, eq["eq_no2"], eq["c_no2_eq"]],
                ["N₂O₄", st.session_state.gas_n2o4, eq["eq_n2o4"], eq["c_n2o4_eq"]],
            ],
            columns=["물질", "현재 mol", "평형 mol", "평형 농도(M)"],
        )
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.write("Q와 K의 시간 변화")
        st.line_chart(path.set_index("시간")[["Q", "K"]])
        st.write("정반응 속도와 역반응 속도")
        st.line_chart(path.set_index("시간")[["정반응 속도", "역반응 속도"]])
        if live_history and len(st.session_state.history) >= 2:
            st.write("조건 변화 누적 기록")
            hist = pd.DataFrame(st.session_state.history)
            st.line_chart(hist.set_index("순서")[["Q", "K"]])
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Chromate experiment
# -----------------------------
else:
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("조건 변화")
        st.markdown('<div class="reaction-box">Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺</div>', unsafe_allow_html=True)
        temp_c = st.slider("온도 조건 변화 (°C)", 0, 100, 25, 1)
        st.divider()
        st.write("농도 / 물질 첨가·제거")
        material = st.selectbox("첨가 가능 물질", ["HCl", "NaOH", "H₂O"])
        amount = st.slider("조작량", 0.01, 0.50, 0.10, 0.01)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("첨가", use_container_width=True):
                if material == "HCl":
                    st.session_state.hplus += amount
                elif material == "NaOH":
                    st.session_state.hplus = max(0.001, st.session_state.hplus - amount)
                else:
                    st.session_state.solution_volume += amount
        with c2:
            if st.button("제거", use_container_width=True):
                if material == "HCl":
                    st.session_state.hplus = max(0.001, st.session_state.hplus - amount)
                elif material == "NaOH":
                    st.session_state.hplus += amount
                else:
                    st.session_state.solution_volume = max(0.30, st.session_state.solution_volume - amount)
        with c3:
            if st.button("초기화", use_container_width=True):
                st.session_state.cr2o7 = CHROMATE_DEFAULTS["cr2o7"]
                st.session_state.cro4 = CHROMATE_DEFAULTS["cro4"]
                st.session_state.hplus = CHROMATE_DEFAULTS["hplus"]
                st.session_state.solution_volume = CHROMATE_DEFAULTS["solution_volume"]
                st.session_state.history = []
                st.session_state.last_signature = None
        st.caption("HCl을 넣으면 H⁺가 증가하여 주황색 Cr₂O₇²⁻ 쪽이 유리해집니다. NaOH는 H⁺를 줄여 노란색 CrO₄²⁻ 쪽을 유리하게 만듭니다.")
        live_history = st.checkbox("조건 변화 기록을 그래프에 누적", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    volume_l = max(float(st.session_state.solution_volume), 0.30)
    k_value = chromate_k(temp_c)
    eq = chromate_equilibrium(st.session_state.cr2o7, st.session_state.cro4, st.session_state.hplus, volume_l, k_value)
    direction, direction_sentence = direction_text(eq["q_initial"], k_value)
    path = chromate_path(
        st.session_state.cr2o7,
        st.session_state.cro4,
        st.session_state.hplus,
        eq["eq_cr2o7"],
        eq["eq_cro4"],
        eq["eq_hplus"],
        volume_l,
        k_value,
        temp_c,
    )
    signature = (
        "chromate",
        round(st.session_state.cr2o7, 4),
        round(st.session_state.cro4, 4),
        round(st.session_state.hplus, 4),
        round(volume_l, 3),
        round(temp_c, 1),
    )
    if live_history:
        append_history(signature, "Cr₂O₇/CrO₄", eq["q_initial"], k_value, path["정반응 속도"].iloc[0], path["역반응 속도"].iloc[0])

    with center:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        components.html(
            chromate_visual_html(temp_c, eq["eq_cr2o7"], eq["eq_cro4"], eq["eq_hplus"], volume_l),
            height=540,
            scrolling=False,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("실험 결과")
        m1, m2 = st.columns(2)
        m1.metric("평형상수 K", f"{k_value:.4g}")
        m2.metric("초기 반응지수 Q", f"{eq['q_initial']:.4g}")
        m3, m4 = st.columns(2)
        m3.metric("평형 이동", direction)
        m4.metric("부피", f"{volume_l:.2f} L")
        st.markdown(
            f"""
            <span class="status-pill">{escape(direction_sentence)}</span>
            <span class="status-pill">Cr₂O₇²⁻는 주황색, CrO₄²⁻는 노란색입니다.</span>
            """,
            unsafe_allow_html=True,
        )
        st.write("계산식")
        st.code("Cr₂O₇²⁻ + H₂O ⇌ 2CrO₄²⁻ + 2H⁺\nK = [CrO₄²⁻]²[H⁺]² / [Cr₂O₇²⁻]\nQ = [CrO₄²⁻]초기²[H⁺]초기² / [Cr₂O₇²⁻]초기", language="text")
        table = pd.DataFrame(
            [
                ["Cr₂O₇²⁻", st.session_state.cr2o7, eq["eq_cr2o7"], eq["c_cr2o7_eq"]],
                ["CrO₄²⁻", st.session_state.cro4, eq["eq_cro4"], eq["c_cro4_eq"]],
                ["H⁺", st.session_state.hplus, eq["eq_hplus"], eq["c_hplus_eq"]],
            ],
            columns=["물질", "현재 mol", "평형 mol", "평형 농도(M)"],
        )
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.write("Q와 K의 시간 변화")
        st.line_chart(path.set_index("시간")[["Q", "K"]])
        st.write("정반응 속도와 역반응 속도")
        st.line_chart(path.set_index("시간")[["정반응 속도", "역반응 속도"]])
        if live_history and len(st.session_state.history) >= 2:
            st.write("조건 변화 누적 기록")
            hist = pd.DataFrame(st.session_state.history)
            st.line_chart(hist.set_index("순서")[["Q", "K"]])
        st.markdown('</div>', unsafe_allow_html=True)

st.info(
    "활용 팁 — 그래프는 조건을 바꿀 때마다 즉시 갱신됩니다. "
    "분자 애니메이션은 중앙 용기 안에 통합되어 있으며, 실제 실험값보다는 르샤틀리에 원리와 Q-K 비교를 이해하기 위한 교육용 시뮬레이터입니다."
)
