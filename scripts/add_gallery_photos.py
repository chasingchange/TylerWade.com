"""Move photos dropped into add-to-gallery/ into the site's gallery.

For each image: save a web-sized JPEG in uploads/, a WebP thumbnail in
uploads/t/, add it to the top of gallery.json, and delete the original
from add-to-gallery/. Run by .github/workflows/add-gallery-photos.yml.
"""
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

try:
    from pillow_heif import register_heif_opener  # iPhone .heic photos
    register_heif_opener()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "add-to-gallery"
UPLOADS = ROOT / "uploads"
THUMBS = UPLOADS / "t"
MANIFEST = ROOT / "gallery.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
FULL_MAX = 2000   # longest side of the full-size photo
THUMB_MAX = 1000  # longest side of the gallery tile


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "photo"


def unique_slug(base):
    slug, n = base, 2
    while (UPLOADS / f"{slug}.jpg").exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


def main():
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    photos = sorted(p for p in INBOX.iterdir() if p.suffix.lower() in EXTS)
    added = []
    for path in photos:
        try:
            img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        except Exception as e:
            print(f"skipping {path.name}: {e}")
            continue
        slug = unique_slug(slugify(path.stem))
        full = img.copy()
        full.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS)
        full.save(UPLOADS / f"{slug}.jpg", quality=88, optimize=True, progressive=True)
        thumb = img.copy()
        thumb.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
        thumb.save(THUMBS / f"{slug}.webp", quality=82)
        added.append({"src": f"uploads/{slug}.jpg", "ratio": round(img.width / img.height, 3)})
        path.unlink()
        print(f"added {path.name} -> uploads/{slug}.jpg ({img.width}x{img.height})")
    if added:
        # newest uploads go to the top of the gallery
        MANIFEST.write_text(json.dumps(added[::-1] + manifest, indent=2) + "\n")
    print(f"{len(added)} photo(s) added")


if __name__ == "__main__":
    main()
