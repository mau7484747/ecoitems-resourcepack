#!/usr/bin/env python3
"""Refine only the Christmas crate: replace painted exterior lamps with 3D lanterns
and close the hollow support below the display road. The rest of the model is kept.
"""
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(".")
MODEL = ROOT / "assets/minecraft/models/custom/maumod/mausmp/weihnachtskiste/double_chest.json"
LIVE = ROOT / "assets/minecraft/textures/custom/maumod/mausmp/weihnachtskiste"
BACKUP = ROOT / "BACKUP_WEIHNACHTSKISTE_TEXTURES/assets/minecraft/textures/custom/maumod/mausmp/weihnachtskiste"

def save_png(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)

def make_metal(path, dark=False):
    rng = random.Random(211121)
    image = Image.new("RGBA", (128, 128))
    px = image.load()
    for y in range(128):
        for x in range(128):
            edge = min(x, y, 127-x, 127-y)
            shade = 0.72 + 0.18 * math.sin((x / 127) * math.pi)
            shade += 0.08 * math.sin((y / 127) * math.pi * 2)
            shade += rng.uniform(-0.035, 0.035)
            if dark:
                base = (63, 37, 19)
                factor = shade * (0.72 if edge < 5 else 1.0)
            else:
                base = (198, 139, 46)
                factor = shade * (0.70 if edge < 5 else 1.0)
            px[x, y] = tuple(max(0, min(255, int(c * factor))) for c in base) + (255,)
    d = ImageDraw.Draw(image)
    if dark:
        d.rectangle((4, 4, 123, 123), outline=(117, 76, 35, 255), width=4)
        d.rectangle((10, 10, 117, 117), outline=(34, 23, 17, 255), width=2)
        for x in (16, 111):
            for y in (16, 111):
                d.ellipse((x-3, y-3, x+3, y+3), fill=(202, 149, 68, 255), outline=(39, 26, 17, 255))
    else:
        d.rectangle((3, 3, 124, 124), outline=(250, 218, 133, 255), width=3)
        d.rectangle((8, 8, 119, 119), outline=(111, 68, 20, 255), width=2)
        for x in range(15, 116, 12):
            d.line((x, 13, x, 114), fill=(224, 176, 76, 150), width=1)
        d.line((12, 12, 115, 12), fill=(255, 237, 175, 255), width=2)
        d.line((12, 115, 115, 115), fill=(92, 54, 18, 255), width=2)
        for x in (17, 111):
            for y in (17, 111):
                d.ellipse((x-3, y-3, x+3, y+3), fill=(255, 229, 155, 255), outline=(87, 51, 17, 255))
    save_png(image, path)

def make_glow(path):
    rng = random.Random(4137)
    frames = []
    strengths = (0.92, 1.00, 0.95, 1.04)
    for strength in strengths:
        image = Image.new("RGBA", (128, 128))
        px = image.load()
        for y in range(128):
            for x in range(128):
                nx = (x - 63.5) / 63.5
                ny = (y - 63.5) / 63.5
                radius = min(1.0, math.sqrt(nx*nx + ny*ny))
                core = max(0.0, 1.0 - radius)
                edge = max(0.0, min(1.0, (radius - 0.68) / 0.32))
                noise = rng.uniform(-2.0, 2.0)
                r = (138 + 102 * core) * strength - 22 * edge + noise
                g = (67 + 157 * core) * strength - 24 * edge + noise
                b = (18 + 74 * core) * strength - 9 * edge + noise
                px[x, y] = (max(0, min(255, int(r))),
                            max(0, min(255, int(g))),
                            max(0, min(255, int(b))), 255)
        d = ImageDraw.Draw(image)
        d.rectangle((2, 2, 125, 125), outline=(67, 39, 18, 255), width=5)
        d.rectangle((7, 7, 120, 120), outline=(243, 183, 72, 255), width=3)
        d.line((17, 13, 17, 114), fill=(255, 233, 166, 230), width=4)
        d.line((23, 14, 23, 108), fill=(255, 249, 216, 170), width=2)
        d.line((110, 17, 110, 111), fill=(255, 205, 91, 210), width=3)
        d.line((30, 12, 97, 12), fill=(255, 243, 198, 200), width=2)
        frames.append(image)
    strip = Image.new("RGBA", (128, 512))
    for index, frame in enumerate(frames):
        strip.paste(frame, (0, index * 128))
    save_png(strip, path)
    meta = {
        "animation": {
            "width": 128,
            "height": 128,
            "frametime": 5,
            "frames": [0, 1, 2, 3]
        }
    }
    path.with_suffix(path.suffix + ".mcmeta").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

