"""
rules.py
========
Inference Engine and Rule Base for the Agriculture Expert System.

This module implements a classic Forward-Chaining Rule-Based AI Expert System:
1. Rule: Class representing an IF-THEN rule (Antecedent -> Consequent).
2. WorkingMemory: Stores known facts and newly deduced conclusions.
3. RuleBase: Collection of domain-specific IF-THEN rules.
4. InferenceEngine: Evaluates Working Memory against the Rule Base via Forward Chaining,
   collecting matched rules and generating explainable justification traces.
"""

from typing import Dict, Any, List, Optional
from knowledge_base import (
    CROPS_DATABASE,
    SOIL_PROFILES,
    CROP_PROBLEMS_DATABASE,
    SOIL_PH_GUIDELINES
)


class Rule:
    """
    Represents an individual IF-THEN production rule.
    """
    def __init__(
        self,
        rule_id: str,
        name: str,
        category: str,
        antecedents_description: str,
        condition_func,
        action_func,
        explanation: str
    ):
        self.rule_id = rule_id
        self.name = name
        self.category = category
        self.antecedents_description = antecedents_description
        self.condition_func = condition_func
        self.action_func = action_func
        self.explanation = explanation

    def evaluate(self, working_memory: Dict[str, Any]) -> bool:
        """Evaluates whether the rule's IF conditions are satisfied by working memory."""
        try:
            return bool(self.condition_func(working_memory))
        except Exception:
            return False

    def fire(self, working_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the THEN action of the rule and returns deduction data."""
        return self.action_func(working_memory)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "category": self.category,
            "condition": self.antecedents_description,
            "explanation": self.explanation
        }


class WorkingMemory:
    """
    Represents the Working Memory in an Expert System.
    Stores initial facts asserted by the user and derived facts generated during inference.
    """
    def __init__(self, initial_facts: Optional[Dict[str, Any]] = None):
        self.facts: Dict[str, Any] = initial_facts.copy() if initial_facts else {}
        self.derived_facts: Dict[str, Any] = {}
        self.fired_rules: List[Rule] = []
        self.audit_trace: List[Dict[str, Any]] = []

    def set_fact(self, key: str, value: Any):
        self.facts[key] = value

    def get_fact(self, key: str, default: Any = None) -> Any:
        return self.facts.get(key, default)

    def add_derived(self, key: str, value: Any):
        self.derived_facts[key] = value

    def record_fired_rule(self, rule: Rule, output: Dict[str, Any]):
        self.fired_rules.append(rule)
        self.audit_trace.append({
            "rule_id": rule.rule_id,
            "name": rule.name,
            "category": rule.category,
            "condition": rule.antecedents_description,
            "explanation": rule.explanation,
            "output": output
        })


class InferenceEngine:
    """
    Forward-Chaining Inference Engine.
    Matches facts in Working Memory against Rules in the Rule Base.
    """
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def run_forward_chaining(
        self,
        facts: Dict[str, Any],
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes forward chaining inference over working memory facts.
        Returns matched rules, unmatched rules, derived conclusions, and complete trace.
        """
        wm = WorkingMemory(facts)
        matched_rules: List[Dict[str, Any]] = []
        unmatched_rules: List[Dict[str, Any]] = []
        conclusions: List[Dict[str, Any]] = []

        # Filter rules by category if requested
        candidate_rules = [
            r for r in self.rules
            if category_filter is None or r.category == category_filter
        ]

        for rule in candidate_rules:
            is_matched = rule.evaluate(wm.facts)
            if is_matched:
                deduction = rule.fire(wm.facts)
                wm.record_fired_rule(rule, deduction)
                conclusions.append(deduction)
                matched_rules.append({
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "category": rule.category,
                    "condition": rule.antecedents_description,
                    "explanation": rule.explanation,
                    "deduction": deduction
                })
            else:
                unmatched_rules.append({
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "category": rule.category,
                    "condition": rule.antecedents_description,
                    "explanation": rule.explanation
                })

        return {
            "working_memory_facts": wm.facts,
            "matched_rules": matched_rules,
            "unmatched_rules": unmatched_rules,
            "conclusions": conclusions,
            "audit_trace": wm.audit_trace
        }


# ==============================================================================
# RULE BASE DEFINITIONS (Knowledge Representation)
# ==============================================================================

def build_rule_base() -> List[Rule]:
    """
    Constructs the set of 25+ domain IF-THEN rules across:
    - Crop Recommendation
    - Disease & Problem Diagnosis
    - Soil & Fertilizer Advice
    """
    rules: List[Rule] = []

    # --------------------------------------------------------------------------
    # CATEGORY 1: CROP RECOMMENDATION RULES
    # --------------------------------------------------------------------------

    # Rule 1: Soybean and Cotton in Kharif Black Soil with Medium/High Rain
    rules.append(Rule(
        rule_id="R-CROP-01",
        name="Kharif Black Soil Cash & Oilseed Crops",
        category="Crop Recommendation",
        antecedents_description="IF season is 'Kharif' AND soil_type is 'Black' AND rainfall in ['Medium', 'High']",
        condition_func=lambda f: (
            f.get("season") == "Kharif" and
            f.get("soil_type") == "Black" and
            f.get("rainfall") in ["Medium", "High"]
        ),
        action_func=lambda f: {
            "crop": ["Soybean", "Cotton"],
            "suitability": "Highly Suitable",
            "justification": "Deep black soils offer high water retention ideal for Kharif crops like Soybean and Cotton when rainfall is medium to high."
        },
        explanation="Black soil (vertisol) expands and retains moisture during monsoon rains, fulfilling the high moisture demand of Soybean and Cotton root zones."
    ))

    # Rule 2: Wheat in Rabi Alluvial with Irrigation
    rules.append(Rule(
        rule_id="R-CROP-02",
        name="Rabi Alluvial Irrigated Wheat",
        category="Crop Recommendation",
        antecedents_description="IF season is 'Rabi' AND irrigation is 'Yes' AND soil_type is 'Alluvial'",
        condition_func=lambda f: (
            f.get("season") == "Rabi" and
            f.get("irrigation") == "Yes" and
            f.get("soil_type") == "Alluvial" and
            f.get("temperature", 20) <= 28
        ),
        action_func=lambda f: {
            "crop": ["Wheat"],
            "suitability": "Highly Suitable",
            "justification": "Alluvial soils in cool Rabi winter with assured irrigation provide ideal conditions for Crown Root Initiation and grain filling in Wheat."
        },
        explanation="Wheat requires cool growing temperatures (12-25°C) and fertile loamy alluvial plains with timely irrigation at critical stages."
    ))

    # Rule 3: Rice in Kharif/Summer with High Rain or Assured Irrigation
    rules.append(Rule(
        rule_id="R-CROP-03",
        name="High Moisture Rice / Paddy",
        category="Crop Recommendation",
        antecedents_description="IF rainfall is 'High' AND (irrigation is 'Yes' OR rainfall is 'High') AND soil_type in ['Alluvial', 'Black'] AND season in ['Kharif', 'Summer']",
        condition_func=lambda f: (
            f.get("rainfall") == "High" and
            f.get("soil_type") in ["Alluvial", "Black"] and
            f.get("season") in ["Kharif", "Summer"] and
            f.get("temperature", 25) >= 20
        ),
        action_func=lambda f: {
            "crop": ["Rice"],
            "suitability": "Highly Suitable",
            "justification": "Paddy requires continuous heavy soil moisture, high rainfall, and clayey/alluvial soils with low percolation losses."
        },
        explanation="Rice requires standing water during early vegetative stages. Heavy alluvial and black soils retard water percolation."
    ))

    # Rule 4: Pearl Millet / Bajra in Sandy or Red Soil with Low/Medium Rain
    rules.append(Rule(
        rule_id="R-CROP-04",
        name="Arid / Semi-Arid Pearl Millet (Bajra)",
        category="Crop Recommendation",
        antecedents_description="IF soil_type in ['Sandy', 'Red'] AND rainfall in ['Low', 'Medium'] AND season in ['Kharif', 'Summer']",
        condition_func=lambda f: (
            f.get("soil_type") in ["Sandy", "Red"] and
            f.get("rainfall") in ["Low", "Medium"] and
            f.get("season") in ["Kharif", "Summer"] and
            f.get("temperature", 28) >= 22
        ),
        action_func=lambda f: {
            "crop": ["Millets"],
            "suitability": "Highly Suitable",
            "justification": "Millets (Bajra) possess deep fibrous roots and high photosynthetic water-use efficiency, thriving in coarse sandy/red soils under dry conditions."
        },
        explanation="Pearl Millet is a drought-tolerant C4 cereal that can survive in fast-draining, nutrient-poor sandy soils where other cereals fail."
    ))

    # Rule 5: Groundnut in Sandy or Red Soil with Moderate Moisture
    rules.append(Rule(
        rule_id="R-CROP-05",
        name="Loose Soil Groundnut / Peanut",
        category="Crop Recommendation",
        antecedents_description="IF soil_type in ['Sandy', 'Red'] AND season in ['Kharif', 'Summer'] AND pH between 5.5 and 7.5",
        condition_func=lambda f: (
            f.get("soil_type") in ["Sandy", "Red"] and
            f.get("season") in ["Kharif", "Summer"] and
            5.5 <= f.get("soil_ph", 6.5) <= 7.5 and
            f.get("temperature", 25) >= 20
        ),
        action_func=lambda f: {
            "crop": ["Groundnut"],
            "suitability": "Highly Suitable",
            "justification": "Groundnut requires light, friable, loose sandy or red soils so that flower pegs can easily enter the ground for underground pod formation."
        },
        explanation="Heavy soils cause peg breakage during harvest; well-drained sandy/red loams enable seamless pod expansion and simple digging."
    ))

    # Rule 6: Mustard in Rabi season with Low to Medium Rainfall
    rules.append(Rule(
        rule_id="R-CROP-06",
        name="Rabi Cool-Season Mustard",
        category="Crop Recommendation",
        antecedents_description="IF season is 'Rabi' AND temperature between 10°C and 26°C AND soil_type in ['Alluvial', 'Sandy', 'Black']",
        condition_func=lambda f: (
            f.get("season") == "Rabi" and
            10 <= f.get("temperature", 18) <= 26 and
            f.get("soil_type") in ["Alluvial", "Sandy", "Black"] and
            f.get("rainfall") in ["Low", "Medium"]
        ),
        action_func=lambda f: {
            "crop": ["Mustard"],
            "suitability": "Highly Suitable",
            "justification": "Mustard thrives in cool, dry winter weather with mild moisture. Excessive humidity or rainfall induces white rust and aphid outbreaks."
        },
        explanation="Mustard requires dry weather during maturity and pod filling; cold nights and warm sunny days boost oil synthesis."
    ))

    # Rule 7: Chickpea / Gram in Rabi Season with Low Rainfall
    rules.append(Rule(
        rule_id="R-CROP-07",
        name="Rabi Pulse / Chickpea (Gram)",
        category="Crop Recommendation",
        antecedents_description="IF season is 'Rabi' AND rainfall is 'Low' AND soil_type in ['Black', 'Alluvial', 'Red']",
        condition_func=lambda f: (
            f.get("season") == "Rabi" and
            f.get("rainfall") == "Low" and
            f.get("soil_type") in ["Black", "Alluvial", "Red"] and
            10 <= f.get("temperature", 20) <= 28
        ),
        action_func=lambda f: {
            "crop": ["Gram"],
            "suitability": "Highly Suitable",
            "justification": "Chickpea (Gram) is well-suited to residual moisture in post-monsoon soils. It requires dry weather and is vulnerable to root rot under high moisture."
        },
        explanation="Legumes like Chickpea develop strong taproots that exploit subsoil moisture in winter, fixing atmospheric nitrogen without needing heavy irrigation."
    ))

    # Rule 8: Maize in Alluvial, Red, or Black Soil with Medium/High Rain
    rules.append(Rule(
        rule_id="R-CROP-08",
        name="Versatile Cereal Maize",
        category="Crop Recommendation",
        antecedents_description="IF soil_type in ['Alluvial', 'Red', 'Black'] AND temperature between 18°C and 35°C AND rainfall in ['Medium', 'High']",
        condition_func=lambda f: (
            f.get("soil_type") in ["Alluvial", "Red", "Black"] and
            18 <= f.get("temperature", 25) <= 35 and
            f.get("rainfall") in ["Medium", "High"] and
            5.8 <= f.get("soil_ph", 6.5) <= 7.8
        ),
        action_func=lambda f: {
            "crop": ["Maize"],
            "suitability": "Moderately to Highly Suitable",
            "justification": "Maize can be grown across diverse seasons provided there is good soil drainage and steady moisture during flowering."
        },
        explanation="Maize has high biomass accumulation and wide adaptability, but requires adequate soil aeration and cannot tolerate water stagnation."
    ))

    # Rule 9: Sugarcane in Perennial/Kharif with High Water & Warm Climate
    rules.append(Rule(
        rule_id="R-CROP-09",
        name="Perennial Cash Crop Sugarcane",
        category="Crop Recommendation",
        antecedents_description="IF rainfall is 'High' AND irrigation is 'Yes' AND soil_type in ['Alluvial', 'Black'] AND temperature >= 20°C",
        condition_func=lambda f: (
            f.get("rainfall") == "High" and
            f.get("irrigation") == "Yes" and
            f.get("soil_type") in ["Alluvial", "Black"] and
            f.get("temperature", 25) >= 20 and
            6.0 <= f.get("soil_ph", 7.0) <= 8.0
        ),
        action_func=lambda f: {
            "crop": ["Sugarcane"],
            "suitability": "Suitable for Long-Term Cultivation",
            "justification": "Sugarcane is an intensive annual crop requiring deep alluvial or black soils with guaranteed year-round irrigation."
        },
        explanation="Sugarcane has a long duration (10-12 months) and consumes substantial water; only viable with assured irrigation infrastructure."
    ))

    # Rule 10: Sandy Soil Drought Warning Rule
    rules.append(Rule(
        rule_id="R-CROP-10",
        name="Drought Stress Warning for Coarse Sandy Soil",
        category="Crop Recommendation",
        antecedents_description="IF soil_type is 'Sandy' AND rainfall is 'Low' AND irrigation is 'No'",
        condition_func=lambda f: (
            f.get("soil_type") == "Sandy" and
            f.get("rainfall") == "Low" and
            f.get("irrigation") == "No"
        ),
        action_func=lambda f: {
            "crop": ["Millets"],
            "suitability": "Restricted to Hardy Millets Only",
            "justification": "Severe drought risk. Water-intensive crops (Rice, Sugarcane, Vegetables) will experience total crop failure under dry sandy conditions without irrigation.",
            "warning": "Water-holding capacity is critically low. Restrict planting to drought-hardy Millets (Bajra) or cluster beans."
        },
        explanation="Sandy soil exhibits rapid gravitational percolation. Without irrigation or high rain, soil moisture drops below permanent wilting point rapidly."
    ))

    # Rule 11: Acidic Soil Restriction Rule
    rules.append(Rule(
        rule_id="R-CROP-11",
        name="Acidic Soil Constraint on Sensitive Crops",
        category="Crop Recommendation",
        antecedents_description="IF soil_ph < 5.5",
        condition_func=lambda f: f.get("soil_ph", 7.0) < 5.5,
        action_func=lambda f: {
            "crop": ["Rice"],
            "suitability": "Acid-Tolerant Only (Liming Mandatory for Others)",
            "justification": "Strongly acidic soil causes aluminum toxicity and immobilizes phosphorus. Highly sensitive crops like Wheat and Cotton will experience severe root burn."
        },
        explanation="At pH < 5.5, soluble aluminum and manganese ions become toxic to plant root tips while phosphate binds tightly to iron/aluminum oxides."
    ))

    # Rule 12: High Salinity / Alkaline Soil Restriction Rule
    rules.append(Rule(
        rule_id="R-CROP-12",
        name="Alkaline / Sodic Soil Limitation",
        category="Crop Recommendation",
        antecedents_description="IF soil_ph > 8.2",
        condition_func=lambda f: f.get("soil_ph", 7.0) > 8.2,
        action_func=lambda f: {
            "crop": ["Millets", "Mustard"],
            "suitability": "Salt-Tolerant Only (Soil Reclamation Advised)",
            "justification": "High alkalinity and sodium saturation impair soil structure and cause severe zinc and iron chlorosis in sensitive legumes and pulses."
        },
        explanation="High pH (>8.2) causes micronutrients like iron, zinc, and manganese to precipitate into forms unavailable for plant uptake."
    ))

    # --------------------------------------------------------------------------
    # CATEGORY 2: CROP PROBLEM & DISEASE DIAGNOSIS RULES
    # --------------------------------------------------------------------------

    # Rule 13: Yellow Leaves with Adequate/High Moisture -> Nutrient Deficiency
    rules.append(Rule(
        rule_id="R-DIAG-01",
        name="Yellow Leaves Under Adequate Moisture (Nutrient Deficiency)",
        category="Crop Diagnosis",
        antecedents_description="IF 'Yellow leaves' in symptoms AND soil_moisture in ['Adequate', 'High']",
        condition_func=lambda f: (
            "Yellow leaves" in f.get("symptoms", []) and
            f.get("soil_moisture") in ["Adequate", "High"]
        ),
        action_func=lambda f: {
            "possible_cause": "Nitrogen or Iron Deficiency / Potential Root Asphyxiation",
            "category": "Nutrient Deficiency or Excess Water",
            "suggested_action": "Check lower leaves vs upper leaves. If lower leaves yellow first, suspect Nitrogen deficiency. If upper leaves yellow with green veins, suspect Iron/Zinc deficiency. If soil is waterlogged, drain water to aerate roots.",
            "prevention": "Perform a laboratory soil and tissue test before adding synthetic nitrogen. Apply compost and well-rotted FYM.",
            "consult_expert_when": "Yellowing intensifies rapidly or is accompanied by rotting stem bases."
        },
        explanation="Chlorophyll synthesis requires adequate Nitrogen, Iron, and Magnesium. When moisture is normal, leaf yellowing (chlorosis) typically points to mineral deficiency rather than drought."
    ))

    # Rule 14: Wilting with Low Soil Moisture -> Drought / Water Stress
    rules.append(Rule(
        rule_id="R-DIAG-02",
        name="Wilting Under Dry Soil (Moisture Deficit Stress)",
        category="Crop Diagnosis",
        antecedents_description="IF 'Wilting' in symptoms AND soil_moisture is 'Low'",
        condition_func=lambda f: (
            "Wilting" in f.get("symptoms", []) and
            f.get("soil_moisture") == "Low"
        ),
        action_func=lambda f: {
            "possible_cause": "Acute Water Stress / Temporary or Permanent Wilting",
            "category": "Environmental / Water Deficit",
            "suggested_action": "Check root-zone moisture 5-10 cm below surface. Provide immediate light-to-moderate irrigation during evening or early morning to prevent thermal shock.",
            "prevention": "Apply organic mulch (straw or dried leaves) to reduce soil evaporation. Adopt drip or sprinkler irrigation.",
            "consult_expert_when": "Plants fail to recover turgidity within 12 hours after deep irrigation."
        },
        explanation="When transpiration rate exceeds water absorption by roots due to dry soil, plant cells lose turgor pressure, leading to visible wilting."
    ))

    # Rule 15: Wilting Despite Adequate/High Moisture -> Vascular Pathogen / Root Rot
    rules.append(Rule(
        rule_id="R-DIAG-03",
        name="Wilting in Wet Soil (Suspected Vascular Wilt or Root Rot)",
        category="Crop Diagnosis",
        antecedents_description="IF 'Wilting' in symptoms AND soil_moisture in ['Adequate', 'High']",
        condition_func=lambda f: (
            "Wilting" in f.get("symptoms", []) and
            f.get("soil_moisture") in ["Adequate", "High"]
        ),
        action_func=lambda f: {
            "possible_cause": "Vascular Fungal/Bacterial Wilt (e.g., Fusarium, Ralstonia) or Root Rot / Damping Off",
            "category": "Soil-Borne Pathogen / Root Disease",
            "suggested_action": "Cut open the lower stem of an affected plant. Look for dark brown vascular discoloration or milky bacterial ooze in a glass of water. Halt all excess watering.",
            "prevention": "Treat future seeds with bio-fungicide (Trichoderma viride). Practice multi-year crop rotation with non-host crops.",
            "consult_expert_when": "Immediately. Soil-borne vascular wilts spread quickly and cannot be cured by watering."
        },
        explanation="Vascular pathogens clog the plant's xylem vessels, preventing water transport up the stem even when soil water is abundant."
    ))

    # Rule 16: Brown Spots on Leaves -> Suspected Fungal or Bacterial Leaf Spot
    rules.append(Rule(
        rule_id="R-DIAG-04",
        name="Brown Spots / Foliar Lesions (Fungal / Bacterial Leaf Spot)",
        category="Crop Diagnosis",
        antecedents_description="IF 'Brown spots on leaves' in symptoms",
        condition_func=lambda f: "Brown spots on leaves" in f.get("symptoms", []),
        action_func=lambda f: {
            "possible_cause": "Foliar Fungal Infection (e.g., Early Blight, Cercospora, Alternaria) or Potassium Deficiency",
            "category": "Foliar Disease or Potassium Deficiency",
            "suggested_action": "Inspect lesion shape: concentric target rings usually indicate fungal blight. Scorched leaf margins indicate Potassium deficiency. Remove and safely dispose of infected foliage.",
            "prevention": "Avoid wetting the crop canopy during irrigation. Spray neem oil (5 ml/L) or copper-based protective fungicide if humidity is high.",
            "consult_expert_when": "Spots multiply rapidly across more than 20% of the upper canopy."
        },
        explanation="Warm and humid microclimates enable fungal spores to germinate on moist leaves, creating necrotic brown dead tissue zones."
    ))

    # Rule 17: White Powder on Leaves -> Powdery Mildew
    rules.append(Rule(
        rule_id="R-DIAG-05",
        name="White Powdery Coating (Suspected Powdery Mildew)",
        category="Crop Diagnosis",
        antecedents_description="IF 'White powder on leaves' in symptoms",
        condition_func=lambda f: "White powder on leaves" in f.get("symptoms", []),
        action_func=lambda f: {
            "possible_cause": "Powdery Mildew Fungal Infection (Erysiphe / Podosphaera)",
            "category": "Fungal Infestation",
            "suggested_action": "Prune overcrowded foliage to allow direct sunlight penetration. Spray wettable sulphur (2 g/L) or bio-fungicide like Ampelomyces quisqualis.",
            "prevention": "Maintain wider plant-to-plant spacing to enhance wind circulation. Avoid excessive nitrogen which produces succulent vulnerable leaves.",
            "consult_expert_when": "Coating covers flower buds or developing fruit/pods."
        },
        explanation="Powdery mildew produces superficial fungal hyphae and conidia spores resembling talcum powder on leaf surfaces."
    ))

    # Rule 18: Stunted Growth with Soil pH Imbalance
    rules.append(Rule(
        rule_id="R-DIAG-06",
        name="Stunted Growth from Nutritional / pH Constraint",
        category="Crop Diagnosis",
        antecedents_description="IF 'Stunted growth' in symptoms AND (soil_ph < 6.0 OR soil_ph > 7.8)",
        condition_func=lambda f: (
            "Stunted growth" in f.get("symptoms", []) and
            (f.get("soil_ph", 7.0) < 6.0 or f.get("soil_ph", 7.0) > 7.8)
        ),
        action_func=lambda f: {
            "possible_cause": "pH-Induced Nutrient Lockup (Phosphorus fixation or micronutrient unavailability)",
            "category": "Soil Chemical Barrier",
            "suggested_action": "Check root development for swelling or knotting (nematodes). Test soil pH and amend with lime (if acidic) or gypsum/organic matter (if alkaline).",
            "prevention": "Maintain soil organic matter above 0.75% to buffer root zone pH and stimulate beneficial mycorrhizal fungi.",
            "consult_expert_when": "Roots display distinct galls or swelling (indicating root-knot nematodes)."
        },
        explanation="Extreme soil pH locks Phosphorus and essential trace minerals into insoluble chemical compounds that roots cannot absorb."
    ))

    # Rule 19: Compound Symptoms: Yellow Leaves AND Stunted Growth
    rules.append(Rule(
        rule_id="R-DIAG-07",
        name="Compound Symptom: Yellowing + Stunted Growth (Severe Depletion or Root Stress)",
        category="Crop Diagnosis",
        antecedents_description="IF 'Yellow leaves' in symptoms AND 'Stunted growth' in symptoms",
        condition_func=lambda f: (
            "Yellow leaves" in f.get("symptoms", []) and
            "Stunted growth" in f.get("symptoms", [])
        ),
        action_func=lambda f: {
            "possible_cause": "Severe Generalized Soil Nutrient Depletion or Root-Knot Nematode Infestation",
            "category": "Compound Root / Nutritional Stress",
            "suggested_action": "Dig up a sample plant carefully with root ball intact. Wash soil and inspect roots for knots, black rot, or stunted taproot. Apply balanced vermicompost.",
            "prevention": "Rotate crops with Marigold (Tagetes) which naturally reduces root nematode populations. Submit soil for comprehensive fertility profiling.",
            "consult_expert_when": "Patches of stunted yellow plants expand in circular clusters across the field."
        },
        explanation="When both vegetative height and chlorophyll synthesis are simultaneously restricted, the limiting factor is almost invariably in the root system or broad-spectrum nutrient exhaustion."
    ))

    # --------------------------------------------------------------------------
    # CATEGORY 3: SOIL & FERTILIZER MANAGEMENT RULES
    # --------------------------------------------------------------------------

    # Rule 20: Strongly Acidic Soil Management
    rules.append(Rule(
        rule_id="R-SOIL-01",
        name="Strongly Acidic Soil Reclamation (pH < 5.5)",
        category="Soil Management",
        antecedents_description="IF soil_ph < 5.5",
        condition_func=lambda f: f.get("soil_ph", 7.0) < 5.5,
        action_func=lambda f: {
            "soil_status": "Strongly Acidic",
            "recommendation": "Apply agricultural lime (calcium carbonate) or dolomite based on laboratory buffer test.",
            "fertilizer_advice": "Do NOT apply acid-forming fertilizers like Ammonium Sulfate or Urea in excessive quantities. Add Rock Phosphate or SSP instead of DAP if unlimed.",
            "soil_testing_mandatory": True,
            "organic_practices": "Incorporate well-rotted farmyard manure or vermicompost to buffer soil acidity."
        },
        explanation="Acidic soils (pH < 5.5) suffer from aluminum and manganese toxicity and rapid phosphorus precipitation as aluminum phosphate."
    ))

    # Rule 21: Moderately Acidic Soil Advice
    rules.append(Rule(
        rule_id="R-SOIL-02",
        name="Moderately Acidic Soil Conditioning (pH 5.5 to 6.4)",
        category="Soil Management",
        antecedents_description="IF 5.5 <= soil_ph < 6.5",
        condition_func=lambda f: 5.5 <= f.get("soil_ph", 7.0) < 6.5,
        action_func=lambda f: {
            "soil_status": "Moderately Acidic",
            "recommendation": "Mild liming or wood ash application if cultivating sensitive crops like pulses or wheat. Highly suitable for Tea, Rice, and Potato.",
            "fertilizer_advice": "Apply Single Super Phosphate (SSP) which supplies Phosphorus, Calcium (19%), and Sulphur (11%).",
            "soil_testing_mandatory": True,
            "organic_practices": "Use biofertilizers like Phosphate Solubilizing Bacteria (PSB) to unlock fixed phosphorus."
        },
        explanation="At pH 5.5 - 6.4, nutrient availability is generally fair, but legume nodulation bacteria (Rhizobium) perform better near neutral pH."
    ))

    # Rule 22: Optimal Neutral Soil Management
    rules.append(Rule(
        rule_id="R-SOIL-03",
        name="Optimal Neutral Soil Maintenance (pH 6.5 to 7.5)",
        category="Soil Management",
        antecedents_description="IF 6.5 <= soil_ph <= 7.5",
        condition_func=lambda f: 6.5 <= f.get("soil_ph", 7.0) <= 7.5,
        action_func=lambda f: {
            "soil_status": "Optimal / Balanced Neutral",
            "recommendation": "Ideal agronomic condition. No chemical pH amendment needed.",
            "fertilizer_advice": "Apply balanced NPK fertilizers strictly in accordance with crop requirements and soil test cards. Avoid indiscriminate over-fertilization.",
            "soil_testing_mandatory": True,
            "organic_practices": "Maintain regular additions of compost and practice legume-inclusive crop rotations to preserve organic carbon."
        },
        explanation="The pH range 6.5 to 7.5 ensures maximum simultaneous availability of Nitrogen, Phosphorus, Potassium, Calcium, Magnesium, and Micronutrients."
    ))

    # Rule 23: Moderately Alkaline Soil Advice
    rules.append(Rule(
        rule_id="R-SOIL-04",
        name="Moderately Alkaline Soil Management (pH 7.6 to 8.4)",
        category="Soil Management",
        antecedents_description="IF 7.5 < soil_ph < 8.5",
        condition_func=lambda f: 7.5 < f.get("soil_ph", 7.0) < 8.5,
        action_func=lambda f: {
            "soil_status": "Moderately Alkaline",
            "recommendation": "Incorporate green manure crops (such as Dhaincha or Sunnhemp) and decomposed farmyard manure to release organic acids.",
            "fertilizer_advice": "Use physiologically acid-forming fertilizers such as Ammonium Sulfate or Urea. Supplement with Zinc Sulfate (25 kg/ha) and foliar Iron chelate.",
            "soil_testing_mandatory": True,
            "organic_practices": "Avoid high-bicarbonate irrigation water. Add humic acid extracts to enhance micronutrient uptake."
        },
        explanation="In alkaline soils (pH 7.6-8.4), free calcium carbonates lock phosphorus and induce widespread Zinc and Iron deficiencies."
    ))

    # Rule 24: Strongly Alkaline / Sodic Soil Reclamation
    rules.append(Rule(
        rule_id="R-SOIL-05",
        name="Strongly Alkaline / Sodic Soil Reclamation (pH >= 8.5)",
        category="Soil Management",
        antecedents_description="IF soil_ph >= 8.5",
        condition_func=lambda f: f.get("soil_ph", 7.0) >= 8.5,
        action_func=lambda f: {
            "soil_status": "Strongly Alkaline / Sodic",
            "recommendation": "Chemical reclamation with Agricultural Gypsum (Calcium Sulfate) is strongly recommended, followed by leaching with good quality water.",
            "fertilizer_advice": "Do NOT apply sodium-containing or alkaline fertilizers. Soil testing is indispensable before planting any commercial crop.",
            "soil_testing_mandatory": True,
            "organic_practices": "Grow salt-tolerant green manuring crops (Dhaincha) and ensure surface drainage to prevent salt accumulation."
        },
        explanation="Excess exchangeable sodium disperses soil clay particles, destroying soil structure, suffocating roots, and causing extreme nutrient toxicity."
    ))

    # Rule 25: Sandy Soil Nutrient Leaching Mitigation
    rules.append(Rule(
        rule_id="R-SOIL-06",
        name="Sandy Soil Leaching Management",
        category="Soil Management",
        antecedents_description="IF soil_type is 'Sandy'",
        condition_func=lambda f: f.get("soil_type") == "Sandy",
        action_func=lambda f: {
            "soil_status": "Coarse Textured / Low CEC",
            "recommendation": "Split fertilizer applications into 3 to 4 smaller doses rather than 1 or 2 heavy bulk doses to stop nutrient leaching into groundwater.",
            "fertilizer_advice": "Use slow-release or neem-coated urea and organic biofertilizers.",
            "soil_testing_mandatory": True,
            "organic_practices": "Incorporate biochar or green manure to permanently enhance moisture-holding capacity and cation exchange capacity (CEC)."
        },
        explanation="Coarse sand grains possess minimal surface charge; soluble nitrates and potassium wash right past shallow root zones during rain or irrigation."
    ))

    # Rule 26: Black Soil Aeration & Drainage Management
    rules.append(Rule(
        rule_id="R-SOIL-07",
        name="Black Soil Drainage & Aeration Management",
        category="Soil Management",
        antecedents_description="IF soil_type is 'Black'",
        condition_func=lambda f: f.get("soil_type") == "Black",
        action_func=lambda f: {
            "soil_status": "Heavy Clay / Vertisol",
            "recommendation": "Construct broad bed and furrow (BBF) systems to facilitate surface drainage and prevent water stagnation.",
            "fertilizer_advice": "Deep placement of phosphorus fertilizer is beneficial because heavy clay binds phosphorus near the surface.",
            "soil_testing_mandatory": True,
            "organic_practices": "Incorporate coarse crop residues to alleviate heavy soil compaction and enhance aeration during monsoon rains."
        },
        explanation="Black clay expands when wet, drastically slowing down internal percolation and risking root asphyxiation during continuous rains."
    ))

    return rules


# ==============================================================================
# FACADE FUNCTIONS FOR EASY APPLICATION ACCESS
# ==============================================================================

# Global Rule Engine instance
_GLOBAL_RULES = build_rule_base()
_GLOBAL_ENGINE = InferenceEngine(_GLOBAL_RULES)


def get_all_rules() -> List[Rule]:
    """Returns the complete rule base."""
    return _GLOBAL_RULES


def run_crop_recommendation(
    soil_type: str,
    soil_ph: float,
    season: str,
    temperature: float,
    rainfall: str,
    irrigation: str
) -> Dict[str, Any]:
    """
    Evaluates crop suitability using Forward Chaining over the Rule Base.
    """
    facts = {
        "soil_type": soil_type,
        "soil_ph": float(soil_ph),
        "season": season,
        "temperature": float(temperature),
        "rainfall": rainfall,
        "irrigation": irrigation
    }
    result = _GLOBAL_ENGINE.run_forward_chaining(facts, category_filter="Crop Recommendation")

    # Aggregate candidate crops from fired rules
    recommended_crops = []
    for conclusion in result["conclusions"]:
        crops = conclusion.get("crop", [])
        if isinstance(crops, list):
            for c in crops:
                if c not in recommended_crops:
                    recommended_crops.append(c)
        elif isinstance(crops, str) and crops not in recommended_crops:
            recommended_crops.append(crops)

    result["recommended_crops"] = recommended_crops
    return result


def run_crop_diagnosis(
    crop_type: str,
    symptoms: List[str],
    soil_moisture: str,
    recent_weather: Optional[str] = "Normal"
) -> Dict[str, Any]:
    """
    Diagnoses crop problems and diseases using Forward Chaining.
    """
    facts = {
        "crop_type": crop_type,
        "symptoms": symptoms,
        "soil_moisture": soil_moisture,
        "recent_weather": recent_weather
    }
    result = _GLOBAL_ENGINE.run_forward_chaining(facts, category_filter="Crop Diagnosis")
    return result


def run_soil_management_advice(
    soil_type: str,
    soil_ph: float,
    organic_matter_status: str = "Medium"
) -> Dict[str, Any]:
    """
    Evaluates soil condition and outputs fertilizer/soil management advice.
    """
    facts = {
        "soil_type": soil_type,
        "soil_ph": float(soil_ph),
        "organic_matter_status": organic_matter_status
    }
    result = _GLOBAL_ENGINE.run_forward_chaining(facts, category_filter="Soil Management")
    return result
