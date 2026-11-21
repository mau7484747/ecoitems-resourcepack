#!/usr/bin/env python3
"""Build the animated MAUSMP winter-pickaxe material atlas (8 frames, 128x1024)."""
from PIL import Image, ImageDraw
from pathlib import Path
import math, random
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/minecraft/textures/item/netherite_pickaxe_mau_winter.png"
SIZE=128; CELL=32; FRAMES=8
random.seed(214748)
atlas=Image.new("RGBA",(SIZE,SIZE),(0,0,0,255))
def make_tile(top,bottom):
 im=Image.new("RGBA",(CELL,CELL),(0,0,0,255)); d=ImageDraw.Draw(im)
 for y in range(CELL):
  t=y/(CELL-1); col=tuple(round(top[i]*(1-t)+bottom[i]*t) for i in range(3))+(255,)
  d.line((0,y,CELL,y),fill=col)
 return im
def place(c,r,im): atlas.alpha_composite(im,(c*CELL,r*CELL))
def flecks(d,colors,count):
 for _ in range(count):
  x=random.randint(1,30); y=random.randint(1,30); col=random.choice(colors)
  d.rectangle((x,y,x+random.choice((0,1)),y+random.choice((0,1))),fill=col)
# Ruby crystal blade
im=make_tile((152,21,43),(29,3,20)); d=ImageDraw.Draw(im)
d.polygon([(1,9),(9,2),(25,4),(31,12),(26,26),(10,30),(2,21)],fill=(125,8,34,255),outline=(255,162,153,255))
d.polygon([(2,9),(9,2),(16,12),(8,18)],fill=(231,71,81,255)); d.polygon([(9,2),(25,4),(21,14),(16,12)],fill=(255,129,124,255))
d.polygon([(25,4),(31,12),(23,22),(21,14)],fill=(97,5,29,255)); d.line([(2,9),(9,2),(25,4),(31,12)],fill=(255,235,220,255),width=2)
d.line([(4,14),(14,8),(24,10),(29,16)],fill=(255,85,92,255),width=2); flecks(d,[(255,183,168,255),(247,68,77,255),(71,5,24,255)],26); place(0,0,im)
# Ice
im=make_tile((222,251,255),(65,135,177)); d=ImageDraw.Draw(im)
d.polygon([(1,25),(4,9),(12,1),(23,4),(31,19),(24,30)],fill=(174,230,248,255),outline=(255,255,255,255))
d.polygon([(4,9),(12,1),(16,14),(9,21)],fill=(255,255,255,255)); d.polygon([(12,1),(23,4),(24,18),(16,14)],fill=(149,215,240,255))
d.line([(2,25),(4,9),(12,1),(23,4),(31,19)],fill=(255,255,255,255),width=2); flecks(d,[(255,255,255,255),(143,224,250,255)],28); place(1,0,im)
# Gold
im=make_tile((255,232,148),(104,58,12)); d=ImageDraw.Draw(im)
d.rectangle((2,2,29,29),outline=(255,248,199,255)); d.rectangle((5,5,26,26),outline=(164,101,23,255))
d.arc((6,6,25,26),185,510,fill=(255,244,171,255),width=2); d.line([(6,23),(13,15),(20,21),(27,8)],fill=(255,238,152,255),width=2)
for x,y in ((5,5),(26,5),(5,26),(26,26)): d.ellipse((x-1,y-1,x+1,y+1),fill=(255,255,220,255))
flecks(d,[(255,248,192,255),(202,135,32,255)],18); place(2,0,im)
# Dark metal
im=make_tile((72,82,95),(17,24,36)); d=ImageDraw.Draw(im)
for y in range(2,32,3): d.line((1,y,31,y),fill=(142,154,166,140),width=1)
d.rectangle((2,2,29,29),outline=(201,163,79,255))
for x,y in ((5,5),(26,5),(5,26),(26,26)): d.ellipse((x-1,y-1,x+1,y+1),fill=(230,192,103,255))
place(3,0,im)
# Wood
im=make_tile((111,61,31),(29,13,9)); d=ImageDraw.Draw(im)
for x in (4,8,12,18,23,28): d.line((x,1,x+random.choice((-2,0,2)),30),fill=random.choice(((172,103,54,255),(70,35,19,255),(205,130,73,210))),width=1)
d.ellipse((10,10,22,23),outline=(187,119,61,255)); d.ellipse((13,13,19,20),outline=(44,20,12,255)); place(0,1,im)
# Velvet
im=make_tile((139,16,43),(45,3,21)); d=ImageDraw.Draw(im)
for s in range(-32,64,9):
 d.line((s,0,s+32,32),fill=(246,194,141,255),width=1); d.line((s,32,s+32,0),fill=(91,15,34,255),width=1)
for x in (5,14,23):
 for y in (5,14,23): d.point((x,y),fill=(255,224,178,255))
d.rectangle((1,1,30,30),outline=(239,220,185,255)); place(1,1,im)
# Fur
im=make_tile((255,255,244),(151,159,171)); d=ImageDraw.Draw(im)
for _ in range(120):
 x=random.randint(1,30); y=random.randint(1,30)
 d.line((x,y,x+random.choice((-1,0,1)),min(31,y+random.randint(1,4))),fill=random.choice(((255,255,255,255),(226,231,232,255),(179,188,195,255))),width=1)
place(2,1,im)
# Evergreen
im=make_tile((16,76,46),(2,21,23)); d=ImageDraw.Draw(im)
for x in (5,12,19,26):
 d.line((x,3,x+2,29),fill=(123,161,74,255),width=1)
 for y in (8,15,22):
  d.polygon([(x,y),(x-5,y-3),(x-2,y+2)],fill=(35,126,57,255)); d.polygon([(x+1,y+2),(x+6,y-2),(x+3,y+4)],fill=(22,96,45,255))
