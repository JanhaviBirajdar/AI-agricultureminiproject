# 🌾 AgriExpert AI: Rule-Based Expert System for Agriculture

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/AI_Paradigm-Expert_System-059669?style=for-the-badge&logo=semanticweb&logoColor=white" alt="AI Paradigm" />
  <img src="https://img.shields.io/badge/Inference-Forward_Chaining-0284C7?style=for-the-badge" alt="Forward Chaining" />
  <img src="https://img.shields.io/badge/Explainability-100%25_Auditable-10B981?style=for-the-badge" alt="Explainability" />
  <img src="https://img.shields.io/badge/Unit_Tests-17_Passing-brightgreen?style=for-the-badge" alt="Unit Tests" />
</p>

<p align="center">
  <strong>An explainable, deterministic Artificial Intelligence platform replicating senior agronomist heuristics through formal production rules and data-driven forward chaining.</strong>
</p>

---

## 📌 Executive Summary

Modern agriculture faces severe productivity challenges due to unpredictable climate shifts, delayed expert advisory, misdiagnosed plant diseases, and unscientific chemical fertilizer use.

Unlike statistical "black-box" machine learning models that require thousands of training records and can hallucinate erroneous advice, **AgriExpert AI** encapsulates human agronomic expertise into formal **declarative IF–THEN production rules**. It executes a **Forward-Chaining Inference Engine** to deliver scientific, transparent, and auditable advisory with zero hallucinations.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AGRIEXPERT AI AT A GLANCE                              │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────────────┤
│   🧠 26 Rules       │   🌾 10 Crops       │   ⚡ < 1 ms Latency  │   🎯 100% Explainable│
│ Active Production   │ Detailed Agronomic  │ Ultra-Fast Forward  │ Every Deduction Ties │
│ Knowledge Base      │ Dossiers & NPK      │ Chaining Inference  │ to a Fired Rule ID   │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────────────┘
```

---

## 🏛️ AI Architecture Pipeline

The system is architected around classic Knowledge Engineering paradigms:

```text
  +-------------------------------------------------------------------------+
  |                        1. USER INPUT DATA                               |
  |  (Cropping Season, Soil Type, pH, Temperature, Rainfall, Symptoms)      |
  +------------------------------------+------------------------------------+
                                       |
                                       v
  +-------------------------------------------------------------------------+
  |                       2. WORKING MEMORY                                 |
  |  Active runtime fact-store (Dynamic Python Dictionary)                  |
  +------------------------------------+------------------------------------+
                                       |
                                       v
  +-------------------------------------------------------------------------+
  |                   3. FORWARD-CHAINING INFERENCE ENGINE                  |
  |  Systematically iterates across candidate production rules              |
  |  Evaluates IF conditions (antecedents) against active facts             |
  +------------------------------------+------------------------------------+
                                       |
               +-----------------------+-----------------------+
               |                                               |
               v                                               v
  +---------------------------+                   +-------------------------+
  |    4. FIRED RULES AUDIT   |                   |  5. DOMAIN KNOWLEDGE    |
  |  Collects matched rule IDs|                   |  Crops Database, Soil   |
  |  and justifications       |                   |  Profiles, Pathogens    |
  +------------+--------------+                   +------------+------------+
               |                                               |
               +-----------------------+-----------------------+
                                       |
                                       v
  +-------------------------------------------------------------------------+
  |                 6. EXPLAINABLE ADVISORY & DOSSIER                       |
  |  • Candidate Recommended Crops (with duration, N-P-K, & tips)           |
  |  • Suspected Disease Diagnoses & Immediate Cultural Actions             |
  |  • Soil Chemical Amendments (Lime/Gypsum) & pH Spectrum Meter           |
  |  • Downloadable Official Farmer Advisory Report (.txt)                  |
  +-------------------------------------------------------------------------+