def make_lower_body(path, snow=False):
    rng = random.Random(9381 if snow else 9380)
    image = Image.new("RGBA", (128, 128))
    px = image.load()
    if snow:
        for y in range(128):
            for x in range(128):
                n = rng.randint(-6, 6)
                base = (218, 231, 236)
                px[x, y] = tuple(max(0, min(255, c+n)) for c in base) + (255,)
        d = ImageDraw.Draw(image)
        for y in range(8, 128, 22):
            d.line((0, y, 127, y-2), fill=(245, 251, 253, 255), width=2)
            d.line((0, y+3, 127, y+1), fill=(181, 205, 215, 180), width=1)
        for _ in range(220):
            x, y = rng.randrange(128), rng.randrange(128)
            c = rng.choice(((255,255,255,220), (177,202,215,180), (238,246,249,230)))
            d.point((x, y), fill=c)
    else:
        for y in range(128):
            for x in range(128):
                band = x % 12
                n = rng.randint(-5, 5)
                if band < 2:
                    base = (56, 2, 13)
                elif band < 8:
                    base = (126, 7, 25)
                else:
                    base = (82, 3, 17)
                shade = 1.0 - 0.10 * (y / 127)
                px[x, y] = tuple(max(0, min(255, int(c * shade) + n)) for c in base) + (255,)
        d = ImageDraw.Draw(image)
        for x in range(0, 128, 12):
            d.line((x+1, 0, x+1, 127), fill=(183, 32, 45, 255), width=1)
            d.line((x+8, 0, x+8, 127), fill=(40, 1, 10, 255), width=2)
        d.line((0, 5, 127, 5), fill=(208, 54, 63, 255), width=2)
        d.line((0, 122, 127, 122), fill=(43, 1, 9, 255), width=3)
    save_png(image, path)

def patch_lamp_sprites(source_path, target_path, is_front):
    source = Image.open(source_path).convert("RGBA")
    width, height = source.size
    frame_h = 128
    if height % frame_h != 0:
        raise SystemExit(f"Unexpected animated texture height in {source_path}: {source.size}")
    expected_width = 256 if is_front else 128
    if width != expected_width:
        raise SystemExit(f"Unexpected texture width in {source_path}: {source.size}")
    result = source.copy()
    for frame_y in range(0, height, frame_h):
        frame = source.crop((0, frame_y, width, frame_y + frame_h))
        if is_front:
            # Remove only the two painted lamp sprites. Clean background is copied from
            # the adjacent, undisturbed garland and ribbed red panel.
            patches = [
                ((4, 16, 30, 70), (34, 16, 60, 70)),
                ((226, 16, 252, 70), (196, 16, 222, 70)),
            ]
        else:
            # The side atlas has one lamp high on one end and one lower at the other.
            patches = [
                ((2, 46, 28, 100), (30, 46, 56, 100)),
                ((100, 18, 126, 72), (72, 18, 98, 72)),
            ]
        for target, donor in patches:
            patch = frame.crop(donor)
            frame.paste(patch, target[:2])
        result.paste(frame, (0, frame_y))
    save_png(result, target_path)

def faces(texture, uv=(0, 0, 16, 16)):
    return {
        direction: {"uv": list(uv), "texture": "#" + texture}
        for direction in ("north", "south", "east", "west", "up", "down")
    }

def add_box(model, frm, to, texture, custom_faces=None):
    model["elements"].append({
        "from": [round(float(v), 4) for v in frm],
        "to": [round(float(v), 4) for v in to],
        "faces": custom_faces if custom_faces is not None else faces(texture)
    })

