# Kód – Raktári munkaórák hatékonysága

Ez a mappa egy git-repó. Csak kód és konfiguráció kerül gitbe, adat és kimenet soha.

## Python-környezet (uv)
- A projektnek saját környezete van, amit az **uv** kezel. Csomagot csak `uv add <csomag>`-gal telepíts (jóváhagyás után), futtatás: `uv run python src/<szkript>.py`.
- A környezet NEM a OneDrive-ban van: a `UV_PROJECT_ENVIRONMENT` változó (a projekt `.claude/settings.json`-jában) a `C:\venvs\raktari-munkaorak` mappára mutat. Ne hozz létre `.venv` mappát a OneDrive-ban.
- `pyproject.toml` és `uv.lock` gitbe kerül, így a környezet bármikor újraépíthető (`uv sync`).

## Felépítés
- `src/config.py` – minden útvonal egy helyen; a forrásadat: `../forrasok/`, az üzleti kimenet: `../kimenetek/`
- `src/` – szkriptek, mindegyik önállóan futtatható
- `data/` – köztes, tisztított adatok (parquet/csv) – gitignore
- `output/` – munka-kimenetek, ábrák – gitignore; a végleges anyag a `../kimenetek/` mappába megy

## Git
- Kis, értelmes commitok magyar üzenettel (pl. „Napi adattábla: PDA-órák tevékenységenként”).
- Commit és push csak kérésre. A távoli repó (GitHub / Azure DevOps) a biztonsági mentés: rendszeresen pusholj, mert a OneDrive-szinkron és a git ritkán, de összeakadhat.
