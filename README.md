# Auto FTP Sync Plus

**[English](#english)** | **[Deutsch](#deutsch)**

---

<a name="english"></a>
## English

**Auto FTP Sync Plus** is a Kodi addon that keeps your favourites and addon data in sync across devices (FTP, SFTP, SMB), runs backups and restores, rotates menu backgrounds from URLs or network paths, and cleans cache and thumbnails on a schedule. It is used together with the **Arctic Zephyr – Doku-Kanal** skin, which is offered in the same repository.

### Features

- **Sync:** Syncs your favourites (`favourites.xml`) and, optionally, addon_data (packed as ZIP) with a remote server so you can use the same setup on several Kodi devices. Choose what to sync in the addon settings.
- **Protocols:** FTP, SFTP (Kodi xbmcvfs), and SMB (Kodi xbmcvfs). No extra addons needed for SFTP/SMB on supported Kodi builds.
- **Connection profiles:** Up to 3 saved profiles (e.g. Home, Office, NAS), each with name, host, user, password and base path. The **active profile** is selected under **Settings → Connection**; sync always uses that profile.
- **First-run wizard:** On first start, a wizard guides you through enabling sync, choosing main system, connection type, host, credentials and folder. You can run it again from the addon menu under “Run first-time setup again”.
- **Image sources:** Menu background images can rotate from a list of URLs, a local folder, or a network path (SMB/NFS). Configure under **Settings → Images**.
- **Backup/Restore:** Create a full userdata backup as ZIP (saved locally or to a URL). In settings you can include **addon_data** (addon settings, caches). Restore from a local file or from a URL; optionally clear userdata before restore. **Maintenance → Backup** and **Maintenance → Restore** in the addon menu.
- **Auto-Clean:** Automatically deletes cache, packages, thumbnails and log files on a schedule (e.g. daily or weekly) to free space and keep Kodi fast. Configure interval in addon settings.
- **Repository:** Install and update the addon and skin from the **Doku-Kanal** repository (hosted on GitHub). One-time repo ZIP install, then all updates via Kodi’s repository.

### Requirements

- **Kodi 21** (Omega) or newer
- Static favourite folders (Anime, Horror, …) are managed by the addon; no external addon required. Location: `addon_data/plugin.program.auto.ftp.sync/Static Favourites/`
- For SFTP: Kodi with vfs.sftp support (or addon)
- Other addons’ data (e.g. Shortlist) in addon_data is synced when “sync addon_data” is enabled

### Installation (Kodi standard)

Installation order: (1) install the repo addon from ZIP once, (2) enable unknown sources if required, (3) install the addon (and optionally the skin) from the repo. After that, updates are delivered through the repo.

1. **Install the repo addon (one-time)**  
   Download `repository.dokukanal-1.0.0.zip` from [Releases](https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases) (or from the repo `output/` folder). In Kodi go to **Add-ons** → **Add-on browser** (or **Install from zip file**) → **Install from zip file** and select the downloaded ZIP. This installs the Doku-Kanal repository; all future updates come from this repo, no need to download the repo ZIP again.

2. **Unknown sources**  
   If Kodi asks to allow unknown sources, go to **Settings** → **Add-ons** → **Unknown sources** and enable it. This is only needed for the first install from ZIP.

3. **Install addon and skin from the repo**  
   **Add-ons** → **Add-on browser** → **Install from repository** → select **Doku-Kanal** → install **Auto FTP Sync**. Optionally install the skin **Arctic Zephyr – Doku-Kanal** from the same repository (look under Look and feel / Skins or in the program addons list).

4. **Updates**  
   Once the repo is installed, Kodi will check for updates automatically. The repo points to this GitHub repository; you get new addon and skin versions through **Add-ons** → **My add-ons** → **Check for updates** or when Kodi updates on its own.

### Repo URLs (GitHub)

- **addons.xml:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/addons.xml`
- **addons.xml.md5:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/addons.xml.md5`
- **ZIP downloads:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/`

### Versioning

[Semantic Versioning 2.0.0](https://semver.org/) (MAJOR.MINOR.PATCH). First release: **1.0.0**.

### License / Credits

- **Auto FTP Sync:** Doku-Kanal
- **Skin Arctic Zephyr – Doku-Kanal:** Based on Arctic Zephyr (jurialmunkey, beatmasterrs). See skin addon for license.

---

<a name="deutsch"></a>
## Deutsch

**Auto FTP Sync Plus** ist ein Kodi-Addon, das Favoriten und Addon-Daten zwischen Geräten synchron hält (FTP, SFTP, SMB), Backups erstellt und wiederherstellt, Menü-Hintergründe aus URLs oder Netzwerkpfaden rotieren lässt und Cache sowie Thumbnails nach Zeitplan aufräumt. Es wird zusammen mit dem Skin **Arctic Zephyr – Doku-Kanal** genutzt, der im gleichen Repository angeboten wird.

### Features

- **Sync:** Synchronisiert deine Favoriten (`favourites.xml`) und optional addon_data (als ZIP) mit einem Server, damit du dieselbe Konfiguration auf mehreren Kodi-Geräten nutzen kannst. Was synchronisiert wird, stellst du in den Addon-Einstellungen ein.
- **Protokolle:** FTP, SFTP (Kodi xbmcvfs) und SMB (Kodi xbmcvfs). Für SFTP/SMB sind auf unterstützten Kodi-Versionen keine Zusatz-Addons nötig.
- **Verbindungsprofile:** Bis zu 3 gespeicherte Profile (z. B. Zuhause, Büro, NAS) mit Name, Host, Benutzer, Passwort und Basis-Pfad. Das **aktive Profil** wählst du unter **Einstellungen → Verbindung**; der Sync nutzt immer dieses Profil.
- **Ersteinrichtungs-Assistent:** Beim ersten Start führt ein Assistent durch Aktivierung des Syncs, Hauptsystem ja/nein, Verbindungstyp, Host, Zugangsdaten und Ordner. Du kannst ihn im Addon-Menü unter „Ersteinrichtung erneut ausführen“ erneut starten.
- **Bildquellen:** Menü-Hintergrundbilder können aus einer URL-Liste, einem lokalen Ordner oder einem Netzwerkpfad (SMB/NFS) rotieren. Einstellung unter **Einstellungen → Bilder**.
- **Backup/Restore:** Erstellt ein Userdata-Backup als ZIP (lokal oder per URL). In den Einstellungen kannst du **addon_data** (Addon-Einstellungen, Caches) einbeziehen. Wiederherstellung aus lokaler Datei oder von URL; optional vorher userdata bereinigen. **Wartung → Backup** und **Wartung → Wiederherstellung** im Addon-Menü.
- **Auto-Clean:** Löscht automatisch Cache, Packages, Thumbnails und Logs nach Zeitplan (z. B. täglich oder wöchentlich), um Speicher freizugeben und Kodi schlank zu halten. Intervall in den Addon-Einstellungen.
- **Repository:** Addon und Skin werden aus dem **Doku-Kanal**-Repository (GitHub) installiert und aktualisiert. Repo-ZIP einmal installieren, danach alle Updates über das Repository.

### Voraussetzungen

- **Kodi 21** (Omega) oder neuer
- Statische Favoritenordner (Anime, Horror, …) werden vom Addon verwaltet; kein externes Addon nötig. Speicherort: `addon_data/plugin.program.auto.ftp.sync/Static Favourites/`
- Für SFTP: Kodi mit vfs.sftp-Unterstützung (bzw. Addon)
- Daten anderer Addons (z. B. Shortlist) im addon_data werden mit synchronisiert, wenn die Option „addon_data synchronisieren“ aktiviert ist

### Installation (Kodi-Standard)

Reihenfolge: (1) Repo-Addon einmal per ZIP installieren, (2) bei Bedarf „Unbekannte Quellen“ erlauben, (3) Addon (und optional Skin) aus dem Repo installieren. Danach kommen Updates über das Repo.

1. **Repo-Addon einmalig installieren**  
   `repository.dokukanal-1.0.0.zip` von den [Releases](https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases) (oder aus dem Ordner `repo/output/`) herunterladen. In Kodi **Add-ons** → **Addon-Browser** (bzw. **Von ZIP-Datei installieren**) → **Von ZIP-Datei installieren** wählen und die ZIP-Datei auswählen. Damit ist das Doku-Kanal-Repository installiert; alle weiteren Updates kommen über dieses Repo, das Repo-ZIP brauchst du nur einmal.

2. **Unbekannte Quellen**  
   Falls Kodi danach fragt: **Einstellungen** → **Add-ons** → **Unbekannte Quellen** erlauben. Nur für die erste Installation von einer ZIP nötig.

3. **Addon und Skin aus dem Repo installieren**  
   **Add-ons** → **Addon-Browser** → **Addons aus Repository installieren** → **Doku-Kanal** wählen → **Auto FTP Sync** installieren. Optional den Skin **Arctic Zephyr – Doku-Kanal** aus demselben Repository installieren (unter Darstellung/Skins oder bei den Programm-Addons).

4. **Updates**  
   Sobald das Repo installiert ist, prüft Kodi automatisch auf Updates. Das Repo zeigt auf dieses GitHub-Repository; neue Addon- und Skin-Versionen erhältst du über **Add-ons** → **Meine Add-ons** → **Auf Updates prüfen** oder durch die automatische Update-Prüfung von Kodi.

### Repo-URLs (GitHub)

- **addons.xml:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/addons.xml`
- **addons.xml.md5:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/addons.xml.md5`
- **ZIP-Downloads:** `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus-2026/main/repo/output/`

### Versionierung

[Semantic Versioning 2.0.0](https://semver.org/) (MAJOR.MINOR.PATCH). Erstes Release: **1.0.0**.

### Lizenz / Credits

- **Auto FTP Sync:** Doku-Kanal
- **Skin Arctic Zephyr – Doku-Kanal:** Basiert auf Arctic Zephyr (jurialmunkey, beatmasterrs). Lizenz siehe Skin-Addon.
