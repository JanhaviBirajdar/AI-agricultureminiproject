"""
knowledge_base.py
=================
Knowledge Base for the Rule-Based Agriculture Expert System.

This module acts as the domain repository (Knowledge Base) in traditional
AI Expert System architecture. It stores declarative agronomic facts,
crop profiles, soil characteristics, symptom-disease mappings, and soil pH guidelines.
"""

# ==============================================================================
# 1. CROP PROFILES (Domain Facts)
# ==============================================================================
CROPS_DATABASE = {
    "Rice": {
        "name": "Rice (Oryza sativa)",
        "category": "Cereal / Staple",
        "suitable_seasons": ["Kharif", "Summer"],
        "suitable_soils": ["Alluvial", "Black"],
        "min_ph": 5.5,
        "max_ph": 7.5,
        "optimal_ph": "6.0 - 7.0",
        "min_temp": 20,
        "max_temp": 38,
        "optimal_temp": "22°C - 32°C",
        "rainfall_requirement": ["High"],
        "irrigation_dependency": "High (Standing water or frequent irrigation required)",
        "duration": "120 - 150 days",
        "npk_general_ratio": "100:50:50 kg/ha (N:P:K)",
        "description": "Rice is a water-intensive staple crop suited for warm, humid climates with heavy clayey or alluvial soils that hold moisture.",
        "management_tip": "Maintain 2-5 cm standing water during tillering to panicle initiation. Avoid water deficit during flowering."
    },
    "Wheat": {
        "name": "Wheat (Triticum aestivum)",
        "category": "Cereal / Winter Crop",
        "suitable_seasons": ["Rabi"],
        "suitable_soils": ["Alluvial", "Black"],
        "min_ph": 6.0,
        "max_ph": 7.8,
        "optimal_ph": "6.2 - 7.2",
        "min_temp": 10,
        "max_temp": 28,
        "optimal_temp": "15°C - 24°C",
        "rainfall_requirement": ["Low", "Medium"],
        "irrigation_dependency": "Moderate (Critical at Crown Root Initiation and Flowering)",
        "duration": "110 - 140 days",
        "npk_general_ratio": "120:60:40 kg/ha (N:P:K)",
        "description": "Wheat is the premier Rabi cereal requiring cool growing conditions and mild, dry weather during grain ripening.",
        "management_tip": "Apply the first irrigation at Crown Root Initiation (21 days after sowing). Avoid terminal heat stress during grain filling."
    },
    "Cotton": {
        "name": "Cotton (Gossypium hirsutum)",
        "category": "Commercial / Fiber Crop",
        "suitable_seasons": ["Kharif"],
        "suitable_soils": ["Black", "Alluvial"],
        "min_ph": 6.0,
        "max_ph": 8.0,
        "optimal_ph": "6.5 - 7.5",
        "min_temp": 21,
        "max_temp": 38,
        "optimal_temp": "25°C - 35°C",
        "rainfall_requirement": ["Medium", "High"],
        "irrigation_dependency": "Moderate (Resistant to brief dry spells, vulnerable to waterlogging)",
        "duration": "150 - 180 days",
        "npk_general_ratio": "100:50:50 kg/ha (N:P:K)",
        "description": "Cotton is known as 'White Gold'. Thrives best in deep, moisture-retentive black cotton soils (regur).",
        "management_tip": "Ensure excellent drainage. Waterlogging during early seedling or boll development severely reduces yield."
    },
    "Soybean": {
        "name": "Soybean (Glycine max)",
        "category": "Oilseed / Legume",
        "suitable_seasons": ["Kharif"],
        "suitable_soils": ["Black", "Alluvial"],
        "min_ph": 6.0,
        "max_ph": 7.5,
        "optimal_ph": "6.3 - 7.2",
        "min_temp": 20,
        "max_temp": 35,
        "optimal_temp": "24°C - 30°C",
        "rainfall_requirement": ["Medium", "High"],
        "irrigation_dependency": "Low to Moderate (Rainfed during Kharif, supplementary irrigation if dry spell)",
        "duration": "90 - 110 days",
        "npk_general_ratio": "20:60:40 kg/ha (N:P:K) + Rhizobium biofertilizer",
        "description": "Soybean is a high-protein legume that enriches soil through biological nitrogen fixation.",
        "management_tip": "Inoculate seeds with Rhizobium culture before sowing to enhance natural nodulation and nitrogen fixing."
    },
    "Maize": {
        "name": "Maize / Corn (Zea mays)",
        "category": "Cereal / Coarse Grain",
        "suitable_seasons": ["Kharif", "Rabi", "Summer"],
        "suitable_soils": ["Alluvial", "Red", "Black"],
        "min_ph": 5.8,
        "max_ph": 7.8,
        "optimal_ph": "6.0 - 7.2",
        "min_temp": 18,
        "max_temp": 36,
        "optimal_temp": "21°C - 30°C",
        "rainfall_requirement": ["Medium", "High"],
        "irrigation_dependency": "Moderate (Sensitive to drought at tasseling and silking)",
        "duration": "90 - 120 days",
        "npk_general_ratio": "120:60:40 kg/ha (N:P:K)",
        "description": "Maize is a versatile C4 cereal with high yield potential, adaptable to diverse seasons with proper drainage.",
        "management_tip": "Maintain weed-free conditions during the first 30-40 days. Avoid waterlogging around root zones."
    },
    "Millets": {
        "name": "Pearl Millet / Bajra (Pennisetum glaucum)",
        "category": "Millet / Nutri-cereal",
        "suitable_seasons": ["Kharif", "Summer"],
        "suitable_soils": ["Sandy", "Red", "Black"],
        "min_ph": 5.5,
        "max_ph": 8.5,
        "optimal_ph": "6.5 - 7.8",
        "min_temp": 22,
        "max_temp": 42,
        "optimal_temp": "28°C - 36°C",
        "rainfall_requirement": ["Low", "Medium"],
        "irrigation_dependency": "Low (Highly drought and heat tolerant)",
        "duration": "75 - 90 days",
        "npk_general_ratio": "60:30:20 kg/ha (N:P:K)",
        "description": "Millets are climate-resilient nutri-cereals that survive harsh arid conditions and nutrient-poor sandy soils.",
        "management_tip": "Ideal for dryland farming. Requires minimal fertilizer inputs and tolerates low rainfall."
    },
    "Groundnut": {
        "name": "Groundnut / Peanut (Arachis hypogaea)",
        "category": "Oilseed / Legume",
        "suitable_seasons": ["Kharif", "Summer"],
        "suitable_soils": ["Sandy", "Red"],
        "min_ph": 5.5,
        "max_ph": 7.2,
        "optimal_ph": "6.0 - 6.8",
        "min_temp": 20,
        "max_temp": 35,
        "optimal_temp": "25°C - 30°C",
        "rainfall_requirement": ["Low", "Medium"],
        "irrigation_dependency": "Moderate (Critical at pegging and pod formation)",
        "duration": "105 - 125 days",
        "npk_general_ratio": "25:50:40 kg/ha (N:P:K) + Gypsum 400 kg/ha",
        "description": "Groundnut requires well-drained, loose sandy loam or red soil so pegs can easily penetrate the soil to form pods.",
        "management_tip": "Apply gypsum at 40-45 days after sowing during flowering to ensure calcium supply for healthy pod filling."
    },
    "Mustard": {
        "name": "Mustard (Brassica juncea)",
        "category": "Oilseed / Winter Crop",
        "suitable_seasons": ["Rabi"],
        "suitable_soils": ["Alluvial", "Sandy", "Black"],
        "min_ph": 6.0,
        "max_ph": 7.8,
        "optimal_ph": "6.2 - 7.4",
        "min_temp": 12,
        "max_temp": 26,
        "optimal_temp": "15°C - 22°C",
        "rainfall_requirement": ["Low", "Medium"],
        "irrigation_dependency": "Low to Moderate (1 to 2 irrigations at flowering & siliqua stage)",
        "duration": "100 - 120 days",
        "npk_general_ratio": "80:40:40 kg/ha (N:P:K) + 20 kg/ha Sulphur",
        "description": "Mustard is a major winter oilseed that requires cool dry weather and modest soil moisture.",
        "management_tip": "Sulphur application is essential to increase oil content. Protect against aphid infestation during flowering."
    },
    "Gram": {
        "name": "Chickpea / Bengal Gram (Cicer arietinum)",
        "category": "Pulse / Legume",
        "suitable_seasons": ["Rabi"],
        "suitable_soils": ["Black", "Alluvial", "Red"],
        "min_ph": 6.0,
        "max_ph": 8.0,
        "optimal_ph": "6.2 - 7.5",
        "min_temp": 10,
        "max_temp": 28,
        "optimal_temp": "18°C - 24°C",
        "rainfall_requirement": ["Low"],
        "irrigation_dependency": "Low (Sensitive to excess moisture; thrives on residual soil moisture)",
        "duration": "95 - 115 days",
        "npk_general_ratio": "20:40:20 kg/ha (N:P:K)",
        "description": "Chickpea is a hardy winter legume that thrives on conserved soil moisture and fixes atmospheric nitrogen.",
        "management_tip": "Avoid over-irrigation. Water stagnation causes severe collar rot and wilt."
    },
    "Sugarcane": {
        "name": "Sugarcane (Saccharum officinarum)",
        "category": "Commercial / Perennial Cash Crop",
        "suitable_seasons": ["Kharif", "Rabi", "Summer"],
        "suitable_soils": ["Alluvial", "Black"],
        "min_ph": 6.0,
        "max_ph": 8.0,
        "optimal_ph": "6.5 - 7.5",
        "min_temp": 20,
        "max_temp": 38,
        "optimal_temp": "24°C - 33°C",
        "rainfall_requirement": ["High"],
        "irrigation_dependency": "High (Year-round assured irrigation mandatory)",
        "duration": "300 - 365 days",
        "npk_general_ratio": "250:100:100 kg/ha (N:P:K)",
        "description": "Sugarcane is a long-duration cash crop requiring heavy soils, high fertility, and constant water availability.",
        "management_tip": "Adopt drip irrigation and trash mulching to save 30-40% water and suppress weeds."
    }
}

