# Tests

Run on 2026-11-18 (WIB) in this workspace, Python 3.12.3, Pillow 10.2.0.

## Commands

```sh
cd ~/workspace/makefun-entries/news-image-20261117
python3 main.py
sha256sum out/entry.png
python3 main.py
sha256sum out/entry.png
```

## Results

- Run 1: `wrote /output/entry.png` + `wrote out/entry.png`
- Run 2: identical output, same hashes
- SHA-256 (both runs, both paths): `dbcdd9d919207d7e381a9ceeb386f7dbe0ddb599c7b14baa8da431bf3aebc854`
- Size: 142,476 bytes (< 1 MiB limit)
- Dimensions: 1024 × 1024 px (Pillow-verified, PNG format)
- Determinism: byte-identical across two runs — PASS
- Visual check: image opened and inspected; title "WORLD NEWS — 17 NOVEMBER
  2026", all six story blocks legible, high contrast, no overlapping or
  truncated text; footer "Summary of 17 Nov 2026 world news" present.
- Harness code path (MAKEFUN_ENV_URL unset) exits after writing the image;
  the register/healthz/done behaviour was implemented per the program/v1
  spec but not exercised against a live harness in this session.

Note: an earlier draft had the Tech card summary truncated ("says he would
return" without "if asked."); the summary was shortened and re-verified —
final SHA-256 above is for the fixed version.
