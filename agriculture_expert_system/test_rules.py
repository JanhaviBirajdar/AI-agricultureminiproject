"""
test_rules.py
=============
Automated test suite for the Agriculture Expert System rule base and inference engine.

Tests cover:
- Different seasons (Kharif, Rabi, Summer) and soil types (Black, Alluvial, Red, Sandy)
- Rainfall levels (Low, Medium, High) and irrigation availability (Yes, No)
- Crop problem diagnoses (Yellow leaves, Wilting, White powder, Stunted growth)
- Extreme soil pH values (Acidic, Neutral, Alkaline)
- Soil texture-specific management (Sandy leaching, Black soil drainage)
- Unmatched / edge cases where no crop rule fires
- Integrity and count of rule base (guaranteeing >= 15 rules)
"""

import unittest
from rules import (
    run_crop_recommendation,
    run_crop_diagnosis,
    run_soil_management_advice,
    get_all_rules,
    InferenceEngine,
    Rule
)
from knowledge_base import CROPS_DATABASE, SOIL_PROFILES, CROP_PROBLEMS_DATABASE


class TestAgricultureExpertSystem(unittest.TestCase):

    def test_rule_base_minimum_count(self):
        """Verify the rule base contains at least 15 production rules as required."""
        rules = get_all_rules()
        self.assertGreaterEqual(
            len(rules), 15,
            f"Expected at least 15 rules in the Rule Base, but found {len(rules)}"
        )
        # Check rule attributes integrity
        for rule in rules:
            self.assertTrue(rule.rule_id, "Rule must have a valid rule_id")
            self.assertTrue(rule.name, "Rule must have a human-readable name")
            self.assertTrue(rule.antecedents_description, "Rule must describe its antecedents")
            self.assertTrue(rule.explanation, "Rule must include an explainable justification")

    def test_crop_recommendation_kharif_black_soil(self):
        """Test Kharif season with Black soil and High rainfall -> Soybean, Cotton, Rice."""
        result = run_crop_recommendation(
            soil_type="Black",
            soil_ph=6.8,
            season="Kharif",
            temperature=28.0,
            rainfall="High",
            irrigation="Yes"
        )
        self.assertIn("Soybean", result["recommended_crops"])
        self.assertIn("Cotton", result["recommended_crops"])
        self.assertIn("Rice", result["recommended_crops"])
        
        # Verify matched rule IDs in trace
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-CROP-01", fired_ids)
        self.assertIn("R-CROP-03", fired_ids)

    def test_crop_recommendation_rabi_alluvial_wheat(self):
        """Test Rabi season with Alluvial soil, low rain, and irrigation -> Wheat & Mustard."""
        result = run_crop_recommendation(
            soil_type="Alluvial",
            soil_ph=6.5,
            season="Rabi",
            temperature=20.0,
            rainfall="Low",
            irrigation="Yes"
        )
        self.assertIn("Wheat", result["recommended_crops"])
        self.assertIn("Mustard", result["recommended_crops"])
        
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-CROP-02", fired_ids)
        self.assertIn("R-CROP-06", fired_ids)

    def test_crop_recommendation_sandy_drought_scenario(self):
        """Test Sandy soil with Low rainfall and No irrigation -> Hardy Millets & Drought Warning."""
        result = run_crop_recommendation(
            soil_type="Sandy",
            soil_ph=7.0,
            season="Kharif",
            temperature=32.0,
            rainfall="Low",
            irrigation="No"
        )
        self.assertIn("Millets", result["recommended_crops"])
        
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-CROP-04", fired_ids)
        self.assertIn("R-CROP-10", fired_ids)
        
        # Verify that water-intensive crops are NOT recommended
        self.assertNotIn("Rice", result["recommended_crops"])
        self.assertNotIn("Sugarcane", result["recommended_crops"])

    def test_crop_recommendation_groundnut_red_soil(self):
        """Test Groundnut suitability in Red loose soil during Kharif."""
        result = run_crop_recommendation(
            soil_type="Red",
            soil_ph=6.5,
            season="Kharif",
            temperature=27.0,
            rainfall="Medium",
            irrigation="Yes"
        )
        self.assertIn("Groundnut", result["recommended_crops"])
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-CROP-05", fired_ids)

    def test_crop_recommendation_acidic_soil_constraint(self):
        """Test acidic soil constraint rule triggers when pH < 5.5."""
        result = run_crop_recommendation(
            soil_type="Red",
            soil_ph=4.8,
            season="Kharif",
            temperature=26.0,
            rainfall="High",
            irrigation="Yes"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-CROP-11", fired_ids)

    def test_crop_recommendation_extreme_weather_no_match(self):
        """Test edge case where extreme weather (52°C) produces no suitable crop rule match."""
        result = run_crop_recommendation(
            soil_type="Sandy",
            soil_ph=7.0,
            season="Rabi", # Season/temp mismatch (Rabi with 52°C)
            temperature=52.0,
            rainfall="Low",
            irrigation="No"
        )
        # R-CROP-10 fires because Sandy + Low rain + No irrigation,
        # but traditional Rabi crops (Wheat, Mustard, Gram) require 10-28°C and should NOT fire.
        self.assertNotIn("Wheat", result["recommended_crops"])
        self.assertNotIn("Mustard", result["recommended_crops"])
        self.assertNotIn("Gram", result["recommended_crops"])

    def test_diagnosis_yellow_leaves_adequate_moisture(self):
        """Test Yellow leaves with adequate soil moisture -> Nutrient deficiency deduction."""
        result = run_crop_diagnosis(
            crop_type="Wheat",
            symptoms=["Yellow leaves"],
            soil_moisture="Adequate"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-DIAG-01", fired_ids)
        
        # Verify deduction content
        deduction = result["conclusions"][0]
        self.assertIn("Nitrogen", deduction["possible_cause"])

    def test_diagnosis_wilting_dry_soil(self):
        """Test Wilting with Low soil moisture -> Moisture deficit / water stress."""
        result = run_crop_diagnosis(
            crop_type="Cotton",
            symptoms=["Wilting"],
            soil_moisture="Low"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-DIAG-02", fired_ids)
        self.assertIn("Water Stress", result["conclusions"][0]["possible_cause"])

    def test_diagnosis_wilting_wet_soil(self):
        """Test Wilting despite High soil moisture -> Vascular wilt / root rot."""
        result = run_crop_diagnosis(
            crop_type="Tomato",
            symptoms=["Wilting"],
            soil_moisture="High"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-DIAG-03", fired_ids)
        self.assertIn("Vascular", result["conclusions"][0]["possible_cause"])

    def test_diagnosis_white_powder(self):
        """Test White powder on leaves -> Powdery Mildew."""
        result = run_crop_diagnosis(
            crop_type="Groundnut",
            symptoms=["White powder on leaves"],
            soil_moisture="Adequate"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-DIAG-05", fired_ids)
        self.assertIn("Powdery Mildew", result["conclusions"][0]["possible_cause"])

    def test_diagnosis_compound_symptoms(self):
        """Test combination of Yellow leaves and Stunted growth -> Rule 19 compound rule."""
        result = run_crop_diagnosis(
            crop_type="Soybean",
            symptoms=["Yellow leaves", "Stunted growth"],
            soil_moisture="Adequate"
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-DIAG-01", fired_ids) # Single symptom rule
        self.assertIn("R-DIAG-07", fired_ids) # Compound symptom rule

    def test_soil_management_strongly_acidic(self):
        """Test soil pH < 5.5 triggers agricultural lime recommendation."""
        result = run_soil_management_advice(
            soil_type="Red",
            soil_ph=4.5
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-SOIL-01", fired_ids)
        lime_conclusion = [c for c in result["conclusions"] if "lime" in c.get("recommendation", "").lower()]
        self.assertTrue(len(lime_conclusion) > 0, "Acidic soil must recommend lime")

    def test_soil_management_optimal_neutral(self):
        """Test soil pH 7.0 reports optimal balanced neutral status."""
        result = run_soil_management_advice(
            soil_type="Alluvial",
            soil_ph=7.0
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-SOIL-03", fired_ids)

    def test_soil_management_strongly_alkaline(self):
        """Test soil pH >= 8.5 triggers agricultural gypsum reclamation."""
        result = run_soil_management_advice(
            soil_type="Black",
            soil_ph=8.9
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-SOIL-05", fired_ids)
        gypsum_conclusion = [c for c in result["conclusions"] if "gypsum" in c.get("recommendation", "").lower()]
        self.assertTrue(len(gypsum_conclusion) > 0, "Strongly alkaline soil must recommend gypsum")

    def test_soil_texture_sandy_leaching_rule(self):
        """Test Sandy soil triggers split nitrogen and leaching prevention rule."""
        result = run_soil_management_advice(
            soil_type="Sandy",
            soil_ph=6.8
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-SOIL-06", fired_ids)

    def test_soil_texture_black_drainage_rule(self):
        """Test Black soil triggers clay drainage & aeration rule."""
        result = run_soil_management_advice(
            soil_type="Black",
            soil_ph=7.2
        )
        fired_ids = [r["rule_id"] for r in result["matched_rules"]]
        self.assertIn("R-SOIL-07", fired_ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