def add_front_lantern(model, cx):
    # A real wall-mounted fixture: backing plate, projecting bracket, hanging chain,
    # four-sided glass body, metal rails, caps and small fasteners.
    add_box(model, (cx-.52, 3.10, 2.31), (cx+.52, 4.70, 2.57), "lanternDark")
    add_box(model, (cx-.56, 4.58, 2.25), (cx+.56, 4.76, 2.58), "frame")
    add_box(model, (cx-.13, 4.48, 1.72), (cx+.13, 4.65, 2.47), "frame")
    add_box(model, (cx-.09, 4.18, 1.82), (cx+.09, 4.48, 2.02), "gold")
    add_box(model, (cx-.15, 4.03, 1.79), (cx+.15, 4.20, 2.06), "frame")
    # Upper and lower crowns.
    add_box(model, (cx-.44, 3.94, 1.43), (cx+.44, 4.13, 2.13), "frame")
    add_box(model, (cx-.45, 2.96, 1.43), (cx+.45, 3.15, 2.13), "frame")
    # Glowing chamber sits behind the metal cage.
    add_box(model, (cx-.29, 3.16, 1.61), (cx+.29, 3.91, 1.99), "glow")
    add_box(model, (cx-.28, 3.18, 1.47), (cx+.28, 3.89, 1.54), "glow")
    # Four vertical corner rails on the front and rear edges.
    for x1, x2 in ((cx-.43, cx-.32), (cx+.32, cx+.43)):
        add_box(model, (x1, 3.13, 1.43), (x2, 3.96, 1.58), "frame")
        add_box(model, (x1, 3.13, 1.99), (x2, 3.96, 2.13), "frame")
    # Crossbars and raised trim.
    for y1, y2 in ((3.12, 3.23), (3.84, 3.95)):
        add_box(model, (cx-.40, y1, 1.43), (cx+.40, y2, 1.58), "gold")
        add_box(model, (cx-.40, y1, 1.99), (cx+.40, y2, 2.13), "gold")
    # Bottom and top finials, plus visible screws on the backplate.
    add_box(model, (cx-.14, 2.75, 1.72), (cx+.14, 2.96, 1.95), "gold")
    add_box(model, (cx-.13, 4.12, 1.72), (cx+.13, 4.31, 1.95), "gold")
    for x in (cx-.40, cx+.40):
        for y in (3.27, 4.47):
            add_box(model, (x-.055, y-.055, 2.22), (x+.055, y+.055, 2.30), "gold")

def add_side_lantern(model, surface_x, direction, cz):
    # This version is mounted to the left/right outer wall and projects outward.
    inner = surface_x + direction * 0.30
    outer = surface_x + direction * 0.92
    xlo, xhi = sorted((inner, outer))
    plate_lo, plate_hi = sorted((surface_x - direction * 0.05, surface_x + direction * 0.20))
    add_box(model, (plate_lo, 3.10, cz-.52), (plate_hi, 4.70, cz+.52), "lanternDark")
    # Wall bracket and short hanging chain.
    arm_lo, arm_hi = sorted((surface_x + direction * 0.02, surface_x + direction * 0.66))
    add_box(model, (arm_lo, 4.55, cz-.11), (arm_hi, 4.72, cz+.11), "frame")
    chain_lo, chain_hi = sorted((surface_x + direction * 0.58, surface_x + direction * 0.75))
    add_box(model, (chain_lo, 4.14, cz-.07), (chain_hi, 4.56, cz+.07), "gold")
    add_box(model, (chain_lo, 4.00, cz-.14), (chain_hi, 4.18, cz+.14), "frame")
    # Upper and lower lantern crowns.
    add_box(model, (xlo, 3.96, cz-.44), (xhi, 4.15, cz+.44), "frame")
    add_box(model, (xlo, 2.98, cz-.44), (xhi, 3.17, cz+.44), "frame")
    # Amber chamber and exposed glass panel at the outside face.
    glass_lo, glass_hi = sorted((surface_x + direction * 0.43, surface_x + direction * 0.79))
    add_box(model, (glass_lo, 3.18, cz-.29), (glass_hi, 3.91, cz+.29), "glow")
    pane_lo, pane_hi = sorted((surface_x + direction * 0.86, surface_x + direction * 0.92))
    add_box(model, (pane_lo, 3.20, cz-.28), (pane_hi, 3.89, cz+.28), "glow")
    # Metal cage: four vertical posts and two horizontal rails.
    for z1, z2 in ((cz-.43, cz-.32), (cz+.32, cz+.43)):
        add_box(model, (xlo, 3.14, z1), (xhi, 3.97, z2), "frame")
    for y1, y2 in ((3.12, 3.23), (3.84, 3.95)):
        add_box(model, (xlo, y1, cz-.40), (xhi, y2, cz+.40), "gold")
    # Finials and small fasteners on the outer side.
    finial_lo, finial_hi = sorted((surface_x + direction * 0.88, surface_x + direction * 1.06))
    add_box(model, (finial_lo, 2.76, cz-.12), (finial_hi, 2.98, cz+.12), "gold")
    add_box(model, (finial_lo, 4.13, cz-.12), (finial_hi, 4.34, cz+.12), "gold")
    screw_lo, screw_hi = sorted((surface_x + direction * 0.96, surface_x + direction * 1.04))
    for z in (cz-.36, cz+.36):
        for y in (3.32, 4.48):
            add_box(model, (screw_lo, y-.055, z-.055), (screw_hi, y+.055, z+.055), "gold")

