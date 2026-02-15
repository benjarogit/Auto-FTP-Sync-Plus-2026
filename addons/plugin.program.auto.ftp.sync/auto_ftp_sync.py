# -*- coding: utf-8 -*-
"""
Auto FTP Sync - Kodi service addon.
Syncs favourites and addon_data via FTP, optional image rotation and startup file copies.
Kodi Matrix (Python 3); cross-platform (special://, xbmcvfs).
"""
import os
import random
import urllib.request
import re
import xbmc
import xbmcaddon
import xbmcvfs
import time
import zipfile

#
# =========================
#  1) GRUNDEINSTELLUNGEN
# =========================
#

# Aktivierung
ADDON = xbmcaddon.Addon()
ENABLED = ADDON.getSettingBool('enable_sync')
IS_MAIN_SYSTEM = ADDON.getSettingBool('is_main_system')

# Verbindung: Werte aus aktivem Profil (_get_active_profile_settings)

# Favouriten
OVERWRITE_STATIC = ADDON.getSettingBool('overwrite_static')
CUSTOM_FOLDER = ADDON.getSettingString('custom_folder')
SPECIFIC_CUSTOM_FOLDER = ADDON.getSettingString('specific_custom_folder')

# Pfade (FTP_PATH wird dynamisch aus aktivem Profil gebaut)
ADDON_ID = ADDON.getAddonInfo('id')
LOCAL_FAVOURITES = os.path.join(xbmcvfs.translatePath('special://userdata'), 'favourites.xml')
STATIC_FAVOURITES_PATH = os.path.join(xbmcvfs.translatePath('special://userdata'), 'addon_data', ADDON_ID, 'Static Favourites')
ICON_PATH = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'images', 'icon.png')

# Statische Ordner (leere Einträge entfernt)
STATIC_FOLDERS = [f.strip() for f in ADDON.getSettingString('static_folders').split(',') if f.strip()]

# Bilder
IMAGE_SOURCE_IDX = int(ADDON.getSettingString('image_source') or '0')
IMAGE_LIST_URL = ADDON.getSettingString('image_list_url')
IMAGE_LOCAL_FOLDER = xbmcvfs.translatePath(ADDON.getSettingString('image_local_folder') or '')
IMAGE_NETWORK_PATH = (ADDON.getSettingString('image_network_path') or '').strip()
LOCAL_IMAGE_PATH = os.path.join(xbmcvfs.translatePath('special://userdata'), 'marvel.jpg')
ADDON_IMAGE_PATH = os.path.join(xbmcvfs.translatePath('special://home/addons/plugin.video.xstream'), 'fanart.jpg')
ENABLE_IMAGE_ROTATION = ADDON.getSettingBool('enable_image_rotation')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')

# EXTRA SYNC
ENABLE_ADDON_SYNC = ADDON.getSettingBool('addon_sync')
ENABLE_ADDON_STARTUPFILE = ADDON.getSettingBool('startup_file')

# Mehrsprachigkeit
LANGUAGE = ADDON.getLocalizedString


def _get_active_profile_settings():
    """
    Liest die Einstellungen des aktiven Verbindungsprofils.
    Returns: dict mit connection_type, host, user, password, base_path, sftp_port
    """
    idx = int(ADDON.getSettingString('active_profile') or '0')
    idx = 0 if idx not in (0, 1, 2) else idx
    if idx == 0:
        # Profil 1 (Standard): bisherige Keys
        ct = int(ADDON.getSettingString('connection_type') or '0')
        ct = ('ftp', 'sftp', 'smb')[ct] if 0 <= ct <= 2 else 'ftp'
        return {
            'connection_type': ct,
            'host': ADDON.getSettingString('ftp_host') or '',
            'user': ADDON.getSettingString('ftp_user') or '',
            'password': ADDON.getSettingString('ftp_pass') or '',
            'base_path': ADDON.getSettingString('ftp_base_path') or '',
            'sftp_port': ADDON.getSettingString('sftp_port') or '22',
        }
    if idx == 1:
        prefix = 'profile_2_'
    else:
        prefix = 'profile_3_'
    ct = int(ADDON.getSettingString(prefix + 'connection_type') or '0')
    ct = ('ftp', 'sftp', 'smb')[ct] if 0 <= ct <= 2 else 'ftp'
    return {
        'connection_type': ct,
        'host': ADDON.getSettingString(prefix + 'host') or '',
        'user': ADDON.getSettingString(prefix + 'user') or '',
        'password': ADDON.getSettingString(prefix + 'pass') or '',
        'base_path': ADDON.getSettingString(prefix + 'base_path') or '',
        'sftp_port': ADDON.getSettingString(prefix + 'sftp_port') or '22',
    }


