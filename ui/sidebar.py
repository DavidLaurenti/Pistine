import streamlit as st

def render_sidebar():
    """Disegna la barra laterale per la gestione dei giocatori e del mazziere."""
    with st.sidebar:
        st.header("Gestione Tavolo")

        # Aggiunta Giocatori
        nuovo_giocatore = st.text_input("Nome Giocatore")
        if st.button("Aggiungi al Tavolo"):
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
                st.rerun()

        st.divider()

        if st.button("🔴 Resetta Partita"):
            st.session_state['punteggi'] = {k: 0.0 for k in st.session_state['giocatori']}
            st.session_state['storico'] = []
            st.rerun()