\
import re
RE_URL = re.compile(r"(rbxassetid://)(\d+)")
RE_WEB = re.compile(r"(https?://www\.roblox\.com/asset/\?id=)(\d+)")
RE_BARE = re.compile(r'([\"\\\'])(\d{3,})([\"\\\'])')
def rewrite_place(xml_text: str, id_map: dict):
    def rep_url(m):
        old = m.group(2)
        return m.group(1) + str(id_map.get(old, old))
    text = RE_URL.sub(rep_url, xml_text)
    text = RE_WEB.sub(rep_url, text)
    out = []
    for ln in text.splitlines():
        if ("Animation" in ln) or ("AnimationId" in ln) or ("LoadAnimation" in ln):
            ln = RE_BARE.sub(lambda m: m.group(1) + str(id_map.get(m.group(2), m.group(2))) + m.group(3), ln)
        out.append(ln)
    return "\\n".join(out)