def _get_backend():
    """Return sync backend (FTP/SFTP/SMB) from active profile settings."""
    from resources.lib import sync_backend
    p = _get_active_profile_settings()
    return sync_backend.get_backend(
        p['connection_type'], p['host'], p['user'], p['password'],
        p['base_path'] or '', p['sftp_port']
    )


def _remote_path(*path_parts):
    """Baut Remote-Pfad für Sync (Basis aus aktivem Profil). path_parts ohne führenden Slash."""
    base = (_get_active_profile_settings()['base_path'] or '').strip().strip('/')
    segs = [base, 'auto_fav_sync'] if base else ['auto_fav_sync']
    segs.extend(str(p).strip('/') for p in path_parts if p)
    return '/' + '/'.join(segs)


def show_notification(message_id, duration=5000, **kwargs):
    """
    Zeigt eine Kodi-Notification an.

    Args:
        message_id (int): Die Message-ID für den Lokalisierungstext.
        duration (int): Anzeigedauer in Millisekunden. Standard 5000.
        **kwargs: Optionale Platzhalter für format() im lok. String.

    Returns:
        None
    """
    message = LANGUAGE(message_id).format(**kwargs)
    xbmc.executebuiltin(f'Notification({LANGUAGE(30001)}, {message}, {duration}, {ICON_PATH})')
    time.sleep(duration / 1000)  # Warte, bis die Benachrichtigung abgeschlossen ist


def sync_standard_favourites():
    """
    Synchronisiert die Haupt-Favoriten (favourites.xml).

    Returns:
        bool: True bei Erfolg, sonst False.
    """
    backend = _get_backend()
    ftp_path = _remote_path(CUSTOM_FOLDER, 'favourites.xml')
    if IS_MAIN_SYSTEM:
        return backend.upload(LOCAL_FAVOURITES, ftp_path)
    return backend.download(ftp_path, LOCAL_FAVOURITES)

def sync_static_favourites():
    """
    Synchronisiert statische Favoritenordner (z.B. Anime, Horror).
    Speicherort: addon_data/plugin.program.auto.ftp.sync/Static Favourites/<folder>/favourites.xml

    Returns:
        bool: True wenn mindestens ein Ordner verarbeitet wurde.
    """
    if not STATIC_FOLDERS:
        return False
    backend = _get_backend()
    for folder in STATIC_FOLDERS:
        folder_dir = os.path.join(STATIC_FAVOURITES_PATH, folder)
        if IS_MAIN_SYSTEM:
            if not xbmcvfs.exists(folder_dir):
                xbmcvfs.mkdirs(folder_dir)
        local_static_path = os.path.join(folder_dir, 'favourites.xml')
        remote_static_path = _remote_path(CUSTOM_FOLDER, folder, 'favourites.xml')
        if IS_MAIN_SYSTEM:
            if xbmcvfs.exists(local_static_path):
                backend.upload(local_static_path, remote_static_path)
        else:
            backend.download(remote_static_path, local_static_path)
            if OVERWRITE_STATIC and folder == SPECIFIC_CUSTOM_FOLDER:
                specific_remote_static_path = _remote_path(SPECIFIC_CUSTOM_FOLDER, 'favourites.xml')
                backend.download(specific_remote_static_path, local_static_path)
    return True

