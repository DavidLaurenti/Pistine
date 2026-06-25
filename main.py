# main.py
import streamlit as st
import pandas as pd

# Importiamo le funzioni dai nostri nuovi moduli!
from core.state import init_session_state
from ui.sidebar import render_sidebar

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="PISTINE", page_icon="🂡")
st.title("PISTINAE")

# 2. INIZIALIZZAZIONE MEMORIA
init_session_state()

# 3. BARRA LATERALE
render_sidebar()

# --- LOGICA ANNULLA ULTIMA MANO ---
if st.session_state['storico']:
    col_undo, _ = st.columns([1, 3])
    with col_undo:
        if st.button("↩️ Annulla Ultima Mano", type="secondary"):
            try:
                if not st.session_state['storico']:
                    st.warning("Nessuna mano da annullare.")
                    st.stop()

                ultima_mano = st.session_state['storico'].pop()
                for nome, punti in ultima_mano.items():
                    if nome in st.session_state['punteggi']:
                        st.session_state['punteggi'][nome] -= punti
                    else:
                        st.session_state['punteggi'][nome] = -punti

                st.success("Ultima mano annullata!")
                st.rerun()
            except Exception as e:
                st.error(f"Errore nell'annullamento: {e}")

# --- AREA PRINCIPALE ---
if len(st.session_state['giocatori']) < 2:
    st.info("Aggiungi giocatori")
else:
    st.markdown(f"### Mazziere attuale: **:red[{st.session_state['mazziere_corrente']}]** 🎩")
    st.write("Inserisci vincite/perdite degli altri.")

    # FORM INSERIMENTO
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

        conferma = st.form_submit_button("💰 Conferma Mano")

        if conferma:
            punti_mazziere = -somma_giocatori
            punti_round[st.session_state['mazziere_corrente']] = punti_mazziere

            st.session_state['storico'].append(punti_round)
            for nome, p in punti_round.items():
                if nome in st.session_state['punteggi']:
                    st.session_state['punteggi'][nome] += p
                else:
                    st.session_state['punteggi'][nome] = p
            st.rerun()

    # CLASSIFICA E STORICO
    st.divider()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Bilancio")
        if st.session_state['punteggi']:
            df = pd.DataFrame(list(st.session_state['punteggi'].items()), columns=['Giocatore', 'Bilancio'])
            df = df.sort_values(by='Bilancio', ascending=False)
            st.dataframe(df, hide_index=True)

            somma = sum(st.session_state['punteggi'].values())
            if abs(somma) > 0.001:
                st.caption(f"⚠️ Check Somma: {somma:.2f}")
        else:
            st.write("Nessun giocatore.")

    with col2:
        st.subheader("Ultimi Round")
        if st.session_state['storico']:
            df_storico = pd.DataFrame(st.session_state['storico'])
            df_storico = df_storico.iloc[::-1]
            st.dataframe(df_storico, use_container_width=True, height=200)

    # STATISTICHE
    st.divider()
    if st.checkbox("Mostra Statistiche Avanzate"):
        if len(st.session_state['storico']) > 0:
            st.caption("Andamento Bilancio nel Tempo")
            history_data = []
            current_sums = {name: 0.0 for name in st.session_state['giocatori']}
            history_data.append(current_sums.copy())

            for mano in st.session_state['storico']:
                for nome, punti in mano.items():
                    current_sums[nome] = current_sums.get(nome, 0.0) + punti
                history_data.append(current_sums.copy())

            df_chart = pd.DataFrame(history_data)
            st.line_chart(df_chart)
        else:
            st.info("Gioca qualche mano per vedere i grafici!")