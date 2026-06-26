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

def turno_matto():
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