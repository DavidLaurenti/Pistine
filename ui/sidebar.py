import streamlit as st
import random

import core.db as db

def render_sidebar():
    """Disegna la barra laterale per la gestione dei giocatori e del mazziere."""
    with st.sidebar:
        st.header("Gestione Tavolo")

        # Aggiunta Giocatori
        with st.form("form_nuovo_giocatore", clear_on_submit=True):
            nuovo_giocatore = st.text_input("Nome Giocatore").strip()
            if st.form_submit_button("Aggiungi al Tavolo"):
                if nuovo_giocatore and nuovo_giocatore not in st.session_state['giocatori']:
                    if st.session_state.get('turno_matto') and nuovo_giocatore not in st.session_state['matti_da_fare']:
                        st.session_state['matti_da_fare'].append(nuovo_giocatore)
                    if nuovo_giocatore == "Flavio":
                        st.snow()
                    st.session_state['giocatori'].append(nuovo_giocatore)
                    if nuovo_giocatore not in st.session_state['punteggi']:
                        st.session_state['punteggi'][nuovo_giocatore] = 0.0
                    if len(st.session_state['giocatori']) == 1:
                        st.session_state['mazziere_corrente'] = nuovo_giocatore
                    db.salva_stato_sessione(st.session_state)
                    st.rerun()
                
        st.divider()

        # SELEZIONE DEL MAZZIERE
        if st.session_state['giocatori']:
            st.subheader("Seleziona nuovo mazziere")
            # Gestione sicura dell'indice (se il mazziere cambia o viene rimosso)
            try:
                if st.session_state['mazziere_corrente'] in st.session_state['giocatori']:
                    index_mazziere = st.session_state['giocatori'].index(st.session_state['mazziere_corrente'])
                else:
                    index_mazziere = 0
            except ValueError:
                index_mazziere = 0

            mazziere = st.selectbox(
                "Seleziona il Mazziere attuale:",
                st.session_state['giocatori'],
                index=index_mazziere
            )

            if mazziere != st.session_state['mazziere_corrente']:
                st.session_state['mazziere_corrente'] = mazziere
                db.salva_stato_sessione(st.session_state)
                st.rerun()

        st.divider()

        # CONTATORE TURNO MATTO: chi l'ha già fatto e chi manca ancora
        if st.session_state.get('turno_matto'):
            st.subheader("🃏 Turno Matto")
            da_fare = st.session_state.get('matti_da_fare', [])
            fatto = [g for g in st.session_state['giocatori'] if g not in da_fare]

            st.markdown(f"✅ **Fatto** ({len(fatto)}): {', '.join(fatto) if fatto else '—'}")
            st.markdown(f"⏳ **Da fare** ({len(da_fare)}): {', '.join(da_fare) if da_fare else 'Tutti fatto! 🎉'}")

            st.divider()

        if st.button("🔴 Resetta Partita"):
            st.session_state['punteggi'] = {k: 0.0 for k in st.session_state['giocatori']}
            st.session_state['storico'] = []

            # Resetta anche lo stato del Turno Matto, altrimenti resta agganciato
            # a mani/giocatori della partita precedente.
            if st.session_state.get('turno_matto'):
                st.session_state['matti_da_fare'] = st.session_state['giocatori'].copy()
                base = st.session_state['matto_base']
                var = st.session_state['matto_var']
                st.session_state['prossimo_target_matto'] = max(1, random.randint(base - var, base + var))
                st.session_state['matto_corrente'] = None
                st.session_state['mostra_banner_matto'] = False
            db.salva_stato_sessione(st.session_state)
            st.rerun()