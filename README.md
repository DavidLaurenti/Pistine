# Pistine

Mini app in Streamlit per contare i punteggi di **Pistine**, una variante del Sette e Mezzo a cui vengono aggiunti elementi del Black Jack.

🎲 Gioca subito su [pistine-matte.streamlit.app](https://pistine-matte.streamlit.app)

È utilizzabile in generale per tutti i giochi in cui, a ogni turno, un mazziere gioca contro gli altri giocatori e la sua vincita corrisponde alla somma invertita (di segno + o -) delle vincite/perdite degli altri.

## Funzionalità

- Impostazione iniziale di giocatori e primo mazziere
- Registrazione delle vincite/perdite ad ogni mano, con calcolo automatico del punteggio del mazziere
- Storico delle mani giocate, con possibilità di annullare l'ultima
- Aggiunta giocatori e cambio mazziere a partita in corso
- Classifica e grafici sull'andamento del bilancio
- Turno Matto opzionale: turno matto allora si gioca duro

## Avvio

```bash
pip install -r requirements.txt
streamlit run main.py
```

---

Ancora in lavorazione, ma funzionante. Enjoy, giocare sempre responsabilmente.
