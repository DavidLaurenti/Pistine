"""Persistenza della partita su database.

Usa Turso (libSQL) quando sono presenti le credenziali nei secrets di
Streamlit: cosi' lo stato sopravvive ai riavvii/redeploy dell'app anche
su Streamlit Community Cloud, dove il filesystem locale e' effimero.
In assenza di credenziali (es. sviluppo in locale) ripiega su un file
SQLite locale (libreria standard, nessuna dipendenza in piu').

Nota: non usiamo `libsql_client.dbapi2` perche' su Python 3.14 (usato
da Streamlit Community Cloud) va in crash all'import: internamente
importa `sqlite3.version`, un attributo rimosso dalla libreria
standard in quella versione di Python. `create_client_sync` non ha
questo problema.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import sqlite3

import streamlit as st

_LOCAL_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pistine.db"

# Le uniche chiavi di session_state che compongono una partita: sono
# quelle che servono per ricostruire il gioco esattamente com'era.
CHIAVI_STATO = [
    'giocatori', 'punteggi', 'storico', 'mazziere_corrente', 'turno_matto',
    'matti_da_fare', 'prossimo_target_matto', 'matto_corrente',
    'matto_base', 'matto_var',
]

_CREA_TABELLA = """
CREATE TABLE IF NOT EXISTS partite (
    game_id TEXT PRIMARY KEY,
    stato_json TEXT NOT NULL,
    aggiornata_il TEXT NOT NULL
)
"""

_UPSERT = """
INSERT INTO partite (game_id, stato_json, aggiornata_il) VALUES (?, ?, ?)
ON CONFLICT(game_id) DO UPDATE SET
    stato_json = excluded.stato_json,
    aggiornata_il = excluded.aggiornata_il
"""

_SELECT = "SELECT stato_json FROM partite WHERE game_id = ?"


def _turso_config():
    try:
        turso = st.secrets["turso"]
    except Exception:
        return None, None
    return turso.get("url"), turso.get("auth_token")


def _forza_https(url: str) -> str:
    """Riscrive libsql:// e wss:// in https://.

    Il protocollo websocket di questa libreria non regge l'handshake
    con i server Turso attuali (fallisce con "400 Invalid response
    status"); la variante HTTP dello stesso protocollo (Hrana-over-HTTP)
    funziona correttamente con le stesse credenziali, quindi la usiamo
    sempre indipendentemente dallo schema fornito da `turso db show`.
    """
    if url.startswith("libsql://") or url.startswith("wss://"):
        return "https://" + url.split("://", 1)[1]
    if url.startswith("ws://"):
        return "http://" + url.split("://", 1)[1]
    return url


@st.cache_resource
def _connessione():
    url, auth_token = _turso_config()
    if url:
        import libsql_client
        client = libsql_client.create_client_sync(url=_forza_https(url), auth_token=auth_token)
        client.execute(_CREA_TABELLA)
        return ("turso", client)
    else:
        _LOCAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(_LOCAL_DB_PATH), check_same_thread=False)
        conn.execute(_CREA_TABELLA)
        conn.commit()
        return ("sqlite", conn)


def _esegui(sql, params):
    tipo, conn = _connessione()
    if tipo == "sqlite":
        conn.execute(sql, params)
        conn.commit()
    else:
        conn.execute(sql, list(params))


def _leggi_una_riga(sql, params):
    tipo, conn = _connessione()
    if tipo == "sqlite":
        return conn.execute(sql, params).fetchone()
    else:
        rs = conn.execute(sql, list(params))
        return rs.rows[0] if rs.rows else None


def stato_da_session(session_state) -> dict:
    """Estrae dalla session_state solo le chiavi che compongono una partita."""
    return {chiave: session_state[chiave] for chiave in CHIAVI_STATO if chiave in session_state}


def salva_partita(game_id: str, stato: dict) -> None:
    _esegui(_UPSERT, [game_id, json.dumps(stato), datetime.now(timezone.utc).isoformat()])


def carica_partita(game_id: str) -> dict | None:
    riga = _leggi_una_riga(_SELECT, [game_id])
    if riga is None:
        return None
    return json.loads(riga[0])


def salva_stato_sessione(session_state) -> None:
    """Salva lo stato corrente della partita in corso, se ne esiste una."""
    game_id = session_state.get('game_id')
    if game_id:
        salva_partita(game_id, stato_da_session(session_state))
