# main.py
import streamlit as st

# I nostri moduli
from core.state import init_session_state
from core.logic import processa_mano
from ui.sidebar import render_sidebar
from ui.setup import render_setup
from ui.dashboard import render_dashboard

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="PISTINE", page_icon="🂡")
st.title("PISTINAE")

# 2. INIZIALIZZAZIONE MEMORIA
init_session_state()

# 3. GESTIONE FASI DEL GIOCO
if st.session_state['fase_gioco'] == 'setup':
    render_setup()

elif st.session_state['fase_gioco'] == 'gioco':
    # Barra Laterale (Aggiungi/Cambia Mazziere)
    render_sidebar()

    # --- LOGICA ANNULLA ULTIMA MANO ---
    if st.session_state['storico']:
        col_undo, _ = st.columns([1, 3])
        with col_undo:
            if st.button("↩️ Annulla Ultima Mano", type="secondary"):
                try:
                    ultima_mano = st.session_state['storico'].pop()
                    for nome, punti in ultima_mano.items():
                        if not str(nome).startswith('_'): # Ignora metadati del matto
                            if nome in st.session_state['punteggi']:
                                st.session_state['punteggi'][nome] -= punti
                            else:
                                st.session_state['punteggi'][nome] = -punti
                    st.success("Ultima mano annullata!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore: {e}")

    # --- AREA PRINCIPALE: TAVOLO DA GIOCO ---
    if len(st.session_state['giocatori']) < 2:
        st.info("Aggiungi giocatori per iniziare.")
    else:
        st.markdown(f"### Mazziere attuale: **:red[{st.session_state['mazziere_corrente']}]** 🎩")

        # --- TRIGGER E ANIMAZIONE TURNO MATTO ---
        if st.session_state.get('turno_matto', False) and len(st.session_state.get('matti_da_fare', [])) > 0:
            mani_giocate = len(st.session_state['storico'])
            mazziere = st.session_state['mazziere_corrente']
            
            # Se abbiamo raggiunto la soglia delle mani...
            if mani_giocate >= st.session_state['prossimo_target_matto']:
                
                # Il mazziere attuale DEVE e PUÒ farlo?
                if mazziere in st.session_state['matti_da_fare']:
                    # Se non lo avevamo ancora innescato, facciamolo ora!
                    if st.session_state.get('matto_corrente') != mazziere:
                        st.session_state['matto_corrente'] = mazziere
                        st.session_state['mostra_banner_matto'] = True
                else:
                    # SILENZIO ASSOLUTO: Il turno matto è in agguato per il prossimo cambio mazziere.
                    st.session_state['matto_corrente'] = None
            
            # Disegna il banner SE c'è un matto corrente valido
            if st.session_state.get('matto_corrente') is not None:
                if st.session_state.get('mostra_banner_matto', False):
                    html_matto = f"""
                    <style>
                    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
                    .matto-box {{ background-color: #ffe6e6; padding: 20px; border-radius: 15px; border: 5px solid #ff0000; text-align: center; margin-bottom: 20px; }}
                    .matto-text {{ color: #ff0000; font-size: 36px; font-weight: 900; animation: blinker 0.6s linear infinite; margin: 0; }}
                    </style>
                    <div class="matto-box">
                        <p class="matto-text">🔔 TURNO MATTO! TURNO MATTO 🔔</p>
                        <h2 style="color: black; margin-top: 15px;">Tocca al banco: <b>{st.session_state['matto_corrente']}</b>!</h2>
                    </div>
                    """
                    st.markdown(html_matto, unsafe_allow_html=True)
                    
                    # Due pulsanti affiancati per decidere cosa fare
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("❌ Chiudi Avviso e Gioca"):
                            st.session_state['mostra_banner_matto'] = False
                            st.rerun()
                    with col_btn2:
                        if st.button("⏭️ Posticipa Turno Matto"):
                            import random
                            # Nascondiamo tutto e spostiamo l'agguato di 2-4 mani nel futuro
                            st.session_state['mostra_banner_matto'] = False
                            st.session_state['matto_corrente'] = None
                            st.session_state['prossimo_target_matto'] = mani_giocate + random.randint(2, 4)
                            st.rerun()
                else:
                    st.warning(f"🃏 Promemoria: Questa mano è il Turno Matto del banco (**{st.session_state['matto_corrente']}**)")

        # --- FORM INSERIMENTO PUNTI ---
        st.write("Inserisci vincite/perdite degli altri.")
        with st.form("form_mano", clear_on_submit=True):
            punti_round = {}
            cols = st.columns(len(st.session_state['giocatori']))
            somma_giocatori = 0.0

            for i, nome in enumerate(st.session_state['giocatori']):
                with cols[i]:
                    if nome == st.session_state['mazziere_corrente']:
                        st.text_input(f"{nome} (Banco)", value="?", disabled=True)
                    else:
                        val = st.number_input(f"{nome}", step=0.5, value=0.0)
                        punti_round[nome] = val
                        somma_giocatori += val

            if st.form_submit_button("💰 Conferma Mano"):
                processa_mano(punti_round, somma_giocatori)
                st.rerun()

        # --- DASHBOARD (Classifiche e Grafici) ---
        render_dashboard()