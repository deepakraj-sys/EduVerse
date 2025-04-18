"""
This module contains information about API integrations for the EduVerse platform.
"""

# Define API integration data
api_integrations = [
    {
        "name": "Khan Academy API",
        "category": "Educational Content",
        "description": "Access to a vast library of educational videos and exercises.",
        "use_cases": [
            "Supplement custom learning paths with Khan Academy resources",
            "Import specific exercises for module-aligned practice",
            "Map Khan Academy content to EduVerse learning objectives"
        ],
        "implementation_complexity": "Medium",
        "documentation_url": "https://api-explorer.khanacademy.org/"
    },
    {
        "name": "Quizlet API",
        "category": "Educational Content",
        "description": "Integration of flashcards and study sets across various subjects.",
        "use_cases": [
            "Import subject-specific flashcards into modules",
            "Allow students to create and share study sets",
            "Enable spaced repetition learning within the platform"
        ],
        "implementation_complexity": "Low",
        "documentation_url": "https://quizlet.com/api/2.0/docs"
    },
    {
        "name": "PhishTank API",
        "category": "Cybersecurity Tools",
        "description": "Real-time phishing URL data for simulations.",
        "use_cases": [
            "Create realistic phishing simulation exercises",
            "Update cybersecurity modules with current threat examples",
            "Train students to identify phishing patterns"
        ],
        "implementation_complexity": "Medium",
        "documentation_url": "https://phishtank.org/api_info.php"
    },
    {
        "name": "Google Safe Browsing API",
        "category": "Cybersecurity Tools",
        "description": "Checking URLs against Google's constantly updated lists of unsafe web resources.",
        "use_cases": [
            "Implement URL safety checking in student research activities",
            "Demonstrate real-time threat detection",
            "Build safe browsing simulations"
        ],
        "implementation_complexity": "Medium",
        "documentation_url": "https://developers.google.com/safe-browsing"
    },
    {
        "name": "VirusTotal API",
        "category": "Cybersecurity Tools",
        "description": "Aggregated data on malicious files and URLs.",
        "use_cases": [
            "Demonstrate multi-engine virus scanning",
            "Analyze potentially malicious files in a safe environment",
            "Compare detection rates across security vendors"
        ],
        "implementation_complexity": "High",
        "documentation_url": "https://developers.virustotal.com/reference"
    },
    {
        "name": "Blockly",
        "category": "Data Visualization and Interaction",
        "description": "Visual programming interface for creating interactive coding lessons.",
        "use_cases": [
            "Create drag-and-drop programming exercises",
            "Build logic challenges for younger students",
            "Design algorithm visualization activities"
        ],
        "implementation_complexity": "Medium",
        "documentation_url": "https://developers.google.com/blockly"
    },
    {
        "name": "Urban Institute's Education Data API",
        "category": "Data Visualization and Interaction",
        "description": "Access to a wide range of educational data for analysis and visualization.",
        "use_cases": [
            "Incorporate real educational statistics into lessons",
            "Create data visualization exercises for students",
            "Build comparative analyses across educational institutions"
        ],
        "implementation_complexity": "High",
        "documentation_url": "https://educationdata.urban.org/documentation/"
    }
]

# Get all API categories
def get_all_api_categories():
    categories = set()
    for api in api_integrations:
        categories.add(api["category"])
    return sorted(list(categories))

# Get APIs by category
def get_apis_by_category(category):
    return [api for api in api_integrations if api["category"] == category]

# Get API by name
def get_api_by_name(name):
    for api in api_integrations:
        if api["name"] == name:
            return api
    return None

# Get API distribution by category
def get_api_distribution():
    categories = {}
    for api in api_integrations:
        category = api["category"]
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    
    return {
        "categories": list(categories.keys()),
        "counts": list(categories.values())
    }

# Get all API names
def get_all_api_names():
    return [api["name"] for api in api_integrations]

# Get complexity distribution
def get_complexity_distribution():
    complexity_counts = {"Low": 0, "Medium": 0, "High": 0}
    for api in api_integrations:
        complexity = api["implementation_complexity"]
        complexity_counts[complexity] += 1
    
    return {
        "complexities": list(complexity_counts.keys()),
        "counts": list(complexity_counts.values())
    }
