"""Optional asset preparation (Pillow required); normal static builds need only stdlib."""
from pathlib import Path
import json
import sys
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'static' / 'images'
OUT = IMAGES / 'optimized'
OUT.mkdir(exist_ok=True)
manifest = json.loads((OUT / 'manifest.json').read_text()) if (OUT / 'manifest.json').exists() else {}
selected = set(sys.argv[1:])
for source in sorted(IMAGES.iterdir()):
    if selected and source.name not in selected:
        continue
    if source.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.avif'):
        continue
    with Image.open(source) as original:
        im = ImageOps.exif_transpose(original)
        if source.name == 'earth.png' and im.mode == 'RGBA':
            im = im.crop(im.getbbox())
        # Preserve slide artwork and embedded text losslessly.
        artwork = source.stem.lower().startswith(('lesson', 'slide')) or 'logo' in source.stem.lower() or source.stem.lower() == 'taskit'
        if not artwork:
            im.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        dest = OUT / (source.name + '.webp')
        im.save(dest, format='WEBP', lossless=artwork, quality=86, method=6)
        if dest.stat().st_size < source.stat().st_size:
            manifest[source.name] = {'file': 'optimized/' + dest.name, 'width': im.width, 'height': im.height,
                                     'original_bytes': source.stat().st_size, 'bytes': dest.stat().st_size}
        else:
            dest.unlink()
            manifest.pop(source.name, None)
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
before = sum(i['original_bytes'] for i in manifest.values())
after = sum(i['bytes'] for i in manifest.values())
print(f'{len(manifest)} images optimized: {before:,} → {after:,} bytes ({(1-after/before)*100:.1f}% smaller).')
