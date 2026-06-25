import streamlit as st
import pandas as pd

def render_dashboard():
    """Disegna le classifiche, lo storico e i grafici."""
    st.divider()
    col1, col2 = st.columns([1, 2])

    # --- TABELLA BILANCIO ---
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

    # --- TABELLA STORICO ---
    with col2:
        st.subheader("Ultimi Round")
        if st.session_state['storico']:
            df_storico = pd.DataFrame(st.session_state['storico'])
            
            # --- NOVITÀ: Nascondiamo le colonne di sistema ---
            colonne_segrete = [col for col in df_storico.columns if str(col).startswith('_')]
            if colonne_segrete:
                df_storico = df_storico.drop(columns=colonne_segrete)
                
            # Invertiamo per avere l'ultimo round in cima
            df_storico = df_storico.iloc[::-1]
            st.dataframe(df_storico, use_container_width=True, height=200)

    # --- GRAFICI AVANZATI ---
    st.divider()
    if st.checkbox("Mostra Statistiche Avanzate"):
        if len(st.session_state['storico']) > 0:
            st.caption("Andamento Bilancio nel Tempo")
            history_data = []
            current_sums = {name: 0.0 for name in st.session_state['giocatori']}
            history_data.append(current_sums.copy())

            for mano in st.session_state['storico']:
                for nome, punti in mano.items():
                    # Usiamo .get() e ignoriamo le chiavi di sistema del matto
                    if not str(nome).startswith('_'):
                        current_sums[nome] = current_sums.get(nome, 0.0) + punti
                history_data.append(current_sums.copy())

            df_chart = pd.DataFrame(history_data)
            st.line_chart(df_chart)
        else:
            st.info("Gioca qualche mano per vedere i grafici!")