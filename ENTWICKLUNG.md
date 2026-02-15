# Entwicklung & Workspace

## Workspace = Repo (1:1)

Dieser Ordner **Auto-FTP-Sync-Plus** ist das komplette GitHub-Repository. In Cursor/VS Code diesen Ordner als Workspace öffnen (oder die Datei `../kodi.code-workspace`, die genau diesen Ordner lädt). Dann siehst du nur:

- `addons/` – Plugin und Skin (Quellcode)
- `repo/` – Build-Skript, Repository-Addon, `output/`
- `README.md`, `CHANGELOG.md`, `gitpush.sh`, `.gitignore`

Keine anderen Ordner (kein addons-, userdata-, backups-Ordner von Kodi im Workspace). So ist der Workspace 1:1 identisch mit dem, was auf GitHub liegt – abgesehen von Dateien, die durch `.gitignore` ausgeschlossen sind (z. B. `__pycache__/`, `.DS_Store`).

## Lokale Kodi-Tests

Die Kodi-Installation liegt außerhalb des Repos (z. B. unter `.kodi/`). Zum Testen des Addons:

- Inhalte von `addons/plugin.program.auto.ftp.sync` nach `.kodi/addons/plugin.program.auto.ftp.sync` kopieren (oder Verzeichnis dort verlinken).
- Skin ggf. ebenso nach `.kodi/addons/skin.arctic.zephyr.doku` kopieren.

Änderungen immer **hier im Repo** machen; danach für den Test nach `.kodi/addons/` übernehmen. So bleibt das Repo die einzige Quelle.

## Push, Tag, Release

```bash
# Nur committen und pushen
./gitpush.sh "Deine Commit-Nachricht"

# Release inkl. Tag (danach auf GitHub Release anlegen)
./gitpush.sh "Release 1.0.0" v1.0.0
```

Das Script baut das Repo (`repo/build_repo.py`), staged alle Änderungen (inkl. `repo/output/`), committet, pusht. Bei zweitem Argument (Tag) wird zusätzlich der Tag erstellt und gepusht; die Ausgabe sagt dir, wie du auf GitHub das Release mit Beschreibung aus dem CHANGELOG anlegst.

## Was nicht auf GitHub geht

- `.gitignore` sorgt dafür, dass z. B. `__pycache__/`, `*.pyc`, `.DS_Store`, `*.log` nicht committed werden.
- `repo/output/` **wird** committed (addons.xml, Addon-ZIPs), damit GitHub Raw die Dateien für Kodi bereitstellen kann.
