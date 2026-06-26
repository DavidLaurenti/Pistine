# main.py
import streamlit as st

# I nostri moduli
from core.state import init_session_state
import core.logic as logic
import ui.setup as stp
from ui.sidebar import render_sidebar
import ui.dashboard as dash

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="PISTINE", page_icon="🂡")
st.title("PISTINAE")

# 2. INIZIALIZZAZIONE MEMORIA
init_session_state()

# 3. GESTIONE FASI DEL GIOCO
if st.session_state['fase_gioco'] == 'setup':
    stp.render_setup()

elif st.session_state['fase_gioco'] == 'gioco':
    # Barra Laterale (Aggiungi/Cambia Mazziere)
    render_sidebar()

    # --- LOGICA ANNULLA ULTIMA MANO ---
    logic.annulla_mano()

    # --- AREA PRINCIPALE: TAVOLO DA GIOCO ---
    if len(st.session_state['giocatori']) < 2:
        st.info("Aggiungi giocatori per iniziare.")
    else:
        st.markdown(f"### Mazziere attuale: **:red[{st.session_state['mazziere_corrente']}]** 🎩")

        # --- TRIGGER E ANIMAZIONE TURNO MATTO ---
        stp.turno_matto()

        # --- FORM INSERIMENTO PUNTI ---
        dash.inserimento_punti_form()
        # --- DASHBOARD (Classifiche e Grafici) ---
        dash.render_dashboard()