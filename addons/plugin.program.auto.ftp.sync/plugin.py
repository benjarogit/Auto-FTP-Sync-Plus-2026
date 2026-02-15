# -*- coding: utf-8 -*-
"""
Plugin entry point: grouped menu (Sync, Wartung, Info, Einstellungen).
Wartung contains Backup, Restore, Auto-Clean. Info opens the help/info dialog.
"""
import os
import sys
import urllib.parse

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_URL = f"plugin://{ADDON_ID}"
ICON = os.path.join(xbmcvfs.translatePath(ADDON.getAddonInfo('path')), 'resources', 'images', 'icon.png')


def _l(s):
    return ADDON.getLocalizedString(s)


def run_action(action):
    if action == 'backup':
        from resources.lib import backup_restore
        backup_restore.run_backup()
    elif action == 'restore':
        from resources.lib import backup_restore
        backup_restore.run_restore()
    elif action == 'autoclean':
        from resources.lib import auto_clean
        auto_clean.run_auto_clean()
        auto_clean.set_next_run()
        xbmcgui.Dialog().ok(ADDON.getLocalizedString(30001), _l(30047))
    elif action == 'settings':
        ADDON.openSettings()
    elif action == 'info':
        show_info_dialog()
    elif action == 'about':
        show_about_dialog()
    elif action == 'first_run_again':
        from resources.lib import first_run
        first_run.reset_and_run()


def show_info_dialog():
    """Open the scrollable info/help dialog (Anleitung)."""
    title = _l(30073)
    text = _l(30074)
    xbmcgui.Dialog().textviewer(title, text)


def show_about_dialog():
    """Show About dialog: plugin name/version, skin name/version, optional skin-optimized hint."""
    plugin_name = ADDON.getAddonInfo('name')
    plugin_version = ADDON.getAddonInfo('version')
    skin_id = xbmc.getInfoLabel('Skin.Id') or ''
    skin_name = xbmc.getInfoLabel('Skin.Name') or skin_id or _l(30075)
    skin_version = ''
    if skin_id:
        skin_addon = xbmcaddon.Addon(skin_id)
        skin_version = skin_addon.getAddonInfo('version') or ''
    lines = [
        f"Plugin: {plugin_name}",
        f"Version: {plugin_version}",
        f"Skin: {skin_name}",
    ]
    if skin_version:
        lines.append(f"Skin-Version: {skin_version}")
    if skin_id == 'skin.arctic.zephyr.doku':
        lines.append("")
        lines.append(_l(30080))
    text = "[CR]".join(lines)
    xbmcgui.Dialog().textviewer(_l(30079), text)


def add_item(label, action, icon=None):
    if icon is None:
        icon = ICON
    url = f"{ADDON_URL}/?action={action}"
    li = xbmcgui.ListItem(label)
    li.setArt({'icon': icon})
    xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=False)


def add_category_item(label, category_name, icon=None):
    """Add a folder that shows a sublist (category)."""
    url = f"{ADDON_URL}/?action=category&name={category_name}"
    li = xbmcgui.ListItem(label)
    li.setArt({'icon': icon or ICON})
    xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=True)


handle = int(sys.argv[1])
params = urllib.parse.parse_qs(sys.argv[2].lstrip('?'))
action = (params.get('action') or [None])[0]
category = (params.get('name') or [None])[0]
mode = (params.get('mode') or [None])[0]
folder = (params.get('folder') or [None])[0]
path_param = (params.get('path') or [None])[0]
cmd_param = (params.get('cmd') or [None])[0]

# Execute a favourite command (from static folder list)
if action == 'execute' and cmd_param:
    cmd = urllib.parse.unquote_plus(cmd_param)
    if cmd:
        xbmc.executebuiltin(cmd)
    xbmcplugin.endOfDirectory(handle)
    sys.exit(0)

# Static favourites folder listing (mode=static&folder=Anime or path=...)
if mode == 'static':
    from resources.lib import static_favourites
    folder_name = folder
    if not folder_name and path_param:
        path_dec = urllib.parse.unquote_plus(path_param)
        folder_name = path_dec.replace('\\', '/').strip('/').split('/')[-1]
    if folder_name:
        items = static_favourites.read_favourites(folder_name)
        for name, thumb, cmd in items:
            url = f"{ADDON_URL}/?action=execute&cmd={urllib.parse.quote_plus(cmd)}"
            li = xbmcgui.ListItem(label=name)
            if thumb:
                li.setArt({'icon': thumb, 'thumb': thumb})
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)
    sys.exit(0)

# Direct actions (no folder)
if action in ('backup', 'restore', 'autoclean', 'settings', 'info', 'about', 'first_run_again'):
    run_action(action)
    xbmcplugin.endOfDirectory(handle)
elif action == 'category' and category == 'maintenance':
    xbmcplugin.setPluginCategory(handle, _l(30070))
    add_item(_l(30060), 'backup')   # Backup erstellen
    add_item(_l(30063), 'restore')  # Restore aus Backup
    add_item(_l(30051), 'autoclean')
    xbmcplugin.endOfDirectory(handle)
elif action == 'category' and category == 'sync':
    xbmcplugin.setPluginCategory(handle, _l(30069))
    add_item(_l(30071), 'info')
    add_item(_l(30079), 'about')
    add_item(_l(30100), 'first_run_again')
    xbmcplugin.endOfDirectory(handle)
else:
    # Main menu: Sync, Wartung, Info, Einstellungen
    xbmcplugin.setPluginCategory(handle, ADDON.getAddonInfo('name'))
    add_category_item(_l(30069), 'sync')           # Sync
    add_category_item(_l(30070), 'maintenance')    # Wartung
    add_item(_l(30071), 'info')                    # Anleitung & Einrichtung
    add_item(_l(30062), 'settings')                 # Einstellungen
    xbmcplugin.endOfDirectory(handle)
