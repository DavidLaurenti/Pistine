import streamlit as st

def init_session_state():
    """Inizializza le variabili di sessione se non sono già presenti."""
    if 'fase_gioco' not in st.session_state:
        st.session_state['fase_gioco'] = 'setup'  # Fase iniziale del gioco
    if 'turno_matto' not in st.session_state:
        st.session_state['turno_matto'] = False
    
    if 'giocatori' not in st.session_state:
        st.session_state['giocatori'] = []
    if 'punteggi' not in st.session_state:
        st.session_state['punteggi'] = {}
    if 'storico' not in st.session_state:
        st.session_state['storico'] = []
    if 'mazziere_corrente' not in st.session_state:
        st.session_state['mazziere_corrente'] = None

    # Variabili per la gestione del turno matto
    if 'matti_da_fare' not in st.session_state:
        st.session_state['matti_da_fare'] = []
    if 'prossimo_target_matto' not in st.session_state:
        st.session_state['prossimo_target_matto'] = 0
    if 'matto_corrente' not in st.session_state:
        st.session_state['matto_corrente'] = None
    if 'matto_base' not in st.session_state:
        st.session_state['matto_base'] = 18
    if 'matto_var' not in st.session_state:
        st.session_state['matto_var'] = 5
    if 'mostra_banner_matto' not in st.session_state:
        st.session_state['mostra_banner_matto'] = False