# -*- coding: utf-8 -*-
"""
Backup and Restore (ZIP snapshot) for Kodi userdata / full home.
Uses addon settings for paths; no dependency on Open Wizard CONFIG.
Supports restore from local file or from URL.
"""
import os
import re
import zipfile
import urllib.request
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
HOME = xbmcvfs.translatePath('special://home')
USERDATA = xbmcvfs.translatePath('special://userdata')

# Excludes (folder names or path fragments)
EXCLUDE_DIRS = ['cache', 'temp', 'packages', 'archive_cache']
EXCLUDE_FILES = ['kodi.log', 'kodi.old.log', 'xbmc.log', 'xbmc.old.log', '.DS_Store']
LOG_PREFIX = "[BackupRestore]"


def _get_backup_path():
    path = ADDON.getSettingString('backup_path')
    if path:
        return xbmcvfs.translatePath(path)
    return os.path.join(HOME, 'backups')


def _get_restore_path():
    path = ADDON.getSettingString('restore_path')
    if path:
        return xbmcvfs.translatePath(path)
    return HOME


def _download_zip_from_url(url, target_path, progress_dialog=None):
    """
    Download a ZIP file from url to target_path.
    progress_dialog: optional xbmcgui.DialogProgress to update.
    Returns True on success, False on failure.
    """
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Kodi-Addon'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            total = int(resp.headers.get('Content-Length', 0)) or None
            read_so_far = 0
            chunk_size = 65536
            with open(target_path, 'wb') as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    read_so_far += len(chunk)
                    if progress_dialog and total and total > 0:
                        pct = min(100, int(read_so_far / total * 100))
                        progress_dialog.update(pct, ADDON.getLocalizedString(30067))
        return True
    except Exception as e:
        xbmc.log(f"{LOG_PREFIX} Download failed: {e}", xbmc.LOGERROR)
        return False


def _sanitize_name(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip() or 'backup'


def _format_size(size):
    for u in ('B', 'KB', 'MB', 'GB'):
        if size < 1024:
            return f"{size:.1f} {u}"
        size /= 1024
    return f"{size:.1f} TB"


def create_backup(include_addon_data=True, target_base=None):
    """
    Create a ZIP backup of userdata (or full home if desired).
    Uses backup_path from settings; optional dialog for name.
    """
    dialog = xbmcgui.Dialog()
    progress = xbmcgui.DialogProgress()
    backup_base = target_base or _get_backup_path()
    try:
        if not os.path.isdir(backup_base):
            os.makedirs(backup_base, exist_ok=True)
    except OSError as e:
        xbmc.log(f"{LOG_PREFIX} Cannot create backup dir: {e}", xbmc.LOGERROR)
        dialog.ok(ADDON.getLocalizedString(30038), ADDON.getLocalizedString(30043))
        return False

    name = dialog.input(ADDON.getLocalizedString(30039), type=xbmcgui.INPUT_ALPHANUM)
    if not name:
        return False
    name = _sanitize_name(name)
    zip_path = os.path.join(backup_base, f"{name}.zip")
    source_root = USERDATA  # backup userdata (guisettings, addon_data, etc.)
    exclude_dirs = list(EXCLUDE_DIRS)
    if not include_addon_data:
        exclude_dirs.append('addon_data')

    # Collect files
    to_add = []
    for root, dirs, files in os.walk(source_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_root = os.path.relpath(root, source_root)
        if rel_root == '.':
            rel_root = ''
        for f in files:
            if f in EXCLUDE_FILES or f.startswith('._') or f.lower().endswith('.pyo'):
                continue
            to_add.append((os.path.join(root, f), os.path.join(rel_root, f) if rel_root else f))

    total = len(to_add)
    if total == 0:
        dialog.ok(ADDON.getLocalizedString(30038), ADDON.getLocalizedString(30044))
        return False

    progress.create(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30040))
    written = 0
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
            for i, (abs_path, arcname) in enumerate(to_add):
                if progress.iscanceled():
                    progress.close()
                    if os.path.exists(zip_path):
                        try:
                            os.remove(zip_path)
                        except OSError:
                            pass
                    return False
                try:
                    zf.write(abs_path, os.path.join('userdata', arcname))
                    written += 1
                except Exception as e:
                    xbmc.log(f"{LOG_PREFIX} Skip {arcname}: {e}", xbmc.LOGERROR)
                pct = int((i + 1) / total * 100)
                progress.update(pct, f"{i + 1} / {total}\n{arcname}")
        progress.close()
        size = os.path.getsize(zip_path)
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30041).format(path=zip_path, size=_format_size(size)))
        return True
    except Exception as e:
        progress.close()
        xbmc.log(f"{LOG_PREFIX} Backup failed: {e}", xbmc.LOGERROR)
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30042).format(err=str(e)))
        return False


