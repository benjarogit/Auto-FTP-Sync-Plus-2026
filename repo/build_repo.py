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
                rel = full.relative_to(src)
                # Kodi expects first ZIP entry to be the addon-id folder (repository.dokukanal/...)
                arc = f"{addon_id}/{rel.as_posix()}"
                zf.write(full, arc)
    return zip_name


def _normalize_zip_name(n: str) -> str:
    return n.replace("\\", "/")


def validate_addon_zip(zip_path: Path, addon_id: str) -> list[str]:
    """
    Validate addon ZIP: structure (Kodi expects addon-id folder first), addon.xml
    well-formed and required fields, and that referenced assets exist in the ZIP.
    Returns list of error messages; empty if valid.
    """
    errors: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = [n.replace("\\", "/") for n in zf.namelist()]

    if not names:
        errors.append("ZIP is empty")
        return errors

    # 1) Structure: first entry must be addon_id/...
    first = names[0]
    if not first.startswith(addon_id + "/"):
        errors.append(f"First ZIP entry must be '{addon_id}/...', got: {first}")

    addon_xml_path = f"{addon_id}/addon.xml"
    if addon_xml_path not in names:
        errors.append(f"ZIP must contain '{addon_xml_path}'")
        return errors  # cannot continue without addon.xml

    # 2) Parse addon.xml (syntax + content)
    with zipfile.ZipFile(zip_path, "r") as zf:
        try:
            xml_bytes = zf.read(addon_xml_path)
            root = ET.fromstring(xml_bytes)
        except ET.ParseError as e:
            errors.append(f"addon.xml is not valid XML: {e}")
            return errors

    if root.tag != "addon":
        errors.append(f"addon.xml root element must be <addon>, got <{root.tag}>")

    xml_id = root.get("id")
    if not xml_id:
        errors.append("addon.xml: missing attribute 'id'")
    elif xml_id != addon_id:
        errors.append(f"addon.xml: id must be '{addon_id}', got '{xml_id}'")

    version = root.get("version")
    if not version or not version.strip():
        errors.append("addon.xml: missing or empty 'version'")
    else:
        v = version.strip()
        if not all(c in "0123456789." for c in v.replace(".", "")):
            errors.append(f"addon.xml: version should be numeric (e.g. 1.0.0), got '{version}'")

    if not (root.get("name") or "").strip():
        errors.append("addon.xml: missing or empty 'name'")

    # 3) Referenced assets (icon, fanart, screenshots) must exist in ZIP
    prefix = addon_id + "/"
    zip_set = set(names)
    for ext in root.findall(".//extension[@point='xbmc.addon.metadata']"):
        assets = ext.find("assets")
        if assets is None:
            continue
        for tag in ("icon", "fanart", "screenshot"):
            for node in assets.findall(tag):
                if node.text:
                    path_in_zip = prefix + node.text.strip().replace("\\", "/")
                    if path_in_zip not in zip_set:
                        errors.append(f"addon.xml references missing file: {node.text.strip()}")

    return errors


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
            zip_path = out_dir / zip_name
            val_errors = validate_addon_zip(zip_path, addon_id)
            if val_errors:
                raise SystemExit(
                    f"Validation failed: {zip_name}\n  " + "\n  ".join(val_errors)
                )
            print(f"Created {zip_name}")
        except SystemExit:
            raise
        except Exception as e:
            print(f"ZIP {addon_id}: {e}")
    build_addons_xml(out_dir)
    build_md5(out_dir)
    print("Done. Upload contents of", out_dir, "to your server and set repo URLs in repository addon.")


if __name__ == "__main__":
    main()
