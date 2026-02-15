# -*- coding: utf-8 -*-
"""
Static favourites: read and display favourites.xml from addon_data/.../Static Favourites/<folder>/.
Used by plugin.py for mode=static; same storage used by auto_ftp_sync for sync.
"""
import os
import re
import urllib.parse

import xbmcvfs
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

STATIC_FAVOURITES_BASENAME = 'Static Favourites'


def get_static_favourites_path():
    """Return absolute path to the Static Favourites base directory."""
    profile = xbmcvfs.translatePath(ADDON.getAddonInfo('profile'))
    return os.path.join(profile, STATIC_FAVOURITES_BASENAME)


def get_folder_path(folder_name):
    """Return absolute path to the given folder's directory (e.g. .../Static Favourites/Anime)."""
    base = get_static_favourites_path()
    return os.path.join(base, folder_name.strip())


def get_favourites_xml_path(folder_name):
    """Return absolute path to favourites.xml for the given folder."""
    return os.path.join(get_folder_path(folder_name), 'favourites.xml')


def read_favourites(folder_name):
    """
    Read favourites.xml for the given folder and return a list of (name, thumb, command).
    Returns [] if file does not exist or is invalid.
    """
    path = get_favourites_xml_path(folder_name)
    if not path or not xbmcvfs.exists(path):
        return []

    try:
        f = xbmcvfs.File(path, 'rb')
        xml = f.read().decode('utf-8', errors='replace')
        f.close()
    except Exception:
        return []

    # Kodi format: <favourite name="..." thumb="...">command</favourite>
    items = []
    for m in re.finditer(r'<favourite\s+([^>]+)>(.*?)</favourite>', xml, re.DOTALL):
        attrs, body = m.group(1), m.group(2).strip()
        name = ''
        thumb = ''
        for attr in re.finditer(r'(\w+)="([^"]*)"', attrs):
            key, val = attr.group(1).lower(), attr.group(2)
            if key == 'name':
                name = val.replace('&quot;', '"').replace('&amp;', '&')
            elif key == 'thumb':
                thumb = val.replace('&quot;', '"').replace('&amp;', '&')
        cmd = body.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        if name or cmd:
            items.append((name or 'Item', thumb, cmd))
    return items
