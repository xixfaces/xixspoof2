import os
from .rbxlmini import rbxl_to_xml_minimal

def load_place_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".rbxlx":
        with open(path,"r",encoding="utf-8") as f:
            return f.read()
    if ext == ".rbxl":
        with open(path,"rb") as f:
            data=f.read()
        return rbxl_to_xml_minimal(data)
    raise RuntimeError(f"Unsupported: {ext}. Use rbxl or rbxlx")
