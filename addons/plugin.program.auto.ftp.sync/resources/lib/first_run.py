# -*- coding: utf-8 -*-
"""
Ersteinrichtungs-Assistent: Geführter Dialog beim ersten Start.
Setzt Einstellungen und first_run_done-Flag.
"""
import xbmc
import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()


def _l(msg_id):
    return ADDON.getLocalizedString(msg_id)


def run_wizard():
    """
    Zeigt den Ersteinrichtungs-Dialog und schreibt die Werte in die Einstellungen.
    Setzt am Ende first_run_done auf true.
    """
    d = xbmcgui.Dialog()
    # 1) Sync aktivieren?
    enable_sync = d.yesno(_l(30092), _l(30093))
    ADDON.setSettingBool('enable_sync', enable_sync)
    if not enable_sync:
        ADDON.setSettingBool('first_run_done', True)
        d.ok(_l(30092), _l(30094))
        return
    # 2) Hauptsystem?
    is_main = d.yesno(_l(30092), _l(30095))
    ADDON.setSettingBool('is_main_system', is_main)
    # 3) Verbindungstyp
    conn_labels = [_l(30096), _l(30097), _l(30098)]  # FTP, SFTP, SMB
    idx = d.select(_l(30099), conn_labels)
    if idx < 0:
        return
    ADDON.setSettingString('connection_type', str(idx))
    # 4) Host
    host = d.input(_l(30012), type=xbmcgui.INPUT_IPADDRESS)
    if host is None:
        return
    ADDON.setSettingString('ftp_host', host or '')
    # 5) User
    user = d.input(_l(30013))
    if user is None:
        return
    ADDON.setSettingString('ftp_user', user or '')
    # 6) Passwort
    password = d.input(_l(30014), type=xbmcgui.INPUT_PASSWORD)
    if password is None:
        return
    ADDON.setSettingString('ftp_pass', password or '')
    # 7) Basispfad
    base = d.input(_l(30011), default='kodi')
    if base is None:
        return
    ADDON.setSettingString('ftp_base_path', base or '')
    # 8) Benutzerdefinierter Ordnername
    custom = d.input(_l(30006), default='MyDevice')
    if custom is None:
        return
    ADDON.setSettingString('custom_folder', custom or '')
    # 9) Optional: Statische Ordner
    static = d.input(_l(30009), default='')
    if static is not None:
        ADDON.setSettingString('static_folders', static or '')
    # 10) Hinweis Anleitung
    d.ok(_l(30092), _l(30094))
    ADDON.setSettingBool('first_run_done', True)
    xbmc.log("First-run wizard completed.", xbmc.LOGINFO)


def maybe_run():
    """Startet den Assistenten nur, wenn first_run_done noch nicht gesetzt ist."""
    try:
        done = ADDON.getSettingString('first_run_done') == 'true'
        if not done:
            run_wizard()
    except Exception as e:
        xbmc.log(f"First-run wizard: {e}", xbmc.LOGERROR)


def reset_and_run():
    """Setzt first_run_done zurück und startet den Assistenten (Menüpunkt)."""
    ADDON.setSettingBool('first_run_done', False)
    run_wizard()
