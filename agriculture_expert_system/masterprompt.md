Act as a professional Python developer and AI project mentor. Build a complete, beginner-friendly Artificial Intelligence mini project titled:

**“Rule-Based Expert System for Agriculture Using Python”**

### 1. Project Objective
Develop a rule-based expert system that provides basic agricultural recommendations based on user inputs such as soil type, soil pH, season, temperature, rainfall, irrigation availability, and crop symptoms.

The system must use a traditional rule-based AI approach with IF–THEN conditions. Do not use machine learning, external AI APIs, or paid services.

### 2. Technology Stack
- Programming Language: Python
- User Interface: Streamlit
- Rule Engine: Python functions and IF–ELIF–ELSE conditions
- Data Storage: Local Python dictionaries or JSON file
- Development Environment: VS Code or Antigravity
- Deployment: Must run locally on a student's computer

### 3. Main Features

**Feature 1: Crop Recommendation System**
Ask the user to enter:
- Soil type: Black, Alluvial, Red, or Sandy
- Soil pH: 3.0 to 10.0
- Season: Kharif, Rabi, or Summer
- Average temperature in °C
- Rainfall level: Low, Medium, or High
- Irrigation availability: Yes or No

Use predefined IF–THEN rules to recommend suitable crops, such as rice, wheat, cotton, soybean, maize, or millets, according to the selected conditions.

Show the recommended crops with a brief explanation of which rules matched. Support multiple recommendations when appropriate.

**Feature 2: Basic Crop Disease and Problem Diagnosis**
Ask the user to select crop type and observed symptoms, such as:
- Yellow leaves
- Brown spots on leaves
- Wilting
- White powder on leaves
- Stunted growth

Use predefined rules to identify possible causes, such as nutrient deficiency, water stress, or a possible fungal disease.

Display possible causes, suggested preventive actions, and when the farmer should consult an agricultural expert. Never claim that a symptom alone confirms a disease.

**Feature 3: Fertilizer and Soil Advice**
Use soil pH and other available inputs to provide general soil-management suggestions. Recommend soil testing before applying fertilizers. Do not prescribe exact fertilizer doses without sufficient soil-test information.

**Feature 4: Explainable Rule-Based AI**
Display:
- Input conditions
- Rules that matched
- Final recommendation
- Explanation of why the recommendation was generated

Create a separate Python file for the rules so that the project clearly demonstrates knowledge representation and inference.

### 4. Rule Engine
Create at least 15 sample IF–THEN rules covering crop selection, basic crop problems, and soil management.

Example rules:

Rule 1:
IF season is Kharif AND soil type is Black AND rainfall is Medium or High
THEN recommend soybean or cotton for further evaluation.

Rule 2:
IF season is Rabi AND irrigation is available AND soil type is Alluvial
THEN consider wheat as a candidate crop.

Rule 3:
IF leaves are yellow AND soil moisture is adequate
THEN consider nutrient deficiency as one possible cause and suggest soil testing.

Rule 4:
IF plant is wilting AND soil moisture is low
THEN suggest checking irrigation and root-zone moisture.

Rules must be transparent, readable, and editable. Avoid contradictory recommendations and explain any limitations.

Treat these examples as educational rules, not universal agronomic advice. Crop suitability must be checked against local conditions.

### 5. User Interface
Create an attractive, responsive Streamlit application with:
- Project title and agriculture-themed design
- Home page explaining the expert system
- Crop recommendation page
- Crop problem diagnosis page
- Soil management page
- Results displayed in clear cards or sections
- Matched-rule explanations
- Reset or clear-input functionality
- A disclaimer that recommendations are preliminary and location-dependent

Use simple English and intuitive input controls suitable for a beginner.

### 6. Project Folder Structure
Create the following structure:

agriculture_expert_system/
    app.py
    rules.py
    knowledge_base.py
    requirements.txt
    README.md
    project_report.md
    test_rules.py

Responsibilities:
- app.py: Streamlit interface
- rules.py: Inference engine and IF–THEN rules
- knowledge_base.py: Crop information and knowledge base
- requirements.txt: Required Python packages
- README.md: Setup and execution instructions
- project_report.md: Mini-project documentation
- test_rules.py: Basic automated tests for the rules

### 7. AI Concepts to Demonstrate
Clearly implement and document:
- Knowledge Base
- Rule Base
- Working Memory for user inputs
- Inference Engine
- Forward Chaining
- Explainable Recommendations

The system should evaluate user facts against rules and generate conclusions. Keep the implementation simple enough to explain during an engineering viva.

### 8. Testing
Add test cases for:
- Different seasons and soil types
- Low and high rainfall
- Irrigation availability
- Yellow leaves and wilting symptoms
- Missing or invalid inputs
- Situations where no suitable recommendation can be made

Make sure the application runs without errors.

### 9. Documentation
Generate a project report containing:
1. Title
2. Abstract
3. Problem Statement
4. Objectives
5. Existing System and Proposed System
6. Hardware and Software Requirements
7. System Architecture
8. Knowledge Base and Rule Table
9. Algorithm
10. Flowchart
11. Implementation Details
12. Test Cases and Results
13. Advantages and Limitations
14. Future Scope
15. Conclusion

Also provide common AI mini-project viva questions with simple answers.

### 10. Final Requirements
Build the actual working project files, not just sample code or a design mockup.

Install only the necessary dependencies. Include exact commands to create a virtual environment, install requirements, and run the application.

Before finishing:
- Test the rule engine.
- Fix errors.
- Verify the application starts successfully.
- Explain each file and the main rules in beginner-friendly language.
- Do not claim that tests passed unless they have actually been executed.

Start by creating the project folder and implementing the complete working application.