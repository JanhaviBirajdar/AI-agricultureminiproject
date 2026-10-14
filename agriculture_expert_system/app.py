"""
app.py
======
Interactive Streamlit Web Application for the
Rule-Based Expert System for Agriculture Using Python.

Features:
- Home: Architecture, AI concepts, working memory, inference engine overview
- Crop Recommendation: Multi-criteria crop evaluation with transparent rule matching
- Problem Diagnosis: Crop symptom diagnostics with moisture context and preventive guidance
- Soil & Fertilizer Advice: Soil pH classification, soil-texture considerations, and fertilizer advice
- AI Rule Visualizer: Deep-dive inspection of the rule base and forward chaining trace
"""

import os
import sys

# Ensure local modules (rules, knowledge_base) are resolvable regardless of working directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import streamlit as st
from typing import List, Dict, Any
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
# PAGE CONFIGURATION & CUSTOM THEME
# ==============================================================================
st.set_page_config(
    page_title="AgriExpert | AI Expert System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich agricultural aesthetics, modern cards, and badges
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Force Pristine White Theme regardless of system preference */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }

    /* Text & Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700;
    }

    p, span, label {
        color: #1e293b;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* App Header Banner */
    .app-hero-banner {
        background: linear-gradient(135deg, #134e4a 0%, #065f46 50%, #047857 100%);
        color: white !important;
        padding: 2.2rem 2.4rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(6, 95, 70, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .app-hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }

    .app-hero-sub {
        font-size: 1.05rem;
        font-weight: 400;
        color: #d1fae5 !important;
        margin-top: 0.5rem;
    }

    /* Feature Card in White Theme */
    .custom-card {
        background-color: #ffffff !important;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1 !important;
    }

    .custom-card h4, .custom-card h5 {
        color: #0f172a !important;
        font-weight: 700;
    }

    /* Streamlit Form Widgets in White Theme */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }

    div[data-baseweb="select"] svg {
        fill: #475569 !important;
    }

    .stNumberInput input, .stTextInput input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }

    /* Streamlit Expanders */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem;
    }

    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-weight: 600 !important;
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
        background: #fffbeb !important;
        color: #b45309 !important;
        border-color: #fde68a !important;
    }

    /* Status Pill */
    .status-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        border-radius: 9999px;
        letter-spacing: 0.5px;
    }

    .status-success {
        background: #dcfce7 !important;
        color: #15803d !important;
    }

    .status-warning {
        background: #fef3c7 !important;
        color: #b45309 !important;
    }

    .status-danger {
        background: #fee2e2 !important;
        color: #b91c1c !important;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        background: #fffbeb !important;
        border-left: 4px solid #f59e0b !important;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #92400e !important;
        margin-top: 1.5rem;
        border-top: 1px solid #fef3c7;
        border-right: 1px solid #fef3c7;
        border-bottom: 1px solid #fef3c7;
    }

    .disclaimer-box strong {
        color: #78350f !important;
    }

    /* AI Explanatory Box */
    .ai-explainer {
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    /* Sidebar Branding */
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
    }

    .sidebar-brand h2 {
        font-weight: 800;
        color: #065f46 !important;
        margin: 0.2rem 0 0 0;
        font-size: 1.35rem;
    }

    .sidebar-brand span {
        font-size: 0.8rem;
        color: #64748b !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# SIDEBAR NAVIGATION & CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 2.8rem; line-height: 1;">🌱</div>
        <h2>AgriExpert AI</h2>
        <span>Rule-Based Expert System (v1.0)</span>
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
    st.markdown("### ⚙️ Quick Actions")
    if st.button("🔄 Reset All Form Inputs", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.82rem; color: #64748b; line-height: 1.4;">
        <strong>Project Type:</strong> AI Mini-Project<br>
        <strong>Inference Engine:</strong> Forward Chaining<br>
        <strong>Knowledge Base:</strong> Agronomic Heuristics<br>
        <strong>Rule Count:</strong> 26 Active Rules
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: HOME / OVERVIEW
# ==============================================================================
if page == "🏠 Home / Overview":
    st.markdown("""
    <div class="app-hero-banner">
        <h1 class="app-hero-title">Rule-Based Expert System for Agriculture</h1>
        <p class="app-hero-sub">
            An explainable, deterministic Artificial Intelligence system providing scientific
            agronomic advisory through Forward-Chaining IF–THEN inference.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown("### 🎯 What is an Expert System?")
        st.write(
            "An **Expert System** is one of the foundational paradigms of Artificial Intelligence. "
            "Unlike 'black-box' Machine Learning algorithms that rely on statistical patterns, "
            "an expert system encapsulates human domain knowledge into formal logical rules (**IF–THEN**) "
            "and reasons over user facts using an **Inference Engine** to reach conclusions with 100% explainability."
        )

        st.markdown("### 🧩 Core Components of Our AI Architecture")
        st.markdown("""
        1. **Knowledge Base (KB):** Declarative facts representing crop requirements, soil physical and chemical profiles, plant disease pathology, and soil pH thresholds.
        2. **Rule Base:** A collection of 26 curated **IF–THEN** production rules created in collaboration with agronomic literature.
        3. **Working Memory:** The active scratchpad storing facts input by the user (e.g., current season, soil type, observed leaf symptoms) and intermediate deductions.
        4. **Inference Engine (Forward Chaining):** Evaluates facts in Working Memory against rule antecedents (IF condition), fires satisfied rules, and deduces conclusions (THEN actions).
        5. **Explanation Facility:** Provides complete transparent audits showing **which** rules fired, **why** they fired, and the agronomic justification behind each advisory.
        """)

    with col2:
        st.markdown("### 🏛️ Architecture Flow")
        st.markdown("""
        ```mermaid
        graph TD
            A[User Inputs] --> B[Working Memory]
            C[(Knowledge Base)] --> D[Rule Base]
            B --> E[Inference Engine]
            D --> E
            E -->|Forward Chaining| F[Matched Rules]
            F --> G[Explainable Recommendations]
            F --> H[Audit Trace & Justifications]
        ```
        """)

        st.info(
            "💡 **Student Viva Tip:** In an engineering viva, emphasize that this project uses **Forward Chaining** (data-driven reasoning): "
            "we start from initial known facts (soil, weather, symptoms) and move forward to infer conclusions (suitable crops or diagnosed conditions)."
        )

    st.markdown("---")
    st.markdown("### 🚀 Available Expert Modules")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="custom-card">
            <h4>🌾 Crop Recommendation</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Evaluates soil type, pH, season, temperature, rainfall, and irrigation to recommend optimal candidate crops with matched rules.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        c2.markdown("""
        <div class="custom-card">
            <h4>🔍 Problem Diagnosis</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Analyzes observed foliar symptoms, soil moisture levels, and weather to infer potential fungal diseases, nutrient deficits, or water stress.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        c3.markdown("""
        <div class="custom-card">
            <h4>🧪 Soil & Fertilizer Advice</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Assesses soil pH classification and soil texture to deliver chemical amendment advisories (liming/gypsum) and nutrient balancing guidelines.
            </p>
        </div>
        """, unsafe_allow_html=True)

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
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);">
        <h1 class="app-hero-title">🌾 Crop Recommendation Expert System</h1>
        <p class="app-hero-sub">
            Infer suitable crops based on soil characteristics, seasonal dynamics, rainfall, and irrigation availability.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📥 1. Enter Agricultural Parameters")
        with st.form("crop_form"):
            season = st.selectbox(
                "📅 Current Cropping Season",
                ["Kharif", "Rabi", "Summer"],
                help="Kharif (Monsoon / Autumn), Rabi (Winter / Spring), Summer (Zaid / Hot dry season)"
            )

            soil_type = st.selectbox(
                "🌱 Soil Texture / Type",
                ["Black", "Alluvial", "Red", "Sandy"],
                help="Physical texture and moisture characteristics of your farmland"
            )

            col_ph, col_temp = st.columns(2)
            with col_ph:
                soil_ph = st.slider(
                    "🧪 Soil pH Level",
                    min_value=3.0,
                    max_value=10.0,
                    value=6.8,
                    step=0.1,
                    help="Soil reaction: 3-5.5 strongly acidic, 6.5-7.5 neutral/ideal, 8.5-10 alkaline"
                )
            with col_temp:
                temperature = st.number_input(
                    "🌡️ Avg Temperature (°C)",
                    min_value=5.0,
                    max_value=50.0,
                    value=26.0,
                    step=1.0,
                    help="Average ambient temperature during the crop vegetative phase"
                )

            col_rain, col_irrig = st.columns(2)
            with col_rain:
                rainfall = st.selectbox(
                    "🌧️ Expected Rainfall",
                    ["Low", "Medium", "High"],
                    index=1,
                    help="Low (< 500 mm), Medium (500 - 1000 mm), High (> 1000 mm)"
                )
            with col_irrig:
                irrigation = st.selectbox(
                    "💧 Assured Irrigation Available?",
                    ["Yes", "No"],
                    index=0,
                    help="Canal, borewell, tube-well, or drip irrigation availability"
                )

            submit_crop = st.form_submit_button("🌿 Evaluate Crop Suitability", use_container_width=True)

    with col_result:
        st.markdown("### 📋 2. AI Inference Results")
        if submit_crop:
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
                st.success(f"🎉 **{len(recommended_crops)} Candidate Crop(s) Recommended!**")
                
                # Display badges
                crop_badges_html = " ".join([
                    f"<span class='rule-badge' style='font-size: 1rem; padding: 0.35rem 0.8rem; margin: 0.2rem;'>🌾 {c}</span>"
                    for c in recommended_crops
                ])
                st.markdown(crop_badges_html, unsafe_allow_html=True)
                st.write("")

                # Detail cards for each recommended crop
                for crop_name in recommended_crops:
                    profile = CROPS_DATABASE.get(crop_name, {})
                    with st.expander(f"📖 Crop Dossier: **{profile.get('name', crop_name)}**", expanded=True):
                        c_a, c_b = st.columns([1, 1])
                        with c_a:
                            st.write(f"**Category:** {profile.get('category', 'N/A')}")
                            st.write(f"**Optimal pH:** {profile.get('optimal_ph', 'N/A')}")
                            st.write(f"**Duration:** {profile.get('duration', 'N/A')}")
                        with c_b:
                            st.write(f"**Optimal Temp:** {profile.get('optimal_temp', 'N/A')}")
                            st.write(f"**General N-P-K:** `{profile.get('npk_general_ratio', 'N/A')}`")
                            st.write(f"**Irrigation Need:** {profile.get('irrigation_dependency', 'N/A')}")
                        
                        st.write(f"**Agronomic Summary:** {profile.get('description', '')}")
                        st.info(f"💡 **Management Tip:** {profile.get('management_tip', '')}")
            else:
                st.warning(
                    "⚠️ **No standard crops matched all your strict environmental constraints.**\n\n"
                    "Possible reasons: Temperature may be outside typical cultivation ranges, or low rainfall "
                    "without irrigation limits crop establishment. Review the unmatched rules below."
                )

            # Explainable AI Card: Matched Rules
            st.markdown("#### 🧠 Matched Rules (Explainable AI Trace)")
            if matched_rules:
                for mr in matched_rules:
                    st.markdown(f"""
                    <div class="custom-card" style="border-left: 4px solid #10b981;">
                        <span class="rule-badge">{mr['rule_id']} • {mr['name']}</span>
                        <p style="margin: 0.3rem 0; font-family: monospace; font-size: 0.85rem; color: #334155;">
                            <strong>Condition:</strong> {mr['condition']}
                        </p>
                        <p style="margin: 0.3rem 0; font-size: 0.9rem; color: #047857;">
                            <strong>Deduction:</strong> {mr['deduction'].get('justification', '')}
                        </p>
                        <p style="margin: 0; font-size: 0.85rem; color: #64748b;">
                            <em>Agronomic Justification:</em> {mr['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No rule conditions were satisfied.")

            # Working Memory snapshot
            with st.expander("🔍 View Working Memory Snapshot (Facts in Fact Base)"):
                st.json(working_memory)

        else:
            st.info("👈 Select your agricultural parameters on the left and click **Evaluate Crop Suitability** to start inference.")


# ==============================================================================
# PAGE 3: PROBLEM & DISEASE DIAGNOSIS
# ==============================================================================
elif page == "🔍 Problem & Disease Diagnosis":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #7c2d12 0%, #9a3412 50%, #ea580c 100%);">
        <h1 class="app-hero-title">🔍 Crop Problem & Symptom Diagnosis</h1>
        <p class="app-hero-sub">
            Identify potential foliar diseases, nutrient imbalances, or water stress using symptom-based forward chaining.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_diag_in, col_diag_out = st.columns([1, 1], gap="large")

    with col_diag_in:
        st.markdown("### 🩺 1. Observed Field Symptoms")
        with st.form("diagnosis_form"):
            crop_type = st.selectbox(
                "🌾 Affected Crop Type",
                ["Rice", "Wheat", "Cotton", "Soybean", "Maize", "Groundnut", "Mustard", "Gram", "Sugarcane", "Tomato", "Other"]
            )

            symptoms = st.multiselect(
                "🌿 Observed Foliar & Plant Symptoms (Select all that apply)",
                [
                    "Yellow leaves",
                    "Brown spots on leaves",
                    "Wilting",
                    "White powder on leaves",
                    "Stunted growth"
                ],
                default=["Yellow leaves"],
                help="Select one or more visual symptoms noticed in your field"
            )

            soil_moisture = st.radio(
                "💧 Soil Moisture Level in Root Zone (5-10 cm deep)",
                ["Low", "Adequate", "High"],
                index=1,
                help="Low: soil is crumbly dry; Adequate: moist but not dripping; High: saturated/waterlogged"
            )

            recent_weather = st.selectbox(
                "🌦️ Recent Microclimate / Weather Pattern",
                ["Normal / Clear", "High Humidity / Overcast", "Prolonged Drought / High Heat", "Recent Heavy Unseasonal Rain"]
            )

            submit_diag = st.form_submit_button("🔍 Diagnose Symptoms", use_container_width=True)

    with col_diag_out:
        st.markdown("### 📊 2. Diagnostic Assessment")
        if submit_diag:
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
                                Possible Cause: {deduction.get('possible_cause', 'Unspecified')}
                            </h4>
                            <p style="margin: 0.4rem 0; font-size: 0.9rem;">
                                <strong>Category:</strong> {deduction.get('category', 'General')}
                            </p>
                            <p style="margin: 0.4rem 0; font-size: 0.9rem; color: #1e293b;">
                                <strong>Immediate Suggested Action:</strong> {deduction.get('suggested_action', '')}
                            </p>
                            <p style="margin: 0.4rem 0; font-size: 0.9rem; color: #047857;">
                                <strong>Preventive Management:</strong> {deduction.get('prevention', '')}
                            </p>
                            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 0.6rem; margin-top: 0.6rem; font-size: 0.85rem; color: #991b1b;">
                                <strong>🚨 When to Consult an Agronomist / KVK:</strong> {deduction.get('consult_expert_when', 'If symptoms persist.')}
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
            st.info("👈 Select observed symptoms and root-zone moisture on the left to begin diagnosis.")


# ==============================================================================
# PAGE 4: SOIL & FERTILIZER ADVICE
# ==============================================================================
elif page == "🧪 Soil & Fertilizer Advice":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #115e59 0%, #0f766e 50%, #14b8a6 100%);">
        <h1 class="app-hero-title">🧪 Soil Health & Fertilizer Advisory</h1>
        <p class="app-hero-sub">
            Scientific soil pH interpretation, soil-type texture dynamics, and balanced fertilizer guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_soil_in, col_soil_out = st.columns([1, 1], gap="large")

    with col_soil_in:
        st.markdown("### 🧪 1. Soil Parameters")
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
                "🍂 Soil Organic Carbon Status (if known from soil health card)",
                options=["Low (< 0.5%)", "Medium (0.5% - 0.75%)", "High (> 0.75%)"],
                value="Medium (0.5% - 0.75%)"
            )

            submit_soil = st.form_submit_button("🧪 Generate Soil Advice", use_container_width=True)

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

            # Profile overview
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #14b8a6;">
                <h4>Soil Profile: {soil_profile.get('name', soil_type)}</h4>
                <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Texture:</strong> {soil_profile.get('texture', '')}</p>
                <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Water Retention:</strong> {soil_profile.get('water_retention', '')}</p>
                <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Native Fertility:</strong> {soil_profile.get('inherent_fertility', '')}</p>
            </div>
            """, unsafe_allow_html=True)

            # Display matched rules
            for mr in matched_soil_rules:
                deduction = mr["deduction"]
                st.markdown(f"""
                <div class="custom-card">
                    <span class="rule-badge rule-badge-soil">{mr['rule_id']} • {mr['name']}</span>
                    <h5 style="margin: 0.3rem 0; color: #0f766e;">Status: {deduction.get('soil_status', '')}</h5>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem;">
                        <strong>Amendment Advice:</strong> {deduction.get('recommendation', '')}
                    </p>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem; color: #1e293b;">
                        <strong>Fertilizer Strategy:</strong> {deduction.get('fertilizer_advice', '')}
                    </p>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem; color: #047857;">
                        <strong>Organic Practices:</strong> {deduction.get('organic_practices', '')}
                    </p>
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
            st.info("👈 Enter your soil details on the left and click **Generate Soil Advice**.")


# ==============================================================================
# PAGE 5: AI RULE BASE & TRACE INSPECTOR (EXPLAINABLE AI)
# ==============================================================================
elif page == "🧠 AI Rule Base & Trace Inspector":
    st.markdown("""
    <div class="app-hero-banner" style="background: linear-gradient(135deg, #312e81 0%, #3730a3 50%, #4338ca 100%);">
        <h1 class="app-hero-title">🧠 AI Rule Base & Forward-Chaining Inspector</h1>
        <p class="app-hero-sub">
            Complete transparency into knowledge representation, production rules, and logical inference trace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    rules = get_all_rules()
    st.markdown(f"### 📚 Knowledge Base Rules ({len(rules)} Total Rules Loaded)")

    filter_category = st.selectbox(
        "Filter Rules by Sub-System Category",
        ["All Categories", "Crop Recommendation", "Crop Diagnosis", "Soil Management"]
    )

    filtered_rules = [
        r for r in rules
        if filter_category == "All Categories" or r.category == filter_category
    ]

    st.write(f"Showing **{len(filtered_rules)}** rules in category **{filter_category}**:")

    for r in filtered_rules:
        with st.expander(f"📌 **{r.rule_id}**: {r.name} [{r.category}]"):
            st.markdown(f"**Antecedents (IF Condition):**")
            st.code(r.antecedents_description, language="python")
            st.markdown(f"**Agronomic Justification (Explanation):**")
            st.info(r.explanation)

    st.markdown("---")
    st.markdown("### 🎓 Engineering Viva Concept Reference")
    st.markdown("""
    | AI Concept | Implementation in this Project |
    | :--- | :--- |
    | **Knowledge Representation** | Explicit IF–THEN declarative production rules in `rules.py` and structured domain profiles in `knowledge_base.py`. |
    | **Working Memory** | Dynamic dictionary storing user input facts (`season`, `soil_type`, `symptoms`, etc.) during runtime. |
    | **Inference Engine** | `InferenceEngine.run_forward_chaining()` iterating over candidate rules and firing satisfied antecedents. |
    | **Forward Chaining** | Data-driven reasoning: Starting from user facts -> matching rule antecedents -> deducing recommendations. |
    | **Explainable AI (XAI)** | Every fired rule logs its unique `rule_id`, evaluated conditions, and human-readable agronomic justification. |
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem 0;'>"
    "🌾 Artificial Intelligence Mini Project: Rule-Based Expert System for Agriculture Using Python • Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
