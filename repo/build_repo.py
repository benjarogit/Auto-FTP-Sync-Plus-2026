#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Kodi repository: create addons.xml, addons.xml.md5, and ZIPs for each addon.
Run from project root with: python3 repo/build_repo.py
Addons to include: plugin.program.auto.ftp.sync, repository.dokukanal, skin.arctic.zephyr.doku.
Output: addons.xml, addons.xml.md5, *.zip in repo/output/.
Output in repo/output/ is used for the GitHub repository; commit it after each release.
"""
import hashlib
import os
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Paths relative to repo/
REPO_DIR = Path(__file__).resolve().parent
ADDONS_SOURCE = REPO_DIR.parent / "addons"  # .kodi/addons
OUTPUT_DIR = REPO_DIR / "output"
ADDON_IDS = [
    "plugin.program.auto.ftp.sync",
    "repository.dokukanal",
    "skin.arctic.zephyr.doku",
]


def make_zip(addon_id: str, out_dir: Path) -> str:
    """Create ZIP for addon_id; return path to zip."""
    src = ADDONS_SOURCE / addon_id
    if not src.is_dir():
        raise FileNotFoundError(f"Addon folder not found: {src}")
    addon_xml = src / "addon.xml"
    if not addon_xml.exists():
        raise FileNotFoundError(f"addon.xml not found in {src}")
    tree = ET.parse(addon_xml)
    root = tree.getroot()
    version = root.get("version", "1.0.0")
    zip_name = f"{addon_id}-{version}.zip"
    zip_path = out_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for root_dir, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                if f.endswith(".zip"):
                    continue
                full = Path(root_dir) / f
                arc = full.relative_to(src)
                zf.write(full, arc)
    return zip_name


def get_addon_xml_string(addon_id: str) -> str:
    """Return full content of addon.xml for addon_id."""
    path = ADDONS_SOURCE / addon_id / "addon.xml"
    if not path.exists():
        # Repository addon might be in repo/repository.dokukanal
        path = REPO_DIR / addon_id / "addon.xml"
    if not path.exists():
        raise FileNotFoundError(f"addon.xml not found for {addon_id}")
    return path.read_text(encoding="utf-8").strip()


def build_addons_xml(out_dir: Path) -> None:
    """Build addons.xml from all addon.xml files."""
    addons = []
    for addon_id in ADDON_IDS:
        try:
            xml_str = get_addon_xml_string(addon_id)
            # Wrap in addon tag if not already (addon.xml is a single <addon>)
            if not xml_str.lstrip().startswith("<?xml"):
                xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml_str
            addons.append(xml_str)
        except FileNotFoundError as e:
            print(f"Skip {addon_id}: {e}")
    addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
    for a in addons:
        # Extract inner <addon>...</addon> from file (strip XML decl if present)
        a = a.strip()
        if a.startswith("<?xml"):
            a = a.split("?>", 1)[-1].strip()
        addons_xml += a + "\n"
    addons_xml += "</addons>\n"
    out_path = out_dir / "addons.xml"
    out_path.write_text(addons_xml, encoding="utf-8")
    print(f"Wrote {out_path}")


def build_md5(out_dir: Path) -> None:
    """Build addons.xml.md5 from addons.xml."""
    xml_path = out_dir / "addons.xml"
    if not xml_path.exists():
        raise FileNotFoundError("addons.xml not found; run build_addons_xml first")
    data = xml_path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    (out_dir / "addons.xml.md5").write_text(md5, encoding="utf-8")
    print(f"Wrote {out_dir / 'addons.xml.md5'} ({md5})")


def main():
    import shutil
    out_dir = OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    repo_addon_src = REPO_DIR / "repository.dokukanal"
    repo_addon_dest = ADDONS_SOURCE / "repository.dokukanal"
    # Ensure repo addon has an icon (copy from script addon if missing)
    repo_icon = repo_addon_src / "icon.png"
    if not repo_icon.exists():
        src_icon = ADDONS_SOURCE / "plugin.program.auto.ftp.sync" / "resources" / "images" / "icon.png"
        if src_icon.exists():
            shutil.copy2(src_icon, repo_icon)
            print(f"Copied icon to {repo_icon}")
    # Copy repository addon from repo/ to addons so it can be zipped
    if repo_addon_src.is_dir() and not repo_addon_dest.is_dir():
        shutil.copytree(repo_addon_src, repo_addon_dest)
        print(f"Copied repository addon to {repo_addon_dest}")
    for addon_id in ADDON_IDS:
        try:
            zip_name = make_zip(addon_id, out_dir)
            print(f"Created {zip_name}")
        except Exception as e:
            print(f"ZIP {addon_id}: {e}")
    build_addons_xml(out_dir)
    build_md5(out_dir)
    print("Done. Upload contents of", out_dir, "to your server and set repo URLs in repository addon.")


if __name__ == "__main__":
    main()