for x,y in ((9,7),(22,17),(14,25)): d.ellipse((x-2,y-2,x+2,y+2),fill=(187,13,26,255),outline=(255,145,114,255))
place(3,1,im)
# Star
im=make_tile((255,244,178),(117,64,12)); d=ImageDraw.Draw(im); pts=[]
for i in range(16):
 a=-math.pi/2+i*math.pi/8; r=14 if i%2==0 else 6; pts.append((16+math.cos(a)*r,16+math.sin(a)*r))
d.polygon(pts,fill=(255,200,55,255),outline=(255,250,215,255)); d.ellipse((11,11,21,21),fill=(255,241,153,255),outline=(161,91,12,255)); d.ellipse((14,14,18,18),fill=(255,255,230,255)); place(0,2,im)
# Candy cane
im=make_tile((255,255,247),(202,206,203)); d=ImageDraw.Draw(im)
for s in range(-32,64,9): d.polygon([(s,0),(s+5,0),(s+32,32),(s+27,32)],fill=(190,12,34,255))
d.rectangle((1,1,30,30),outline=(235,206,153,255)); place(1,2,im)
# Runes
im=make_tile((61,13,27),(11,6,17)); d=ImageDraw.Draw(im); d.rectangle((2,2,29,29),outline=(192,139,59,255))
for x in (9,16,23):
 d.line((x,5,x,27),fill=(255,211,93,255),width=2); d.line((x-4,11,x+4,15),fill=(255,238,148,255),width=1); d.line((x+4,18,x-4,23),fill=(196,130,43,255),width=1)
place(2,2,im)
# Bell
im=make_tile((255,226,116),(105,58,13)); d=ImageDraw.Draw(im); d.arc((8,2,24,18),180,360,fill=(255,246,193,255),width=2)
d.polygon([(9,14),(23,14),(29,26),(3,26)],fill=(223,157,37,255),outline=(255,235,153,255)); d.line((4,25,28,25),fill=(128,76,17,255),width=2); d.ellipse((14,26,18,30),fill=(255,247,200,255)); place(0,3,im)
# Icicle
im=make_tile((220,251,255),(58,131,174)); d=ImageDraw.Draw(im)
for x,w,h in ((2,9,20),(11,10,28),(21,9,23)):
 d.polygon([(x,2),(x+w,2),(x+w//2,h)],fill=(168,228,247,255),outline=(255,255,255,255)); d.line((x+2,4,x+w//2,h-3),fill=(255,255,255,255),width=1)
place(1,3,im)
# Polished gold
im=make_tile((255,255,218),(158,92,16)); d=ImageDraw.Draw(im)
d.polygon([(2,4),(30,4),(27,9),(5,9)],fill=(255,255,244,255)); d.polygon([(5,9),(27,9),(27,27),(5,30)],fill=(236,170,43,255),outline=(255,247,185,255)); d.line((6,11,26,11),fill=(255,255,219,255),width=1); place(2,3,im)
# Frost
im=make_tile((18,72,101),(3,24,51)); d=ImageDraw.Draw(im); d.rectangle((2,2,29,29),outline=(154,229,249,255))
for i in range(6):
 a=i*math.pi/3; x=16+math.cos(a)*12; y=16+math.sin(a)*12
 d.line((16,16,x,y),fill=(236,253,255,255),width=1); a2=a+math.pi/4; bx=16+math.cos(a)*8; by=16+math.sin(a)*8
 d.line((bx,by,bx+math.cos(a2)*4,by+math.sin(a2)*4),fill=(172,235,255,255),width=1)
place(3,3,im)
# Animated frames: red core pulse, traveling ruby glints and a tiny star twinkle.
frames=[]
for frame in range(FRAMES):
 f=atlas.copy(); energy=make_tile((45,4,24),(6,9,24)); d=ImageDraw.Draw(energy); phase=frame*math.pi/4
 cx=16+round(math.sin(phase)*1.5); cy=16+round(math.cos(phase)*1.5)
 for rad,col in ((14,(105,6,34,255)),(11,(176,14,47,255)),(8,(239,42,63,255)),(5,(255,122,104,255)),(2,(255,241,191,255))):
  d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=col,outline=(255,211,166,200))
 for i in range(8):
  a=phase*.55+i*math.pi/4; d.line((cx+math.cos(a)*4,cy+math.sin(a)*4,cx+math.cos(a+.35)*14,cy+math.sin(a+.35)*14),fill=(255,117,98,255),width=1)
 d.ellipse((cx-2,cy-2,cx+2,cy+2),fill=(255,255,237,255)); f.alpha_composite(energy,(3*CELL,2*CELL))
 d=ImageDraw.Draw(f); bx=frame*3; d.line((1+bx,8,8+bx,14),fill=(255,234,202,255),width=1); d.ellipse((4+bx,6,6+bx,8),fill=(255,255,243,255))
 sx=4+(frame*6)%24; sy=4+(frame*3)%24; d.line((sx-2,sy,sx+2,sy),fill=(255,255,242,255),width=1); d.line((sx,sy-2,sx,sy+2),fill=(255,255,242,255),width=1)
 frames.append(f)
sheet=Image.new("RGBA",(SIZE,SIZE*FRAMES),(0,0,0,255))
for i,frame in enumerate(frames): sheet.alpha_composite(frame,(0,i*SIZE))
OUT.parent.mkdir(parents=True,exist_ok=True)
sheet.convert("RGB").quantize(colors=64,method=Image.Quantize.MEDIANCUT).save(OUT,optimize=True)
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes), {FRAMES} frames, {SIZE}x{SIZE*FRAMES}")
