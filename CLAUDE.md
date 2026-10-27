# Kód – Raktári munkaórák hatékonysága

Ez a mappa egy git-repó. Csak kód és konfiguráció kerül gitbe, adat és kimenet soha.

## Python-környezet (uv)
- A projektnek saját környezete van, amit az **uv** kezel. Csomagot csak `uv add <csomag>`-gal telepíts (jóváhagyás után), futtatás: `uv run python src/<szkript>.py`.
- A környezet NEM a OneDrive-ban van: a `UV_PROJECT_ENVIRONMENT` változó (a projekt `.claude/settings.json`-jában) a `C:\venvs\raktari-munkaorak` mappára mutat. Ne hozz létre `.venv` mappát a OneDrive-ban.
- `pyproject.toml` és `uv.lock` gitbe kerül, így a környezet bármikor újraépíthető (`uv sync`).

## SQL-kapcsolat
- Szerver: `mdbwh`, adatbázis: `OLAP_DAXELES` (pl. `factDurataActivitate`, `dimActivitatiDepozit`, `factColectari`). Csak olvasunk (`SELECT`).
- A belépési adatok (SQL-felhasználó, jelszó) a `C:\Users\<felhasznalo>\.config\raktari-munkaorak\db.env` fájlban vannak – a OneDrive-on és a giten kívül. Minta: `db.env.example`.
- A jelszót Karesz írja be. A kód csak beolvassa; jelszót soha ne írj ki képernyőre, logba, fájlba, és ne tedd parancssori paraméterbe.

## Felépítés
- `src/config.py` – minden útvonal egy helyen; a forrásadat: `../forrasok/`, az üzleti kimenet: `../kimenetek/`
- `src/` – szkriptek, mindegyik önállóan futtatható
- `data/` – köztes, tisztított adatok (parquet/csv) – gitignore
- `output/` – munka-kimenetek, ábrák – gitignore; a végleges anyag a `../kimenetek/` mappába megy

## Git
- Kis, értelmes commitok magyar üzenettel (pl. „Napi adattábla: PDA-órák tevékenységenként”).
- Commit és push csak kérésre. A távoli repó (GitHub / Azure DevOps) a biztonsági mentés: rendszeresen pusholj, mert a OneDrive-szinkron és a git ritkán, de összeakadhat.
