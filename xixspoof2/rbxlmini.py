\
import re
RE_URL = re.compile(rb"(rbxassetid://)(\d{3,})")
RE_WEB = re.compile(rb"https?://www\.roblox\.com/asset/\?id=(\d{3,})")
RE_BARE = re.compile(rb"[\"'](\d{3,})[\"']")
def rbxl_to_xml_minimal(data: bytes) -> str:
    ids = set()
    for m in RE_URL.finditer(data): ids.add(m.group(2).decode('ascii','ignore'))
    for m in RE_WEB.finditer(data): ids.add(m.group(1).decode('ascii','ignore'))
    if ids:
        for m in RE_BARE.finditer(data): ids.add(m.group(1).decode('ascii','ignore'))
    if not ids:
        raise RuntimeError("rbxlmini could not find animation IDs in the RBXL. Save as .rbxlx and retry.")
    xml = ['<roblox version="4">']
    for aid in sorted(ids, key=lambda x: int(x)):
        xml.append(f'<Item class="Animation"><Properties><Content name="AnimationId">rbxassetid://{aid}</Content></Properties></Item>')
    xml.append("</roblox>")
    return "\\n".join(xml)
