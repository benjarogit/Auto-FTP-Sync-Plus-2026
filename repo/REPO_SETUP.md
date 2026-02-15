# Repo einrichten und pflegen (Doku-Kanal)

Diese Anleitung beschreibt, wo du das Repo hostest, was du hochlädst und wie Nutzer es verwenden.

**Dieses Projekt:** Das Repository wird über **GitHub Raw-URLs** betrieben. Die URLs in `repository.dokukanal/addon.xml` zeigen auf `https://raw.githubusercontent.com/benjarogit/Auto-FTP-Sync-Plus/main/repo/output/`. Der Inhalt von `repo/output/` wird nach jedem Release committed, damit Kodi die Addons von GitHub laden kann.

## 1. Wo das Repo liegt

Das Repo ist ein **normales Verzeichnis auf einem Webserver** (eigener Server, Webspace, GitHub Releases o. ä.). Wichtig: Erreichbar per **HTTP/HTTPS** (HTTPS empfohlen). Beispiele:

- `https://dein-server.de/kodi/repo/`
- Ein Ordner auf deinem Webspace
- GitHub Releases, wenn du feste ZIP-URLs nutzt

## 2. Verzeichnisstruktur auf dem Server (nach Upload)

Der **gesamte Inhalt** von `repo/output/` kommt in **ein** Verzeichnis auf dem Server, z. B.:

- `addons.xml`
- `addons.xml.md5`
- `plugin.program.auto.ftp.sync-1.0.x.zip`
- `repository.dokukanal-1.0.0.zip`
- `skin.arctic.zephyr.doku-3.0.3.zip` (falls Skin mitgebaut wird)

Keine Unterordner nötig – Kodi erwartet die ZIPs und die beiden XML-Dateien im gleichen Verzeichnis wie die `<datadir>`-URL.

## 3. URLs in repository.dokukanal eintragen

Nach dem Build die Platzhalter in `repository.dokukanal/addon.xml` durch deine echten **HTTPS**-URLs ersetzen (Kodi empfiehlt HTTPS; bei HTTP erscheint eine Warnung):

- **`<info>`** = direkte URL zu `addons.xml`, z. B. `https://dein-server.de/kodi/repo/addons.xml`
- **`<checksum>`** = direkte URL zu `addons.xml.md5`, z. B. `https://dein-server.de/kodi/repo/addons.xml.md5`
- **`<datadir>`** = Basis-URL des Repo-Ordners **mit abschließendem Schrägstrich**, z. B. `https://dein-server.de/kodi/repo/`

Kodi lädt zuerst `addons.xml` und `addons.xml.md5`; die ZIP-URLs werden aus `<datadir>` + Addon-ID + Version gebildet.

## 4. Ablauf für dich (einmalig / bei Updates)

1. **Lokal bauen:** Im Repo-Root (Auto-FTP-Sync-Plus) ausführen:
   ```bash
   python3 repo/build_repo.py
   ```
2. **Hochladen:** Den Inhalt von `repo/output/` per FTP/SFTP/rsync/scp in das Repo-Verzeichnis auf dem Server legen. Bestehende `addons.xml`, `addons.xml.md5` und geänderte ZIPs überschreiben.
3. Es ist kein separates „Repo anlegen“ auf dem Server nötig – Verzeichnis anlegen + Upload **ist** das Repo.

## 5. Ablauf für Nutzer

1. **Einmalig:** `repository.dokukanal-1.0.0.zip` manuell installieren („Addon aus ZIP installieren“).
2. In Kodi: Addons → Addon-Installation aus unbekannten Quellen erlauben (falls noch nicht geschehen).
3. Repo „Doku-Kanal“ erscheint; „Auto FTP Sync“ (und ggf. Skin „Arctic Zephyr – Doku-Kanal“) aus dem Repo installieren oder aktualisieren.
4. **Updates:** Sobald das Repo installiert ist, prüft Kodi automatisch auf Addon-Updates. Neue Versionen von Auto FTP Sync und Skin erscheinen unter Addons → Updates bzw. beim Aufruf des Repos – vorausgesetzt, die Repo-URLs auf deinem Server sind korrekt und du hast nach einem Release `build_repo.py` ausgeführt und den Inhalt von `output/` erneut hochgeladen.

## Hinweise

- **Kodi-Version:** Auto FTP Sync benötigt Kodi 21 (Omega) oder neuer.
- Nach Änderung von `addons.xml` ändert sich die MD5 – Kodi erkennt Updates dann korrekt.
- Bei CDN oder speziellem Server ggf. CORS/Cache beachten.
