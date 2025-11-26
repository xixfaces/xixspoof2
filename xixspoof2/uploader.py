from concurrent.futures import ThreadPoolExecutor, as_completed
from .logutil import info, warn
from .roblox import RobloxAPI
def upload_all(cookie, ids, group, threads):
    api=RobloxAPI(cookie)
    id_map={}; errors=[]
    def do(old):
        data=api.dl(old)
        nid=api.upload(data, f"Clone_{old}", "Uploaded via xixspoof2", group)
        return old, nid
    total=len(ids)
    info(f"Re-uploading {total} animation(s)…")
    with ThreadPoolExecutor(max_workers=max(1, threads)) as ex:
        futs={ex.submit(do, oid): oid for oid in ids}
        done=0
        for fut in as_completed(futs):
            done+=1
            old=futs[fut]
            try:
                o,n=fut.result(); id_map[o]=n
                info(f"[{done}/{total}] {o} -> {n}")
            except Exception as e:
                warn(f"[{done}/{total}] {old} FAILED: {e}"); errors.append((old,str(e)))
    return id_map, errors
