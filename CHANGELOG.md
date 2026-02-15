# Changelog

Alle wichtigen Änderungen werden hier dokumentiert. Das Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.15] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.14.

### English

Release 1.0.15

- Plugin and repo updates since v1.0.14.

---

## [1.0.14] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.13.

### English

Release 1.0.14

- Plugin and repo updates since v1.0.13.

---

## [1.0.13] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.12.

### English

Release 1.0.13

- Plugin and repo updates since v1.0.12.

---

## [1.0.12] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.11.

### English

Release 1.0.12

- Plugin and repo updates since v1.0.11.

---

## [1.0.11] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.10.

### English

Release 1.0.11

- Plugin and repo updates since v1.0.10.

---

## [1.0.10] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.9.

### English

Release 1.0.10

- Plugin and repo updates since v1.0.9.

---

## [1.0.9] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.8.

### English

Release 1.0.9

- Plugin and repo updates since v1.0.8.

---

## [1.0.8] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.7.

### English

Release 1.0.8

- Plugin and repo updates since v1.0.7.

---

## [1.0.7] – 2026-02-15

- Plugin- und Repo-Updates seit v1.0.6.

### English

Release 1.0.7

- Plugin and repo updates since v1.0.6.

---

## [1.0.6] – 2026-02-15

- Release 1.0.6

### English

- Release 1.0.6

---

## [1.0.5] – 2026-02-15

- Update repo output and docs

### English

- Update repo output and docs

---

## [1.0.4] – 2026-02-15

- Release 1.0.4

### English

- Release 1.0.4

---

## [1.0.3] – 2026-02-15

- Release 1.0.3

### English

- Release 1.0.3

---

## [1.0.2] – 2026-02-15

- Repository: Install aus dem Repo („Aus Repo installieren“) funktioniert wieder; SHA256-Hash-Prüfung wurde entfernt, da keine pro-Addon-Hashes in addons.xml vorlagen.
- Keine Änderungen am Plugin- oder Skin-Verhalten.

### English

- Repository: Installation from the repo (“Install from repository”) works again; SHA256 hash verification was removed because addons.xml did not provide per-addon hashes.
- No changes to plugin or skin behaviour.

---

## [1.0.0] – 2025-02-15

Erstes Release: Du kannst Favoriten und addon_data bequem zwischen Geräten synchronisieren, Backups anlegen und die Wartung automatisieren.

### Sync – Was ist neu?

- **FTP, SFTP und SMB:** Du wählst in den Einstellungen den Verbindungstyp (FTP, SFTP oder SMB). Kein separates Addon nötig für SMB/SFTP (Kodi-eigene Funktionen).
- **Verbindungsprofile:** Bis zu 3 Profile (z. B. Zuhause, Büro, NAS) mit Namen, Host, Benutzer, Passwort und Basis-Pfad. Das **aktive Profil** bestimmst du in den Einstellungen unter **Verbindung**; der Sync nutzt immer dieses Profil.
- **Ersteinrichtungs-Assistent:** Beim ersten Start führt dich ein Assistent Schritt für Schritt durch die Einrichtung (Sync aktivieren, Hauptsystem ja/nein, Verbindungstyp, Host, Benutzer, Passwort, Ordner). Den Assistenten kannst du später im Addon-Menü unter „Ersteinrichtung erneut ausführen“ nochmal starten.
- **Bildquellen:** Hintergrundbilder können aus einer URL-Liste, einem lokalen Ordner oder einem Netzwerkpfad (SMB/NFS) rotieren. Einstellungen unter **Bilder**.

### Backup & Restore – Was bringt’s?

- **Backup-Option:** In den Einstellungen kannst du wählen, ob **addon_data** ins Backup einbezogen wird (z. B. Addon-Einstellungen, Caches). Backup erstellen und Wiederherstellung findest du im Addon-Menü unter **Wartung**.
- **Wiederherstellung:** Aus einer lokalen ZIP-Datei oder direkt von einer URL. Optional: vorher userdata bereinigen.

### Wartung – Auto-Clean

- **Auto-Clean** räumt automatisch Cache, Packages, Thumbnails und Logs. Du legst in den Einstellungen fest, wie oft (z. B. täglich, wöchentlich). So bleibt Kodi schlank und schnell.

### Repository & Build

- **Doku-Kanal-Repository:** Das Addon wird über das Repository „Doku-Kanal“ installiert und aktualisiert (GitHub Raw-URLs). Siehe README und REPO_SETUP für die Repo-URLs.
- **Build-Skript:** `repo/build_repo.py` erzeugt addons.xml und Addon-ZIPs in `repo/output/` für GitHub.

### English

First release: Sync favourites and addon_data between devices, create backups, and automate maintenance.

**Sync:** Choose connection type (FTP, SFTP or SMB) in settings; no separate addon needed for SMB/SFTP (Kodi built-in). Up to 3 connection profiles (e.g. Home, Office, NAS) with name, host, user, password and base path; the active profile is set under **Settings → Connection**. First-run wizard guides you through setup; you can run it again from the addon menu under “Run first-time setup again”. Background images can rotate from a URL list, local folder or network path (SMB/NFS); settings under **Images**.

**Backup & Restore:** In settings you can include **addon_data** in backups. Create backup and restore from the addon menu under **Maintenance**; restore from local ZIP or URL, optionally clean userdata first.

**Auto-Clean:** Cleans cache, packages, thumbnails and logs on a schedule (e.g. daily, weekly); configurable in settings.

**Repository:** The addon is installed and updated via the Doku-Kanal repository (GitHub Raw URLs). See README and REPO_SETUP for repo URLs.

---[1.0.4]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.4[1.0.6]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.6[1.0.8]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.8[1.0.10]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.10[1.0.12]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.12[1.0.14]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.14
[1.0.15]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.15

[1.0.13]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.13

[1.0.11]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.11

[1.0.9]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.9

[1.0.7]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.7

[1.0.5]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.5

[1.0.3]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.3

[1.0.2]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.2
[1.0.0]: https://github.com/benjarogit/Auto-FTP-Sync-Plus-2026/releases/tag/v1.0.0
