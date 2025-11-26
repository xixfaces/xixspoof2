import json, time, re, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TIMEOUT = 60
RE_NUM = re.compile(r"(\d{3,})")

def _make_session(cookie: str) -> requests.Session:
    s = requests.Session()
    s.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
    retry = Retry(total=5, connect=5, read=5, backoff_factor=0.6, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=False, raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    s.mount("https://", adapter); s.mount("http://", adapter)
    s.headers.update({"User-Agent": "xixspoof2/1.1.0","Accept": "application/json, text/plain, */*","Origin": "https://create.roblox.com","Referer": "https://create.roblox.com/","Connection": "keep-alive"})
    return s

class RobloxAPI:
    def __init__(self, cookie: str):
        self.s = _make_session(cookie)
        self.xcsrf = None
        self._refresh_xcsrf()

    def _refresh_xcsrf(self):
        r = self.s.post("https://auth.roblox.com/v2/logout", timeout=TIMEOUT)
        token = r.headers.get("x-csrf-token")
        if token:
            self.xcsrf = token
            self.s.headers["x-csrf-token"] = token

    def _post_with_xcsrf(self, url: str, **kwargs) -> requests.Response:
        r = self.s.post(url, timeout=TIMEOUT, **kwargs)
        if r.status_code == 403:
            new = r.headers.get("x-csrf-token")
            if new:
                self.xcsrf = new
                self.s.headers["x-csrf-token"] = new
                r = self.s.post(url, timeout=TIMEOUT, **kwargs)
        return r

    def dl(self, aid: str) -> bytes:
        r = self.s.get(f"https://assetdelivery.roblox.com/v1/asset/?id={aid}", timeout=TIMEOUT)
        r.raise_for_status()
        return r.content

    def up_primary(self, data: bytes, name: str, desc: str, group: int | None):
        url = "https://publish.roblox.com/v1/assets"
        files = {"fileContent": ("animation.rbxm", data, "application/octet-stream")}
        body = {"assetType": "Animation","name": name,"description": desc,"isPublic": False,"allowComments": False}
        if group: body["groupId"] = group
        r = self._post_with_xcsrf(url, data={"request": json.dumps(body)}, files=files)
        if r.ok:
            try:
                aid = r.json().get("assetId")
                return int(aid) if aid else None
            except Exception:
                return None
        return None

    def up_legacy(self, data: bytes, name: str, desc: str, group: int | None):
        url = "https://www.roblox.com/assets/upload"
        files = {"file": ("animation.rbxm", data, "application/octet-stream")}
        form = {"assetTypeId": "24","name": name,"description": desc,"ispublic": "False","allowComments": "False","genreTypeId": "1"}
        if group: form["groupId"] = str(group)
        r = self._post_with_xcsrf(url, data=form, files=files)
        if r.ok:
            m = RE_NUM.search(r.text)
            if m:
                return int(m.group(1))
        return None

    def upload(self, data: bytes, name: str, desc: str, group: int | None) -> int:
        nid = self.up_primary(data, name, desc, group)
        if nid:
            return nid
        time.sleep(0.4)
        nid = self.up_legacy(data, name, desc, group)
        if not nid:
            raise RuntimeError("Upload failed")
        return nid
