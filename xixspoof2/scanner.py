import re, xml.etree.ElementTree as ET
from .logutil import info
RE_INT_ID   = re.compile(r"\b(\d{3,})\b")
RE_URL      = re.compile(r"rbxassetid://(\d+)")
RE_WEB      = re.compile(r"https?://www\.roblox\.com/asset/\?id=(\d+)")
def _iter_instance_nodes(root):
    for tag in ("Item","Instance"):
        for node in root.iter(tag):
            yield node
def scan_xml(xml_text: str):
    ids=set()
    try:
        root=ET.fromstring(xml_text)
    except Exception:
        for m in RE_URL.finditer(xml_text): ids.add(m.group(1))
        for m in RE_WEB.finditer(xml_text): ids.add(m.group(1))
        return ids
    for node in _iter_instance_nodes(root):
        props=node.find("Properties")
        if props is None: continue
        for c in list(props):
            n=(c.get("name") or c.get("Name") or "").lower()
            if n=="animationid":
                val=(c.text or "").strip()
                m=RE_URL.search(val) or RE_WEB.search(val) or RE_INT_ID.search(val)
                if m: ids.add(m.group(1))
    for p in root.iter("ProtectedString"):
        src=p.text or ""
        for m in RE_URL.finditer(src): ids.add(m.group(1))
        for m in RE_WEB.finditer(src): ids.add(m.group(1))
        for line in src.splitlines():
            if ("AnimationId" in line) or ("LoadAnimation" in line) or ("Animation(" in line) or ("Animator" in line):
                for m in RE_INT_ID.finditer(line): ids.add(m.group(1))
    for m in RE_URL.finditer(xml_text): ids.add(m.group(1))
    for m in RE_WEB.finditer(xml_text): ids.add(m.group(1))
    return ids