```

---

## 🌟 Key Features & Sub-Systems

### 1. 🌾 Multi-Criteria Crop Recommendation
- Evaluates soil type (*Black, Alluvial, Red, Sandy*), tested soil pH (3.0 – 10.0), season (*Kharif, Rabi, Summer*), ambient temperature, rainfall ranges, and irrigation infrastructure.
- Features an **Interactive Soil pH Visual Color Gauge** that tracks soil reaction from Strongly Acidic (pH 3.0) to Neutral (pH 7.0) to Strongly Alkaline (pH 10.0).
- Delivers comprehensive **Crop Dossiers** featuring botanical classifications, optimal temperature bands, maturity duration, and N-P-K fertilizer formulations.
- Generates a **1-Click Downloadable Official Farmer Advisory Report (`.txt`)**.

### 2. 🔍 Foliar Problem & Disease Diagnosis
- Evaluates visual symptoms (*Yellow leaves, Wilting, Brown spots, White powder, Stunted growth*) in combination with root-zone soil moisture (*Low, Adequate, High*) and recent weather patterns.
- Distinguishes nutrient deficiencies (Nitrogen, Iron) from fungal infestations (*Powdery Mildew, Leaf Spots/Blight*) and water stress.
- Provides immediate field action checklists, preventive cultural practices, and explicit guidance on when to consult local **Krishi Vigyan Kendras (KVK)**.

### 3. 🧪 Soil Chemistry & Fertilizer Advisory
- Dynamically classifies soil into 5 agronomic pH regimes:
  - Strongly Acidic ($pH < 5.5$) $\rightarrow$ Prescribes Agricultural Lime ($CaCO_3$)
  - Moderately Acidic ($5.5 \le pH < 6.5$) $\rightarrow$ Suitable for acid-tolerant crops
  - Neutral / Ideal ($6.5 \le pH \le 7.5$) $\rightarrow$ Maximum nutrient bioavailability
  - Moderately Alkaline ($7.5 < pH \le 8.5$) $\rightarrow$ Micronutrient monitoring
  - Strongly Alkaline / Sodic ($pH > 8.5$) $\rightarrow$ Prescribes Gypsum ($CaSO_4 \cdot 2H_2O$)
- Explains soil physical texture dynamics (water retention, leaching tendencies, inherent fertility).

### 4. 🧠 Transparent Rule Base & Knowledge Matrix Inspector
- Searchable directory of all **26 active production rules** categorized by sub-system.
- Displays formal Python antecedent logic and published agronomic justification for every rule.
- Interactive **Knowledge Base Matrix** comparing all 10 candidate crops in a structured data table.
- Built-in **Viva Voce Master Guide** covering core AI concepts for viva preparation.

---

## ⚡ Quick 1-Click Demo Scenarios (Viva-Ready)

| Scenario | Geography / Test Condition | Expected Fired Rules | Recommended Advisory |
| :--- | :--- | :--- | :--- |
| **🌾 Punjab Rabi Wheat** | Rabi • Alluvial soil • pH 6.8 • 18°C • Med Rain • Irrigated | `R-CROP-02`, `R-CROP-06` | **Wheat** & **Mustard** candidate crops; balanced NPK advisory. |
| **☁️ Vidarbha Cotton** | Kharif • Black soil • pH 7.2 • 28°C • Med Rain • Irrigated | `R-CROP-01`, `R-CROP-07` | **Soybean** & **Cotton**; drainage and boll protection tip. |
| **🌧️ Assam Lowland Rice** | Kharif • Alluvial soil • pH 6.2 • 29°C • High Rain • Irrigated | `R-CROP-03` | **Rice (Paddy)**; standing water tillering management. |
| **🏜️ Rajasthan Millets** | Kharif • Sandy soil • pH 7.6 • 32°C • Low Rain • Rainfed | `R-CROP-04`, `R-CROP-10` | **Millets (Bajra)**; drought survival warning. |
| **🍃 Powdery Mildew Demo** | Tomato • White powder • Adequate moisture • Humid overcast | `R-DIAG-04` | Suspected **Powdery Mildew**; wettable sulphur spray & pruning. |
| **🍂 Nitrogen Deficiency Demo**| Rice • Yellow leaves • Adequate moisture • Clear weather | `R-DIAG-01` | Suspected **Nitrogen / Iron Deficiency**; soil health testing. |

---

## 🚀 Installation & Local Execution

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your system.

### 2. Setup Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Automated Unit Tests
```bash
python -m unittest test_rules.py
```
*Expected Result:* `Ran 17 tests in 0.001s ... OK`

### 5. Launch the Web Application
```bash
streamlit run app.py
```

Open your browser at:
👉 **`http://localhost:8501`**

---

## 🎓 Engineering Viva Voce Master Cheat Sheet

| Question | Clear Academic Answer |
| :--- | :--- |
| **Why not use Deep Learning?** | Deep learning is a statistical black-box. In agriculture, an erroneous pesticide or crop recommendation can ruin a farmer's livelihood. Rule-based expert systems provide **100% auditable, deterministic reasoning** where every deduction links to an agronomic rule. |
| **What is Forward Chaining?** | Forward chaining is a data-driven reasoning strategy: it starts from initial known facts in Working Memory, tests rule antecedents (`IF`), fires matching rules, and infers conclusions (`THEN`). |
| **What is Working Memory?** | Working Memory is the dynamic runtime scratchpad where initial user inputs (soil, pH, symptoms) and intermediate inferred facts are stored during an active inference session. |
| **How is conflict resolution handled?** | In this system, rules are partitioned by sub-system category (Crop, Diagnosis, Soil), and candidate crop conclusions are merged and deduplicated while preserving individual justification traces. |

---

## ⚖️ Academic Disclaimer
*This expert system is developed as an educational demonstration of Knowledge Representation and Reasoning (KRR) in Artificial Intelligence. In commercial farming, localized microclimates, seed varieties, and official laboratory soil tests from Krishi Vigyan Kendras (KVK) must always take precedence.*

---

<p align="center">
  Developed with ❤️ for AI Mini-Projects • 100% Explainable Artificial Intelligence
</p>