def main():
    if not MODEL.is_file():
        raise SystemExit(f"Missing Christmas model: {MODEL}")
    if not LIVE.is_dir() or not BACKUP.is_dir():
        raise SystemExit("Live or backup Christmas texture directory is missing.")

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    if len(model.get("elements", [])) < 237:
        raise SystemExit("The expected restored 237-element Christmas model is not present.")

    # Always rebuild the cleaned facade atlases from the untouched backup originals.
    for filename, is_front in (("front.png", True), ("side.png", False)):
        patch_lamp_sprites(BACKUP / filename, LIVE / filename, is_front)

    # High-resolution materials for attached lanterns and the support beneath the road.
    make_metal(LIVE / "lantern_frame.png", dark=False)
    make_metal(LIVE / "lantern_dark.png", dark=True)
    make_glow(LIVE / "lantern_glow.png")
    make_lower_body(LIVE / "lower_body.png", snow=False)
    make_lower_body(LIVE / "lower_body_top.png", snow=True)

    model.setdefault("textures", {})
    model["textures"].update({
        "lanternDark": "minecraft:custom/maumod/mausmp/weihnachtskiste/lantern_dark",
        "base": "minecraft:custom/maumod/mausmp/weihnachtskiste/lower_body",
        "baseTop": "minecraft:custom/maumod/mausmp/weihnachtskiste/lower_body_top",
    })

    # Add geometry once. The support fits directly below the existing floor/road
    # platform, so it fills the hollow without changing the sleigh, reindeer or trees.
    support_exists = any(
        e.get("from") == [-0.28, 6.75, 4.38] and e.get("to") == [16.28, 8.54, 11.62]
        for e in model["elements"]
    )
    if not support_exists:
        support_faces = {
            "north": {"uv": [0,0,16,16], "texture": "#base"},
            "south": {"uv": [0,0,16,16], "texture": "#base"},
            "east": {"uv": [0,0,16,16], "texture": "#base"},
            "west": {"uv": [0,0,16,16], "texture": "#base"},
            "up": {"uv": [0,0,16,16], "texture": "#baseTop"},
            "down": {"uv": [0,0,16,16], "texture": "#lanternDark"},
        }
        add_box(model, (-0.28, 6.75, 4.38), (16.28, 8.54, 11.62), "base", support_faces)

        # Raised trim along the plinth's visible perimeter.
        add_box(model, (-0.34, 6.72, 4.34), (16.34, 6.86, 4.50), "gold")
        add_box(model, (-0.34, 6.72, 11.50), (16.34, 6.86, 11.66), "gold")
        add_box(model, (-0.42, 6.72, 4.50), (-0.28, 6.86, 11.50), "gold")
        add_box(model, (16.28, 6.72, 4.50), (16.42, 6.86, 11.50), "gold")

        # Two proper exterior lanterns on the front and two on each side.
        add_front_lantern(model, -1.28)
        add_front_lantern(model, 17.28)
        for side_x, direction in ((-2.50, -1), (18.50, 1)):
            add_side_lantern(model, side_x, direction, 3.65)
            add_side_lantern(model, side_x, direction, 12.35)
    else:
        print("Christmas lamp/base geometry already refined; no duplicate cubes added.")

    MODEL.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Refined Christmas model: {len(model['elements'])} geometry elements.")
    print("Added one solid support under the road and six wall-mounted exterior lanterns.")
    print("Cleaned the flat lamp sprites from front/side atlases; preserved the other crate animations.")
    print("Only Christmas-crate model and texture assets were written.")

if __name__ == "__main__":
    main()
