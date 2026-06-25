import streamlit as st
import random

def render_setup():
    st.header("Impostazioni Iniziali")
    st.write("Configura il gioco prima di iniziare a giocare. Sballino.")

    # Inserimento giocatori
    nomi_input = st.text_input("Nome Giocatore")

    # Creazione lista dei giocatori
    nomi_list = [nome.strip() for nome in nomi_input.split(",") if nome.strip()]

    primo_mazziere = None
    if len(nomi_list) >= 2:
        primo_mazziere = st.selectbox("Seleziona il primo mazziere", nomi_list)
    
    st.divider()

    # Creazione turno matto
    turno_matto = st.toggle("Abilita Turno Matto", value=False)

    if turno_matto:
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Ogni quante mani (Media)?", min_value=1, value=18)
        with col2:
            var = st.number_input("Varianza (± mani)", min_value=0, value=5)

    if st.button("Inizia Gioco"):
        if len(nomi_list) < 2:
            st.error("Aggiungi almeno due giocatori.")
        elif not primo_mazziere:
            st.error("Seleziona il primo mazziere.")
        else:
            # Inizializza lo stato di sessione
            st.session_state['giocatori'] = nomi_list
            st.session_state['punteggi'] = {nome: 0 for nome in nomi_list}
            st.session_state['mazziere_corrente'] = primo_mazziere
            st.session_state['turno_matto'] = turno_matto
            
        
        # Algoritmo del turno matto
        # Algoritmo del turno matto
        if turno_matto:
            st.session_state['matto_base'] = base
            st.session_state['matto_var'] = var

            # Copiamo la lista di chi deve fare il matto
            st.session_state['matti_da_fare'] = nomi_list.copy()

            # Calcolo della prima estrazione
            primo_target = random.randint(base - var, base + var)
            st.session_state['prossimo_target_matto'] = max(1, primo_target)
        
        st.session_state['fase_gioco'] = 'gioco'
        st.success("Tutto pronto. Non pentirtene.")
        st.rerun()