from translations import TRANSLATIONS
import streamlit as st

def get_translation(key):
    """Get translation with fallback to English or key itself"""
    lang = st.session_state.language
    if lang in TRANSLATIONS:
        # Try to get translation in selected language
        translation = TRANSLATIONS[lang].get(key)
        if translation:
            return translation
        # Fallback to English if key not found in selected language
        if lang != 'en':
            translation = TRANSLATIONS['en'].get(key)
            if translation:
                return translation
    # Return key itself if no translation found
    return key
