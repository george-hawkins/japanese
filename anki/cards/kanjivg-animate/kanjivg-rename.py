import os, shutil

src, dst = "kanji", "kanjivg"

os.makedirs(dst, exist_ok=True)

for name in os.listdir(src):
  if not name.endswith(".svg"): continue

  cp = int(name[:-4], 16)
  shutil.copy(os.path.join(src, name), os.path.join(dst, f"_kanjivg-{chr(cp)}.svg"))
