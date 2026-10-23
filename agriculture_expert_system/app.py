"""
app.py
======
Interactive Streamlit Web Application for the
Rule-Based Expert System for Agriculture Using Python.

Features:
- Home / Overview: Modern dashboard, KPI metrics, architecture pipeline, 1-click viva demos
- Crop Recommendation: Multi-criteria crop evaluation with live pH spectrum meter & dossiers
- Problem Diagnosis: Crop symptom diagnostics with moisture context, severity & KVK alerts
- Soil & Fertilizer Advice: Soil pH color gauge, texture dynamics, chemical & organic amendments
- AI Rule Base & Trace Inspector: Transparent rule inspection, knowledge matrix & viva Q&A
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import streamlit as st

# Ensure local modules are resolvable regardless of working directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from rules import (
    run_crop_recommendation,
    run_crop_diagnosis,
    run_soil_management_advice,
    get_all_rules
)
from knowledge_base import (
    CROPS_DATABASE,
    SOIL_PROFILES,
    CROP_PROBLEMS_DATABASE,
    SOIL_PH_GUIDELINES
)

# ==============================================================================
# PAGE CONFIGURATION & THEME
# ==============================================================================
st.set_page_config(
    page_title="AgriExpert AI | Rule-Based Agriculture Expert System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics, glassmorphism, responsive cards, and contrast fixes
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Base App Styling */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.9) !important;
        backdrop-filter: blur(8px);
    }

    /* Headings outside hero banners */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.3px;
    }

    p, span, label {
        color: #334155;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }

    /* Hero Banner with Specific Contrast Fix */
    .app-hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        padding: 2.2rem 2.6rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 14px 30px -8px rgba(6, 95, 70, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.18);
        position: relative;
        overflow: hidden;
    }

    .app-hero-banner::after {
        content: '';
        position: absolute;
        top: -40%;
        right: -20%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
        pointer-events: none;
    }

    .app-hero-title {
        color: #ffffff !important;
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.25 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
    }

    .app-hero-sub {
        font-size: 1.05rem !important;
        font-weight: 400 !important;
        color: #e6fffa !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0 !important;
        line-height: 1.55 !important;
        max-width: 900px !important;
        opacity: 0.95 !important;
    }

    /* Glowing Badge in Hero */
    .hero-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(6px);
        color: #ffffff !important;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Metric & KPI Cards */
    .kpi-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }

    .kpi-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }

    .kpi-desc {
        font-size: 0.82rem;
        color: #10b981;
        font-weight: 600;
    }

    /* Feature Card */
    .custom-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }

    .custom-card h4 {
        color: #0f172a;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 0.6rem;
    }

    /* Crop Dossier Card */
    .crop-dossier {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.04);
        border-top: 4px solid #10b981;
    }

    .crop-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #f1f5f9;
    }

    .crop-name {
        font-size: 1.3rem;
        font-weight: 800;
        color: #065f46;
        margin: 0;
    }

    .crop-sci {
        font-size: 0.85rem;
        font-style: italic;
        color: #64748b;
    }

    .crop-badge-tag {
        background: #ecfdf5;
        color: #047857;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        border: 1px solid #a7f3d0;
    }

    .mini-stat-box {
        background: #f8fafc;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    .mini-stat-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
    }

    .mini-stat-val {
        font-size: 0.95rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.1rem;
    }

    /* Rule Badge */
    .rule-badge {
        display: inline-block;
        background: #ecfdf5 !important;
        color: #047857 !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        border: 1px solid #a7f3d0 !important;
        margin-bottom: 0.5rem;
    }

    .rule-badge-soil {
        background: #eff6ff !important;
        color: #1d4ed8 !important;
        border-color: #bfdbfe !important;
    }

    .rule-badge-diag {
        background: #fff7ed !important;
        color: #c2410c !important;
        border-color: #fed7aa !important;
    }

    /* Pipeline Architecture Box */
    .pipe-step {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .pipe-icon {
        font-size: 2rem;
        margin-bottom: 0.4rem;
    }

    .pipe-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #0f172a;
    }

    .pipe-sub {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 0.2rem;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.3rem;
        border-radius: 10px;
        font-size: 0.88rem;
        color: #92400e;
        margin-top: 1.5rem;
        border-top: 1px solid #fef3c7;
        border-right: 1px solid #fef3c7;
        border-bottom: 1px solid #fef3c7;
        line-height: 1.5;
    }

    /* Sidebar Branding */
    .sidebar-brand {
        text-align: center;
        padding: 1.2rem 0.5rem 1rem 0.5rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
        background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%);
        border-radius: 14px;
    }

    .sidebar-brand h2 {
        font-weight: 800;
        color: #065f46 !important;
        margin: 0.4rem 0 0.1rem 0;
        font-size: 1.35rem;
        letter-spacing: -0.5px;
    }

    .sidebar-brand span {
        font-size: 0.8rem;
        color: #059669 !important;
        font-weight: 600;
    }

    /* Streamlit UI Polish */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# HELPER FUNCTIONS: UI COMPONENTS & PRESETS
# ==============================================================================

def render_ph_spectrum(soil_ph: float):
    """Renders a dynamic visual color gauge for soil pH with pointer position."""
    pct = max(0.0, min(100.0, ((soil_ph - 3.0) / 7.0) * 100.0))
    
    if soil_ph < 5.5:
        category = "Strongly Acidic"
        bg_col = "#fee2e2"
        text_col = "#b91c1c"
        border_col = "#fca5a5"
        advisory_hint = "Requires Agricultural Lime (CaCO3) amendment."
    elif soil_ph < 6.5:
        category = "Moderately Acidic"
        bg_col = "#ffedd5"
        text_col = "#c2410c"
        border_col = "#fdba74"
        advisory_hint = "Suitable for Rice, Tea, and Potato."
    elif soil_ph <= 7.5:
        category = "Neutral / Optimal"
        bg_col = "#dcfce7"
        text_col = "#15803d"
        border_col = "#86efac"
        advisory_hint = "Maximum bioavailability of Nitrogen, Phosphorus, and Potassium."
    elif soil_ph <= 8.5:
        category = "Moderately Alkaline"
        bg_col = "#e0f2fe"
        text_col = "#0369a1"
        border_col = "#7dd3fc"
        advisory_hint = "Watch for micronutrient fixations (Zinc, Iron)."
    else:
        category = "Strongly Alkaline / Sodic"
        bg_col = "#f3e8ff"
        text_col = "#7e22ce"
        border_col = "#d8b4fe"
        advisory_hint = "Requires Gypsum (CaSO4·2H2O) + deep leaching."

    st.markdown(f"""
    <div style="background: #ffffff; border-radius: 14px; padding: 1.1rem; border: 1px solid #e2e8f0; margin: 1rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 0.85rem; font-weight: 700; color: #1e293b;">🧪 Soil Reaction Spectrum (pH {soil_ph:.1f})</span>
            <span style="font-size: 0.75rem; font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 9999px; background: {bg_col}; color: {text_col}; border: 1px solid {border_col}; text-transform: uppercase;">
                {category}
            </span>
        </div>
        <div style="position: relative; height: 14px; border-radius: 9999px; background: linear-gradient(to right, #ef4444 0%, #f97316 20%, #eab308 40%, #10b981 55%, #06b6d4 75%, #8b5cf6 100%); margin: 1.1rem 0 0.6rem 0;">
            <div style="position: absolute; left: calc({pct}% - 8px); top: -6px; width: 16px; height: 26px; background: #0f172a; border: 2px solid #ffffff; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.35);"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; font-weight: 600;">
            <span>3.0 (Acidic)</span>
            <span>5.5</span>
            <span>7.0 (Neutral)</span>
            <span>8.5</span>
            <span>10.0 (Alkaline)</span>
        </div>
        <div style="font-size: 0.8rem; color: #475569; margin-top: 0.5rem; background: #f8fafc; padding: 0.4rem 0.7rem; border-radius: 8px;">
            💡 <strong>Agronomic Note:</strong> {advisory_hint}
        </div>
    </div>
    """, unsafe_allow_html=True)


def generate_crop_advisory_text(params: dict, recommended_crops: list, matched_rules: list) -> str:
    """Generates an exportable Farmer Advisory Report."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = [
        "================================================================================",
        "                     AGRIEXPERT AI: FARMER ADVISORY REPORT                      ",
        "         Rule-Based Expert System for Agriculture (Forward Chaining)            ",
        "================================================================================",
        f"Generated Timestamp : {now_str}",
        f"Cropping Season     : {params.get('season')}",
        f"Soil Type           : {params.get('soil_type')}",
        f"Soil pH             : {params.get('soil_ph')}",
        f"Avg Temperature     : {params.get('temperature')} °C",
        f"Rainfall Level      : {params.get('rainfall')}",
        f"Irrigation Access   : {params.get('irrigation')}",
        "--------------------------------------------------------------------------------",
        "RECOMMENDED CANDIDATE CROPS:",
        "--------------------------------------------------------------------------------"
    ]
    if recommended_crops:
        for idx, crop in enumerate(recommended_crops, 1):
            info = CROPS_DATABASE.get(crop, {})
            report.append(f"{idx}. {info.get('name', crop)}")
            report.append(f"   Category   : {info.get('category')}")
            report.append(f"   Duration   : {info.get('duration')}")
            report.append(f"   Optimal pH : {info.get('optimal_ph')}")
            report.append(f"   N-P-K Ratio: {info.get('npk_general_ratio')}")
            report.append(f"   Advisory   : {info.get('management_tip')}")
            report.append("")
    else:
        report.append("No standard crops matched all environmental constraints.")

    report.append("--------------------------------------------------------------------------------")
    report.append("EXPLAINABLE AI AUDIT TRACE (MATCHED PRODUCTION RULES):")
    report.append("--------------------------------------------------------------------------------")
    for mr in matched_rules:
        report.append(f"• Rule ID: {mr['rule_id']} - {mr['name']}")
        report.append(f"  Condition Evaluated: {mr['condition']}")
        report.append(f"  Deduction: {mr['deduction'].get('justification', '')}")
        report.append(f"  Agronomic Reasoning: {mr['explanation']}")
        report.append("")
    report.append("================================================================================")
    report.append("DISCLAIMER: Educational prototype. Please verify with local Krishi Vigyan Kendra.")
    report.append("================================================================================")
    return "\n".join(report)


