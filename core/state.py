import streamlit as st

def init_session_state():
    """Inizializza le variabili di sessione se non sono già presenti."""
    if 'giocatori' not in st.session_state:
        st.session_state['giocatori'] = []
    if 'punteggi' not in st.session_state:
        st.session_state['punteggi'] = {}
    if 'storico' not in st.session_state:
        st.session_state['storico'] = []
    if 'mazziere_corrente' not in st.session_state:
        st.session_state['mazziere_corrente'] = None