import re

RE_URL = re.compile(r"(rbxassetid://)(\d+)")
RE_WEB = re.compile(r"(https?://www\.roblox\.com/asset/\?id=)(\d+)")
RE_BARE = re.compile(r'(["\'])(\d{3,})(["\'])')

def rewrite_place(xml_text: str, id_map: dict):
    def rep_url(m):
        old=m.group(2)
        return m.group(1)+str(id_map.get(old,old))
    xml=RE_URL.sub(rep_url, xml_text)
    xml=RE_WEB.sub(rep_url, xml)

    lines=xml.splitlines()
    out=[]
    for ln in lines:
        if "Animation" in ln or "AnimationId" in ln:
            ln=RE_BARE.sub(lambda m: m.group(1)+str(id_map.get(m.group(2),m.group(2)))+m.group(3), ln)
        out.append(ln)
    return "\n".join(out)
