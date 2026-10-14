# 🌾 Rule-Based Expert System for Agriculture Using Python

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![AI-Paradigm](https://img.shields.io/badge/AI%20Paradigm-Rule--Based%20Expert%20System-green.svg)]()
[![Inference Engine](https://img.shields.io/badge/Inference-Forward%20Chaining-orange.svg)]()
[![Explainability](https://img.shields.io/badge/Explainability-100%25%20Transparent-brightgreen.svg)]()

An interactive, explainable, and beginner-friendly Artificial Intelligence mini project developed in Python and Streamlit. The system implements a traditional **Rule-Based Expert System** using formal **IF–THEN production rules** and a **Forward-Chaining Inference Engine** to deliver scientific agricultural advisory without relying on black-box machine learning models or paid cloud APIs.

---

## 📌 Project Overview

Agriculture in developing nations faces severe productivity bottlenecks due to untimely crop advisory, misdiagnosed plant diseases, and unbalanced chemical fertilizer usage. This project replicates the decision-making heuristics of an agricultural extension officer (agronomist) through an explainable AI architecture:

1. **Crop Recommendation System:** Recommends optimal candidate crops (Rice, Wheat, Cotton, Soybean, Maize, Millets, Groundnut, Mustard, Gram, Sugarcane) based on soil texture, soil pH, season, temperature, rainfall, and irrigation availability.
2. **Crop Problem & Disease Diagnosis:** Infers potential foliar diseases (Powdery Mildew, Leaf Spots/Blight), water stress, and nutrient deficiencies (Nitrogen, Iron, Phosphorus) based on observed symptoms and soil moisture context.
3. **Soil Health & Fertilizer Management:** Interprets soil pH and texture to prescribe chemical amendments (agricultural lime or gypsum) and balanced N-P-K fertilizer strategies, strictly advocating laboratory soil testing.
4. **Explainable AI (XAI) Engine:** Discloses working memory facts, evaluated conditions, matched rule IDs, and agronomic justifications behind every conclusion.

---

## 🧠 Core AI Concepts Demonstrated

| Component | AI Role in Expert Systems | Implementation in Code |
| :--- | :--- | :--- |
| **Knowledge Base (KB)** | Domain repository of agronomic facts, crop requirements, and pathology profiles | `knowledge_base.py` (`CROPS_DATABASE`, `SOIL_PROFILES`, `CROP_PROBLEMS_DATABASE`, `SOIL_PH_GUIDELINES`) |
| **Rule Base** | Curated collection of 26 production rules encoded as `IF <conditions> THEN <deductions>` | `rules.py` (`Rule` class & `build_rule_base()`) |
| **Working Memory** | Dynamic memory storing initial input facts and derived conclusions during a session | `rules.py` (`WorkingMemory` class) |
| **Inference Engine** | Reasoning mechanism that systematically evaluates facts against rules | `rules.py` (`InferenceEngine` class) |
| **Forward Chaining** | Data-driven reasoning: begins with known environmental facts and proceeds forward to fire rules | `InferenceEngine.run_forward_chaining()` |
| **Explanation Facility** | Mechanism justifying why a conclusion was drawn and which rules fired | `matched_rules` trace displayed on Streamlit cards |

---

## 📂 Project Directory Structure

```text
agriculture_expert_system/
│
├── app.py                # Interactive Streamlit Web Application (UI)
├── rules.py              # Rule Base (26 IF-THEN rules) & Forward-Chaining Inference Engine
├── knowledge_base.py     # Domain Knowledge Base (Crop dossiers, soil traits, disease facts)
├── requirements.txt      # Project dependencies (Streamlit)
├── test_rules.py         # Automated unit test suite (17 comprehensive test cases)
├── README.md             # Setup, architecture guide, and usage instructions
└── project_report.md     # Full 15-section academic mini-project report with Viva Q&A
```

---

## ⚡ Quick Start & Installation

### Step 1: Open Terminal / Command Prompt
Navigate to the project directory:
```bash
cd agriculture_expert_system
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
**On Windows:**
```powershell
py -m venv venv
.\venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install Streamlit using pip:
```bash
pip install -r requirements.txt
```
*(Or run `py -m pip install -r requirements.txt`)*

---

## 🧪 Running the Automated Test Suite

Before launching the web interface, verify that the forward-chaining inference engine and all 26 production rules pass their test specifications:

```bash
python -m unittest test_rules.py
```
*(On Windows if `python` is aliased to `py`, run: `py -m unittest test_rules.py`)*

**Expected Output:**
```text
Ran 17 tests in 0.001s

OK
```

All 17 automated unit tests validate:
- Rule base minimum count (>= 15 rules)
- Kharif black soil multi-crop firing (Soybean, Cotton, Rice)
- Rabi alluvial wheat and mustard evaluation
- Sandy soil drought risk and millet selection
- Acidic and alkaline soil constraints
- Yellow leaves under adequate moisture vs. wilting in dry/wet soil
- White powdery mildew detection
- Liming and gypsum recommendations
- Graceful handling of unmatched / extreme environmental values

---

## 🌐 Launching the Web Application

Start the Streamlit application locally:

```bash
streamlit run app.py
```
*(Or: `py -m streamlit run app.py`)*

Streamlit will launch local web server at:
👉 **`http://localhost:8501`**

Open this address in your preferred web browser (Google Chrome, Edge, Firefox, or Safari).

---

## 📖 How to Use the Application

### 1. 🏠 Home / Overview
- Explains the expert system paradigm, knowledge base architecture, working memory, and forward chaining.
- Displays the interactive architectural flow diagram.

### 2. 🌾 Crop Recommendation
1. Select the **Cropping Season** (*Kharif*, *Rabi*, or *Summer*).
2. Choose your **Soil Texture** (*Black*, *Alluvial*, *Red*, or *Sandy*).
3. Set the **Soil pH** slider (e.g., 6.5 - 7.5).
4. Enter the **Average Temperature** (e.g., 26°C).
5. Select expected **Rainfall** (*Low*, *Medium*, *High*) and **Irrigation Availability** (*Yes* or *No*).
6. Click **🌿 Evaluate Crop Suitability**.
7. The system displays recommended candidate crops, crop dossiers (growth duration, N-P-K ratios, management tips), and the **Explainable AI trace** listing the exact rules that fired.

### 3. 🔍 Problem & Disease Diagnosis
1. Select the **Affected Crop** (e.g., *Wheat*, *Cotton*, *Tomato*).
2. Check observed **Foliar Symptoms** (e.g., *Yellow leaves*, *Wilting*, *Brown spots*, *White powder*).
3. Specify the **Soil Moisture Level** in the root zone (*Low*, *Adequate*, *High*).
4. Click **🔍 Diagnose Symptoms**.
5. The system outputs potential causes, suggested immediate interventions, preventive agronomic management, and when an agricultural extension officer (KVK) must be consulted.

### 4. 🧪 Soil & Fertilizer Advice
1. Select **Soil Type** and input **Tested Soil pH**.
2. Click **🧪 Generate Soil Advice**.
3. View the classified pH band (Strongly Acidic, Moderately Acidic, Optimal Neutral, Moderately Alkaline, Strongly Alkaline), required soil amendments (Lime or Gypsum), texture-specific leaching cautions, and mandatory soil-testing advice.

### 5. 🧠 AI Rule Base & Trace Inspector
- Browse all 26 rules with their formal antecedents (`IF` condition) and agronomic explanations (`THEN` deduction).
- Filter rules by category to understand how declarative knowledge is structured.

---

## 📋 Sample Test Scenarios for Demonstrations

| Scenario | Input Parameters | Expected Fired Rules | Expected Output |
| :--- | :--- | :--- | :--- |
| **Monsoon Cash Crop** | Kharif, Black soil, High rain, 28°C, Irrigation Yes, pH 6.8 | `R-CROP-01`, `R-CROP-03` | Recommends **Soybean**, **Cotton**, and **Rice**. |
| **Winter Cereal** | Rabi, Alluvial soil, Low rain, 20°C, Irrigation Yes, pH 6.5 | `R-CROP-02`, `R-CROP-06` | Recommends **Wheat** and **Mustard**. |
| **Arid Sandy Land** | Kharif, Sandy soil, Low rain, 32°C, Irrigation No, pH 7.0 | `R-CROP-04`, `R-CROP-10` | Recommends **Millets (Bajra)**; triggers **Drought Stress Warning**. |
| **Yellow Foliage** | Symptom: *Yellow leaves*, Soil Moisture: *Adequate* | `R-DIAG-01` | Deduce **Nitrogen or Iron deficiency / Root Asphyxiation**; recommends soil test. |
| **Moisture Deficit** | Symptom: *Wilting*, Soil Moisture: *Low* | `R-DIAG-02` | Deduce **Acute Water Stress**; suggests root-zone irrigation and mulching. |
| **Pathogen Wilt** | Symptom: *Wilting*, Soil Moisture: *High* | `R-DIAG-03` | Deduce **Suspected Vascular Wilt / Root Rot**; urgent stem incision check & KVK consult. |
| **Acidic Farmland** | Soil pH: 4.8, Soil Type: Red | `R-SOIL-01` | Prescribes **Agricultural Lime**; warns against unbuffered acidifying fertilizers. |

---

## 🎓 Viva Questions & Quick Answers

- **Q1: Why use a Rule-Based Expert System instead of Deep Learning or Machine Learning?**
  * *Answer:* Agricultural decisions directly affect a farmer's livelihood. Machine learning models act as opaque "black boxes" that cannot easily explain why a prediction was made. Rule-based systems provide 100% transparency, deterministic reasoning, and can be edited directly by agricultural scientists without retraining large neural networks.
- **Q2: What is Forward Chaining?**
  * *Answer:* Forward Chaining is a bottom-up, data-driven inference strategy. It starts with known input facts placed into Working Memory and evaluates rule conditions (IF). When conditions match, the rule fires and adds its conclusion to the output or working memory.
- **Q3: What happens if contradictory rules exist?**
  * *Answer:* In advanced expert systems, conflict resolution strategies (such as rule prioritization, specificity, or certainty factors) resolve contradictions. In our system, rules are mutually partitioned and validated through unit tests.

---

## ⚖️ Educational Disclaimer
*This software is created for computer science and artificial intelligence educational demonstrations. Crop suitability and disease treatments should be confirmed with local agronomists and laboratory soil testing before financial investments are made.*
