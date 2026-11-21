#!/usr/bin/env python3
"""Build an 8-frame animated material atlas for the MAUSMP winter pickaxe.
The atlas is 128x1024: eight 128x128 frames stacked vertically.
Minecraft model UV coordinates stay in the 0..16 range; each material occupies a 4x4 UV tile.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math
import random

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/minecraft/textures/item/netherite_pickaxe_mau_winter.png"
SIZE=128
CELL=32
FRAMES=8
random.seed(214748)

def gradient(top,bottom):
    im=Image.new("RGBA",(CELL,CELL),(0,0,0,255))
    d=ImageDraw.Draw(im)
    for y in range(CELL):
        t=y/(CELL-1)
        color=tuple(round(top[i]*(1-t)+bottom[i]*t) for i in range(3))+(255,)
        d.line((0,y,CELL,y),fill=color)
    return im

atlas=Image.new("RGBA",(SIZE,SIZE),(0,0,0,255))
def place(col,row,im):
    atlas.alpha_composite(im,(col*CELL,row*CELL))

def sparkles(draw,colors,n):
    for _ in range(n):
        x=random.randint(1,30)
        y=random.randint(1,30)
        color=random.choice(colors)
        draw.rectangle((x,y,x+random.choice((0,1)),y+random.choice((0,1))),fill=color)

# Ruby crystal pickaxe blade.
im=gradient((170,27,48),(32,4,22)); d=ImageDraw.Draw(im)
d.polygon([(1,10),(8,2),(25,4),(31,13),(25,28),(9,30),(2,21)],fill=(119,5,31,255),outline=(255,184,174,255))
d.polygon([(2,10),(8,2),(16,13),(8,20)],fill=(241,88,94,255))
d.polygon([(8,2),(25,4),(21,15),(16,13)],fill=(255,148,137,255))
d.polygon([(25,4),(31,13),(25,28),(21,15)],fill=(94,5,27,255))
d.line([(2,10),(8,2),(25,4),(31,13)],fill=(255,246,231,255),width=2)
d.line([(4,19),(14,12),(25,15),(28,22)],fill=(255,73,82,255),width=2)
sparkles(d,[(255,221,206,255),(255,95,96,255),(69,4,20,255)],30)
place(0,0,im)

# Frosted blue-white cutting edge.
im=gradient((244,255,255),(67,137,183)); d=ImageDraw.Draw(im)
d.polygon([(1,25),(4,9),(12,1),(24,4),(31,19),(24,30)],fill=(178,234,251,255),outline=(255,255,255,255))
d.polygon([(4,9),(12,1),(16,14),(9,21)],fill=(255,255,255,255))
d.polygon([(12,1),(24,4),(24,18),(16,14)],fill=(150,219,245,255))
d.line([(2,25),(4,9),(12,1),(24,4),(31,19)],fill=(255,255,255,255),width=2)
sparkles(d,[(255,255,255,255),(146,229,253,255)],26)
place(1,0,im)

# Polished antique gold filigree.
im=gradient((255,239,166),(104,58,13)); d=ImageDraw.Draw(im)
d.rectangle((2,2,29,29),outline=(255,248,209,255),width=1)
d.rectangle((5,5,26,26),outline=(164,101,23,255))
d.arc((6,6,25,26),185,510,fill=(255,244,171,255),width=2)
d.line([(6,23),(13,15),(20,21),(27,8)],fill=(255,238,152,255),width=2)
for x,y in ((5,5),(26,5),(5,26),(26,26)):
    d.ellipse((x-1,y-1,x+1,y+1),fill=(255,255,220,255))
sparkles(d,[(255,248,192,255),(202,135,32,255)],18)
place(2,0,im)

# Dark brushed metal.
im=gradient((75,86,101),(17,23,35)); d=ImageDraw.Draw(im)
for y in range(2,32,3):
    d.line((1,y,31,y),fill=(142,154,166,155),width=1)
d.rectangle((2,2,29,29),outline=(201,163,79,255))
for x,y in ((5,5),(26,5),(5,26),(26,26)):
    d.ellipse((x-1,y-1,x+1,y+1),fill=(230,192,103,255))
place(3,0,im)

# 50/50 shaft tile: left half candy cane, right half carved walnut with gold runes.
im=gradient((126,69,37),(34,15,10)); d=ImageDraw.Draw(im)
d.rectangle((0,0,15,31),fill=(250,249,235,255))
for s in range(-32,48,8):
    d.polygon([(s,0),(s+4,0),(s+28,32),(s+24,32)],fill=(187,10,33,255))
d.rectangle((0,0,15,31),outline=(255,255,255,255))
for x in (18,22,27):
    d.line((x,2,x,29),fill=(89,43,21,255),width=1)
for y in (6,14,22):
    d.line((18,y,29,y),fill=(175,115,62,255),width=1)
    d.line((20,y-3,27,y+3),fill=(247,205,112,255),width=1)
d.line((16,0,16,31),fill=(255,221,130,255),width=2)
place(0,1,im)

# Quilted red velvet.
im=gradient((156,18,47),(48,3,24)); d=ImageDraw.Draw(im)
for s in range(-32,64,8):
    d.line((s,0,s+32,32),fill=(244,193,144,255),width=1)
    d.line((s,32,s+32,0),fill=(86,13,34,255),width=1)
for x in (5,14,23):
    for y in (5,14,23):
        d.point((x,y),fill=(255,226,181,255))
d.rectangle((1,1,30,30),outline=(239,220,185,255))
place(1,1,im)

# Soft white fur.
im=gradient((255,255,250),(142,151,162)); d=ImageDraw.Draw(im)
for _ in range(140):
    x=random.randint(1,30); y=random.randint(1,30)
    d.line((x,y,x+random.choice((-1,0,1)),min(31,y+random.randint(1,4))),
           fill=random.choice(((255,255,255,255),(225,231,234,255),(181,190,198,255))),width=1)
place(2,1,im)

# Evergreen sprigs and holly berries.
im=gradient((20,86,48),(2,22,22)); d=ImageDraw.Draw(im)
for x in (5,12,19,26):
    d.line((x,3,x+2,29),fill=(123,161,74,255),width=1)
    for y in (8,15,22):
        d.polygon([(x,y),(x-5,y-3),(x-2,y+2)],fill=(35,126,57,255))
        d.polygon([(x+1,y+2),(x+6,y-2),(x+3,y+4)],fill=(22,96,45,255))
for x,y in ((9,7),(22,17),(14,25)):
    d.ellipse((x-2,y-2,x+2,y+2),fill=(187,13,26,255),outline=(255,145,114,255))
place(3,1,im)

# Eight-point golden star.
im=gradient((255,247,187),(117,64,12)); d=ImageDraw.Draw(im); points=[]
for i in range(16):
    a=-math.pi/2+i*math.pi/8
    radius=14 if i%2==0 else 6
    points.append((16+math.cos(a)*radius,16+math.sin(a)*radius))
d.polygon(points,fill=(255,200,55,255),outline=(255,250,215,255))
d.ellipse((11,11,21,21),fill=(255,241,153,255),outline=(161,91,12,255))
d.ellipse((14,14,18,18),fill=(255,255,230,255))
place(0,2,im)

# Red-white candy cane.
im=gradient((255,255,250),(206,210,206)); d=ImageDraw.Draw(im)
for s in range(-32,64,8):
    d.polygon([(s,0),(s+4,0),(s+28,32),(s+24,32)],fill=(194,11,35,255))
d.rectangle((1,1,30,30),outline=(235,206,153,255))
place(1,2,im)

# Gold runic inlay.
im=gradient((66,14,28),(11,6,17)); d=ImageDraw.Draw(im)
d.rectangle((2,2,29,29),outline=(192,139,59,255))
for x in (9,16,23):
    d.line((x,5,x,27),fill=(255,211,93,255),width=2)
    d.line((x-4,11,x+4,15),fill=(255,238,148,255),width=1)
    d.line((x+4,18,x-4,23),fill=(196,130,43,255),width=1)
place(2,2,im)

# Brass bell.
im=gradient((255,231,129),(105,58,13)); d=ImageDraw.Draw(im)
d.arc((8,2,24,18),180,360,fill=(255,246,193,255),width=2)
d.polygon([(9,14),(23,14),(29,26),(3,26)],fill=(223,157,37,255),outline=(255,235,153,255))
d.line((4,25,28,25),fill=(128,76,17,255),width=2)
d.ellipse((14,26,18,30),fill=(255,247,200,255))
place(0,3,im)

# Translucent ice teeth.
im=gradient((231,252,255),(58,131,174)); d=ImageDraw.Draw(im)
for x,w,h in ((2,9,20),(11,10,28),(21,9,23)):
    d.polygon([(x,2),(x+w,2),(x+w//2,h)],fill=(168,228,247,255),outline=(255,255,255,255))
    d.line((x+2,4,x+w//2,h-3),fill=(255,255,255,255),width=1)
place(1,3,im)

# Bright gold edge highlight.
im=gradient((255,255,228),(158,92,16)); d=ImageDraw.Draw(im)
d.polygon([(2,4),(30,4),(27,9),(5,9)],fill=(255,255,244,255))
d.polygon([(5,9),(27,9),(27,27),(5,30)],fill=(236,170,43,255),outline=(255,247,185,255))
d.line((6,11,26,11),fill=(255,255,219,255),width=1)
place(2,3,im)

# Frost filigree.
im=gradient((18,72,101),(3,24,51)); d=ImageDraw.Draw(im)
d.rectangle((2,2,29,29),outline=(154,229,249,255))
for i in range(6):
    a=i*math.pi/3
    x=16+math.cos(a)*12; y=16+math.sin(a)*12
    d.line((16,16,x,y),fill=(236,253,255,255),width=1)
    a2=a+math.pi/4; bx=16+math.cos(a)*8; by=16+math.sin(a)*8
    d.line((bx,by,bx+math.cos(a2)*4,by+math.sin(a2)*4),fill=(172,235,255,255),width=1)
place(3,3,im)

# Eight animation frames: pulsing red core and a moving crystalline glint.
frames=[]
for frame in range(FRAMES):
    current=atlas.copy()
    energy=gradient((54,5,27),(5,8,23)); d=ImageDraw.Draw(energy)
    phase=frame*math.pi/4
    cx=16+round(math.sin(phase)*1.4)
    cy=16+round(math.cos(phase)*1.4)
    for radius,color in ((14,(105,6,34,255)),(11,(176,14,47,255)),
                         (8,(239,42,63,255)),(5,(255,122,104,255)),
                         (2,(255,241,191,255))):
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=color,
                  outline=(255,211,166,220))
    for i in range(8):
        angle=phase*.55+i*math.pi/4
        d.line((cx+math.cos(angle)*4,cy+math.sin(angle)*4,
                cx+math.cos(angle+.35)*14,cy+math.sin(angle+.35)*14),
               fill=(255,117,98,255),width=1)
    d.ellipse((cx-2,cy-2,cx+2,cy+2),fill=(255,255,237,255))
    current.alpha_composite(energy,(3*CELL,2*CELL))
    d=ImageDraw.Draw(current)
    bx=(frame*3)%112
    d.line((bx,8,bx+8,15),fill=(255,238,210,255),width=1)
    d.ellipse((bx+3,5,bx+5,7),fill=(255,255,245,255))
    sx=4+(frame*6)%24
    sy=4+(frame*3)%24
    d.line((sx-2,sy,sx+2,sy),fill=(255,255,242,255),width=1)
    d.line((sx,sy-2,sx,sy+2),fill=(255,255,242,255),width=1)
    frames.append(current)

sheet=Image.new("RGBA",(SIZE,SIZE*FRAMES),(0,0,0,255))
for index,frame in enumerate(frames):
    sheet.alpha_composite(frame,(0,index*SIZE))
OUT.parent.mkdir(parents=True,exist_ok=True)
sheet.convert("RGB").quantize(colors=128,method=Image.Quantize.MEDIANCUT).save(OUT,optimize=True)
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes), {FRAMES} frames, {SIZE}x{SIZE*FRAMES}")
