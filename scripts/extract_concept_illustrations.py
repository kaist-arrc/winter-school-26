"""Reuse text-free illustration fragments without changing the originals.

The source diagrams are 1672 x 941. Coordinates deliberately exclude labels;
all new labels are selectable text in concepts/index.html.
Run only when rebuilding the illustration assets (requires Pillow).
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/air4bts_woo'
DESTINATION = ROOT / 'assets/concept-illustrations'
FRAGMENTS = {
    'air-observer': ('29405226-2EC3-4148-92DE-F0D3CD0B64FE.png', (22, 350, 190, 524)),
    'experience-scenes': ('29405226-2EC3-4148-92DE-F0D3CD0B64FE.png', (481, 600, 782, 668)),
    'bts-context': ('29405226-2EC3-4148-92DE-F0D3CD0B64FE.png', (925, 352, 1218, 445)),
    'human-ai': ('29405226-2EC3-4148-92DE-F0D3CD0B64FE.png', (715, 698, 902, 780)),
    'replay-workshop': ('iOS 이미지 (4).jpg', (1150, 169, 1339, 234)),
    'transfer-workshop': ('iOS 이미지 (4).jpg', (382, 113, 548, 273)),
    'paces-everyday': ('7C35FF8E-DB95-42DA-A416-F18C9A2E47D7.png', (1385, 449, 1660, 695)),
}


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for name, (filename, bounds) in FRAGMENTS.items():
        with Image.open(SOURCE / filename) as original:
            if original.size != (1672, 941):
                raise ValueError(f'Unexpected dimensions: {filename}: {original.size}')
            original.crop(bounds).convert('RGB').save(DESTINATION / f'{name}.webp', quality=95)
    print(f'Extracted {len(FRAGMENTS)} illustration fragments; originals unchanged.')


if __name__ == '__main__':
    main()