def _copy_image_to_targets(source_path):
    """Copy image file from source_path to LOCAL_IMAGE_PATH and ADDON_IMAGE_PATH."""
    try:
        with open(source_path, 'rb') as f:
            img_data = f.read()
        with open(LOCAL_IMAGE_PATH, 'wb') as f:
            f.write(img_data)
        with open(ADDON_IMAGE_PATH, 'wb') as f:
            f.write(img_data)
        return True
    except Exception as e:
        xbmc.log(f"Failed to copy image to targets: {e}", xbmc.LOGERROR)
        return False


def download_random_image():
    """
    Lädt ein zufälliges Bild (URL-Liste, lokaler Ordner oder Netzwerkpfad) und speichert es lokal.

    Returns:
        bool: True bei Erfolg, False wenn kein Bild geladen wurde.
    """
    if not ENABLE_IMAGE_ROTATION:
        return False

    # Bildquelle 0 = URL-Liste
    if IMAGE_SOURCE_IDX == 0:
        if not IMAGE_LIST_URL:
            return False
        try:
            with urllib.request.urlopen(IMAGE_LIST_URL) as response:
                content = response.read().decode('utf-8')
                image_urls = re.findall(r'\[img\](.*?)\[/img\]', content)
                if not image_urls:
                    xbmc.log("No image URLs found in the list", xbmc.LOGERROR)
                    return False
                random_image_url = random.choice(image_urls)
                with urllib.request.urlopen(random_image_url) as img_response:
                    img_data = img_response.read()
                    with open(LOCAL_IMAGE_PATH, 'wb') as f:
                        f.write(img_data)
                    with open(ADDON_IMAGE_PATH, 'wb') as f:
                        f.write(img_data)
                show_notification(30031, 5000)
                return True
        except Exception as e:
            xbmc.log(f"Failed to download random image from URL: {e}", xbmc.LOGERROR)
            return False

    # Bildquelle 1 = Lokaler Ordner
    if IMAGE_SOURCE_IDX == 1:
        if not IMAGE_LOCAL_FOLDER or not os.path.isdir(IMAGE_LOCAL_FOLDER):
            return False
        try:
            files = [f for f in os.listdir(IMAGE_LOCAL_FOLDER)
                     if f.lower().endswith(IMAGE_EXTENSIONS)]
            if not files:
                return False
            chosen = os.path.join(IMAGE_LOCAL_FOLDER, random.choice(files))
            if _copy_image_to_targets(chosen):
                show_notification(30031, 5000)
                return True
        except Exception as e:
            xbmc.log(f"Failed to pick image from local folder: {e}", xbmc.LOGERROR)
        return False

    # Bildquelle 2 = Netzwerkpfad (SMB/NFS)
    if IMAGE_SOURCE_IDX == 2:
        if not IMAGE_NETWORK_PATH:
            return False
        path = IMAGE_NETWORK_PATH.rstrip('/') + '/'
        try:
            dirs, files = xbmcvfs.listdir(path)
            images = [f for f in files if f.lower().endswith(IMAGE_EXTENSIONS)]
            if not images:
                return False
            chosen_name = random.choice(images)
            source_url = path + chosen_name
            f = xbmcvfs.File(source_url, 'rb')
            img_data = f.read()
            f.close()
            with open(LOCAL_IMAGE_PATH, 'wb') as out:
                out.write(img_data)
            with open(ADDON_IMAGE_PATH, 'wb') as out:
                out.write(img_data)
            show_notification(30031, 5000)
            return True
        except Exception as e:
            xbmc.log(f"Failed to pick image from network path: {e}", xbmc.LOGERROR)
        return False

    return False

