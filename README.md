# Auto FTP Sync Plus

Kodi-Addon zum automatischen Synchronisieren von Favoriten und addon_data über FTP, SFTP oder SMB – inkl. optionaler Bildrotation, Backup/Restore und Auto-Clean. Dazu der Skin **Arctic Zephyr – Doku-Kanal**, auf die Nutzung mit dem Addon abgestimmt.

## Features

- **Sync:** Favoriten (favourites.xml) und optional addon_data (als ZIP) mit einem Server
- **Protokolle:** FTP, SFTP (xbmcvfs), SMB (xbmcvfs)
- **Verbindungsprofile:** Bis zu 3 Profile (z. B. Zuhause/Büro/NAS); das aktive Profil wählst du in den **Einstellungen → Verbindung**
- **Ersteinrichtungs-Assistent:** Geführter Dialog beim ersten Start
- **Bildquellen:** URL-Liste, lokaler Ordner oder Netzwerkpfad (SMB/NFS) für Hintergrundrotation
- **Backup/Restore:** Userdata als ZIP (lokal oder von URL); Option „addon_data einbeziehen“ in den Einstellungen; Backup und Wiederherstellung im Addon-Menü unter **Wartung**
- **Auto-Clean:** Cache, Packages, Thumbnails, Logs nach Zeitplan
- **Repository:** Installation und Updates über das Doku-Kanal-Repository (GitHub)

## Voraussetzungen

- **Kodi 21** (Omega) oder neuer
- Statische Favoritenordner (Anime, Horror, …) werden vom Addon selbst verwaltet; kein externes Addon nötig. Speicherort: `addon_data/plugin.program.auto.ftp.sync/Static Favourites/`.
- Für SFTP: Kodi mit vfs.sftp-Unterstützung (bzw. Addon)
- Daten anderer Addons (z. B. Shortlist) liegen im addon_data und werden mit synchronisiert, wenn du die Option „addon_data synchronisieren“ aktivierst.

## Installation (Kodi-Standard)

1. **Repo-Addon installieren**  
   Lade `repository.dokukanal-1.0.0.zip` von den [Releases](https://github.com/benjarogit/Auto-FTP-Sync-Plus/releases) oder aus `repo/output/` und installiere es in Kodi über **Add-ons → Addon-Browser → Von ZIP-Datei installieren**.

2. **Unbekannte Quellen**  
   In Kodi: **Einstellungen → Add-ons → Unbekannte Quellen** erlauben (falls noch nicht geschehen).

3. **Addons aus dem Repo**  
   **Add-ons → Addon-Browser → Addons aus Repository installieren** → Repository **Doku-Kanal** wählen → **Auto FTP Sync** und ggf. Skin **Arctic Zephyr – Doku-Kanal** installieren.

4. **Updates**  
   Sobald das Repo-Addon installiert ist, prüft Kodi automatisch auf Updates; die Repo-URLs zeigen auf dieses GitHub-Repository.

## Repo-URLs (GitHub)

Das Repository wird über GitHub Raw-URLs betrieben:

- **addons.xml:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus/main/repo/output/addons.xml`
- **addons.xml.md5:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus/main/repo/output/addons.xml.md5`
- **ZIP-Downloads:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus/main/repo/output/`

## Projektstruktur

- **addons/** – Quellcode von Plugin und Skin  
  - `plugin.program.auto.ftp.sync`  
  - `skin.arctic.zephyr.doku`
- **repo/** – Build-Skript und Repo-Addon  
  - `build_repo.py` – erzeugt addons.xml, addons.xml.md5 und Addon-ZIPs  
  - `repository.dokukanal/` – Repo-Addon (URLs zeigen auf GitHub)  
  - `output/` – Build-Ausgabe (wird für Kodi committed)
- **CHANGELOG.md** – Versionshistorie
- **README.md** – diese Datei

Die Addon-Quellen für Build und GitHub liegen in `addons/`. Für lokale Kodi-Tests kannst du die Inhalte von `addons/plugin.program.auto.ftp.sync` und ggf. den Skin nach `.kodi/addons/` kopieren.

## Build (für Entwickler)

**Repo-Root:** Das geklonte Verzeichnis **Auto-FTP-Sync-Plus** ist das Projekt-Root (dort liegen `addons/`, `repo/`, README, CHANGELOG). Nach dem Klonen von GitHub:

```bash
cd Auto-FTP-Sync-Plus
python3 repo/build_repo.py
```

Die Ausgabe liegt in `repo/output/` (addons.xml, addons.xml.md5, *.zip). Nach einem Release diesen Ordner committen, damit Kodi die neuen Versionen von GitHub laden kann.

## Versionierung

Es gilt [Semantic Versioning 2.0.0](https://semver.org/) (MAJOR.MINOR.PATCH). Erstes Release: **1.0.0**.

## Lizenz / Credits

- **Auto FTP Sync:** Doku-Kanal  
- **Skin Arctic Zephyr – Doku-Kanal:** Basiert auf Arctic Zephyr (jurialmunkey, beatmasterrs). Lizenz siehe Skin-Addon.