# ==============================================================================
# 2. SOIL PROFILES (Domain Facts)
# ==============================================================================
SOIL_PROFILES = {
    "Black": {
        "name": "Black Soil (Regur / Vertisol)",
        "texture": "Clayey, fine-textured",
        "water_retention": "High (Expands when wet, cracks deeply when dry)",
        "drainage": "Slow / Poor internal drainage",
        "inherent_fertility": "Rich in calcium, magnesium, carbonates, and potassium; deficient in nitrogen and phosphorus.",
        "best_suited_for": ["Cotton", "Soybean", "Wheat", "Gram", "Sorghum"],
        "management_advice": "Avoid over-irrigation to prevent waterlogging. Incorporate well-rotted farmyard manure to improve soil aeration."
    },
    "Alluvial": {
        "name": "Alluvial Soil",
        "texture": "Loamy to sandy clay loam",
        "water_retention": "Moderate to High",
        "drainage": "Good to moderate",
        "inherent_fertility": "Highly fertile; rich in potash and lime; deficient in nitrogen and organic matter.",
        "best_suited_for": ["Rice", "Wheat", "Sugarcane", "Maize", "Mustard", "Vegetables"],
        "management_advice": "Ideal agricultural soil. Practice crop rotation with legumes to sustain nitrogen reserves."
    },
    "Red": {
        "name": "Red Soil",
        "texture": "Sandy to loam with ferric oxide concentrations",
        "water_retention": "Low to Moderate",
        "drainage": "High / Rapid percolation",
        "inherent_fertility": "Porous and slightly acidic; deficient in nitrogen, phosphorus, humus, and lime.",
        "best_suited_for": ["Groundnut", "Millets", "Pulses", "Maize", "Castor"],
        "management_advice": "Add generous amounts of organic compost and biofertilizers. Frequent, light irrigations or drip systems are recommended."
    },
    "Sandy": {
        "name": "Sandy Soil",
        "texture": "Coarse particles with loose structure",
        "water_retention": "Very Low (Water drains quickly)",
        "drainage": "Excessive",
        "inherent_fertility": "Low nutrient-holding capacity; prone to rapid leaching of applied fertilizers.",
        "best_suited_for": ["Millets (Bajra)", "Groundnut", "Melons", "Root vegetables"],
        "management_advice": "Split nitrogen fertilizer applications into multiple small doses to prevent leaching into groundwater. Use green manuring to build humus."
    }
}

