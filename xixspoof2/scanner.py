import re, xml.etree.ElementTree as ET
from .logutil import info
from .version import __version__

def scan_xml(xml_text: str):
    ids=set()

    RE_URL = re.compile(r"rbxassetid://(\d+)")
    RE_WEB = re.compile(r"https?://www\.roblox\.com/asset/\?id=(\d+)")
    RE_NUM = re.compile(r"\b(\d{3,})\b")

    root=ET.fromstring(xml_text)

    # AnimationId in properties
    for node in root.iter("Item"):
        cls=node.get("class","")
        props=node.find("Properties")
        if props is not None:
            for c in props:
                if c.get("name")=="AnimationId":
                    txt=(c.text or "").strip()
                    m=RE_URL.search(txt) or RE_WEB.search(txt)
                    if m: ids.add(m.group(1))

    # Script scanning (ProtectedString)
    for node in root.iter("ProtectedString"):
        src=node.text or ""
        for m in RE_URL.finditer(src): ids.add(m.group(1))
        for m in RE_WEB.finditer(src): ids.add(m.group(1))
        for m in RE_NUM.finditer(src): ids.add(m.group(1))

    return ids
