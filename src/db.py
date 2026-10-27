"""SQL-kapcsolat az mdbwh szerverhez (csak olvasás).

A belépési adatok a OneDrive-on és a giten kívüli db.env fájlból jönnek.
A jelszót soha nem írjuk ki; hibaüzenetben sem szerepelhet.
"""
from pathlib import Path

import pandas as pd
import pyodbc

ENV_FILE = Path.home() / ".config" / "raktari-munkaorak" / "db.env"
DRIVER = "ODBC Driver 17 for SQL Server"


def _read_env(path: Path = ENV_FILE) -> dict:
    # Egyszerű KULCS=ÉRTÉK beolvasás, a # kezdetű sorok megjegyzések
    if not path.exists():
        raise FileNotFoundError(f"Hiányzik a belépési fájl: {path} (minta: db.env.example)")
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    missing = [k for k in ("SQL_SERVER", "SQL_DATABASE", "SQL_USER", "SQL_PASSWORD") if not values.get(k)]
    if missing:
        raise ValueError(f"Üres vagy hiányzó beállítás a {path} fájlban: {', '.join(missing)}")
    return values


def _quote(value: str) -> str:
    # ODBC-érték kapcsos zárójelben, hogy a ; és más különleges karakter ne törje el
    return "{" + value.replace("}", "}}") + "}"


def connect() -> pyodbc.Connection:
    cfg = _read_env()
    conn_str = (
        f"DRIVER={{{DRIVER}}};SERVER={cfg['SQL_SERVER']};DATABASE={cfg['SQL_DATABASE']};"
        f"UID={_quote(cfg['SQL_USER'])};PWD={_quote(cfg['SQL_PASSWORD'])};"
        "ApplicationIntent=ReadOnly;"
    )
    try:
        return pyodbc.connect(conn_str, timeout=15, readonly=True)
    except pyodbc.Error as exc:
        # Csak a hibakódot és az üzenetet adjuk tovább, a kapcsolati szöveget (jelszóval) nem
        raise ConnectionError(f"Nem sikerült csatlakozni ({cfg['SQL_SERVER']}): {exc.args[-1]}") from None


def query(sql: str, params: list | None = None) -> pd.DataFrame:
    """SELECT futtatása, eredmény pandas táblában."""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or [])
        cols = [c[0] for c in cur.description]
        return pd.DataFrame.from_records(cur.fetchall(), columns=cols)


if __name__ == "__main__":
    # Kapcsolatteszt
    print(query("select SUSER_SNAME() as belepes, @@SERVERNAME as szerver, DB_NAME() as adatbazis").to_string(index=False))
