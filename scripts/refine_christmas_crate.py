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
                ((4, 14, 31, 116), (60, 14, 87, 116)),
                ((225, 14, 252, 116), (169, 14, 196, 116)),
            ]
        else:
            # The side atlas has one lamp high on one end and one lower at the other.
            patches = [
                ((0, 14, 29, 114), (29, 14, 58, 114)),
                ((99, 14, 128, 114), (70, 14, 99, 114)),
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


def make_pillar_trim(path):
    """A non-figurative vertical brass/red architectural trim tile; no painted lanterns."""
    rng = random.Random(90217)
    image = Image.new("RGBA", (128, 128))
    px = image.load()
    for y in range(128):
        for x in range(128):
            band = x % 32
            grain = rng.randint(-5, 5)
            if band < 3 or 29 <= band:
                base = (43, 10, 17)
            elif 3 <= band < 7 or 25 <= band < 29:
                base = (139, 17, 30)
            elif 7 <= band < 10 or 22 <= band < 25:
                base = (84, 7, 19)
            elif 10 <= band < 22:
                base = (111, 11, 25)
            else:
                base = (0, 0, 0)
            shade = 0.82 + 0.14 * math.sin(y / 127 * math.pi)
            px[x, y] = tuple(max(0, min(255, int(c * shade) + grain)) for c in base) + (255,)
    d = ImageDraw.Draw(image)
    for x in (3, 7, 24, 28):
        d.line((x, 0, x, 127), fill=(224, 174, 82, 255), width=1)
        d.line((x+1, 0, x+1, 127), fill=(83, 44, 17, 255), width=1)
    for y in range(8, 128, 24):
        d.line((9, y, 23, y), fill=(224, 178, 91, 255), width=2)
        d.line((10, y+2, 22, y+2), fill=(58, 21, 17, 255), width=1)
        for x in (11, 21):
            d.ellipse((x-2, y-3, x+2, y+1), fill=(255, 222, 140, 255), outline=(75, 42, 17, 255))
    d.line((12, 0, 12, 127), fill=(172, 40, 46, 255), width=1)
    d.line((19, 0, 19, 127), fill=(44, 4, 14, 255), width=1)
    save_png(image, path)

def make_sleigh_cushion(path):
    """Burgundy quilted velvet for the sleigh seat, with raised seams and gold studs."""
    rng = random.Random(1907)
    image = Image.new("RGBA", (128, 128))
    px = image.load()
    for y in range(128):
        for x in range(128):
            grain = rng.randint(-4, 4)
            shade = 0.78 + 0.19 * math.sin(math.pi * x / 127)
            shade *= 0.9 + 0.1 * math.sin(math.pi * y / 127)
            base = (105, 7, 26)
            px[x, y] = tuple(max(0, min(255, int(c * shade) + grain)) for c in base) + (255,)
    d = ImageDraw.Draw(image)
    for y in range(-64, 192, 32):
        for x in range(-64, 192, 32):
            d.line((x, y+16, x+16, y), fill=(176, 36, 54, 255), width=3)
            d.line((x+16, y, x+32, y+16), fill=(49, 2, 15, 255), width=2)
            d.line((x+32, y+16, x+16, y+32), fill=(176, 36, 54, 255), width=3)
            d.line((x+16, y+32, x, y+16), fill=(49, 2, 15, 255), width=2)
            d.ellipse((x+12, y+12, x+20, y+20), fill=(242, 195, 98, 255), outline=(91, 52, 18, 255))
    d.rectangle((3, 3, 124, 124), outline=(240, 203, 119, 255), width=3)
    d.rectangle((7, 7, 120, 120), outline=(61, 4, 18, 255), width=2)
    save_png(image, path)

def scale_reindeer(model):
    """Reduce both complete reindeer together, keeping all four hooves on the floor."""
    if max((e["to"][1] for e in model["elements"][111:201]), default=0) < 14.0:
        print("Reindeer are already at the reduced scale.")
        return
    groups = (
        (range(111, 153), 6.55),
        (range(153, 201), 9.55),
    )
    sx, sy, sz = 0.86, 0.84, 0.86
    floor_y = 9.20
    center_x = 9.40
    for indices, center_z in groups:
        for index in indices:
            element = model["elements"][index]
            for key in ("from", "to"):
                point = element[key]
                point[0] = center_x + (point[0] - center_x) * sx
                point[1] = floor_y + (point[1] - floor_y) * sy
                point[2] = center_z + (point[2] - center_z) * sz
            if "rotation" in element:
                origin = element["rotation"]["origin"]
                origin[0] = center_x + (origin[0] - center_x) * sx
                origin[1] = floor_y + (origin[1] - floor_y) * sy
                origin[2] = center_z + (origin[2] - center_z) * sz
    print("Scaled both reindeer to 86% width/depth and 84% height; hooves remain on the snow floor.")

def duplicate_stage_lanterns(model):
    """Mirror the two existing 3D lanterns across the scene to make four real fixtures."""
    sentinel = any(
        all(abs(a-b) < 0.002 for a,b in zip(e.get("from", []), [3.74, 12.78, 10.44]))
        for e in model["elements"]
    )
    if sentinel:
        print("The four-corner 3D lantern arrangement is already present.")
        return
    import copy
    original_groups = (range(201, 219), range(219, 237))
    additions = []
    for indices in original_groups:
        for index in indices:
            element = copy.deepcopy(model["elements"][index])
            for key in ("from", "to"):
                z1, z2 = element[key][2], element[key][2]
                element[key][2] = 16.0 - z1
            if "rotation" in element:
                element["rotation"]["origin"][2] = 16.0 - element["rotation"]["origin"][2]
            # Reflection reverses the bounds in Z; restore min/max order.
            if element["from"][2] > element["to"][2]:
                element["from"][2], element["to"][2] = element["to"][2], element["from"][2]
            additions.append(element)
    model["elements"].extend(additions)
    print("Added two mirrored 3D lanterns; the elk display now has four spatial fixtures.")

def add_sleigh_details(model):
    """Add curved runners, padded seat, carriage rails, studs and reins to the sleigh."""
    sentinel = any(
        all(abs(a-b) < 0.002 for a,b in zip(e.get("from", []), [1.82, 9.27, 5.72]))
        for e in model["elements"]
    )
    if sentinel:
        print("The upgraded sleigh details are already present.")
        return
    def box(frm, to, texture, rotation=None):
        e = {
            "from": [round(float(v), 4) for v in frm],
            "to": [round(float(v), 4) for v in to],
            "faces": faces(texture)
        }
        if rotation:
            e["rotation"] = rotation
        model["elements"].append(e)

    # Solid, long brass runners with dark undersides.
    for x1, x2 in ((1.82, 2.18), (5.90, 6.26)):
        box((x1, 9.27, 5.72), (x2, 9.42, 10.55), "dark")
        box((x1-.04, 9.39, 5.82), (x2+.04, 9.53, 10.45), "gold")
        box((x1+.06, 9.49, 6.15), (x2-.06, 9.57, 10.12), "gold")
        # Upturned front and rear runner noses, split into short angled voxel pieces.
        box((x1-.02, 9.42, 5.55), (x2+.02, 9.90, 6.18), "gold",
            {"origin": [x1+.16, 9.44, 6.12], "axis": "x", "angle": 24, "rescale": True})
        box((x1-.02, 9.42, 10.05), (x2+.02, 9.90, 10.72), "gold",
            {"origin": [x1+.16, 9.44, 10.12], "axis": "x", "angle": -24, "rescale": True})
        # Brass cross-brackets tie the runner to the body.
        for z in (6.35, 7.55, 8.75, 9.95):
            box((x1-.03, 9.50, z-.07), (x2+.03, 9.76, z+.07), "gold")

    # Plush inset seat and padded raised backrest.
    box((2.58, 10.25, 6.47), (5.55, 10.48, 9.73), "sleighCushion")
    box((2.55, 10.44, 6.50), (2.83, 11.30, 9.70), "sleighCushion")
    box((2.50, 11.25, 6.42), (2.90, 11.43, 9.78), "gold")
    box((2.83, 10.32, 6.46), (5.45, 10.40, 6.60), "gold")
    box((2.83, 10.32, 9.60), (5.45, 10.40, 9.74), "gold")
    # Raised arm rests and gold-edged carved side panels.
    for x1, x2 in ((2.03, 2.34), (5.78, 6.09)):
        box((x1, 10.48, 6.35), (x2, 10.70, 9.82), "sleigh_red")
        box((x1-.04, 10.66, 6.30), (x2+.04, 10.78, 9.87), "gold")
        for z in (6.55, 7.35, 8.15, 8.95, 9.65):
            box((x1-.06, 10.20, z-.06), (x2+.06, 10.34, z+.06), "gold")
    # A pronounced raised prow and decorated nose toward the reindeer.
    box((5.82, 10.22, 6.16), (6.36, 10.50, 10.04), "sleigh_red")
    box((5.94, 10.48, 6.22), (6.43, 10.66, 9.98), "gold")
    box((6.23, 10.60, 7.55), (6.58, 10.93, 8.65), "gold")
    box((6.32, 10.88, 7.85), (6.66, 11.13, 8.35), "sleigh_red")
    # Tiny gold studs along the outer panels.
    for x in (2.12, 5.95):
        for z in (6.52, 7.22, 7.92, 8.62, 9.32, 9.72):
            box((x-.05, 10.36, z-.05), (x+.05, 10.46, z+.05), "gold")
    # Pair of harness shafts connecting the sleigh to the reindeer.
    for z in (6.55, 9.55):
        box((5.75, 10.02, z-.075), (8.25, 10.18, z+.075), "details")
        box((7.75, 10.08, z-.11), (7.95, 10.29, z+.11), "gold")
        box((5.92, 10.00, z-.10), (6.16, 10.21, z+.10), "gold")
    print("Added detailed sleigh runners, curled noses, cushioned seat, raised prow, trim and twin harness shafts.")

def replace_flat_lamp_sprites(model):
    """The former bell/lamp artwork on pillar faces becomes plain architectural trim."""
    count = 0
    for element in model.get("elements", []):
        for face in element.get("faces", {}).values():
            if face.get("texture") == "#hole":
                face["texture"] = "#pillar"
                count += 1
    print(f"Removed {count} flat bell/lamp image faces from the 3D model's pillars.")


def remove_two_front_uprights(model):
    """Remove the two front-facing dark-red columns marked in the in-game screenshot."""
    targets = (
        ([-2.5, 5.5, 2.54], [-1.45, 18.5, 3.8]),
        ([-2.71, 4.5, 2.33], [-1.24, 6.5, 4.01]),
        ([17.45, 5.5, 2.54], [18.5, 18.5, 3.8]),
        ([17.24, 4.5, 2.33], [18.71, 6.5, 4.01]),
    )
    def same_point(a, b):
        return len(a) == len(b) and all(abs(float(x)-float(y)) < 0.003 for x,y in zip(a,b))
    kept = []
    removed = 0
    for element in model["elements"]:
        if any(same_point(element.get("from", []), frm) and same_point(element.get("to", []), to)
               for frm,to in targets):
            removed += 1
        else:
            kept.append(element)
    model["elements"] = kept
    print(f"Removed the two front-facing screenshot columns and their foot blocks: {removed} cuboids.")
    print("All 3D lanterns, golden lamp parts, glass panels and roof frames are preserved.")

def move_reindeer_back(model):
    """Shift both reduced reindeer and their sleigh shafts toward the rear of the case."""
    deer = model["elements"][111:201]
    if not deer:
        raise SystemExit("Could not find the two reindeer geometry groups.")
    min_z = min(e["from"][2] for e in deer)
    if min_z >= 6.8:
        print(f"Reindeer are already moved back (frontmost Z={min_z:.2f}).")
        return
    dz = 1.20
    for element in deer:
        for key in ("from", "to"):
            element[key][2] += dz
        if "rotation" in element:
            element["rotation"]["origin"][2] += dz

    # Move the six small bars that attach the sleigh to the reindeer by the same distance.
    moved_shafts = 0
    for element in model["elements"][201:]:
        frm, to = element.get("from"), element.get("to")
        if not frm or not to:
            continue
        is_shaft_part = (
            5.70 <= frm[0] <= 7.80
            and 9.98 <= frm[1] <= 10.10
            and 6.35 <= frm[2] <= 9.75
            and to[0] <= 8.30
            and to[1] <= 10.31
            and 0.12 <= (to[2] - frm[2]) <= 0.24
        )
        if is_shaft_part:
            frm[2] += dz
            to[2] += dz
            moved_shafts += 1
            if "rotation" in element:
                element["rotation"]["origin"][2] += dz
    print(f"Moved both reindeer 1.20 blocks further back; moved {moved_shafts} sleigh-shaft parts with them.")

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
    make_pillar_trim(LIVE / "pillar_trim.png")
    make_sleigh_cushion(LIVE / "sleigh_cushion.png")

    model.setdefault("textures", {})
    model["textures"].update({
        "lanternDark": "minecraft:custom/maumod/mausmp/weihnachtskiste/lantern_dark",
        "base": "minecraft:custom/maumod/mausmp/weihnachtskiste/lower_body",
        "baseTop": "minecraft:custom/maumod/mausmp/weihnachtskiste/lower_body_top",
        "pillar": "minecraft:custom/maumod/mausmp/weihnachtskiste/pillar_trim",
        "sleighCushion": "minecraft:custom/maumod/mausmp/weihnachtskiste/sleigh_cushion",
    })

    # Replace the flat bell/lamp motifs before adding the real 3D fixtures.
    replace_flat_lamp_sprites(model)
    scale_reindeer(model)
    move_reindeer_back(model)
    remove_two_front_uprights(model)
    duplicate_stage_lanterns(model)
    add_sleigh_details(model)

    # Add geometry once. The support fits directly below the existing floor/road
    # platform, so it fills the hollow without changing the sleigh, reindeer or trees.
    support = next(
        (e for e in model["elements"]
         if e.get("from") == [-0.28, 6.75, 4.38]
         and e.get("to", [None])[0] == 16.28
         and e.get("to", [None, None, None])[2] == 11.62),
        None
    )
    if support is None:
        support_faces = {
            "north": {"uv": [0,0,16,16], "texture": "#base"},
            "south": {"uv": [0,0,16,16], "texture": "#base"},
            "east": {"uv": [0,0,16,16], "texture": "#base"},
            "west": {"uv": [0,0,16,16], "texture": "#base"},
            "up": {"uv": [0,0,16,16], "texture": "#baseTop"},
            "down": {"uv": [0,0,16,16], "texture": "#lanternDark"},
        }
        add_box(model, (-0.28, 6.75, 4.38), (16.28, 9.15, 11.62), "base", support_faces)
        for frm,to in (
            ((-0.34, 8.95, 4.34), (16.34, 9.09, 4.50)),
            ((-0.34, 8.95, 11.50), (16.34, 9.09, 11.66)),
            ((-0.42, 8.95, 4.50), (-0.28, 9.09, 11.50)),
            ((16.28, 8.95, 4.50), (16.42, 9.09, 11.50)),
        ):
            add_box(model, frm, to, "gold")
    else:
        # The previous fill stopped at 8.54, leaving a 0.64-block air gap.
        # Raise the same solid support to 9.15, just beneath the display floor at 9.18.
        support["to"][1] = 9.15
        # Keep the four brass perimeter rails at the top of the extended support.
        for element in model["elements"]:
            frm, to = element.get("from"), element.get("to")
            if not frm or not to or abs(frm[1]-6.72) > 0.002 or abs(to[1]-6.86) > 0.002:
                continue
            if (abs(frm[0]+0.34)<0.002 and abs(to[0]-16.34)<0.002) or                (abs(frm[0]+0.42)<0.002 and abs(to[0]+0.28)<0.002) or                (abs(frm[0]-16.28)<0.002 and abs(to[0]-16.42)<0.002):
                frm[1], to[1] = 8.95, 9.09
        print("Extended the solid support to y=9.15 directly beneath the display floor at y=9.18.")

    MODEL.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Refined Christmas model: {len(model['elements'])} geometry elements.")
    print("Added one solid support under the road and six wall-mounted exterior lanterns.")
    print("Cleaned the flat lamp sprites from front/side atlases; preserved the other crate animations.")
    print("Only Christmas-crate model and texture assets were written.")

if __name__ == "__main__":
    main()
