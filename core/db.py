"""Persistenza della partita su database.

Usa Turso (libSQL) quando sono presenti le credenziali nei secrets di
Streamlit: cosi' lo stato sopravvive ai riavvii/redeploy dell'app anche
su Streamlit Community Cloud, dove il filesystem locale e' effimero.
In assenza di credenziali (es. sviluppo in locale) ripiega su un file
SQLite locale, usando l'interfaccia DB-API 2.0 di libsql_client per
avere un unico percorso di codice in entrambi i casi.
"""
from datetime import datetime, timezone
from pathlib import Path
import json

import libsql_client.dbapi2 as dbapi2
import streamlit as st

_LOCAL_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pistine.db"

# Le uniche chiavi di session_state che compongono una partita: sono
# quelle che servono per ricostruire il gioco esattamente com'era.
CHIAVI_STATO = [
    'giocatori', 'punteggi', 'storico', 'mazziere_corrente', 'turno_matto',
    'matti_da_fare', 'prossimo_target_matto', 'matto_corrente',
    'matto_base', 'matto_var',
]


def _turso_config():
    try:
        turso = st.secrets["turso"]
    except Exception:
        return None, None
    return turso.get("url"), turso.get("auth_token")


@st.cache_resource
def _connessione():
    url, auth_token = _turso_config()
    if url:
        conn = dbapi2.connect(url, auth_token=auth_token, check_same_thread=False)
    else:
        _LOCAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = dbapi2.connect(str(_LOCAL_DB_PATH), check_same_thread=False)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS partite (
            game_id TEXT PRIMARY KEY,
            stato_json TEXT NOT NULL,
            aggiornata_il TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def stato_da_session(session_state) -> dict:
    """Estrae dalla session_state solo le chiavi che compongono una partita."""
    return {chiave: session_state[chiave] for chiave in CHIAVI_STATO if chiave in session_state}


def salva_partita(game_id: str, stato: dict) -> None:
    conn = _connessione()
    conn.execute(
        """
        INSERT INTO partite (game_id, stato_json, aggiornata_il) VALUES (?, ?, ?)
        ON CONFLICT(game_id) DO UPDATE SET
            stato_json = excluded.stato_json,
            aggiornata_il = excluded.aggiornata_il
        """,
        [game_id, json.dumps(stato), datetime.now(timezone.utc).isoformat()],
    )
    conn.commit()


def carica_partita(game_id: str) -> dict | None:
    conn = _connessione()
    cur = conn.execute("SELECT stato_json FROM partite WHERE game_id = ?", [game_id])
    riga = cur.fetchone()
    if riga is None:
        return None
    return json.loads(riga[0])


def salva_stato_sessione(session_state) -> None:
    """Salva lo stato corrente della partita in corso, se ne esiste una."""
    game_id = session_state.get('game_id')
    if game_id:
        salva_partita(game_id, stato_da_session(session_state))
