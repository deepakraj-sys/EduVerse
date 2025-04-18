"""
PrivEd Protocol - Privacy-by-Design Learning Platform
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import random
import time
import datetime
import hashlib
import uuid
import base64
from typing import List, Dict, Any, Optional
from database_models import get_db
import database_models as models
from sqlalchemy import func

# ------ Data Models & State Management ------

class PrivacySettings:
    def __init__(
        self,
        user_id: str,
        data_sharing_level: str,  # "minimal", "standard", "full"
        anonymized_mode: bool,
        private_browsing: bool,
        content_access_settings: Dict[str, str],
        third_party_consent: Dict[str, bool],
        encryption_level: str  # "standard", "enhanced", "maximum"
    ):
        self.user_id = user_id
        self.data_sharing_level = data_sharing_level
        self.anonymized_mode = anonymized_mode
        self.private_browsing = private_browsing
        self.content_access_settings = content_access_settings
        self.third_party_consent = third_party_consent
        self.encryption_level = encryption_level


class PrivacyMetrics:
    def __init__(
        self,
        user_id: str,
        privacy_score: float,
        data_points_protected: int,
        consent_decisions: int,
        identity_protection_level: str
    ):
        self.user_id = user_id
        self.privacy_score = privacy_score
        self.data_points_protected = data_points_protected
        self.consent_decisions = consent_decisions
        self.identity_protection_level = identity_protection_level


class LearningContent:
    def __init__(
        self,
        id: str,
        title: str,
        content_type: str,
        author: str,
        access_level: str,
        privacy_implications: List[str],
        content: Dict[str, Any]
    ):
        self.id = id
        self.title = title
        self.content_type = content_type
        self.author = author
        self.access_level = access_level
        self.privacy_implications = privacy_implications
        self.content = content


# ------ Sample Data ------

def get_sample_privacy_settings() -> PrivacySettings:
    """Get sample privacy settings."""
    if 'prived_privacy_settings' not in st.session_state:
        # Create default privacy settings
        st.session_state.prived_privacy_settings = PrivacySettings(
            user_id=str(uuid.uuid4()),
            data_sharing_level="standard",
            anonymized_mode=False,
            private_browsing=False,
            content_access_settings={
                "personal_information": "educators_only",
                "assignments": "class_members",
                "discussions": "class_members",
                "activity_logs": "educators_only"
            },
            third_party_consent={
                "analytics": True,
                "content_providers": True,
                "research": False,
                "ai_tools": False
            },
            encryption_level="standard"
        )
    return st.session_state.prived_privacy_settings


def get_sample_privacy_metrics() -> PrivacyMetrics:
    """Get sample privacy metrics."""
    if 'prived_privacy_metrics' not in st.session_state:
        # Create default privacy metrics
        st.session_state.prived_privacy_metrics = PrivacyMetrics(
            user_id=st.session_state.prived_privacy_settings.user_id if hasattr(st.session_state, 'prived_privacy_settings') else str(uuid.uuid4()),
            privacy_score=65.0,
            data_points_protected=37,
            consent_decisions=4,
            identity_protection_level="medium"
        )
    return st.session_state.prived_privacy_metrics


def get_sample_learning_content() -> List[LearningContent]:
    """Get sample learning content."""
    return [
        LearningContent(
            id="content-1",
            title="Introduction to Digital Privacy",
            content_type="lesson",
            author="Dr. Samantha Chen",
            access_level="public",
            privacy_implications=[
                "Basic browsing analytics",
                "Progress tracking"
            ],
            content={
                "description": "An introduction to the fundamentals of digital privacy in the modern world.",
                "objectives": [
                    "Understand the basics of digital privacy",
                    "Identify common privacy threats",
                    "Learn privacy protection strategies"
                ],
                "sections": [
                    {
                        "title": "What is Digital Privacy?",
                        "content": """
                        Digital privacy refers to the protection of personal information that is collected, stored, 
                        and shared through digital channels. In an increasingly connected world, where vast amounts 
                        of data are generated and exchanged every second, understanding and managing your digital 
                        privacy has become essential.
                        
                        Privacy is not just about hiding information - it's about having control over your personal 
                        data and deciding who can access it, how it can be used, and under what conditions.
                        """
                    },
                    {
                        "title": "Why Privacy Matters",
                        "content": """
                        Privacy is a fundamental human right recognized in the UN Declaration of Human Rights, 
                        the International Covenant on Civil and Political Rights, and many other international 
                        and regional treaties.
                        
                        Beyond legal protections, privacy matters because:
                        
                        1. **Personal Autonomy**: Privacy gives you freedom to make your own choices without 
                           surveillance, judgment, or interference.
                           
                        2. **Protection from Harm**: Privacy helps protect you from threats like identity theft, 
                           financial fraud, stalking, and harassment.
                           
                        3. **Power Balance**: Privacy helps balance power between individuals and organizations 
                           that collect and use data.
                        """
                    },
                    {
                        "title": "Common Privacy Threats",
                        "content": """
                        Some common threats to digital privacy include:
                        
                        * **Data Collection**: Companies collecting extensive data about your activities, preferences,
                          and behaviors online.
                          
                        * **Data Breaches**: Security incidents where your personal information is exposed or stolen.
                        
                        * **Identity Theft**: Criminals using your personal information to impersonate you.
                        
                        * **Surveillance**: Monitoring of your activities by companies, governments, or individuals.
                        
                        * **Social Engineering**: Psychological manipulation to trick you into revealing personal 
                          information.
                        """
                    }
                ],
                "assessment": {
                    "questions": [
                        {
                            "question": "Which of the following best describes digital privacy?",
                            "options": [
                                "Keeping all your information secret from everyone",
                                "Using private browsing mode in your web browser",
                                "Having control over your personal information and who can access it",
                                "Avoiding the use of digital technologies altogether"
                            ],
                            "correct_answer": "Having control over your personal information and who can access it"
                        },
                        {
                            "question": "Why is privacy considered important?",
                            "options": [
                                "Only because it's required by law",
                                "It protects personal autonomy and helps balance power dynamics",
                                "It only matters for people with something to hide",
                                "It's mainly important for celebrities and public figures"
                            ],
                            "correct_answer": "It protects personal autonomy and helps balance power dynamics"
                        },
                        {
                            "question": "Which of these is NOT typically considered a privacy threat?",
                            "options": [
                                "Data breaches",
                                "Identity theft",
                                "Using strong passwords",
                                "Extensive data collection"
                            ],
                            "correct_answer": "Using strong passwords"
                        }
                    ]
                }
            }
        ),
        LearningContent(
            id="content-2",
            title="Zero-Knowledge Authentication",
            content_type="interactive_demo",
            author="Prof. Alex Rivera",
            access_level="enrolled",
            privacy_implications=[
                "No personal data collection",
                "Demonstrates encryption with simulated data"
            ],
            content={
                "description": "An interactive demonstration of zero-knowledge authentication principles.",
                "objectives": [
                    "Understand how zero-knowledge proofs work",
                    "Experience a secure authentication process",
                    "Learn how to verify identity without revealing sensitive information"
                ],
                "stages": [
                    {
                        "title": "What is Zero-Knowledge Authentication?",
                        "content": """
                        Zero-knowledge authentication is a method that allows one party (the prover) to prove to 
                        another party (the verifier) that they know a value or secret without revealing any 
                        information about the secret itself.
                        
                        This powerful concept is particularly useful for authentication systems where you need 
                        to prove your identity without actually sharing your password or other sensitive credentials.
                        """
                    },
                    {
                        "title": "Interactive Demonstration",
                        "type": "simulation",
                        "simulation_data": {
                            "secret_value": "password123",  # This is just for simulation
                            "hashed_value": "cbfdac6008f9cab4083784cbd1874f76618d2a97",  # SHA-1 hash
                            "steps": [
                                "User creates a password (secret)",
                                "System stores only a mathematical transformation (hash) of the password",
                                "When logging in, user enters password",
                                "System applies same transformation to the entered password",
                                "System compares the result with stored value",
                                "If they match, authentication succeeds without the actual password ever being stored or transmitted"
                            ]
                        }
                    },
                    {
                        "title": "Real-World Applications",
                        "content": """
                        Zero-knowledge authentication is used in various real-world applications:
                        
                        * **Password Verification**: Modern systems don't store your actual password, only a hash.
                        
                        * **Secure Messaging**: Apps like Signal use zero-knowledge principles to ensure even they 
                          can't read your messages.
                          
                        * **Blockchain & Cryptocurrencies**: Zero-knowledge proofs enable private transactions on 
                          public blockchains.
                          
                        * **Identity Verification**: Proving your age without revealing your birthdate or exact age.
                        """
                    }
                ],
                "interactive_elements": {
                    "password_demo": {
                        "type": "simulation",
                        "description": "Try our interactive zero-knowledge password verification system."
                    },
                    "age_verification_demo": {
                        "type": "simulation",
                        "description": "Experience how you can prove you're over 18 without revealing your exact age."
                    }
                }
            }
        ),
        LearningContent(
            id="content-3",
            title="Decentralized Identity Management",
            content_type="workshop",
            author="Dr. Jordan Patel",
            access_level="restricted",
            privacy_implications=[
                "Group participation tracking",
                "Progress assessment",
                "Workshop material access logs"
            ],
            content={
                "description": "A hands-on workshop exploring decentralized identity systems and self-sovereign identity principles.",
                "objectives": [
                    "Understand the core concepts of decentralized identity",
                    "Create and manage a simulated decentralized identifier (DID)",
                    "Learn how to issue and verify digital credentials"
                ],
                "sections": [
                    {
                        "title": "Understanding Decentralized Identity",
                        "content": """
                        Decentralized identity, also known as self-sovereign identity (SSI), is an approach to digital 
                        identity that gives individuals control over their own identifiers and credentials.
                        
                        Unlike traditional centralized systems where organizations issue and control your digital 
                        identities, decentralized identity puts you in control. You create and own your identifiers, 
                        and you decide when and with whom to share your credentials.
                        
                        Key components of decentralized identity include:
                        
                        * **Decentralized Identifiers (DIDs)**: Globally unique identifiers that don't require a 
                          central registration authority.
                          
                        * **Verifiable Credentials**: Tamper-evident credentials with authorship that can be 
                          cryptographically verified.
                          
                        * **Decentralized Identity Wallets**: Applications that help users manage their DIDs and 
                          credentials.
                        """
                    },
                    {
                        "title": "Workshop Activities",
                        "activities": [
                            {
                                "title": "Creating Your DID",
                                "description": "Learn how to generate a decentralized identifier and manage the associated keys.",
                                "duration_minutes": 25
                            },
                            {
                                "title": "Issuing Verifiable Credentials",
                                "description": "Practice issuing credentials as a trusted authority and adding them to a wallet.",
                                "duration_minutes": 35
                            },
                            {
                                "title": "Selective Disclosure",
                                "description": "Experience how to share only specific information from your credentials.",
                                "duration_minutes": 30
                            }
                        ]
                    },
                    {
                        "title": "Privacy Implications",
                        "content": """
                        Decentralized identity systems offer significant privacy advantages:
                        
                        * **Minimization**: Share only what's needed for each specific interaction.
                        
                        * **Control**: You decide what information to share, when, and with whom.
                        
                        * **Correlation Resistance**: Different DIDs for different relationships prevent tracking 
                          across contexts.
                          
                        * **Revocation**: Ability to revoke access to your information.
                        """
                    }
                ],
                "materials": [
                    {
                        "title": "Workshop Slides",
                        "file_type": "PDF",
                        "size_mb": 2.3
                    },
                    {
                        "title": "DID Creation Tool",
                        "file_type": "Software",
                        "size_mb": 15.7
                    },
                    {
                        "title": "Practice Exercises",
                        "file_type": "PDF",
                        "size_mb": 0.8
                    }
                ]
            }
        ),
        LearningContent(
            id="content-4",
            title="Data Privacy Regulations Around the World",
            content_type="lesson",
            author="Prof. Maria Gonzalez",
            access_level="public",
            privacy_implications=[
                "Basic browsing analytics",
                "Progress tracking"
            ],
            content={
                "description": "An overview of major data privacy regulations across different regions and their implications.",
                "objectives": [
                    "Understand key global privacy regulations",
                    "Compare different approaches to privacy protection",
                    "Learn about compliance requirements for organizations"
                ],
                "sections": [
                    {
                        "title": "European Union: GDPR",
                        "content": """
                        The General Data Protection Regulation (GDPR) is one of the world's strongest sets of data 
                        protection rules. Implemented in May 2018, it provides individuals in the EU with greater 
                        control over their personal data.
                        
                        Key provisions include:
                        
                        * **Right to Access**: Individuals can request access to their personal data.
                        
                        * **Right to Be Forgotten**: Individuals can request the deletion of their personal data.
                        
                        * **Data Portability**: Individuals can request their data in a common format to transfer 
                          to another service.
                          
                        * **Consent Requirements**: Clear, affirmative consent is required for data collection.
                        
                        * **Data Breach Notification**: Organizations must report certain types of breaches within 72 hours.
                        
                        * **Significant Penalties**: Fines can reach up to 4% of global annual revenue or €20 million, 
                          whichever is higher.
                        """
                    },
                    {
                        "title": "United States: Sectoral Approach",
                        "content": """
                        Unlike the EU, the US doesn't have a comprehensive federal privacy law. Instead, it has a 
                        patchwork of sectoral laws at both federal and state levels.
                        
                        Federal laws include:
                        
                        * **HIPAA**: Protects health information.
                        
                        * **FERPA**: Protects student education records.
                        
                        * **GLBA**: Covers financial information.
                        
                        * **COPPA**: Protects children's online privacy.
                        
                        State laws:
                        
                        * **California Consumer Privacy Act (CCPA)**: Gives California residents rights similar to GDPR.
                        
                        * **Virginia Consumer Data Protection Act (VCDPA)**: Provides rights for Virginia residents.
                        
                        * **Colorado Privacy Act**: Offers protection for Colorado residents.
                        """
                    },
                    {
                        "title": "Other Notable Regulations",
                        "content": """
                        * **Brazil's LGPD**: Similar to GDPR, implemented in 2020.
                        
                        * **China's PIPL**: Personal Information Protection Law, implemented in 2021.
                        
                        * **Canada's PIPEDA**: Personal Information Protection and Electronic Documents Act.
                        
                        * **Japan's APPI**: Act on the Protection of Personal Information.
                        
                        * **South Korea's PIPA**: Personal Information Protection Act.
                        
                        * **India's Proposed Data Protection Bill**: Currently under development.
                        """
                    }
                ],
                "assessment": {
                    "questions": [
                        {
                            "question": "Which regulation is considered one of the world's strongest sets of data protection rules?",
                            "options": [
                                "HIPAA",
                                "GDPR",
                                "CCPA",
                                "PIPA"
                            ],
                            "correct_answer": "GDPR"
                        },
                        {
                            "question": "What approach to privacy regulation does the United States primarily follow?",
                            "options": [
                                "Comprehensive federal approach",
                                "No privacy regulations",
                                "Sectoral approach with various laws for different industries",
                                "Voluntary guidelines only"
                            ],
                            "correct_answer": "Sectoral approach with various laws for different industries"
                        },
                        {
                            "question": "Under GDPR, what is the maximum potential fine for serious violations?",
                            "options": [
                                "€1 million",
                                "€5 million",
                                "4% of global annual revenue or €20 million, whichever is higher",
                                "10% of European revenue only"
                            ],
                            "correct_answer": "4% of global annual revenue or €20 million, whichever is higher"
                        }
                    ]
                }
            }
        ),
        LearningContent(
            id="content-5",
            title="Ethical Data Use in Education",
            content_type="discussion",
            author="Community",
            access_level="enrolled",
            privacy_implications=[
                "Discussion participation tracking",
                "User contributions are visible to the class",
                "Profile information visible to participants"
            ],
            content={
                "description": "A moderated discussion about ethical considerations in educational data use.",
                "objectives": [
                    "Engage in thoughtful discussion about ethical data practices",
                    "Consider different perspectives on student data privacy",
                    "Develop a personal ethical framework for educational data"
                ],
                "discussion_topics": [
                    {
                        "title": "Student Data Collection",
                        "prompt": """
                        Educational institutions collect vast amounts of data about students, from academic 
                        performance to behavioral patterns and even social interactions.
                        
                        * What types of student data do you think are appropriate for schools to collect?
                        * What types raise ethical concerns?
                        * How should schools balance personalized learning benefits with privacy protections?
                        """
                    },
                    {
                        "title": "Parental Rights vs. Student Autonomy",
                        "prompt": """
                        As students grow older, questions arise about who should control access to their 
                        educational data.
                        
                        * At what age should students gain more control over their educational data?
                        * What rights should parents retain regardless of student age?
                        * How can we respect both parental oversight and student privacy?
                        """
                    },
                    {
                        "title": "AI and Predictive Analytics",
                        "prompt": """
                        Educational institutions increasingly use AI systems to predict student outcomes, 
                        identify at-risk students, and personalize learning.
                        
                        * What are the benefits and risks of predictive analytics in education?
                        * Could these systems reinforce biases or create self-fulfilling prophecies?
                        * What safeguards should be in place for algorithmic decision-making in education?
                        """
                    }
                ],
                "guidelines": [
                    "Respect diverse viewpoints and experiences",
                    "Support claims with evidence when possible",
                    "Stay on topic and contribute constructively",
                    "Consider implications for different stakeholders",
                    "Be mindful of privacy when sharing personal experiences"
                ]
            }
        )
    ]


def get_sample_classes() -> List[Dict[str, Any]]:
    """Get sample class data."""
    return [
        {
            "id": "class-1",
            "name": "Introduction to Cybersecurity",
            "instructor": "Prof. Alex Rivera",
            "students": 28,
            "privacy_level": "enhanced",
            "data_collection": "minimal"
        },
        {
            "id": "class-2",
            "name": "Data Ethics and Privacy",
            "instructor": "Dr. Samantha Chen",
            "students": 22,
            "privacy_level": "maximum",
            "data_collection": "consent_based"
        },
        {
            "id": "class-3",
            "name": "Digital Citizenship",
            "instructor": "Prof. Jordan Patel",
            "students": 35,
            "privacy_level": "standard",
            "data_collection": "standard"
        }
    ]


def get_sample_activity_data() -> List[Dict[str, Any]]:
    """Get sample user activity data."""
    return [
        {
            "timestamp": "2023-04-10 09:15:22",
            "activity_type": "content_access",
            "details": "Accessed 'Introduction to Digital Privacy'",
            "privacy_impact": "low",
            "data_shared": ["progress_tracking"]
        },
        {
            "timestamp": "2023-04-10 10:32:47",
            "activity_type": "assessment_completion",
            "details": "Completed quiz on 'Introduction to Digital Privacy'",
            "privacy_impact": "medium",
            "data_shared": ["assessment_results", "time_spent", "answers"]
        },
        {
            "timestamp": "2023-04-11 14:20:33",
            "activity_type": "discussion_participation",
            "details": "Posted in 'Ethical Data Use in Education' discussion",
            "privacy_impact": "high",
            "data_shared": ["user_content", "profile_info", "participation_time"]
        },
        {
            "timestamp": "2023-04-12 11:05:18",
            "activity_type": "content_access",
            "details": "Accessed 'Zero-Knowledge Authentication'",
            "privacy_impact": "low",
            "data_shared": ["progress_tracking"]
        },
        {
            "timestamp": "2023-04-12 16:45:02",
            "activity_type": "simulation_interaction",
            "details": "Completed 'Zero-Knowledge Authentication' interactive demo",
            "privacy_impact": "medium",
            "data_shared": ["interaction_patterns", "completion_status"]
        }
    ]


def calculate_privacy_score(settings: PrivacySettings) -> float:
    """Calculate a privacy score based on settings."""
    score = 0
    
    # Data sharing level (0-30 points)
    if settings.data_sharing_level == "minimal":
        score += 30
    elif settings.data_sharing_level == "standard":
        score += 15
    else:  # "full"
        score += 5
    
    # Anonymized mode (0-15 points)
    if settings.anonymized_mode:
        score += 15
    
    # Private browsing (0-10 points)
    if settings.private_browsing:
        score += 10
    
    # Content access settings (0-20 points)
    restricted_settings = ["self_only", "educators_only"]
    restricted_count = sum(1 for setting in settings.content_access_settings.values() if setting in restricted_settings)
    score += (restricted_count / len(settings.content_access_settings)) * 20
    
    # Third party consent (0-15 points)
    consent_denied = sum(1 for consent in settings.third_party_consent.values() if not consent)
    score += (consent_denied / len(settings.third_party_consent)) * 15
    
    # Encryption level (0-10 points)
    if settings.encryption_level == "maximum":
        score += 10
    elif settings.encryption_level == "enhanced":
        score += 5
    else:  # "standard"
        score += 2
    
    return score


def update_metrics_from_settings(settings: PrivacySettings, metrics: PrivacyMetrics):
    """Update privacy metrics based on privacy settings."""
    # Calculate new privacy score
    new_score = calculate_privacy_score(settings)
    metrics.privacy_score = new_score
    
    # Calculate data points protected
    data_points = 60  # total potential data points
    if settings.data_sharing_level == "minimal":
        protected = data_points * 0.8
    elif settings.data_sharing_level == "standard":
        protected = data_points * 0.6
    else:  # "full"
        protected = data_points * 0.3
    
    # Adjust for other settings
    if settings.anonymized_mode:
        protected += 10
    if settings.private_browsing:
        protected += 5
    
    metrics.data_points_protected = int(protected)
    
    # Count consent decisions
    metrics.consent_decisions = len(settings.third_party_consent)
    
    # Determine identity protection level
    if settings.anonymized_mode and settings.data_sharing_level == "minimal" and settings.encryption_level == "maximum":
        metrics.identity_protection_level = "high"
    elif settings.data_sharing_level != "full" and (settings.anonymized_mode or settings.encryption_level != "standard"):
        metrics.identity_protection_level = "medium"
    else:
        metrics.identity_protection_level = "low"
    
    # Update session state
    st.session_state.prived_privacy_metrics = metrics


def update_settings_and_metrics():
    """Update settings and metrics in session state."""
    settings = get_sample_privacy_settings()
    metrics = get_sample_privacy_metrics()
    update_metrics_from_settings(settings, metrics)


# ------ UI Components ------

def run_prived_header():
    """Display the header for PrivEd Protocol module."""
    st.markdown(
        """
        <div style="background-color:#2E3A5C; padding:10px; border-radius:10px; margin-bottom:10px">
            <h1 style="color:white; text-align:center">
                <span style="font-size:1.5em">🔐</span> PrivEd Protocol <span style="font-size:1.5em">🔐</span>
            </h1>
            <h3 style="color:#A3BFFA; text-align:center">Privacy-by-Design Learning Platform</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_privacy_indicator(score: float, size: str = "large"):
    """Render a privacy score indicator."""
    # Determine color based on score
    if score >= 80:
        color = "#48BB78"  # Green
        level = "High"
    elif score >= 60:
        color = "#ECC94B"  # Yellow
        level = "Medium"
    else:
        color = "#F56565"  # Red
        level = "Low"
    
    # Different sizes
    if size == "large":
        outer_size = "130px"
        inner_size = "110px"
        font_size = "24px"
        margin = "20px auto"
    else:  # "small"
        outer_size = "80px"
        inner_size = "70px"
        font_size = "16px"
        margin = "10px auto"
    
    st.markdown(
        f"""
        <div style="width:{outer_size}; height:{outer_size}; border-radius:50%; background:conic-gradient({color} {score}%, #E2E8F0 0); 
             display:flex; align-items:center; justify-content:center; margin:{margin};">
            <div style="width:{inner_size}; height:{inner_size}; border-radius:50%; background:#1A202C; 
                 display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div style="color:{color}; font-size:{font_size}; font-weight:bold;">{score:.0f}%</div>
                <div style="color:white; font-size:14px;">Protection</div>
            </div>
        </div>
        <div style="text-align:center; font-weight:bold; color:{color};">{level} Privacy</div>
        """,
        unsafe_allow_html=True
    )


