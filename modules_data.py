"""
This module contains the structured data for EduVerse's educational modules.
"""

# Define the educational modules data
k12_modules = [
    {
        "name": "Playtory",
        "description": "Story-based learning where subjects like math, science, and language arts are taught through interactive narratives.",
        "features": ["Interactive narratives", "Cross-subject integration", "Personalized reading levels"],
        "category": "K-12 Foundational Learning",
        "age_range": "5-12 years"
    },
    {
        "name": "MathQuest Land",
        "description": "Gamified math adventures tailored to each grade level, promoting problem-solving skills.",
        "features": ["Grade-specific challenges", "Adaptive difficulty", "Real-world applications"],
        "category": "K-12 Foundational Learning",
        "age_range": "6-12 years"
    },
    {
        "name": "EcoSchool Sim",
        "description": "A sustainability simulator teaching environmental science through managing a virtual school ecosystem.",
        "features": ["Resource management", "Environmental impact tracking", "Sustainable design challenges"],
        "category": "K-12 Foundational Learning",
        "age_range": "8-12 years"
    },
    {
        "name": "SkillSprint",
        "description": "Micro-challenges focusing on specific academic and life skills, with daily tasks and animations.",
        "features": ["Daily challenges", "Skill progression tracking", "Animated tutorials"],
        "category": "K-12 Foundational Learning",
        "age_range": "5-12 years"
    },
    {
        "name": "ParentPal",
        "description": "Bridging home and school by translating classroom concepts into fun home activities for parents and children.",
        "features": ["Home activity suggestions", "Parent-teacher communication", "Progress tracking"],
        "category": "K-12 Foundational Learning",
        "age_range": "5-12 years"
    },
    {
        "name": "YoungChangemakers",
        "description": "Empowering students to tackle community challenges through digital teamwork and action plans.",
        "features": ["Project-based learning", "Community engagement", "Digital collaboration tools"],
        "category": "K-12 Foundational Learning",
        "age_range": "9-12 years"
    },
    {
        "name": "EduMentorMatch",
        "description": "A peer learning marketplace connecting older students with younger ones for tutoring and mentorship.",
        "features": ["Peer matching algorithm", "Guided mentorship materials", "Progress tracking"],
        "category": "K-12 Foundational Learning",
        "age_range": "8-12 years"
    },
    {
        "name": "ThinkTank Jr.",
        "description": "A platform hosting monthly real-world challenges, encouraging students to propose innovative solutions.",
        "features": ["Monthly challenges", "Solution submission system", "Collaborative workspaces"],
        "category": "K-12 Foundational Learning",
        "age_range": "9-12 years"
    }
]

cybersecurity_modules = [
    {
        "name": "CyberSafe Campus",
        "description": "A gamified platform teaching cyber hygiene through simulations like phishing emails and password tests.",
        "features": ["Phishing simulations", "Password strength analysis", "Safe browsing habits"],
        "category": "Cybersecurity Education",
        "age_range": "10+ years"
    },
    {
        "name": "PrivEd Protocol",
        "description": "A privacy-centric LMS where students control their data using zero-knowledge encryption and decentralized identities.",
        "features": ["Data privacy controls", "Zero-knowledge encryption", "Decentralized identity management"],
        "category": "Cybersecurity Education",
        "age_range": "14+ years"
    }
]

engineering_modules = [
    # Civil Engineering
    {
        "name": "CivilVerse",
        "description": "Collaborative city-building simulations focusing on zoning laws, infrastructure, and sustainability.",
        "features": ["3D city modeling", "Infrastructure planning", "Collaborative design"],
        "category": "Civil Engineering",
        "age_range": "14+ years"
    },
    {
        "name": "Failure Vault",
        "description": "Exploration of real-world structural failures, analyzing causes and proposing improvements.",
        "features": ["Case studies", "Failure analysis tools", "Improvement proposals"],
        "category": "Civil Engineering",
        "age_range": "16+ years"
    },
    
    # Mechanical Engineering
    {
        "name": "RetroFix Garage",
        "description": "Reverse engineering vintage machines through 3D exploded views and challenges.",
        "features": ["3D mechanical models", "Interactive disassembly", "Engineering principles"],
        "category": "Mechanical Engineering",
        "age_range": "14+ years"
    },
    {
        "name": "ThermoMentor",
        "description": "Interactive thermodynamics tutor with drag-and-drop diagrams and animated lessons.",
        "features": ["Animated thermodynamic processes", "Interactive diagrams", "Problem-solving exercises"],
        "category": "Mechanical Engineering",
        "age_range": "16+ years"
    },
    
    # Chemical Engineering
    {
        "name": "ChemDAO Classroom",
        "description": "A decentralized platform for solving real industrial chemical challenges with token-based rewards.",
        "features": ["Real industry challenges", "Token reward system", "Collaborative problem solving"],
        "category": "Chemical Engineering",
        "age_range": "16+ years"
    },
    
    # Biomedical Engineering
    {
        "name": "BodyVerse Blueprint",
        "description": "A game where students build virtual human systems, simulate diseases, and test treatments.",
        "features": ["Human anatomy modeling", "Disease simulation", "Treatment testing"],
        "category": "Biomedical Engineering",
        "age_range": "14+ years"
    },
    {
        "name": "BioDesign Studio",
        "description": "Crowdsourced innovation hub connecting students with real biomedical challenges from hospitals and NGOs.",
        "features": ["Real-world challenges", "Mentorship connections", "Prototype development"],
        "category": "Biomedical Engineering",
        "age_range": "16+ years"
    }
]

# Compile all modules into a single list for easy access
all_modules = k12_modules + cybersecurity_modules + engineering_modules

# Generate data for module categories and counts for visualization
def get_module_distribution():
    categories = {}
    for module in all_modules:
        category = module["category"]
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    
    # Ensure we have valid numerical data
    if not categories:
        return {
            "categories": ["No Data"],
            "counts": [0]
        }
    
    return {
        "categories": list(categories.keys()),
        "counts": [max(0, count) for count in categories.values()]  # Ensure non-negative values
    }

# Get modules by category
def get_modules_by_category(category):
    return [module for module in all_modules if module["category"] == category]

# Get module by name
def get_module_by_name(name):
    for module in all_modules:
        if module["name"] == name:
            return module
    return None

# Get all module categories
def get_all_categories():
    categories = set()
    for module in all_modules:
        categories.add(module["category"])
    return sorted(list(categories))

# Get all module names
def get_all_module_names():
    return [module["name"] for module in all_modules]