# ==============================================================================
# SIDEBAR NAVIGATION & SYSTEM HEALTH
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 2.6rem; line-height: 1;">🌱</div>
        <h2>AgriExpert AI</h2>
        <span>Explainable Agronomic Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation Menu",
        [
            "🏠 Home / Overview",
            "🌾 Crop Recommendation",
            "🔍 Problem & Disease Diagnosis",
            "🧪 Soil & Fertilizer Advice",
            "🧠 AI Rule Base & Trace Inspector"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Quick Actions")
    if st.button("🔄 Reset All Form Inputs", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.markdown("#### 📊 System Specifications")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #475569; line-height: 1.6; background: #f8fafc; padding: 0.8rem; border-radius: 10px; border: 1px solid #e2e8f0;">
        <strong>AI Architecture:</strong> Production Rule System<br>
        <strong>Inference Engine:</strong> Forward Chaining<br>
        <strong>Total Rule Count:</strong> 26 Active Rules<br>
        <strong>Knowledge Domains:</strong> Crops, Pathogens, Soils<br>
        <strong>Explainability:</strong> 100% Deterministic<br>
        <strong>Status:</strong> <span style="color: #10b981; font-weight: 700;">● Online / Ready</span>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: HOME / OVERVIEW
# ==============================================================================
if page == "🏠 Home / Overview":
    st.markdown("""
    <div class="app-hero-banner">
        <div class="hero-badge-pill">⚡ Explainable AI • Forward Chaining System</div>
        <div class="app-hero-title">Rule-Based Expert System for Agriculture</div>
        <div class="app-hero-sub">
            An explainable, deterministic Artificial Intelligence platform replicating senior agronomist
            heuristics through 26 domain production rules. No black-box machine learning; 100% auditable conclusions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 KPI Stat Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Active Rules</div>
            <div class="kpi-value">26</div>
            <div class="kpi-desc">🌾 10 Crop • 8 Disease • 8 Soil</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Inference Engine</div>
            <div class="kpi-value">Forward</div>
            <div class="kpi-desc">⚡ Data-Driven Reasoning Cycle</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Supported Crops</div>
            <div class="kpi-value">10</div>
            <div class="kpi-desc">🌱 Cereals, Pulses, Cash Crops</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Explainability</div>
            <div class="kpi-value">100%</div>
            <div class="kpi-desc">🎯 Zero AI Hallucinations</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Visual Architecture Pipeline Flow
    st.markdown("### 🏛️ Expert System AI Architecture Pipeline")
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.markdown("""
        <div class="pipe-step">
            <div class="pipe-icon">📥</div>
            <div class="pipe-title">1. Working Memory</div>
            <div class="pipe-sub">User inputs facts: soil, pH, season, moisture, & leaf symptoms.</div>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="pipe-step">
            <div class="pipe-icon">📚</div>
            <div class="pipe-title">2. Knowledge Base</div>
            <div class="pipe-sub">Declarative facts: crop agronomy, soil chemistry, pathogen profiles.</div>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="pipe-step">
            <div class="pipe-icon">⚙️</div>
            <div class="pipe-title">3. Inference Engine</div>
            <div class="pipe-sub">Forward-chains facts against 26 IF-THEN production rules.</div>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="pipe-step">
            <div class="pipe-icon">⚡</div>
            <div class="pipe-title">4. Fired Rules</div>
            <div class="pipe-sub">Satisfied antecedents execute actions and deduce conclusions.</div>
        </div>
        """, unsafe_allow_html=True)
    with p5:
        st.markdown("""
        <div class="pipe-step">
            <div class="pipe-icon">📊</div>
            <div class="pipe-title">5. Advisory & Trace</div>
            <div class="pipe-sub">Delivers tailored advisory with 100% transparent audit justification.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Quick 1-Click Viva Demo Presets
    st.markdown("### ⚡ Quick Demo Scenarios (1-Click Viva Presets)")
    st.markdown("Click any realistic agricultural scenario below to immediately test the Expert System:")

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        if st.button("🌾 Punjab Rabi Wheat\n(Alluvial, Cool, Irrigated)", use_container_width=True):
            st.session_state["crop_season"] = "Rabi"
            st.session_state["crop_soil"] = "Alluvial"
            st.session_state["crop_ph"] = 6.8
            st.session_state["crop_temp"] = 18.0
            st.session_state["crop_rain"] = "Medium"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.info("Loaded Punjab Rabi Wheat scenario! Switch to **🌾 Crop Recommendation**.")

    with d2:
        if st.button("☁️ Vidarbha Kharif Cotton\n(Black Soil, Warm, Rainfed)", use_container_width=True):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Black"
            st.session_state["crop_ph"] = 7.2
            st.session_state["crop_temp"] = 28.0
            st.session_state["crop_rain"] = "Medium"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.info("Loaded Vidarbha Kharif Cotton scenario! Switch to **🌾 Crop Recommendation**.")

    with d3:
        if st.button("🌧️ Assam Valley Rice\n(Alluvial, High Rain, Warm)", use_container_width=True):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Alluvial"
            st.session_state["crop_ph"] = 6.2
            st.session_state["crop_temp"] = 29.0
            st.session_state["crop_rain"] = "High"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.info("Loaded Assam Valley Rice scenario! Switch to **🌾 Crop Recommendation**.")

    with d4:
        if st.button("🏜️ Rajasthan Dryland Millets\n(Sandy Soil, Low Rain, Hot)", use_container_width=True):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Sandy"
            st.session_state["crop_ph"] = 7.6
            st.session_state["crop_temp"] = 32.0
            st.session_state["crop_rain"] = "Low"
            st.session_state["crop_irrig"] = "No"
            st.session_state["auto_eval_crop"] = True
            st.info("Loaded Rajasthan Millets scenario! Switch to **🌾 Crop Recommendation**.")

    st.write("")
    st.markdown("---")

    # Core AI Features Grid
    st.markdown("### 🚀 Available Expert Modules")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="custom-card" style="border-top: 4px solid #059669;">
            <h4>🌾 Crop Recommendation Engine</h4>
            <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                Evaluates soil texture, soil pH, seasonal suitability, ambient temperature, rainfall ranges, 
                and irrigation infrastructure to recommend high-yielding candidate crops with complete agronomic dossiers.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="custom-card" style="border-top: 4px solid #ea580c;">
            <h4>🔍 Problem & Disease Diagnosis</h4>
            <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                Analyzes foliar symptoms (yellowing, brown spots, wilting, powder), soil moisture levels, and microclimate
                to infer probable fungal infections, nutrient imbalances, or irrigation stress with immediate corrective guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="custom-card" style="border-top: 4px solid #0d9488;">
            <h4>🧪 Soil Health & Fertilizer Advice</h4>
            <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                Assesses soil pH classification and physical texture to deliver chemical amendment advisories 
                (agricultural lime vs. gypsum), organic matter management, and scientific balanced fertilization protocols.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Viva Voce FAQ Card
    with st.expander("🎓 Engineering Viva Voce Master Cheat Sheet (Click to Expand)"):
        st.markdown("""
        **Q1: Why use a Rule-Based Expert System instead of Machine Learning for this project?**
        - *Answer:* Traditional ML models (like neural networks or random forests) are "black-boxes" that require thousands of training records and can hallucinate or fail to explain *why* an advisory was given. In agriculture, where misapplying a chemical could destroy a farmer's crop, **100% deterministic explainability** (XAI) is critical. Every conclusion links directly to an agronomic rule.

        **Q2: What is the difference between Forward Chaining and Backward Chaining?**
        - *Answer:* 
          - **Forward Chaining (Data-Driven):** Starts with known facts in Working Memory (e.g., season=Rabi, soil=Alluvial, irrigation=Yes) and checks rule antecedents to deduce new facts (e.g., recommend Wheat). This is what our system implements.
          - **Backward Chaining (Goal-Driven):** Starts with a hypothesis/goal (e.g., "Is Wheat suitable?") and works backward to verify if facts support that hypothesis.

        **Q3: What are the three primary components of an Expert System?**
        - *Answer:* 
          1. **Knowledge Base:** Stores domain facts and heuristics.
          2. **Inference Engine:** Evaluates rules against working memory.
          3. **User Interface / Explanation Facility:** Interacts with the user and justifies deductions.
        """)

    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Academic Disclaimer:</strong> The recommendations provided by this expert system are based on educational
        agronomic heuristics. In real-world farming, local microclimates, seed varieties, and official laboratory soil tests from
        government Krishi Vigyan Kendras (KVK) must always take precedence.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 2: CROP RECOMMENDATION
# ==============================================================================
elif page == "🌾 Crop Recommendation":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #059669 100%);">
        <div class="hero-badge-pill">🌾 Multi-Criteria Evaluation Engine</div>
        <div class="app-hero-title">🌾 Crop Recommendation Expert System</div>
        <div class="app-hero-sub">
            Infer suitable crops based on soil characteristics, seasonal dynamics, rainfall, and irrigation availability
            using Forward-Chaining production rules.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Preset Bar
    st.markdown("##### ⚡ Quick Farm Presets:")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        if st.button("🌾 Punjab Rabi Wheat", key="preset_wheat"):
            st.session_state["crop_season"] = "Rabi"
            st.session_state["crop_soil"] = "Alluvial"
            st.session_state["crop_ph"] = 6.8
            st.session_state["crop_temp"] = 18.0
            st.session_state["crop_rain"] = "Medium"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.rerun()
    with p_col2:
        if st.button("☁️ Vidarbha Kharif Cotton", key="preset_cotton"):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Black"
            st.session_state["crop_ph"] = 7.2
            st.session_state["crop_temp"] = 28.0
            st.session_state["crop_rain"] = "Medium"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.rerun()
    with p_col3:
        if st.button("🌧️ Assam Lowland Rice", key="preset_rice"):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Alluvial"
            st.session_state["crop_ph"] = 6.2
            st.session_state["crop_temp"] = 29.0
            st.session_state["crop_rain"] = "High"
            st.session_state["crop_irrig"] = "Yes"
            st.session_state["auto_eval_crop"] = True
            st.rerun()
    with p_col4:
        if st.button("🏜️ Rajasthan Millets", key="preset_millet"):
            st.session_state["crop_season"] = "Kharif"
            st.session_state["crop_soil"] = "Sandy"
            st.session_state["crop_ph"] = 7.6
            st.session_state["crop_temp"] = 32.0
            st.session_state["crop_rain"] = "Low"
            st.session_state["crop_irrig"] = "No"
            st.session_state["auto_eval_crop"] = True
            st.rerun()

    st.write("")

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📥 1. Environmental & Soil Parameters")
        
        def_season = st.session_state.get("crop_season", "Kharif")
        def_soil = st.session_state.get("crop_soil", "Black")
        def_ph = float(st.session_state.get("crop_ph", 6.8))
        def_temp = float(st.session_state.get("crop_temp", 26.0))
        def_rain = st.session_state.get("crop_rain", "Medium")
        def_irrig = st.session_state.get("crop_irrig", "Yes")

        season_options = ["Kharif", "Rabi", "Summer"]
        soil_options = ["Black", "Alluvial", "Red", "Sandy"]
        rain_options = ["Low", "Medium", "High"]
        irrig_options = ["Yes", "No"]

        with st.form("crop_form"):
            season = st.selectbox(
                "📅 Current Cropping Season",
                season_options,
                index=season_options.index(def_season) if def_season in season_options else 0,
                help="Kharif (Monsoon / Autumn), Rabi (Winter / Spring), Summer (Zaid / Hot dry season)"
            )

            soil_type = st.selectbox(
                "🌱 Soil Texture / Type",
                soil_options,
                index=soil_options.index(def_soil) if def_soil in soil_options else 0,
                help="Physical texture and moisture retention capacity of farmland"
            )

            soil_ph = st.slider(
                "🧪 Tested Soil pH Value",
                min_value=3.0,
                max_value=10.0,
                value=def_ph,
                step=0.1,
                help="Soil reaction: 3.0-5.5 strongly acidic, 6.5-7.5 ideal/neutral, 8.5-10 alkaline"
            )

            col_temp, col_rain = st.columns(2)
            with col_temp:
                temperature = st.number_input(
                    "🌡️ Avg Temperature (°C)",
                    min_value=5.0,
                    max_value=50.0,
                    value=def_temp,
                    step=1.0,
                    help="Average ambient temperature during the crop vegetative phase"
                )
            with col_rain:
                rainfall = st.selectbox(
                    "🌧️ Expected Rainfall",
                    rain_options,
                    index=rain_options.index(def_rain) if def_rain in rain_options else 1,
                    help="Low (< 500 mm), Medium (500 - 1000 mm), High (> 1000 mm)"
                )

            irrigation = st.selectbox(
                "💧 Assured Irrigation Available?",
                irrig_options,
                index=irrig_options.index(def_irrig) if def_irrig in irrig_options else 0,
                help="Canal, borewell, tube-well, or micro-drip irrigation availability"
            )

            submit_crop = st.form_submit_button("🌿 Evaluate Crop Suitability", use_container_width=True)

        render_ph_spectrum(soil_ph)

    with col_result:
        st.markdown("### 📋 2. AI Inference Results & Dossiers")
        
        should_evaluate = submit_crop or st.session_state.get("auto_eval_crop", False)
        if st.session_state.get("auto_eval_crop", False):
            st.session_state["auto_eval_crop"] = False

        if should_evaluate:
            results = run_crop_recommendation(
                soil_type=soil_type,
                soil_ph=soil_ph,
                season=season,
                temperature=temperature,
                rainfall=rainfall,
                irrigation=irrigation
            )

            recommended_crops = results["recommended_crops"]
            matched_rules = results["matched_rules"]
            working_memory = results["working_memory_facts"]

            if recommended_crops:
                st.success(f"🎉 **{len(recommended_crops)} Candidate Crop(s) Successfully Recommended!**")
                
                advisory_report = generate_crop_advisory_text(
                    params={
                        "season": season, "soil_type": soil_type, "soil_ph": soil_ph,
                        "temperature": temperature, "rainfall": rainfall, "irrigation": irrigation
                    },
                    recommended_crops=recommended_crops,
                    matched_rules=matched_rules
                )
                st.download_button(
                    label="📄 Download Official Farmer Advisory Report (.txt)",
                    data=advisory_report,
                    file_name=f"AgriExpert_Advisory_{season}_{soil_type}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.write("")

                for crop_name in recommended_crops:
                    profile = CROPS_DATABASE.get(crop_name, {})
                    st.markdown(f"""
                    <div class="crop-dossier">
                        <div class="crop-header">
                            <div>
                                <span class="crop-name">🌾 {crop_name}</span><br>
                                <span class="crop-sci">{profile.get('name', crop_name)}</span>
                            </div>
                            <span class="crop-badge-tag">{profile.get('category', 'Field Crop')}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin: 0.8rem 0;">
                            <div class="mini-stat-box">
                                <div class="mini-stat-label">Optimal pH</div>
                                <div class="mini-stat-val">{profile.get('optimal_ph', '6.0 - 7.5')}</div>
                            </div>
                            <div class="mini-stat-box">
                                <div class="mini-stat-label">Duration</div>
                                <div class="mini-stat-val">{profile.get('duration', '120d')}</div>
                            </div>
                            <div class="mini-stat-box">
                                <div class="mini-stat-label">Optimal Temp</div>
                                <div class="mini-stat-val">{profile.get('optimal_temp', '20-30°C')}</div>
                            </div>
                            <div class="mini-stat-box">
                                <div class="mini-stat-label">NPK Ratio</div>
                                <div class="mini-stat-val" style="font-size: 0.8rem;">{profile.get('npk_general_ratio', 'General')}</div>
                            </div>
                        </div>
                        <p style="font-size: 0.88rem; color: #334155; margin: 0.5rem 0;">
                            <strong>Agronomic Profile:</strong> {profile.get('description', '')}
                        </p>
                        <div style="background: #f0fdf4; border-left: 3px solid #10b981; padding: 0.5rem 0.8rem; border-radius: 6px; font-size: 0.82rem; color: #065f46;">
                            💡 <strong>Field Management:</strong> {profile.get('management_tip', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(
                    "⚠️ **No standard crops matched all your strict environmental constraints.**\n\n"
                    "Possible reasons: Temperature may be outside typical cultivation ranges, or low rainfall "
                    "without irrigation limits crop establishment. Try adjusting inputs or review unmatched rules below."
                )

            st.markdown("#### 🧠 Explainable AI: Matched Rules Audit Trace")
            if matched_rules:
                for mr in matched_rules:
                    st.markdown(f"""
                    <div class="custom-card" style="border-left: 4px solid #10b981; padding: 1.1rem; margin-bottom: 0.8rem;">
                        <span class="rule-badge">{mr['rule_id']} • {mr['name']}</span>
                        <div style="margin: 0.4rem 0; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #1e293b; background: #f8fafc; padding: 0.5rem; border-radius: 6px;">
                            <strong>IF:</strong> {mr['condition']}
                        </div>
                        <p style="margin: 0.3rem 0; font-size: 0.88rem; color: #047857;">
                            <strong>THEN DEDUCE:</strong> {mr['deduction'].get('justification', '')}
                        </p>
                        <p style="margin: 0; font-size: 0.82rem; color: #64748b;">
                            <em>Agronomic Justification:</em> {mr['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No rule conditions were satisfied.")

            with st.expander("🔍 Inspect Working Memory Snapshot (JSON Facts)"):
                st.json(working_memory)

        else:
            st.info("👈 Select your agricultural parameters on the left (or pick a Quick Preset above) and click **Evaluate Crop Suitability**.")


# ==============================================================================
# PAGE 3: PROBLEM & DISEASE DIAGNOSIS
# ==============================================================================
elif page == "🔍 Problem & Disease Diagnosis":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #78350f 0%, #9a3412 50%, #c2410c 100%);">
        <div class="hero-badge-pill">🩺 Agronomic Pathology Diagnostic Engine</div>
        <div class="app-hero-title">🔍 Crop Problem & Symptom Diagnosis</div>
        <div class="app-hero-sub">
            Identify potential foliar diseases, nutrient imbalances, or water stress using symptom-based forward chaining
            with preventive field guidance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### ⚡ Quick Diagnostic Demos:")
    dp1, dp2, dp3, dp4 = st.columns(4)
    with dp1:
        if st.button("🍃 Powdery Mildew Demo", key="demo_mildew"):
            st.session_state["diag_crop"] = "Tomato"
            st.session_state["diag_symptoms"] = ["White powder on leaves"]
            st.session_state["diag_moisture"] = "Adequate"
            st.session_state["diag_weather"] = "High Humidity / Overcast"
            st.session_state["auto_eval_diag"] = True
            st.rerun()
    with dp2:
        if st.button("🍂 Nitrogen Deficiency Demo", key="demo_n_def"):
            st.session_state["diag_crop"] = "Rice"
            st.session_state["diag_symptoms"] = ["Yellow leaves"]
            st.session_state["diag_moisture"] = "Adequate"
            st.session_state["diag_weather"] = "Normal / Clear"
            st.session_state["auto_eval_diag"] = True
            st.rerun()
    with dp3:
        if st.button("💧 Moisture Stress / Wilting Demo", key="demo_wilt"):
            st.session_state["diag_crop"] = "Cotton"
            st.session_state["diag_symptoms"] = ["Wilting"]
            st.session_state["diag_moisture"] = "Low"
            st.session_state["diag_weather"] = "Prolonged Drought / High Heat"
            st.session_state["auto_eval_diag"] = True
            st.rerun()
    with dp4:
        if st.button("🟤 Fungal Leaf Spot Demo", key="demo_spots"):
            st.session_state["diag_crop"] = "Wheat"
            st.session_state["diag_symptoms"] = ["Brown spots on leaves"]
            st.session_state["diag_moisture"] = "High"
            st.session_state["diag_weather"] = "Recent Heavy Unseasonal Rain"
            st.session_state["auto_eval_diag"] = True
            st.rerun()

    st.write("")

    col_diag_in, col_diag_out = st.columns([1, 1], gap="large")

    with col_diag_in:
        st.markdown("### 🩺 1. Observed Field Symptoms")

        crop_options = ["Rice", "Wheat", "Cotton", "Soybean", "Maize", "Groundnut", "Mustard", "Gram", "Sugarcane", "Tomato", "Other"]
        symptom_options = [
            "Yellow leaves",
            "Brown spots on leaves",
            "Wilting",
            "White powder on leaves",
            "Stunted growth"
        ]
        moisture_options = ["Low", "Adequate", "High"]
        weather_options = ["Normal / Clear", "High Humidity / Overcast", "Prolonged Drought / High Heat", "Recent Heavy Unseasonal Rain"]

        def_diag_crop = st.session_state.get("diag_crop", "Rice")
        def_diag_sym = st.session_state.get("diag_symptoms", ["Yellow leaves"])
        def_diag_moist = st.session_state.get("diag_moisture", "Adequate")
        def_diag_weath = st.session_state.get("diag_weather", "Normal / Clear")

        with st.form("diagnosis_form"):
            crop_type = st.selectbox(
                "🌾 Affected Crop Type",
                crop_options,
                index=crop_options.index(def_diag_crop) if def_diag_crop in crop_options else 0
            )

            symptoms = st.multiselect(
                "🌿 Observed Foliar & Plant Symptoms (Select all that apply)",
                symptom_options,
                default=def_diag_sym,
                help="Select one or more visual symptoms noticed on leaf foliage or stem"
            )

            soil_moisture = st.radio(
                "💧 Soil Moisture Level in Root Zone (5-10 cm depth)",
                moisture_options,
                index=moisture_options.index(def_diag_moist) if def_diag_moist in moisture_options else 1,
                help="Low: crumbly dry; Adequate: moist without standing water; High: waterlogged"
            )

            recent_weather = st.selectbox(
                "🌦️ Recent Microclimate / Weather Pattern",
                weather_options,
                index=weather_options.index(def_diag_weath) if def_diag_weath in weather_options else 0
            )

            submit_diag = st.form_submit_button("🔍 Diagnose Symptoms", use_container_width=True)

    with col_diag_out:
        st.markdown("### 📊 2. Diagnostic Assessment")
        
        should_diag = submit_diag or st.session_state.get("auto_eval_diag", False)
        if st.session_state.get("auto_eval_diag", False):
            st.session_state["auto_eval_diag"] = False

        if should_diag:
            if not symptoms:
                st.warning("⚠️ Please select at least one symptom to evaluate.")
            else:
                diag_results = run_crop_diagnosis(
                    crop_type=crop_type,
                    symptoms=symptoms,
                    soil_moisture=soil_moisture,
                    recent_weather=recent_weather
                )

                matched_diag_rules = diag_results["matched_rules"]

                if matched_diag_rules:
                    st.success(f"Found **{len(matched_diag_rules)} diagnostic rule match(es)** for {crop_type}:")
                    
                    for mr in matched_diag_rules:
                        deduction = mr["deduction"]
                        st.markdown(f"""
                        <div class="custom-card" style="border-left: 4px solid #ea580c;">
                            <span class="rule-badge rule-badge-diag">{mr['rule_id']} • {mr['name']}</span>
                            <h4 style="margin: 0.3rem 0; color: #9a3412;">
                                ⚠️ Possible Cause: {deduction.get('possible_cause', 'Unspecified')}
                            </h4>
                            <p style="margin: 0.3rem 0; font-size: 0.85rem; color: #64748b;">
                                <strong>Category:</strong> {deduction.get('category', 'General')}
                            </p>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.8rem; margin: 0.6rem 0;">
                                <p style="margin: 0 0 0.4rem 0; font-size: 0.88rem; color: #0f172a;">
                                    <strong>Immediate Action:</strong> {deduction.get('suggested_action', '')}
                                </p>
                                <p style="margin: 0; font-size: 0.88rem; color: #047857;">
                                    <strong>Preventive Management:</strong> {deduction.get('prevention', '')}
                                </p>
                            </div>
                            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 0.6rem 0.8rem; font-size: 0.82rem; color: #991b1b;">
                                🚨 <strong>When to Consult KVK:</strong> {deduction.get('consult_expert_when', 'If symptoms persist after 48-72 hours.')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No predefined disease rules matched this specific combination of symptoms.")

                st.markdown("""
                <div class="disclaimer-box">
                    <strong>⚠️ Important Diagnostic Notice:</strong> Visual symptoms alone cannot confirm a definitive viral,
                    fungal, or bacterial diagnosis. High temperatures, salinity, or pesticide drift can mimic disease symptoms.
                    Always verify through your local Krishi Vigyan Kendra (KVK) or plant pathology laboratory before purchasing expensive chemicals.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("👈 Select observed symptoms and root-zone moisture on the left (or click a Demo button above) to begin diagnosis.")


# ==============================================================================
# PAGE 4: SOIL & FERTILIZER ADVICE
# ==============================================================================
elif page == "🧪 Soil & Fertilizer Advice":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #134e4a 0%, #0f766e 50%, #0d9488 100%);">
        <div class="hero-badge-pill">🧪 Soil Chemistry & Amendment Engine</div>
        <div class="app-hero-title">🧪 Soil Health & Fertilizer Advisory</div>
        <div class="app-hero-sub">
            Scientific soil pH interpretation, soil-type texture dynamics, and balanced fertilizer guidance
            advocating official Soil Health Card guidelines.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_soil_in, col_soil_out = st.columns([1, 1], gap="large")

    with col_soil_in:
        st.markdown("### 🧪 1. Soil Test Parameters")
        with st.form("soil_form"):
            soil_type = st.selectbox(
                "🌱 Soil Type / Texture",
                ["Black", "Alluvial", "Red", "Sandy"]
            )

            soil_ph = st.slider(
                "🧪 Tested Soil pH Value",
                min_value=3.0,
                max_value=10.0,
                value=7.0,
                step=0.1
            )

            organic_matter = st.select_slider(
                "🍂 Soil Organic Carbon Status (from Soil Health Card)",
                options=["Low (< 0.5%)", "Medium (0.5% - 0.75%)", "High (> 0.75%)"],
                value="Medium (0.5% - 0.75%)"
            )

            submit_soil = st.form_submit_button("🧪 Generate Soil Health Advice", use_container_width=True)

        render_ph_spectrum(soil_ph)

    with col_soil_out:
        st.markdown("### 📜 2. Soil Management Report")
        if submit_soil:
            soil_results = run_soil_management_advice(
                soil_type=soil_type,
                soil_ph=soil_ph,
                organic_matter_status=organic_matter
            )

            matched_soil_rules = soil_results["matched_rules"]
            soil_profile = SOIL_PROFILES.get(soil_type, {})

            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #0d9488;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; color: #0f766e;">🌱 Profile: {soil_profile.get('name', soil_type)}</h4>
                    <span class="crop-badge-tag">{soil_type} Soil</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 0.6rem 0;">
                    <div class="mini-stat-box">
                        <div class="mini-stat-label">Texture</div>
                        <div class="mini-stat-val" style="font-size: 0.85rem;">{soil_profile.get('texture', '')}</div>
                    </div>
                    <div class="mini-stat-box">
                        <div class="mini-stat-label">Water Retention</div>
                        <div class="mini-stat-val" style="font-size: 0.85rem;">{soil_profile.get('water_retention', '')}</div>
                    </div>
                    <div class="mini-stat-box">
                        <div class="mini-stat-label">Inherent Fertility</div>
                        <div class="mini-stat-val" style="font-size: 0.85rem;">{soil_profile.get('inherent_fertility', '')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for mr in matched_soil_rules:
                deduction = mr["deduction"]
                st.markdown(f"""
                <div class="custom-card">
                    <span class="rule-badge rule-badge-soil">{mr['rule_id']} • {mr['name']}</span>
                    <h5 style="margin: 0.3rem 0; color: #0f766e; font-weight: 700;">Status: {deduction.get('soil_status', '')}</h5>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.8rem; margin: 0.6rem 0;">
                        <p style="margin: 0 0 0.4rem 0; font-size: 0.88rem; color: #1e293b;">
                            <strong>Amendment Advice:</strong> {deduction.get('recommendation', '')}
                        </p>
                        <p style="margin: 0 0 0.4rem 0; font-size: 0.88rem; color: #0f172a;">
                            <strong>Fertilizer Strategy:</strong> {deduction.get('fertilizer_advice', '')}
                        </p>
                        <p style="margin: 0; font-size: 0.88rem; color: #047857;">
                            <strong>Organic Carbon Enrichment:</strong> {deduction.get('organic_practices', '')}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="disclaimer-box">
                <strong>🔬 Scientific Fertilizer Protocol:</strong> Never apply blanket fertilizer doses without an official
                Soil Health Card laboratory test. Fertilizer doses depend on target crop yield, previous crop residue,
                and available soil Nitrogen, Phosphorus, Potassium, and micronutrients.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Enter your soil details on the left and click **Generate Soil Health Advice**.")


# ==============================================================================
# PAGE 5: AI RULE BASE & TRACE INSPECTOR (EXPLAINABLE AI)
# ==============================================================================
elif page == "🧠 AI Rule Base & Trace Inspector":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);">
        <div class="hero-badge-pill">🧠 Knowledge Representation & Production Rules</div>
        <div class="app-hero-title">🧠 AI Rule Base & Forward-Chaining Inspector</div>
        <div class="app-hero-sub">
            Complete transparency into knowledge representation, production rules, and logical inference trace.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_rules, tab_matrix, tab_viva = st.tabs([
        "📚 Rule Base Inspector (26 Rules)",
        "🌾 Knowledge Base Matrix (10 Crops)",
        "🎓 Viva Voce Reference Guide"
    ])

    with tab_rules:
        rules = get_all_rules()
        st.markdown(f"#### 📚 Active Production Rules ({len(rules)} Total)")

        col_fil, col_search = st.columns([1, 2])
        with col_fil:
            filter_category = st.selectbox(
                "Filter Rules by Sub-System Category",
                ["All Categories", "Crop Recommendation", "Crop Diagnosis", "Soil Management"]
            )
        with col_search:
            search_query = st.text_input("🔍 Search Rule by Keyword or ID", placeholder="e.g. Wheat, pH, Mildew, R-CROP-01")

        filtered_rules = [
            r for r in rules
            if (filter_category == "All Categories" or r.category == filter_category)
            and (search_query.lower() in r.name.lower() or search_query.lower() in r.rule_id.lower() or search_query.lower() in r.explanation.lower())
        ]

        st.caption(f"Showing **{len(filtered_rules)}** rules matching filters:")

        for r in filtered_rules:
            with st.expander(f"📌 **{r.rule_id}**: {r.name} [{r.category}]"):
                st.markdown(f"**Antecedent Condition (IF):**")
                st.code(r.antecedents_description, language="python")
                st.markdown(f"**Agronomic Justification (Scientific Explanation):**")
                st.info(r.explanation)

    with tab_matrix:
        st.markdown("#### 🌾 Knowledge Base Crop Agronomic Matrix")
        st.write("A structured overview of all 10 candidate crop profiles encoded in `knowledge_base.py`:")

        crop_matrix_data = []
        for name, data in CROPS_DATABASE.items():
            crop_matrix_data.append({
                "Crop": name,
                "Category": data.get("category"),
                "Seasons": ", ".join(data.get("suitable_seasons", [])),
                "Soils": ", ".join(data.get("suitable_soils", [])),
                "Optimal pH": data.get("optimal_ph"),
                "Optimal Temp": data.get("optimal_temp"),
                "Rainfall": ", ".join(data.get("rainfall_requirement", [])),
                "Duration": data.get("duration"),
                "NPK Ratio": data.get("npk_general_ratio")
            })

        st.dataframe(crop_matrix_data, use_container_width=True)

    with tab_viva:
        st.markdown("#### 🎓 Engineering Viva Voce Concept Reference")
        st.markdown("""
        | AI Concept | Implementation in this Project |
        | :--- | :--- |
        | **Knowledge Representation** | Explicit IF–THEN declarative production rules in `rules.py` and structured domain profiles in `knowledge_base.py`. |
        | **Working Memory** | Dynamic dictionary storing user input facts (`season`, `soil_type`, `symptoms`, etc.) during runtime. |
        | **Inference Engine** | `InferenceEngine.run_forward_chaining()` iterating over candidate rules and firing satisfied antecedents. |
        | **Forward Chaining** | Data-driven reasoning: Starting from user facts -> matching rule antecedents -> deducing recommendations. |
        | **Explainable AI (XAI)** | Every fired rule logs its unique `rule_id`, evaluated conditions, and human-readable agronomic justification. |
        | **Conflict Resolution** | Deduplication and priority handling ensuring candidate crop aggregation without duplicates. |
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 1.5rem 0;'>"
    "🌱 <strong>AgriExpert AI</strong> • Rule-Based Expert System for Agriculture Using Python & Streamlit • 100% Explainable AI"
    "</div>",
    unsafe_allow_html=True
)
