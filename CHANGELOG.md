# Changelog

Alle wichtigen Änderungen werden hier dokumentiert. Das Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

---

[1.0.0]: https://github.com/benjarogit/Auto-FTP-Sync-Plus/releases/tag/v1.0.0