# ==============================================================================
# 3. CROP PROBLEMS & SYMPTOM DATABASE (Domain Facts)
# ==============================================================================
CROP_PROBLEMS_DATABASE = {
    "Yellow leaves": {
        "symptom": "Yellow leaves (Chlorosis)",
        "primary_causes": [
            "Nitrogen deficiency (older lower leaves turn uniformly pale yellow)",
            "Iron or micronutrient deficiency (younger upper leaves yellow while veins remain green)",
            "Waterlogging or root oxygen starvation"
        ],
        "category": "Nutrient Deficiency or Water Stress",
        "risk_level": "Moderate",
        "immediate_action": "Check soil moisture. If soil is soaked, stop irrigation and aerate. If soil is dry, irrigate. Apply balanced foliar spray (urea 1% or micronutrient chelate) only after checking moisture.",
        "prevention": "Perform a comprehensive laboratory soil test to detect nutrient imbalances before applying heavy synthetic fertilizers.",
        "expert_trigger": "If yellowing spreads rapidly to all leaves despite balanced moisture within 48-72 hours."
    },
    "Brown spots on leaves": {
        "symptom": "Brown spots on leaves (Necrotic lesions / Leaf Spot)",
        "primary_causes": [
            "Fungal infection (e.g., Alternaria, Cercospora, or early blight)",
            "Potassium deficiency (brown scorched margins on older leaves)",
            "Bacterial leaf spot (water-soaked brown lesions with yellow halo)"
        ],
        "category": "Suspected Fungal / Bacterial Disease or K Deficiency",
        "risk_level": "Moderate to High",
        "immediate_action": "Prune and destroy severely infected lower leaves. Avoid overhead sprinkler irrigation that keeps leaves wet.",
        "prevention": "Ensure proper plant spacing for air circulation. Spray organic neem seed kernel extract (5%) or contact fungicide (e.g., Mancozeb/Copper oxychloride) if fungal infection is suspected.",
        "expert_trigger": "If spots develop concentric target rings or water-soaked margins, bring an infected leaf sample to your local Krishi Vigyan Kendra (KVK)."
    },
    "Wilting": {
        "symptom": "Wilting (Drooping foliage and loss of turgor)",
        "primary_causes": [
            "Acute water deficit (dry root zone / moisture stress)",
            "Vascular fungal/bacterial wilt (Fusarium, Ralstonia)",
            "Root rot / Nematode infestation damaging water uptake"
        ],
        "category": "Water Stress or Vascular Pathogen",
        "risk_level": "High",
        "immediate_action": "Inspect the root zone 5-10 cm deep. If bone-dry, irrigate immediately. If wet but still wilting, suspect vascular wilt or root rot.",
        "prevention": "Adopt crop rotation with non-host crops. Use Trichoderma viride enriched compost to suppress soil-borne wilt pathogens.",
        "expert_trigger": "If plants remain limp even when soil is moist, or if cut stem oozes milky bacterial stream in water, consult an agronomist immediately."
    },
    "White powder on leaves": {
        "symptom": "White powder on leaves (Powdery Mildew)",
        "primary_causes": [
            "Powdery mildew fungal infestation (Erysiphe / Podosphaera species)",
            "Favored by dry canopy conditions with high relative atmospheric humidity"
        ],
        "category": "Fungal Infection",
        "risk_level": "Moderate",
        "immediate_action": "Remove heavily coated leaves to reduce inoculum. Avoid excessive nitrogen application which produces tender susceptible foliage.",
        "prevention": "Spray wettable sulphur (2 g/L) or neem oil (3-5 ml/L). Ensure adequate sunlight penetration through canopy thinning.",
        "expert_trigger": "If powdery mildew spreads across >30% of the crop canopy during flowering or pod development."
    },
    "Stunted growth": {
        "symptom": "Stunted growth (Poor vigor and shortened internodes)",
        "primary_causes": [
            "Phosphorus deficiency (inhibited root establishment, sometimes purple/bronze leaf tint)",
            "Soil compaction or extreme soil pH locking nutrient bioavailability",
            "Root-knot nematode attack"
        ],
        "category": "Soil Nutritional Barrier or Root Health Issue",
        "risk_level": "Moderate",
        "immediate_action": "Test soil compaction with a penetration rod. Inspect roots for swelling galls (indicating nematodes) or dark decaying roots.",
        "prevention": "Apply well-decomposed organic matter. Ensure soil pH is amended to 6.0-7.5 where phosphorus availability peaks.",
        "expert_trigger": "If roots show prominent irregular knots/galls or plants fail to grow across large patches of the field."
    }
}