def restore_from_zip(zip_path=None, wipe_first=False):
    """
    Restore from a ZIP file into userdata (or home).
    zip_path: full path to zip; if None, show browse dialog.
    """
    dialog = xbmcgui.Dialog()
    progress = xbmcgui.DialogProgress()
    if not zip_path:
        zip_path = dialog.browseSingle(1, ADDON.getLocalizedString(30045), 'files', mask='.zip', useThumbs=False)
    if not zip_path or not zip_path.endswith('.zip'):
        return False
    zip_path = xbmcvfs.translatePath(zip_path) if zip_path.startswith('special://') else zip_path
    if not os.path.exists(zip_path):
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30042).format(err="File not found"))
        return False

    if wipe_first:
        # Optional: clear cache/temp only to avoid conflicts
        cache_path = xbmcvfs.translatePath('special://temp')
        if os.path.exists(cache_path):
            try:
                for entry in os.listdir(cache_path):
                    full = os.path.join(cache_path, entry)
                    if os.path.isfile(full):
                        os.remove(full)
                    elif os.path.isdir(full) and entry != 'archive_cache':
                        import shutil
                        shutil.rmtree(full, ignore_errors=True)
            except Exception as e:
                xbmc.log(f"{LOG_PREFIX} Wipe temp: {e}", xbmc.LOGERROR)

    progress.create(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30046))
    extract_root = HOME  # ZIP contains "userdata/..." so extract to home
    errors = []
    try:
        with zipfile.ZipFile(zip_path, 'r', allowZip64=True) as zf:
            names = [n for n in zf.namelist() if not n.endswith('/')]
            total = len(names)
            for i, name in enumerate(names):
                if progress.iscanceled():
                    progress.close()
                    return False
                # Skip paths targeting this addon's data if we want to avoid overwriting ourselves
                if ADDON_ID in name and 'addon_data' in name:
                    continue
                try:
                    zf.extract(name, extract_root)
                except Exception as e:
                    errors.append(f"{name}: {e}")
                    xbmc.log(f"{LOG_PREFIX} Extract error {name}: {e}", xbmc.LOGERROR)
                pct = int((i + 1) / total * 100)
                progress.update(pct, f"{i + 1} / {total}\n{name}")
        progress.close()
        msg = ADDON.getLocalizedString(30047)
        if errors:
            msg += "\n" + ADDON.getLocalizedString(30048).format(count=len(errors))
        dialog.ok(ADDON.getLocalizedString(30001), msg)
        return True
    except zipfile.BadZipFile as e:
        progress.close()
        xbmc.log(f"{LOG_PREFIX} Bad zip: {e}", xbmc.LOGERROR)
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30042).format(err=str(e)))
        return False
    except Exception as e:
        progress.close()
        xbmc.log(f"{LOG_PREFIX} Restore failed: {e}", xbmc.LOGERROR)
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30042).format(err=str(e)))
        return False


def run_backup():
    """Entry: create backup; include addon_data from setting."""
    include_addon_data = ADDON.getSettingBool('backup_include_addon_data')
    create_backup(include_addon_data=include_addon_data)


def run_restore():
    """Entry: choose local file or URL, then restore; optional wipe."""
    dialog = xbmcgui.Dialog()
    choices = [ADDON.getLocalizedString(30064), ADDON.getLocalizedString(30065)]
    idx = dialog.select(ADDON.getLocalizedString(30038), choices)
    if idx < 0:
        return
    wipe = ADDON.getSettingBool('restore_wipe')
    if dialog.yesno(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30050)):
        wipe = True

    if idx == 0:
        # Local file
        restore_from_zip(zip_path=None, wipe_first=wipe)
        return

    # URL
    url = dialog.input(ADDON.getLocalizedString(30066), type=xbmcgui.INPUT_ALPHANUM)
    if not url or not url.strip():
        return
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30068))
        return

    temp_dir = xbmcvfs.translatePath('special://temp')
    temp_zip = os.path.join(temp_dir, 'restore_download.zip')
    progress = xbmcgui.DialogProgress()
    progress.create(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30067))
    if not _download_zip_from_url(url, temp_zip, progress_dialog=progress):
        progress.close()
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30068))
        return
    progress.close()

    if not os.path.exists(temp_zip) or not temp_zip.endswith('.zip'):
        dialog.ok(ADDON.getLocalizedString(30001), ADDON.getLocalizedString(30068))
        return
    try:
        restore_from_zip(zip_path=temp_zip, wipe_first=wipe)
    finally:
        if os.path.exists(temp_zip):
            try:
                os.remove(temp_zip)
            except OSError:
                pass
