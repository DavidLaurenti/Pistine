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

Senza configurazione aggiuntiva la partita viene salvata in un file SQLite
locale (`data/pistine.db`): riavviando l'app in locale, la partita in corso
non si perde.

## Persistenza online (Turso)

Su Streamlit Community Cloud il filesystem è effimero: un file SQLite
locale può sparire ad ogni riavvio/redeploy dell'app. Per avere una
persistenza vera anche online, collega un database [Turso](https://turso.tech)
(gratuito):

```bash
turso db create pistine
turso db show pistine --url
turso db tokens create pistine
```

Poi copia `.streamlit/secrets.toml.example` in `.streamlit/secrets.toml`
(in locale) — oppure incolla lo stesso contenuto nella sezione **Secrets**
delle impostazioni dell'app su Streamlit Cloud — con l'url e il token
ottenuti sopra. Da quel momento ogni mano viene salvata sul database
cloud: se l'app si riavvia, riaprendo lo stesso URL (con `?game=...`) la
partita riprende esattamente da dov'era.

## Diretta per gli spettatori

Quando la partita è iniziata, nella schermata principale compare un
riquadro "Fai seguire la partita in diretta a chi non gioca" con un link
in sola lettura: chiunque lo apra vede bilancio, storico e turno matto
aggiornarsi da soli ogni pochi secondi, senza poter modificare nulla.

## App sul telefono

L'app è già raggiungibile da mobile via browser: da Chrome/Safari puoi
usare "Aggiungi a schermata Home" per avere un'icona di accesso rapido.
Su Streamlit Community Cloud, però, personalizzare nome e icona di
quell'icona non è attualmente possibile (limite noto della piattaforma,
non dell'app): comparirà come "Streamlit". Per un'icona e un nome
davvero personalizzati serve un hosting diverso, con un lavoro di
migrazione a parte.

---

Ancora in lavorazione, ma funzionante. Enjoy, giocare sempre responsabilmente.
