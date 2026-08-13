# main.py
import streamlit as st

# I nostri moduli
from core.state import init_session_state
import core.db as db
import core.logic as logic
import ui.setup as stp
from ui.sidebar import render_sidebar
import ui.dashboard as dash

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="PISTINE", page_icon="🂡")

game_id_url = st.query_params.get('game')
modalita_spettatore = st.query_params.get('view') == '1'

# --- MODALITA' SPETTATORE: sola lettura, si aggiorna da sola ---
if modalita_spettatore and game_id_url:
    st.title("PISTINAE 👀")

    @st.fragment(run_every=3)
    def vista_live():
        stato = db.carica_partita(game_id_url)
        if not stato:
            st.error("Partita non trovata: il link potrebbe non essere valido.")
            return
        if len(stato.get('giocatori', [])) < 2:
            st.info("La partita non è ancora iniziata.")
            return
        st.markdown(f"### Mazziere attuale: **:red[{stato['mazziere_corrente']}]** 🎩")
        dash.render_dashboard(stato)

    vista_live()
    st.stop()

st.title("PISTINAE")

# 2. INIZIALIZZAZIONE MEMORIA
init_session_state()

# --- RIPRISTINO DOPO RIAVVIO: se il browser ha ancora l'URL della partita
# in corso ma la sessione è nuova (es. l'app è stata riavviata), ricarica
# lo stato dal database invece di ripartire dal setup. ---
if game_id_url and 'game_id' not in st.session_state:
    stato_salvato = db.carica_partita(game_id_url)
    if stato_salvato:
        st.session_state.update(stato_salvato)
        st.session_state['game_id'] = game_id_url
        st.session_state['fase_gioco'] = 'gioco'

# 3. GESTIONE FASI DEL GIOCO
if st.session_state['fase_gioco'] == 'setup':
    stp.render_setup()

elif st.session_state['fase_gioco'] == 'gioco':
    # Suono di inizio partita (se innescato dal setup)
    stp.play_suono_inizio()

    # Link condivisibile per far seguire la partita in diretta
    stp.mostra_link_live()

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