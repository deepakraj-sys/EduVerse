
"""
Accessibility module for EduVerse platform
"""
import streamlit as st
from typing import Dict, List
import json
import os

# Color schemes for different types of color blindness
COLOR_SCHEMES = {
    "default": {
        "primaryColor": "#4CAF50",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6", 
        "textColor": "#262730"
    },
    "protanopia": {
        "primaryColor": "#0066CC",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#E6F3FF",
        "textColor": "#000033"
    },
    "deuteranopia": {
        "primaryColor": "#0044AA",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#E6EEFF",
        "textColor": "#000033"
    },
    "tritanopia": {
        "primaryColor": "#FF5733",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#FFF3E6",
        "textColor": "#330000"
    }
}

# Supported languages with translations
TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to EduVerse",
        "start_learning": "Start Learning",
        "modules": "Learning Modules",
        "progress": "Your Progress",
        "settings": "Settings",
        "color_mode": "Color Vision Mode",
        "language": "Language",
        "screen_reader": "Enable Screen Reader Support"
    },
    "es": {
        "welcome": "Bienvenido a EduVerse",
        "start_learning": "Empezar a Aprender",
        "modules": "Módulos de Aprendizaje",
        "progress": "Tu Progreso",
        "settings": "Configuración",
        "color_mode": "Modo de Visión del Color",
        "language": "Idioma",
        "screen_reader": "Activar Soporte de Lector de Pantalla"
    },
    "fr": {
        "welcome": "Bienvenue sur EduVerse",
        "start_learning": "Commencer l'Apprentissage",
        "modules": "Modules d'Apprentissage",
        "progress": "Votre Progression",
        "settings": "Paramètres",
        "color_mode": "Mode de Vision des Couleurs",
        "language": "Langue",
        "screen_reader": "Activer le Support de Lecteur d'Écran"
    },
    "zh": {
        "welcome": "欢迎来到EduVerse",
        "start_learning": "开始学习",
        "modules": "学习模块",
        "progress": "您的进度",
        "settings": "设置",
        "color_mode": "色觉模式",
        "language": "语言",
        "screen_reader": "启用屏幕阅读器支持"
    }
}

class AccessibilityManager:
    def __init__(self):
        self.initialize_session_state()
        self.apply_settings()

    def initialize_session_state(self):
        """Initialize session state variables if they don't exist"""
        if 'color_scheme' not in st.session_state:
            st.session_state.color_scheme = 'default'
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        if 'screen_reader' not in st.session_state:
            st.session_state.screen_reader = False

    def apply_settings(self):
        """Apply the current accessibility settings"""
        # Apply color scheme
        scheme = COLOR_SCHEMES[st.session_state.color_scheme]
        for key, value in scheme.items():
            st.markdown(f"""
                <style>
                    :root {{
                        --{key}: {value} !important;
                    }}
                </style>
            """, unsafe_allow_html=True)

    def get_translation(self, key: str) -> str:
        """Get translated text for the current language"""
        lang = st.session_state.language
        return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, f"Missing translation: {key}")

    def initialize_sidebar_settings(self):
        """Initialize accessibility settings in the sidebar"""
        st.sidebar.markdown("### 🌐 " + self.get_translation("settings"))
        
        # Color scheme selection
        new_color_scheme = st.sidebar.selectbox(
            self.get_translation("color_mode"),
            list(COLOR_SCHEMES.keys()),
            format_func=lambda x: x.capitalize(),
            index=list(COLOR_SCHEMES.keys()).index(st.session_state.color_scheme)
        )
        
        # Language selection
        new_language = st.sidebar.selectbox(
            self.get_translation("language"),
            list(TRANSLATIONS.keys()),
            format_func=lambda x: {'en': 'English', 'es': 'Español', 'fr': 'Français', 'zh': '中文'}[x],
            index=list(TRANSLATIONS.keys()).index(st.session_state.language)
        )
        
        # Screen reader toggle
        new_screen_reader = st.sidebar.checkbox(
            self.get_translation("screen_reader"),
            value=st.session_state.screen_reader
        )

        # Apply changes if settings were modified
        if (new_color_scheme != st.session_state.color_scheme or 
            new_language != st.session_state.language or 
            new_screen_reader != st.session_state.screen_reader):
            
            st.session_state.color_scheme = new_color_scheme
            st.session_state.language = new_language
            st.session_state.screen_reader = new_screen_reader
            self.apply_settings()
            st.rerun()

def initialize_accessibility_settings():
    """Initialize and return the accessibility manager"""
    manager = AccessibilityManager()
    manager.initialize_sidebar_settings()
    return manager


def add_aria_labels(html: str, label: str) -> str:
    """Wrap HTML with an ARIA label span for accessibility."""
    return f'<div role="region" aria-label="{label}">{html}</div>'
