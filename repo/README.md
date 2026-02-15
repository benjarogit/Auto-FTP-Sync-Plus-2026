# Kodi-Repository (Doku-Kanal)

Dieses Verzeichnis enthält das Repository-Addon und ein Build-Skript für dein Kodi-Repo. Siehe **README.md** und **CHANGELOG.md** im Projekt-Root für Installation und Versionshistorie. Ausführliche Repo-Einrichtung und Pflege: siehe **REPO_SETUP.md**.

## Struktur

- `repository.dokukanal/` – **Quelle** des Repository-Addons (hier bearbeiten; wird von Nutzern installiert, um dein Repo zu nutzen)
- `build_repo.py` – Skript zum Erzeugen von `addons.xml`, `addons.xml.md5` und Addon-ZIPs
- `output/` – Generierte Dateien (wird beim ersten Lauf erstellt). Kann bei Bedarf geleert werden; beim nächsten `build_repo.py`-Lauf wird alles neu erzeugt.

**Hinweis:** Das Skript kopiert `repo/repository.dokukanal` ggf. nach `addons/repository.dokukanal` (Build-Artefakt). Bearbeitung nur unter `repo/repository.dokukanal`.

## Verwendung

1. **URLs anpassen:** Nach dem Build die Platzhalter-URLs in `repository.dokukanal/addon.xml` durch deine echten **HTTPS**-URLs ersetzen (nur HTTPS verwenden; Kodi warnt bei HTTP):
   - `<info>` → z.B. `https://dein-server.de/kodi/repo/addons.xml`
   - `<checksum>` → z.B. `https://dein-server.de/kodi/repo/addons.xml.md5`
   - `<datadir>` → z.B. `https://dein-server.de/kodi/repo/` (mit abschließendem Schrägstrich)

2. **Repo bauen:** Im Projekt-Root (Auto-FTP-Sync-Plus, dort wo `addons/` und `repo/` liegen) ausführen:
   ```bash
   python3 repo/build_repo.py
   ```
   Die Addon-Quellen für den Build liegen ausschließlich in `addons/`. `.kodi/addons/` dient nur der lokalen Kodi-Installation zum Testen.
   Das Skript erstellt in `repo/output/`:
   - `addons.xml`
   - `addons.xml.md5`
   - `plugin.program.auto.ftp.sync-<version>.zip`
   - `repository.dokukanal-1.0.0.zip`

3. **Hochladen:** Den Inhalt von `repo/output/` auf deinen Server in das unter `<datadir>` angegebene Verzeichnis legen.

4. **Repository-Addon installieren:** Nutzer installieren zuerst die `repository.dokukanal-1.0.0.zip` (z.B. über „Addon aus ZIP installieren“), danach können sie „Auto FTP Sync“ und ggf. den Skin aus dem Repo installieren.

Ausführliche Anleitung (Wo hosten, URLs, Ablauf): siehe **REPO_SETUP.md**.

## Skin mit aufnehmen

Der Skin `skin.arctic.zephyr.doku` ist in `ADDON_IDS` in `build_repo.py` bereits eingetragen und wird mitgebaut. Output: `skin.arctic.zephyr.doku-<version>.zip`.

## Versionen

Aktuelle Funktionen (u. a. SFTP/SMB, Verbindungsprofile, Ersteinrichtungs-Assistent, Bildquellen) siehe **CHANGELOG.md** im Projekt-Root.
