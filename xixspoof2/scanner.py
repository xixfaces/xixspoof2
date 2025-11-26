import re, xml.etree.ElementTree as ET
RE_URL   = re.compile(r"rbxassetid://(\d+)")
RE_WEB   = re.compile(r"https?://www\.roblox\.com/asset/\?id=(\d+)")
RE_INTID = re.compile(r"\b(\d{3,})\b")

def _iter_instances(root):
    for tag in ("Item", "Instance"):
        for node in root.iter(tag):
            yield node

def scan_xml(xml_text: str, deep: bool = False):
    ids = set()
    try:
        root = ET.fromstring(xml_text)
    except Exception:
        if deep:
            ids.update(m.group(1) for m in RE_URL.finditer(xml_text))
            ids.update(m.group(1) for m in RE_WEB.finditer(xml_text))
        return ids

    for node in _iter_instances(root):
        cls = node.get("class") or node.get("Class") or ""
        if cls != "Animation":
            continue
        props = node.find("Properties")
        if props is None:
            continue
        for c in props:
            name = (c.get("name") or c.get("Name") or "")
            if name == "AnimationId":
                val = (c.text or "").strip()
                m = RE_URL.search(val) or RE_WEB.search(val)
                if m:
                    ids.add(m.group(1))

    if not deep:
        return ids

    for p in root.iter("ProtectedString"):
        src = p.text or ""
        for m in RE_URL.finditer(src): ids.add(m.group(1))
        for m in RE_WEB.finditer(src): ids.add(m.group(1))
        for line in src.splitlines():
            if ("AnimationId" in line) or ("LoadAnimation" in line) or ("Animator" in line):
                for m in RE_INTID.finditer(line): ids.add(m.group(1))

    for m in RE_URL.finditer(xml_text): ids.add(m.group(1))
    for m in RE_WEB.finditer(xml_text): ids.add(m.group(1))
    return ids
