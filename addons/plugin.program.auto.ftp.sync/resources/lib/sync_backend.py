# -*- coding: utf-8 -*-
"""
Sync backends: FTP, SFTP (via xbmcvfs if vfs.sftp present), SMB (via xbmcvfs).
Each backend provides: upload(local_path, remote_path), download(remote_path, local_path), folder_exists(remote_path).
"""
import ftplib
from urllib.parse import quote
import xbmc
import xbmcvfs


def _norm_ftp_path(path):
    """Ensure path starts with / for FTP."""
    path = path.replace('\\', '/')
    return path if path.startswith('/') else '/' + path


class FTPBackend:
    """FTP backend using ftplib."""
    def __init__(self, host, user, password, base_path):
        self.host = host
        self.user = user
        self.password = password
        self.base_path = _norm_ftp_path(base_path.rstrip('/'))

    def _remote(self, path):
        p = path.replace('\\', '/')
        return p if p.startswith('/') else self.base_path + '/' + p.lstrip('/')

    def upload(self, local_path, remote_path):
        try:
            remote = self._remote(remote_path)
            with ftplib.FTP(self.host) as ftp:
                ftp.login(self.user, self.password)
                with open(local_path, 'rb') as f:
                    ftp.storbinary('STOR ' + remote, f)
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] FTP upload failed: {e}", xbmc.LOGERROR)
            return False

    def download(self, remote_path, local_path):
        try:
            remote = self._remote(remote_path)
            with ftplib.FTP(self.host) as ftp:
                ftp.login(self.user, self.password)
                with open(local_path, 'wb') as f:
                    ftp.retrbinary('RETR ' + remote, f.write)
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] FTP download failed: {e}", xbmc.LOGERROR)
            return False

    def folder_exists(self, remote_path):
        try:
            remote = self._remote(remote_path)
            with ftplib.FTP(self.host) as ftp:
                ftp.login(self.user, self.password)
                ftp.cwd(remote)
            return True
        except ftplib.error_perm as e:
            if '550' in str(e):
                return False
            xbmc.log(f"[AutoFTP] FTP error: {e}", xbmc.LOGERROR)
            return False
        except Exception as e:
            xbmc.log(f"[AutoFTP] FTP folder_exists failed: {e}", xbmc.LOGERROR)
            return False


class SFTPBackend:
    """SFTP backend using xbmcvfs (requires vfs.sftp addon). Remote path: absolute path on server."""
    def __init__(self, host, user, password, base_path, port=22):
        self.host = host
        self.port = int(port) if port else 22
        self.user = quote(user or '', safe='')
        self.password = quote(password or '', safe='')
        self._prefix = f"sftp://{self.user}:{self.password}@{host}:{self.port}/"

    def _remote_url(self, remote_path):
        p = (remote_path or '').replace('\\', '/').strip('/')
        return self._prefix + p if p else self._prefix.rstrip('/') + '/'

    def upload(self, local_path, remote_path):
        url = self._remote_url(remote_path)
        try:
            with open(local_path, 'rb') as f:
                data = f.read()
            f = xbmcvfs.File(url, 'wb')
            f.write(data)
            f.close()
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] SFTP upload failed: {e}", xbmc.LOGERROR)
            return False

    def download(self, remote_path, local_path):
        url = self._remote_url(remote_path)
        try:
            f = xbmcvfs.File(url, 'rb')
            data = f.read()
            f.close()
            with open(local_path, 'wb') as out:
                out.write(data)
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] SFTP download failed: {e}", xbmc.LOGERROR)
            return False

    def folder_exists(self, remote_path):
        try:
            url = self._remote_url(remote_path)
            if not url.endswith('/'):
                url += '/'
            dirs, files = xbmcvfs.listdir(url)
            return True
        except Exception:
            return False


class SMBBackend:
    """SMB backend using xbmcvfs. remote_path = share/path (e.g. myshare/kodi/auto_fav_sync/...)."""
    def __init__(self, host, user, password, base_path):
        self.host = host
        self.user = quote(user or '', safe='')
        self.password = quote(password or '', safe='')
        self._prefix = f"smb://{self.user}:{self.password}@{host}/"

    def _remote_url(self, remote_path):
        p = (remote_path or '').replace('\\', '/').strip('/')
        return self._prefix + p if p else self._prefix.rstrip('/') + '/'

    def upload(self, local_path, remote_path):
        url = self._remote_url(remote_path)
        try:
            with open(local_path, 'rb') as f:
                data = f.read()
            f = xbmcvfs.File(url, 'wb')
            f.write(data)
            f.close()
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] SMB upload failed: {e}", xbmc.LOGERROR)
            return False

    def download(self, remote_path, local_path):
        url = self._remote_url(remote_path)
        try:
            f = xbmcvfs.File(url, 'rb')
            data = f.read()
            f.close()
            with open(local_path, 'wb') as out:
                out.write(data)
            return True
        except Exception as e:
            xbmc.log(f"[AutoFTP] SMB download failed: {e}", xbmc.LOGERROR)
            return False

    def folder_exists(self, remote_path):
        try:
            url = self._remote_url(remote_path)
            if not url.endswith('/'):
                url += '/'
            dirs, files = xbmcvfs.listdir(url)
            return True
        except Exception:
            return False


def get_backend(connection_type, host, user, password, base_path, sftp_port='22'):
    """
    Return a sync backend. connection_type: 'ftp', 'sftp', 'smb'.
    """
    ct = (connection_type or 'ftp').strip().lower()
    if ct == 'sftp':
        return SFTPBackend(host, user, password, base_path, port=sftp_port)
    if ct == 'smb':
        return SMBBackend(host, user, password, base_path)
    return FTPBackend(host, user, password, base_path)