def render_encrypted_text(text: str, fully_encrypted: bool = False):
    """Render text with encryption visualization."""
    if fully_encrypted:
        # Replace all characters with symbols
        encrypted = ''.join(['*' for _ in text])
        st.markdown(
            f"""
            <div style="font-family:monospace; padding:10px; background-color:#1A202C; color:#A3BFFA; 
                 border-radius:5px; position:relative;">
                {encrypted}
                <div style="position:absolute; top:50%; right:10px; transform:translateY(-50%);">
                    🔒
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Partially encrypt text (show some characters)
        encrypted = []
        for i, char in enumerate(text):
            if i % 3 == 0 and char != ' ':
                encrypted.append(char)
            else:
                encrypted.append('*')
        
        encrypted_text = ''.join(encrypted)
        st.markdown(
            f"""
            <div style="font-family:monospace; padding:10px; background-color:#1A202C; color:#A3BFFA; 
                 border-radius:5px; position:relative;">
                {encrypted_text}
                <div style="position:absolute; top:50%; right:10px; transform:translateY(-50%);">
                    🔓
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_data_point(label: str, value: str, show_actual: bool = True, sensitive: bool = False):
    """Render a data point with optional encryption."""
    if sensitive and not show_actual:
        # Show encrypted version
        st.markdown(
            f"""
            <div style="margin-bottom:10px;">
                <div style="font-weight:bold;">{label}</div>
                <div style="font-family:monospace; padding:5px; background-color:#1A202C; color:#A3BFFA; 
                     border-radius:3px;">
                    {'*' * len(value)} 🔒
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Show actual value
        st.markdown(
            f"""
            <div style="margin-bottom:10px;">
                <div style="font-weight:bold;">{label}</div>
                <div style="font-family:monospace; padding:5px; background-color:#2D3748; color:#FFFFFF; 
                     border-radius:3px;">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_consent_toggle(title: str, description: str, key: str, default: bool = True):
    """Render a styled consent toggle with explanation."""
    st.markdown(
        f"""
        <div style="margin-bottom:15px; padding:10px; background-color:#2D3748; border-radius:5px;">
            <div style="font-weight:bold; margin-bottom:5px;">{title}</div>
            <div style="font-size:0.9em; margin-bottom:10px; color:#A0AEC0;">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    return st.toggle("Allow", value=default, key=key)


# ------ Main Application Sections ------

def display_dashboard(settings: PrivacySettings, metrics: PrivacyMetrics):
    """Display the privacy dashboard."""
    st.subheader("📊 Your Privacy Dashboard")
    
    # Main metrics in two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Privacy score
        render_privacy_indicator(metrics.privacy_score)
    
    with col2:
        # Key privacy metrics
        st.markdown("### Privacy Metrics")
        
        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric("Data Points Protected", metrics.data_points_protected)
        with met2:
            st.metric("Consent Decisions Made", metrics.consent_decisions)
        with met3:
            st.metric("Identity Protection", metrics.identity_protection_level.capitalize())
    
    # Identity & Encryption Status
    st.markdown("### Your Identity Status")
    
    id_status = "Anonymous" if settings.anonymized_mode else "Identified"
    id_icon = "🔍" if settings.anonymized_mode else "👤"
    
    enc_level_desc = {
        "standard": "Basic encryption for data in transit",
        "enhanced": "Full encryption for all data with secured keys",
        "maximum": "Zero-knowledge encryption with client-side key management"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="padding:15px; background-color:#2D3748; border-radius:5px; height:100%;">
                <div style="font-size:1.2em; margin-bottom:10px;">Identity Mode: <span style="color:{
                    '#48BB78' if settings.anonymized_mode else '#F56565'
                };">{id_status} {id_icon}</span></div>
                <div>Your identity is currently <strong>{
                    'hidden from other users and instructors' if settings.anonymized_mode 
                    else 'visible to authorized users according to your access settings'
                }</strong>.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="padding:15px; background-color:#2D3748; border-radius:5px; height:100%;">
                <div style="font-size:1.2em; margin-bottom:10px;">Encryption Level: <span style="color:{
                    '#48BB78' if settings.encryption_level == 'maximum' 
                    else '#ECC94B' if settings.encryption_level == 'enhanced'
                    else '#F56565'
                };">{settings.encryption_level.capitalize()} {'🔒' * (
                    3 if settings.encryption_level == 'maximum'
                    else 2 if settings.encryption_level == 'enhanced'
                    else 1
                )}</span></div>
                <div>{enc_level_desc[settings.encryption_level]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Recent Activity with Privacy Impact
    st.markdown("### Recent Activity & Data Sharing")
    
    activities = get_sample_activity_data()
    
    for activity in activities[:3]:  # Show most recent 3 activities
        impact_color = {
            "low": "#48BB78",
            "medium": "#ECC94B",
            "high": "#F56565"
        }[activity["privacy_impact"]]
        
        st.markdown(
            f"""
            <div style="padding:10px; background-color:#2D3748; border-radius:5px; margin-bottom:10px; 
                 border-left:4px solid {impact_color};">
                <div style="display:flex; justify-content:space-between;">
                    <div><strong>{activity["details"]}</strong></div>
                    <div>{activity["timestamp"]}</div>
                </div>
                <div style="margin-top:5px; font-size:0.9em;">
                    Privacy Impact: <span style="color:{impact_color};">{activity["privacy_impact"].capitalize()}</span>
                </div>
                <div style="margin-top:5px; font-size:0.9em;">
                    Data Shared: {", ".join(activity["data_shared"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Data sharing and consent summary
    st.markdown("### Data Sharing & Third-Party Consent")
    
    consent_summary = []
    for service, allowed in settings.third_party_consent.items():
        status = "Allowed" if allowed else "Blocked"
        color = "#F56565" if allowed else "#48BB78"
        icon = "✅" if not allowed else "⚠️"
        
        consent_summary.append(
            f"""
            <div style="display:flex; justify-content:space-between; padding:8px; border-bottom:1px solid #4A5568;">
                <div>{service.replace('_', ' ').title()}</div>
                <div style="color:{color};">{icon} {status}</div>
            </div>
            """
        )
    
    sharing_level_desc = {
        "minimal": "Only essential data required for core functionality is collected",
        "standard": "Basic analytics and progress data is collected for educational purposes",
        "full": "Comprehensive data collection for personalized learning experiences"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="padding:15px; background-color:#2D3748; border-radius:5px;">
                <div style="font-size:1.2em; margin-bottom:10px;">Data Sharing Level: <span style="color:{
                    '#48BB78' if settings.data_sharing_level == 'minimal'
                    else '#ECC94B' if settings.data_sharing_level == 'standard'
                    else '#F56565'
                };">{settings.data_sharing_level.capitalize()}</span></div>
                <div>{sharing_level_desc[settings.data_sharing_level]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="padding:15px; background-color:#2D3748; border-radius:5px;">
                <div style="font-size:1.2em; margin-bottom:10px;">Third-Party Consent Summary</div>
                {"".join(consent_summary)}
            </div>
            """,
            unsafe_allow_html=True
        )


def display_privacy_settings(settings: PrivacySettings, metrics: PrivacyMetrics):
    """Display and manage privacy settings."""
    st.subheader("⚙️ Privacy Settings")
    
    st.write("""
    Control how your data is collected, stored, and shared within the PrivEd Protocol platform.
    These settings affect your privacy level and determine what information is visible to others.
    """)
    
    # Create tabs for different setting categories
    tab1, tab2, tab3, tab4 = st.tabs([
        "General Privacy", 
        "Data Sharing", 
        "Identity & Encryption",
        "Third-Party Consent"
    ])
    
    with tab1:
        st.subheader("General Privacy Settings")
        
        st.markdown("### Data Collection Level")
        
        # Data sharing level
        data_sharing_level = st.radio(
            "Select your data sharing level:",
            ["minimal", "standard", "full"],
            format_func=lambda x: {
                "minimal": "Minimal - Essential functionality only",
                "standard": "Standard - Basic analytics and progress tracking",
                "full": "Full - Comprehensive data for personalized learning"
            }[x],
            index=["minimal", "standard", "full"].index(settings.data_sharing_level)
        )
        
        # Show explanation based on selection
        if data_sharing_level == "minimal":
            st.info("""
            **Minimal Data Collection**
            
            Only essential data required for the platform to function will be collected:
            - Authentication information
            - Course enrollment status
            - Assignment submissions
            
            No analytics, interaction data, or behavioral patterns will be tracked.
            
            Note: This may limit personalization features and instructor insights.
            """)
        elif data_sharing_level == "standard":
            st.info("""
            **Standard Data Collection**
            
            In addition to essential data, basic analytics are collected:
            - Time spent on content
            - Resource access patterns
            - Assessment performance
            - Basic interaction metrics
            
            This data helps improve your learning experience while maintaining reasonable privacy.
            """)
        else:  # "full"
            st.warning("""
            **Full Data Collection**
            
            Comprehensive data collection for maximum personalization:
            - Detailed interaction patterns
            - Learning behavior analytics
            - Content preference analysis
            - Predictive performance modeling
            - Cross-platform activity correlation (when available)
            
            This provides the most personalized experience but has the highest privacy impact.
            """)
        
        # Private browsing mode
        st.markdown("### Session Privacy")
        
        private_browsing = st.toggle(
            "Enable Private Browsing Mode",
            value=settings.private_browsing
        )
        
        if private_browsing:
            st.info("""
            **Private Browsing Enabled**
            
            When enabled:
            - Session data will not be stored after logout
            - Your activity won't be linked to your long-term profile
            - Progress tracking may be limited
            - Personalization features will be reduced
            """)
        else:
            st.info("""
            **Standard Browsing Mode**
            
            Your session data will be recorded and associated with your account for:
            - Tracking progress over time
            - Providing personalized recommendations
            - Analyzing your learning patterns
            """)
    
    with tab2:
        st.subheader("Data Sharing Settings")
        
        st.write("""
        Control what information about you is visible to others on the platform.
        These settings determine who can see different aspects of your activity and profile.
        """)
        
        # Content access settings
        access_settings = {}
        
        st.markdown("### Content Access Settings")
        
        visibility_options = {
            "self_only": "Only Me",
            "educators_only": "Educators Only",
            "class_members": "Class Members",
            "public": "Public"
        }
        
        # Personal information visibility
        access_settings["personal_information"] = st.selectbox(
            "Who can see your personal information?",
            list(visibility_options.keys()),
            format_func=lambda x: visibility_options[x],
            index=list(visibility_options.keys()).index(
                settings.content_access_settings.get("personal_information", "educators_only")
            )
        )
        
        # Assignments visibility
        access_settings["assignments"] = st.selectbox(
            "Who can see your assignments and submissions?",
            list(visibility_options.keys()),
            format_func=lambda x: visibility_options[x],
            index=list(visibility_options.keys()).index(
                settings.content_access_settings.get("assignments", "class_members")
            )
        )
        
        # Discussions visibility
        access_settings["discussions"] = st.selectbox(
            "Who can see your discussion contributions?",
            list(visibility_options.keys()),
            format_func=lambda x: visibility_options[x],
            index=list(visibility_options.keys()).index(
                settings.content_access_settings.get("discussions", "class_members")
            )
        )
        
        # Activity logs visibility
        access_settings["activity_logs"] = st.selectbox(
            "Who can see your activity logs and learning behavior?",
            list(visibility_options.keys()),
            format_func=lambda x: visibility_options[x],
            index=list(visibility_options.keys()).index(
                settings.content_access_settings.get("activity_logs", "educators_only")
            )
        )
    
    with tab3:
        st.subheader("Identity & Encryption Settings")
        
        # Anonymized mode
        st.markdown("### Identity Management")
        
        anonymized_mode = st.toggle(
            "Enable Anonymized Mode",
            value=settings.anonymized_mode
        )
        
        if anonymized_mode:
            st.success("""
            **Anonymized Mode Enabled**
            
            When enabled:
            - Your real identity is hidden from other users
            - You'll be identified by a pseudonym in discussions and group activities
            - Instructors can still verify your submissions for grading
            - Your true identity is protected through zero-knowledge verification
            """)
            
            # Display pseudonym if anonymized mode is enabled
            pseudonym = hashlib.sha256(settings.user_id.encode()).hexdigest()[:8]
            st.markdown(f"""
            **Your Pseudonym**: Student_{pseudonym}
            
            This is how others will see you in the platform.
            """)
        else:
            st.info("""
            **Standard Identity Mode**
            
            Your real identity will be visible to others according to your visibility settings.
            This facilitates easier collaboration and communication with peers and instructors.
            """)
        
        # Encryption level
        st.markdown("### Encryption Settings")
        
        encryption_level = st.radio(
            "Select encryption level:",
            ["standard", "enhanced", "maximum"],
            format_func=lambda x: {
                "standard": "Standard - Basic encryption for data in transit",
                "enhanced": "Enhanced - Full encryption for all data storage and transmission",
                "maximum": "Maximum - Zero-knowledge encryption with client-side key management"
            }[x],
            index=["standard", "enhanced", "maximum"].index(settings.encryption_level)
        )
        
        # Show explanation based on selection
        if encryption_level == "standard":
            st.info("""
            **Standard Encryption**
            
            Basic encryption that protects:
            - Login credentials
            - Data during transmission
            
            Data is stored in an encrypted database but is accessible to the system for analysis and features.
            """)
        elif encryption_level == "enhanced":
            st.info("""
            **Enhanced Encryption**
            
            Comprehensive encryption that protects:
            - All personal data
            - All user-generated content
            - Communication between users
            - Data during storage and transmission
            
            Some system features may require limited access to decrypted data.
            """)
        else:  # "maximum"
            st.success("""
            **Maximum Encryption (Zero-Knowledge)**
            
            The strongest protection available:
            - End-to-end encryption for all data
            - Client-side key management
            - Zero-knowledge architecture where even the platform cannot access your unencrypted data
            - Mathematical proofs for authentication without revealing actual credentials
            
            Some platform features like content recommendations may be limited or unavailable.
            """)
        
        # Show encryption visual demo
        with st.expander("See encryption visualization"):
            st.markdown("### Sample Data with Selected Encryption")
            
            # Sample data to show with different encryption levels
            sample_data = {
                "Personal Information": "Jane Doe, 22, Computer Science Major",
                "Assignment Response": "The principles of zero-knowledge proofs rely on mathematical verification without revealing the underlying information.",
                "Discussion Comment": "I think the GDPR's provisions for data portability are essential for maintaining user control over personal information."
            }
            
            # Display data based on encryption level
            for label, text in sample_data.items():
                st.markdown(f"**{label}:**")
                if encryption_level == "standard":
                    render_encrypted_text(text, fully_encrypted=False)
                elif encryption_level == "enhanced":
                    render_encrypted_text(text, fully_encrypted=True)
                else:  # "maximum"
                    st.markdown("""
                    ```
                    [Client-encrypted data with zero-knowledge proof]
                    Only the intended recipient with proper keys can access this information.
                    ```
                    """)
                st.markdown("---")
    
    with tab4:
        st.subheader("Third-Party Consent Settings")
        
        st.write("""
        Control what data is shared with third-party services integrated with the platform.
        You can revoke consent at any time, but this may limit certain features.
        """)
        
        # Third-party consent toggles
        consent_settings = {}
        
        consent_settings["analytics"] = render_consent_toggle(
            "Analytics Services",
            "Allow the platform to share anonymized usage data with analytics providers to improve the learning experience.",
            "consent_analytics",
            default=settings.third_party_consent.get("analytics", True)
        )
        
        consent_settings["content_providers"] = render_consent_toggle(
            "External Content Providers",
            "Allow access to third-party educational content providers, which may track your interactions with their content.",
            "consent_content",
            default=settings.third_party_consent.get("content_providers", True)
        )
        
        consent_settings["research"] = render_consent_toggle(
            "Educational Research",
            "Allow anonymized data to be used for educational research to improve teaching methodologies and learning outcomes.",
            "consent_research",
            default=settings.third_party_consent.get("research", False)
        )
        
        consent_settings["ai_tools"] = render_consent_toggle(
            "AI Learning Tools",
            "Allow AI-powered tools to analyze your learning patterns to provide personalized recommendations and assistance.",
            "consent_ai",
            default=settings.third_party_consent.get("ai_tools", False)
        )
    
    # Save button for all settings
    st.markdown("---")
    save_col1, save_col2 = st.columns([3, 1])
    with save_col2:
        save_settings = st.button("Save Settings", type="primary")
    
    if save_settings:
        # Update settings in session state
        settings.data_sharing_level = data_sharing_level
        settings.private_browsing = private_browsing
        settings.content_access_settings = access_settings
        settings.anonymized_mode = anonymized_mode
        settings.encryption_level = encryption_level
        settings.third_party_consent = consent_settings
        
        # Update metrics based on new settings
        update_metrics_from_settings(settings, metrics)
        
        st.success("Privacy settings saved successfully!")
        
        # Show new privacy score
        st.metric("New Privacy Score", f"{metrics.privacy_score:.1f}%", 
                 delta=f"{metrics.privacy_score - calculate_privacy_score(get_sample_privacy_settings()):.1f}")
        
        # Update session state
        st.session_state.prived_privacy_settings = settings
        st.session_state.prived_privacy_metrics = metrics
        
        # Prompt to reload dashboard
        st.info("Return to dashboard to see your updated privacy status.")


def display_learning_content_browser():
    """Display the learning content browser with privacy controls."""
    st.subheader("📚 Learning Content")
    
    # Get learning content
    all_content = get_sample_learning_content()
    settings = get_sample_privacy_settings()
    
    # Filter content based on access level
    if settings.data_sharing_level == "minimal":
        visible_content = [c for c in all_content if c.access_level != "restricted"]
    else:
        visible_content = all_content
    
    # Display content
    selected_type = st.radio(
        "Filter by type:",
        ["All"] + list(set(c.content_type for c in visible_content)),
        horizontal=True
    )
    
    # Apply filters
    if selected_type != "All":
        filtered_content = [c for c in visible_content if c.content_type == selected_type]
    else:
        filtered_content = visible_content
    
    # Create content cards
    for content in filtered_content:
        with st.container():
            st.markdown(
                f"""
                <div style="padding:15px; background-color:#2D3748; border-radius:5px; margin-bottom:15px;">
                    <div style="display:flex; justify-content:space-between;">
                        <div style="font-size:1.2em; font-weight:bold;">{content.title}</div>
                        <div style="background-color:#4A5568; padding:2px 8px; border-radius:12px; font-size:0.8em;">
                            {content.content_type.replace('_', ' ').title()}
                        </div>
                    </div>
                    <div style="font-size:0.9em; margin-top:5px; margin-bottom:10px;">
                        By: {content.author}
                    </div>
                    <div style="margin-bottom:10px;">{content.content['description']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Privacy implications and open button
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write("**Privacy implications:**")
                for implication in content.privacy_implications:
                    st.markdown(f"- {implication}")
            
            with col2:
                # Open button
                open_button = st.button("Open Content", key=f"open_{content.id}")
                if open_button:
                    st.session_state.active_content = content
                    st.rerun()


def display_learning_content(content: LearningContent, settings: PrivacySettings):
    """Display specific learning content with privacy controls."""
    st.subheader(content.title)
    
    # Content metadata
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(f"Author: {content.author}")
    with col2:
        st.write(f"Type: {content.content_type.replace('_', ' ').title()}")
    with col3:
        if settings.anonymized_mode:
            st.write(f"Viewing as: Anonymous")
        else:
            st.write(f"Viewing as: Student")
    
    # Privacy consent
    with st.expander("Privacy Implications", expanded=True):
        st.write("**This content has the following privacy implications:**")
        for implication in content.privacy_implications:
            st.write(f"- {implication}")
        
        consent = st.checkbox("I understand and consent to the privacy implications", value=True)
    
    # Only show content if user consents
    if consent:
        # Different rendering based on content type
        if content.content_type == "lesson":
            display_lesson_content(content)
        elif content.content_type == "interactive_demo":
            display_interactive_demo(content)
        elif content.content_type == "workshop":
            display_workshop_content(content)
        elif content.content_type == "discussion":
            display_discussion_content(content, settings)
    else:
        st.warning("You must consent to the privacy implications to view this content.")
    
    # Back button
    back_button = st.button("Back to Content List")
    if back_button:
        if hasattr(st.session_state, 'active_content'):
            del st.session_state.active_content
        st.rerun()


def display_lesson_content(content: LearningContent):
    """Display lesson content."""
    # Objectives
    st.subheader("Learning Objectives")
    for objective in content.content["objectives"]:
        st.markdown(f"- {objective}")
    
    # Sections
    for section in content.content["sections"]:
        st.subheader(section["title"])
        st.markdown(section["content"])
    
    # Assessment if available
    if "assessment" in content.content:
        st.subheader("Knowledge Check")
        
        if "assessment_state" not in st.session_state:
            st.session_state.assessment_state = {
                "current_question": 0,
                "answers": [],
                "score": 0,
                "completed": False
            }
        
        state = st.session_state.assessment_state
        questions = content.content["assessment"]["questions"]
        
        # Display current question if not completed
        if not state["completed"]:
            if state["current_question"] < len(questions):
                question = questions[state["current_question"]]
                
                st.write(f"**Question {state['current_question'] + 1}:** {question['question']}")
                
                answer = st.radio(
                    "Select your answer:",
                    question["options"],
                    key=f"q_{state['current_question']}"
                )
                
                submit = st.button("Submit Answer")
                
                if submit:
                    # Check if answer is correct
                    correct = answer == question["correct_answer"]
                    
                    # Store answer and update score
                    state["answers"].append({
                        "question": question["question"],
                        "user_answer": answer,
                        "correct_answer": question["correct_answer"],
                        "is_correct": correct
                    })
                    
                    if correct:
                        state["score"] += 1
                    
                    # Move to next question
                    state["current_question"] += 1
                    
                    # Mark as completed if all questions answered
                    if state["current_question"] >= len(questions):
                        state["completed"] = True
                    
                    st.rerun()
            else:
                state["completed"] = True
                st.rerun()
        
        # Show results if completed
        if state["completed"]:
            score_percent = (state["score"] / len(questions)) * 100
            
            # Show overall score
            if score_percent >= 80:
                st.success(f"Great job! You scored {score_percent:.1f}%")
                st.balloons()
            elif score_percent >= 60:
                st.warning(f"Good attempt! You scored {score_percent:.1f}%")
            else:
                st.error(f"You need more practice. You scored {score_percent:.1f}%")
            
            # Display question results
            st.subheader("Question Results:")
            for i, answer in enumerate(state["answers"]):
                if answer["is_correct"]:
                    st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                    st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
                else:
                    st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                    st.markdown(f"Your answer: {answer['user_answer']}")
                    st.markdown(f"Correct answer: {answer['correct_answer']}")
                st.markdown("---")
            
            # Reset button
            reset = st.button("Retake Assessment")
            if reset:
                if "assessment_state" in st.session_state:
                    del st.session_state.assessment_state
                st.rerun()


def display_interactive_demo(content: LearningContent):
    """Display interactive demo content."""
    # Initialize demo state if not existing
    if "demo_state" not in st.session_state:
        st.session_state.demo_state = {
            "current_stage": 0,
            "completed_stages": [],
            "simulation_data": {},
            "completed": False
        }
    
    state = st.session_state.demo_state
    stages = content.content["stages"]
    
    # Objectives
    st.subheader("Learning Objectives")
    for objective in content.content["objectives"]:
        st.markdown(f"- {objective}")
    
    # Progress indicator
    progress = (len(state["completed_stages"]) / len(stages)) * 100
    st.progress(progress / 100)
    st.write(f"Progress: {progress:.0f}%")
    
    # Display current stage
    current_stage = state["current_stage"]
    if current_stage < len(stages):
        stage = stages[current_stage]
        
        st.subheader(stage["title"])
        
        # Different rendering based on stage type
        if stage.get("type") == "simulation":
            # Simulation content
            st.markdown(stage["content"] if "content" in stage else "")
            
            # Get simulation data
            simulation_data = stage.get("simulation_data", {})
            
            # Zero-knowledge authentication simulation
            if "Zero-Knowledge Authentication" in content.title:
                with st.expander("Interactive Zero-Knowledge Authentication Demo", expanded=True):
                    st.markdown("""
                    This demonstration shows how zero-knowledge authentication works. 
                    Enter a password below, and we'll show how the system verifies it without ever storing or transmitting the actual password.
                    """)
                    
                    password = st.text_input("Enter a password to test:", type="password")
                    
                    if password:
                        # Calculate hash (in a real ZK system, this would be more complex)
                        password_hash = hashlib.sha1(password.encode()).hexdigest()
                        
                        st.write("### Authentication Process")
                        
                        # Show the steps with a delay to simulate processing
                        steps_container = st.container()
                        
                        with steps_container:
                            st.write("1. Password received by client...")
                            time.sleep(0.5)
                            
                            st.write("2. Generating cryptographic proof...")
                            time.sleep(0.5)
                            
                            # Show hash comparison
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("Your password hash:")
                                st.code(password_hash)
                            
                            with col2:
                                # For demo purposes, show success for the preset password or for any password with length > 10
                                reference_hash = simulation_data["hashed_value"]
                                st.write("Stored hash reference:")
                                st.code(reference_hash)
                            
                            time.sleep(0.5)
                            st.write("3. Verifying proof against stored reference...")
                            time.sleep(0.5)
                            
                            # Authentication result (for demo purposes)
                            if password == simulation_data["secret_value"] or len(password) > 10:
                                st.success("Authentication successful! User verified.")
                                st.balloons()
                                
                                # Add to completed stages if not already done
                                if current_stage not in state["completed_stages"]:
                                    state["completed_stages"].append(current_stage)
                                
                                # Show next button
                                next_stage = st.button("Continue to Next Stage")
                                if next_stage:
                                    state["current_stage"] += 1
                                    st.rerun()
                            else:
                                st.error("Authentication failed. Try again or use a password longer than 10 characters.")
                    
                    # Show explanation of what happened
                    st.write("### What just happened?")
                    st.write("""
                    1. Your password was never sent to the server in its original form
                    2. Only a mathematical proof derived from your password was used
                    3. The server could verify your identity without ever knowing your password
                    4. This is the essence of zero-knowledge authentication
                    """)
            
            # Other simulation types could be added here
        else:
            # Standard content
            st.markdown(stage["content"])
            
            # Add to completed stages if not already done
            if current_stage not in state["completed_stages"]:
                state["completed_stages"].append(current_stage)
            
            # Show next button
            next_stage = st.button("Continue to Next Stage")
            if next_stage:
                state["current_stage"] += 1
                st.rerun()
    
    # All stages completed
    if len(state["completed_stages"]) == len(stages):
        if not state["completed"]:
            state["completed"] = True
            st.success("You've completed all stages of this interactive demo!")
            st.balloons()
    
    # Interactive elements if available
    if "interactive_elements" in content.content and state["completed"]:
        st.subheader("Additional Interactive Elements")
        
        for element_key, element in content.content["interactive_elements"].items():
            st.write(f"**{element_key.replace('_', ' ').title()}**: {element['description']}")
            
            # Add interactive elements here based on type
            if element["type"] == "simulation" and "age_verification_demo" in element_key:
                with st.expander("Age Verification without Revealing Birth Date", expanded=False):
                    st.write("""
                    This demo shows how zero-knowledge proofs can be used to verify someone is over 18 
                    without revealing their exact age or birth date.
                    """)
                    
                    # Simple age verification demo
                    birth_year = st.number_input("Enter your birth year (will not be stored):", 
                                                min_value=1900, max_value=2023, value=2000)
                    
                    verify = st.button("Verify Age")
                    
                    if verify:
                        current_year = datetime.datetime.now().year
                        age = current_year - birth_year
                        
                        st.write("### Zero-Knowledge Age Verification")
                        
                        # Show verification steps
                        st.write("1. Birth year received by client application...")
                        time.sleep(0.5)
                        
                        st.write("2. Converting to age and generating proof...")
                        time.sleep(0.5)
                        
                        st.write("3. Constructing mathematical proof that age ≥ 18 without revealing actual age...")
                        time.sleep(0.5)
                        
                        # Result
                        if age >= 18:
                            st.success(f"✅ Proof verified: Person is over 18 (actual age not transmitted)")
                        else:
                            st.error(f"❌ Proof verification failed: Person is not over 18")
                        
                        st.info("""
                        **Note:** In a real zero-knowledge system, neither the birth year nor the calculated age 
                        would be sent to the server. Only a mathematical proof that the age meets the criteria
                        would be generated and verified.
                        """)


def display_workshop_content(content: LearningContent):
    """Display workshop content."""
    # Objectives
    st.subheader("Workshop Objectives")
    for objective in content.content["objectives"]:
        st.markdown(f"- {objective}")
    
    # Sections
    for section in content.content["sections"]:
        st.subheader(section["title"])
        
        if "content" in section:
            st.markdown(section["content"])
        
        if "activities" in section:
            st.write("### Workshop Activities")
            
            for activity in section["activities"]:
                with st.expander(f"{activity['title']} ({activity['duration_minutes']} minutes)"):
                    st.write(activity["description"])
                    
                    # Add simulated activity content
                    if "Creating Your DID" in activity["title"]:
                        st.write("#### Decentralized Identifier (DID) Creation")
                        
                        # Create a simulated DID
                        did_method = st.selectbox(
                            "Select a DID method:",
                            ["did:key", "did:web", "did:ethr", "did:sol"]
                        )
                        
                        generate_did = st.button("Generate DID")
                        
                        if generate_did:
                            # Generate a random DID based on method
                            did_value = f"{did_method}:z6Mk{uuid.uuid4().hex[:16]}"
                            
                            st.code(did_value)
                            st.success("DID generated successfully!")
                            
                            st.write("**Key Management:**")
                            st.write("""
                            In a real implementation, the DID would be associated with:
                            - A private key (kept secure by the user)
                            - A public key (published and associated with the DID)
                            - A DID document specifying verification methods
                            """)
                    
                    # Activity completion button
                    mark_complete = st.checkbox(f"Mark '{activity['title']}' as completed")
    
    # Materials
    if "materials" in content.content:
        st.subheader("Workshop Materials")
        
        for material in content.content["materials"]:
            st.markdown(f"- **{material['title']}** ({material['file_type']}, {material['size_mb']} MB)")
    
    # Completion certificate
    with st.expander("Workshop Completion Certificate", expanded=False):
        st.write("#### Complete the workshop to receive your certificate")
        
        # Simulated completion progress
        st.progress(0.7)
        st.write("Workshop Progress: 70% completed")
        
        # Certificate placeholder
        st.markdown("""
        ```
        ===============================================
                       CERTIFICATE OF COMPLETION
                       
             This certifies that **Student Name**
             has successfully completed the workshop
             
               DECENTRALIZED IDENTITY MANAGEMENT
                       
                          April 2025
        ===============================================
        ```
        """)
        
        st.info("Complete all workshop activities to unlock your certificate.")


def display_discussion_content(content: LearningContent, settings: PrivacySettings):
    """Display discussion content with privacy controls."""
    # Discussion topics
    topics = content.content["discussion_topics"]
    
    # Guidelines
    st.subheader("Discussion Guidelines")
    for guideline in content.content["guidelines"]:
        st.markdown(f"- {guideline}")
    
    # Identity notice based on privacy settings
    if settings.anonymized_mode:
        st.success("You are participating anonymously. Your real identity is hidden from other participants.")
        
        # Display anonymized identity
        pseudonym = hashlib.sha256(settings.user_id.encode()).hexdigest()[:8]
        st.write(f"**Your Discussion Identity:** Student_{pseudonym}")
    else:
        st.info("You are participating with your real identity visible to other participants according to your privacy settings.")
    
    # Topic selection
    selected_topic_index = st.selectbox(
        "Select a discussion topic:",
        range(len(topics)),
        format_func=lambda i: topics[i]["title"]
    )
    
    selected_topic = topics[selected_topic_index]
    
    # Display selected topic
    st.subheader(selected_topic["title"])
    st.markdown(selected_topic["prompt"])
    
    # Discussion threads (simulated)
    st.subheader("Discussion Threads")
    
    # Generate some sample discussion threads
    sample_threads = [
        {
            "author": "Student_3f7b9a2c" if settings.anonymized_mode else "Maria Chen",
            "timestamp": "2023-04-12 10:23:15",
            "content": "I believe schools should only collect academic performance data and basic attendance information. Behavioral tracking crosses an ethical line, especially when it comes to social interactions.",
            "replies": [
                {
                    "author": "Student_a1c5e8f7" if settings.anonymized_mode else "James Wilson",
                    "timestamp": "2023-04-12 11:05:30",
                    "content": "I respectfully disagree. Behavioral data can help identify patterns that might indicate bullying or other issues that impact learning. The key is transparent policies about how this data is used and protected."
                }
            ]
        },
        {
            "author": "Student_6d2e8b9f" if settings.anonymized_mode else "Carlos Mendez",
            "timestamp": "2023-04-11 15:47:22",
            "content": "The ethical use of AI in education requires careful consideration of bias. If predictive models are trained on historical data that reflects systemic inequities, they risk perpetuating or even amplifying those inequities in their predictions.",
            "replies": []
        }
    ]
    
    # Display threads
    for thread in sample_threads:
        with st.container():
            st.markdown(
                f"""
                <div style="padding:10px; background-color:#2D3748; border-radius:5px; margin-bottom:15px;">
                    <div style="display:flex; justify-content:space-between;">
                        <div style="font-weight:bold;">{thread['author']}</div>
                        <div style="font-size:0.8em; color:#A0AEC0;">{thread['timestamp']}</div>
                    </div>
                    <div style="margin-top:10px;">{thread['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Replies
            for reply in thread["replies"]:
                st.markdown(
                    f"""
                    <div style="padding:10px; background-color:#2D3748; border-radius:5px; margin-bottom:10px; margin-left:30px;">
                        <div style="display:flex; justify-content:space-between;">
                            <div style="font-weight:bold;">{reply['author']}</div>
                            <div style="font-size:0.8em; color:#A0AEC0;">{reply['timestamp']}</div>
                        </div>
                        <div style="margin-top:10px;">{reply['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Reply form for each thread
            with st.expander("Reply to this thread"):
                reply_text = st.text_area("Your reply:", key=f"reply_{thread['author']}")
                post_reply = st.button("Post Reply", key=f"post_{thread['author']}")
                
                if post_reply and reply_text:
                    st.success("Your reply has been posted. Remember that this is a demonstration, and the reply won't actually be saved.")
    
    # New thread form
    st.subheader("Start a New Thread")
    
    new_thread = st.text_area("Share your thoughts on this topic:")
    post_thread = st.button("Post Thread")
    
    if post_thread and new_thread:
        st.success("Your thread has been posted. Remember that this is a demonstration, and the thread won't actually be saved.")
        
        # Privacy notice
        if not settings.anonymized_mode:
            st.warning("""
            **Privacy Notice**: Your post is visible to class members as per your privacy settings.
            If you wish to post anonymously, enable Anonymized Mode in your privacy settings.
            """)
    
    # Data collection notice
    st.info("""
    **Data Usage Notice**: Participation in discussions generates data about your engagement and contributions. 
    This data is protected according to your privacy settings, but instructors may analyze participation patterns.
    """)


def display_classes_browser():
    """Display available classes with privacy information."""
    st.subheader("🏫 Available Classes")
    
    # Get classes data
    classes = get_sample_classes()
    settings = get_sample_privacy_settings()
    
    # Display class cards
    for class_data in classes:
        # Create a visually appealing class card
        st.markdown(
            f"""
            <div style="padding:15px; background-color:#2D3748; border-radius:5px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between;">
                    <div style="font-size:1.2em; font-weight:bold;">{class_data['name']}</div>
                    <div style="background-color:#4A5568; padding:2px 8px; border-radius:12px; font-size:0.8em;">
                        {class_data['students']} Students
                    </div>
                </div>
                <div style="font-size:0.9em; margin-top:5px;">
                    Instructor: {class_data['instructor']}
                </div>
                <div style="display:flex; margin-top:10px;">
                    <div style="margin-right:15px;">
                        <span style="font-weight:bold;">Privacy Level:</span> {class_data['privacy_level'].capitalize()}
                    </div>
                    <div>
                        <span style="font-weight:bold;">Data Collection:</span> {class_data['data_collection'].replace('_', ' ').capitalize()}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Privacy compatibility indicator
        compatibility_level = "high"
        if class_data['privacy_level'] == "maximum" and settings.data_sharing_level != "minimal":
            compatibility_level = "medium"
        elif class_data['privacy_level'] == "standard" and settings.data_sharing_level == "full":
            compatibility_level = "low"
        
        # Compatibility color
        compatibility_color = {
            "high": "#48BB78",
            "medium": "#ECC94B",
            "low": "#F56565"
        }[compatibility_level]
        
        # Compatibility message
        compatibility_message = {
            "high": "This class's privacy settings align well with your personal privacy preferences.",
            "medium": "This class has stricter privacy settings than your current preferences. You may need to adjust your settings.",
            "low": "This class's privacy settings may conflict with your current preferences. Consider adjusting your settings."
        }[compatibility_level]
        
        # Display compatibility indicator
        st.markdown(
            f"""
            <div style="margin-bottom:20px; padding:10px; background-color:#1A202C; border-radius:5px; 
                 border-left:4px solid {compatibility_color};">
                <div style="font-weight:bold; margin-bottom:5px;">
                    Privacy Compatibility: <span style="color:{compatibility_color};">{compatibility_level.capitalize()}</span>
                </div>
                <div style="font-size:0.9em;">{compatibility_message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Enrollment button
        enroll_button = st.button("View Class Details", key=f"enroll_{class_data['id']}")
        
        if enroll_button:
            # In a real app, would navigate to class details page
            st.info("Class details would be displayed here. This is a demonstration.")
        
        st.markdown("---")
    
    # Privacy notice
    st.markdown(
        """
        <div style="padding:15px; background-color:#2D3748; border-radius:5px;">
            <div style="font-weight:bold; margin-bottom:5px;">Your Privacy in Classes</div>
            <div>
                When you enroll in a class, your privacy settings interact with the class privacy level. 
                If you have stricter privacy preferences than the class requires, your settings will be respected. 
                If the class has stricter requirements, you'll need to temporarily adopt those settings while participating.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_data_portability():
    """Display data portability and ownership options."""
    st.subheader("📦 Data Portability & Ownership")
    
    st.write("""
    PrivEd Protocol puts you in control of your educational data. You can export, delete,
    or transfer your data at any time. This aligns with the principle of data portability
    as outlined in regulations like GDPR.
    """)
    
    # Data export options
    st.markdown("### Export Your Data")
    
    export_options = st.multiselect(
        "Select what data to export:",
        [
            "Personal Information",
            "Course Enrollments",
            "Assignment Submissions",
            "Discussion Contributions",
            "Learning Analytics",
            "Grades & Assessments",
            "Account Activity Logs"
        ],
        default=[
            "Personal Information",
            "Course Enrollments",
            "Assignment Submissions"
        ]
    )
    
    export_format = st.radio(
        "Select export format:",
        ["JSON", "CSV", "PDF Report"]
    )
    
    if st.button("Generate Export"):
        if export_options:
            st.success("Data export prepared successfully. In a real application, you would now be able to download your data.")
            
            # Show sample of exported data
            st.write("### Sample Export Preview")
            
            if export_format == "JSON":
                sample_data = {
                    "personal_information": {
                        "user_id": "u123456",
                        "name": "Jane Doe",
                        "email": "jane@example.com"
                    },
                    "course_enrollments": [
                        {
                            "course_id": "CS101",
                            "title": "Introduction to Computer Science",
                            "enrollment_date": "2023-01-15"
                        },
                        {
                            "course_id": "MATH201",
                            "title": "Linear Algebra",
                            "enrollment_date": "2023-02-01"
                        }
                    ]
                }
                
                st.json(sample_data)
            elif export_format == "CSV":
                sample_data = """
                user_id,name,email
                u123456,Jane Doe,jane@example.com
                
                course_id,title,enrollment_date
                CS101,Introduction to Computer Science,2023-01-15
                MATH201,Linear Algebra,2023-02-01
                """
                
                st.code(sample_data)
            else:  # PDF
                st.write("A PDF report would be generated with your selected data.")
        else:
            st.error("Please select at least one data category to export.")
    
    # Data deletion
    st.markdown("### Data Deletion")
    
    st.write("""
    You can request deletion of specific data or your entire account. Note that some data may need to be 
    retained for legal or legitimate educational purposes, such as records of completed courses.
    """)
    
    deletion_options = st.multiselect(
        "Select what data to delete:",
        [
            "Discussion Contributions",
            "Learning Analytics",
            "Activity Logs",
            "Entire Account"
        ]
    )
    
    if "Entire Account" in deletion_options:
        st.warning("""
        **Warning**: Deleting your entire account will remove all your data and cannot be undone. 
        You will lose access to all courses, grades, and materials.
        """)
    
    confirmation = st.text_input("Type 'DELETE' to confirm deletion request:")
    
    if st.button("Request Deletion"):
        if deletion_options and confirmation == "DELETE":
            st.success("Deletion request submitted successfully. In a real application, this would initiate the deletion process.")
        elif not deletion_options:
            st.error("Please select what data you want to delete.")
        else:
            st.error("Please type 'DELETE' to confirm your deletion request.")
    
    # Data transfer
    st.markdown("### Data Transfer")
    
    st.write("""
    You can transfer your educational data to another platform or institution that supports
    interoperable educational data standards.
    """)
    
    transfer_destination = st.selectbox(
        "Select destination platform:",
        ["Other LMS Platform", "Educational Institution", "Personal Data Store"]
    )
    
    transfer_options = st.multiselect(
        "Select what data to transfer:",
        [
            "Course Completion Records",
            "Assignments & Projects",
            "Learning Materials",
            "Grades & Certificates"
        ],
        default=["Course Completion Records", "Grades & Certificates"]
    )
    
    if st.button("Initiate Transfer"):
        if transfer_options:
            st.success(f"Data transfer to {transfer_destination} initiated. In a real application, you would receive further instructions.")
        else:
            st.error("Please select what data you want to transfer.")
    
    # Data rights information
    with st.expander("Learn More About Your Data Rights"):
        st.write("""
        ### Your Rights as a Data Subject
        
        Under modern data protection regulations like GDPR, you have several rights:
        
        - **Right to Access**: You can request a copy of all your personal data.
        - **Right to Rectification**: You can correct inaccurate data.
        - **Right to Erasure**: You can request deletion of your data under certain conditions.
        - **Right to Restrict Processing**: You can limit how your data is used.
        - **Right to Data Portability**: You can obtain and reuse your data across different services.
        - **Right to Object**: You can object to certain types of processing.
        
        PrivEd Protocol is designed to honor these rights through its privacy-by-design architecture.
        """)


# ------ Main Application Function ------

def run_prived_protocol():
    """Main entry point for the PrivEd Protocol application."""
    run_prived_header()
    
    # Sidebar with navigation
    st.sidebar.title("PrivEd Navigation")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["Privacy Dashboard", "Privacy Settings", "Learning Content", "Classes", "Data Portability"]
    )
    
    # Get privacy settings and metrics
    settings = get_sample_privacy_settings()
    metrics = get_sample_privacy_metrics()
    
    # Different pages
    if page == "Privacy Dashboard":
        # Display privacy dashboard
        display_dashboard(settings, metrics)
        
    elif page == "Privacy Settings":
        # Display privacy settings
        display_privacy_settings(settings, metrics)
        
    elif page == "Learning Content":
        # Check if there's an active content selected
        if hasattr(st.session_state, 'active_content'):
            # Display the active content
            display_learning_content(st.session_state.active_content, settings)
        else:
            # Display content browser
            display_learning_content_browser()
            
    elif page == "Classes":
        # Display classes
        display_classes_browser()
        
    elif page == "Data Portability":
        # Display data portability options
        display_data_portability()
    
    # Update settings and metrics if needed
    update_settings_and_metrics()


if __name__ == "__main__":
    run_prived_protocol()