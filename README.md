# xixspoof2 — Python Animation Replacer for Roblox  
✓ Same workflow as your original repo  
✓ Scans entire game for Animation IDs  
✓ Re-uploads animations  
✓ Rewrites all references  
✓ Supports **RBXLX natively**  
✓ Supports **RBXL** using built-in `rbxlmini` extractor (best-effort)

## Install (Windows CMD)
```cmd
cd xixspoof2
python -m venv .venv
.venv\Scripts\activate
pip install -e .
set RBLX_COOKIE=_|WARNING:-DO-NOT-SHARE-THIS.--YOURREALCOOKIE
```

## Dry Run (scan only)
```cmd
xixspoof2 --file "C:\Path\YourGame.rbxlx" --dry-run
xixspoof2 --file "C:\Path\YourGame.rbxl" --dry-run
```

## Real Run (upload + rewrite)
```cmd
xixspoof2 --file "C:\Path\YourGame.rbxlx" --output "C:\Path\YourGame.relinked.rbxlx"
```

## Group Owned Upload
```cmd
xixspoof2 --file "C:\Path\YourGame.rbxlx" --group 12345678 --output "C:\Path\YourGame.relinked.rbxlx"
```

If RBXL cannot be parsed, you will see:
**“Save as .rbxlx in Studio.”**

