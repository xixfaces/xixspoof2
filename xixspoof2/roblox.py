import json, requests, re
from .logutil import info

TIMEOUT = 60
RE_NUM = re.compile(r"(\d{3,})")

class RobloxAPI:
    def __init__(self,cookie:str):
        self.s=requests.Session()
        self.s.cookies.set(".ROBLOSECURITY",cookie,domain=".roblox.com")
        self.s.headers.update({"User-Agent":"xixspoof2/1.0.0"})

    def dl(self,aid):
        r=self.s.get(f"https://assetdelivery.roblox.com/v1/asset/?id={aid}",timeout=TIMEOUT)
        r.raise_for_status()
        return r.content

    def up_primary(self,data,name,desc,group):
        url="https://publish.roblox.com/v1/assets"
        files={"fileContent":("a.rbxm",data,"application/octet-stream")}
        body={"assetType":"Animation","name":name,"description":desc,"isPublic":False,"allowComments":False}
        if group: body["groupId"]=group
        r=self.s.post(url,data={"request":json.dumps(body)},files=files,timeout=TIMEOUT)
        if r.ok:
            try:return int(r.json().get("assetId"))
            except:return None
        return None

    def up_legacy(self,data,name,desc,group):
        url="https://www.roblox.com/assets/upload"
        files={"file":("a.rbxm",data,"application/octet-stream")}
        d={"assetTypeId":"24","name":name,"description":desc,"ispublic":"False","allowComments":"False","genreTypeId":"1"}
        if group: d["groupId"]=str(group)
        r=self.s.post(url,data=d,files=files,timeout=TIMEOUT)
        if r.ok:
            m=RE_NUM.search(r.text)
            if m:return int(m.group(1))
        return None

    def upload(self,data,name,desc,group):
        nid=self.up_primary(data,name,desc,group)
        if nid:return nid
        nid=self.up_legacy(data,name,desc,group)
        if not nid: raise RuntimeError("Upload failed")
        return nid