def copy_custom_startup_file():
    """
    Kopiert eine Custom_Startup.xml in den Skin-Ordner (skin.arctic.zephyr.doku/1080i), falls vorhanden.

    Returns:
        None
    """

    if not ENABLE_ADDON_STARTUPFILE:
        return

    source_path = os.path.join(xbmcvfs.translatePath('special://home/addons/plugin.program.auto.ftp.sync/extras/skin.arctic.zephyr.doku'), 'Custom_Startup.xml')
    destination_folder = xbmcvfs.translatePath('special://home/addons/skin.arctic.zephyr.doku/1080i')
    destination_path = os.path.join(destination_folder, 'Custom_Startup.xml')

    if not os.path.exists(xbmcvfs.translatePath('special://home/addons/skin.arctic.zephyr.doku')):
        xbmc.log("Zielordner für die Custom_Startup.xml existiert nicht. Vorgang wird übersprungen.", xbmc.LOGINFO)
        return

    try:
        # Datei kopieren und überschreiben
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        xbmcvfs.copy(source_path, destination_path)
        xbmc.log(f"Custom_Startup.xml wurde erfolgreich nach {destination_path} kopiert und überschrieben.", xbmc.LOGINFO)
    except Exception as e:
        xbmc.log(f"Fehler beim Kopieren der Custom_Startup.xml: {str(e)}", xbmc.LOGERROR)

def sync_favourites():
    """
    Startet die Synchronisation der Standard-Favoriten sowie der statischen Ordner.

    Returns:
        None
    """
    if not CUSTOM_FOLDER:
        show_notification(30022, 5000)  # Ein benutzerdefinierter Ordnername ist erforderlich
        return

    backend = _get_backend()
    if not backend.folder_exists(_remote_path(CUSTOM_FOLDER)):
        show_notification(30023, 5000, folder=CUSTOM_FOLDER)  # Benutzerdefinierter Ordner nicht gefunden
        return

    # Mach Upload/Download
    result_std = sync_standard_favourites()  # z.B. True/False zurückgeben
    result_stat = sync_static_favourites()   # z.B. True/False

    if result_std or result_stat:
        show_notification(30024, 5000)  # "Favoriten erfolgreich synchronisiert"
    else:
        show_notification(30028, 5000)  # "Fehler bei Favoriten-Sync"

