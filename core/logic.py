import streamlit as st
import random

def processa_mano(punteggi_round, somma_giocatori):
    """Aggiorna punteggi e storico giocatori e gestisci turno matto se abilitato."""
    # 1. Calcolo dei punti del mazziere
    punti_mazziere = -somma_giocatori
    punteggi_round[st.session_state['mazziere_corrente']] = punti_mazziere

    # 2. Gestione Conclusione Turno Matto
    punteggi_round['_is_matto'] = False
    if st.session_state.get('matto_corrente') is not None:
        punteggi_round['_is_matto'] = True
        punteggi_round['_matto_player'] = st.session_state['matto_corrente']
        
        # --- NOVITÀ: Togliamo il mazziere dalla lista di chi deve farlo ---
        if st.session_state['matto_corrente'] in st.session_state['matti_da_fare']:
            st.session_state['matti_da_fare'].remove(st.session_state['matto_corrente'])
            
        # Calcola il target per il PROSSIMO turno matto
        base = st.session_state['matto_base']
        var = st.session_state['matto_var']
        mani_attuali = len(st.session_state['storico'])
        st.session_state['prossimo_target_matto'] = mani_attuali + random.randint(base - var, base + var)
        
        # Resetta il matto corrente
        st.session_state['matto_corrente'] = None

    # 3. Salvataggio Punti nello Storico e nel Bilancio
    st.session_state['storico'].append(punteggi_round)
    
    for nome, p in punteggi_round.items():
        if not str(nome).startswith('_'):  # Ignora i metadati segreti del Turno Matto
            if nome in st.session_state['punteggi']:
                st.session_state['punteggi'][nome] += p
            else:
                st.session_state['punteggi'][nome] = p
    
def annulla_mano():
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
                    