# ==============================================================================
# 4. SOIL PH CLASSIFICATION & ADVICE GUIDELINES
# ==============================================================================
SOIL_PH_GUIDELINES = {
    "Strongly Acidic": {
        "range": (0.0, 5.49),
        "status": "Strongly Acidic (pH < 5.5)",
        "description": "High soil acidity can trigger aluminum and manganese toxicity while locking up phosphorus, calcium, and magnesium.",
        "remedy": "Apply agricultural lime (calcium carbonate) or dolomite lime based on a laboratory buffer pH test. Incorporate organic compost.",
        "suitable_crops": "Tea, Coffee, Potato, Rice (with caution)"
    },
    "Moderately Acidic": {
        "range": (5.5, 6.49),
        "status": "Moderately Acidic (pH 5.5 - 6.4)",
        "description": "Mild acidity. Most micronutrients are readily available, but phosphorus and legume nodulation may be slightly constrained.",
        "remedy": "Light application of lime or wood ash if cultivating sensitive crops like wheat or pulses. Maintain organic matter.",
        "suitable_crops": "Rice, Maize, Soybean, Groundnut, Millets"
    },
    "Optimal Neutral": {
        "range": (6.5, 7.5),
        "status": "Optimal / Neutral (pH 6.5 - 7.5)",
        "description": "Ideal agronomic range. Maximum bioavailability of primary nutrients (N, P, K) and beneficial microbial activity.",
        "remedy": "No chemical pH correction required. Maintain balanced fertility with crop rotation and farmyard manure.",
        "suitable_crops": "All major crops (Wheat, Cotton, Soybean, Rice, Maize, Pulses, Mustard, Sugarcane)"
    },
    "Moderately Alkaline": {
        "range": (7.51, 8.49),
        "status": "Moderately Alkaline (pH 7.6 - 8.4)",
        "description": "Higher presence of calcium carbonates. Phosphorus may precipitate as insoluble calcium phosphate; risk of zinc and iron chlorosis.",
        "remedy": "Apply organic manures, green manure crops (e.g., Dhaincha/Sunnhemp), and acid-forming fertilizers such as ammonium sulfate.",
        "suitable_crops": "Cotton, Wheat, Millets, Mustard, Sugarcane"
    },
    "Strongly Alkaline": {
        "range": (8.5, 14.0),
        "status": "Strongly Alkaline / Sodic (pH >= 8.5)",
        "description": "High sodium saturation leading to poor soil structure, slow water infiltration, and severe nutrient lockup.",
        "remedy": "Apply agricultural gypsum (calcium sulfate) followed by heavy flushing/leaching with good quality irrigation water. Avoid saline water.",
        "suitable_crops": "Barley, Sugarbeet, Salt-tolerant Grasses (Requires active soil reclamation)"
    }
}