def sync_addon_data():
    """
    Synchronisiert den addon_data-Ordner (lokal -> FTP / FTP -> lokal) mittels einer ZIP-Datei.

    Returns:
        bool: False, wenn die Funktion nicht ausgeführt wurde (z.B. deaktiviert). Sonst kein bestimmter Rückgabewert bei Erfolg.
    """
    if not ENABLE_ADDON_SYNC:
        return False  # Falls auf 'false' gesetzt, abbrechen
    if not CUSTOM_FOLDER and not IS_MAIN_SYSTEM:
        xbmc.log("sync_addon_data: Custom Folder nicht gesetzt, überspringe Download.", xbmc.LOGINFO)
        return False

    xbmc.log("Starte sync_addon_data() mit ZIP-Variante", xbmc.LOGINFO)
    local_base_path = xbmcvfs.translatePath('special://userdata/addon_data')
    local_zip_path = os.path.join(xbmcvfs.translatePath('special://userdata'), 'addon_data.zip')
    remote_zip_path = _remote_path(CUSTOM_FOLDER, 'addon_data.zip')

    def create_zip(source_dir, zip_path):
        """
        Erstellt eine ZIP-Datei von einem Quellverzeichnis.

        Args:
            source_dir (str): Pfad zum Quellordner.
            zip_path (str): Zielpfad für das ZIP.

        Returns:
            None
        """
        try:
            xbmc.log(f"Starte die Erstellung der ZIP-Datei: {zip_path}", xbmc.LOGINFO)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
                        xbmc.log(f"Datei zur ZIP hinzugefügt: {file_path} -> {arcname}", xbmc.LOGINFO)
            xbmc.log(f"ZIP-Datei erstellt: {zip_path}", xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Fehler beim Erstellen der ZIP-Datei: {str(e)}", xbmc.LOGERROR)

    def extract_zip(zip_path, target_dir):
        """
        Entpackt eine ZIP-Datei in ein Zielverzeichnis.

        Args:
            zip_path (str): Pfad zur ZIP-Datei.
            target_dir (str): Zielverzeichnis für das Entpacken.

        Returns:
            None
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(target_dir)
                xbmc.log(f"ZIP-Datei erfolgreich entpackt: {zip_path} -> {target_dir}", xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Fehler beim Entpacken der ZIP-Datei: {str(e)}", xbmc.LOGERROR)

    backend = _get_backend()
    if IS_MAIN_SYSTEM:
        # ================
        # Upload-Zweig
        # ================
        xbmc.log("Hauptsystem erkannt. Beginne ZIP-Erstellung.", xbmc.LOGINFO)
        if os.path.exists(local_base_path):
            create_zip(local_base_path, local_zip_path)
            if os.path.exists(local_zip_path):
                xbmc.log(f"ZIP-Datei vorhanden: {local_zip_path}", xbmc.LOGINFO)
                if backend.upload(local_zip_path, remote_zip_path):
                    xbmc.log(f"ZIP erfolgreich hochgeladen: {remote_zip_path}", xbmc.LOGINFO)
                    os.remove(local_zip_path)
                    show_notification(30020, 5000)  # z.B. "Addon-Daten erfolgreich hochgeladen"
                else:
                    xbmc.log("FTP-Upload fehlgeschlagen.", xbmc.LOGERROR)
                    show_notification(30029, 5000)  # z.B. "Fehler beim Upload"
            else:
                xbmc.log(f"FEHLER: ZIP-Datei wurde nicht erstellt: {local_zip_path}", xbmc.LOGERROR)
        else:
            xbmc.log("Lokaler Ordner 'addon_data' existiert nicht.", xbmc.LOGERROR)

    else:
        # ===================
        # Download-Zweig
        # ===================
        xbmc.log("Kein Hauptsystem. Versuche ZIP herunterzuladen.", xbmc.LOGINFO)
        # 1. ZIP herunterladen
        if backend.download(remote_zip_path, local_zip_path):
            xbmc.log(f"ZIP-Datei vom Server heruntergeladen: {local_zip_path}", xbmc.LOGINFO)

            # 2. ZIP entpacken ins addon_data-Verzeichnis
            extract_zip(local_zip_path, local_base_path)

            # 3. Lokale ZIP wieder löschen
            if os.path.exists(local_zip_path):
                os.remove(local_zip_path)
                xbmc.log(f"Lokale ZIP-Datei gelöscht: {local_zip_path}", xbmc.LOGINFO)
            show_notification(30025, 5000)  # "Addon-Daten heruntergeladen & entpackt"
        else:
            xbmc.log("ZIP-Download vom FTP fehlgeschlagen.", xbmc.LOGERROR)
            show_notification(30021, 5000)  # "Fehler beim Herunterladen"

#
# =========================
#   Hauptablauf (Start-up-Reihenfolge)
# =========================
# 0) Ersteinrichtungs-Assistent (nur wenn first_run_done nicht gesetzt)
# 1) Auto-Clean (wenn aktiv und fällig)
# 2) FTP-Sync (addon_data, Favoriten), Bildrotation, Custom_Startup, uservar
# 3) Texture-Cache leeren, ReloadSkin
#
try:
    from resources.lib import first_run
    first_run.maybe_run()
except Exception as e:
    xbmc.log(f"First-run wizard: {e}", xbmc.LOGERROR)

if ENABLED:
    from resources.lib import auto_clean
    xbmc.log("Funktionen werden ausgeführt.", xbmc.LOGINFO)
    # 1) Auto-Clean zuerst (wenn aktiv und fällig)
    try:
        auto_clean.run_if_due()
    except Exception as e:
        xbmc.log(f"Auto-Clean: {e}", xbmc.LOGERROR)
    # 2) Sync und Optionen
    sync_addon_data()
    sync_favourites()
    download_random_image()
    copy_custom_startup_file()
    # 3) Texture-Cache und UI
    auto_clean.clear_thumbs()
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.executebuiltin('Container.Refresh()')
