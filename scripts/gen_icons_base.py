import sys,struct,math;sys.path.insert(0,'/tmp/ic')
from fmt import *
from PIL import ImageDraw,ImageFont
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def unpre(a):
    al=a[...,3:4].astype(np.float32); o=a.copy()
    o[...,:3]=np.clip(np.where(al>0,a[...,:3]*255.0/np.maximum(al,1),0),0,255).astype(np.uint8); return o
def pre(a):
    al=a[...,3:4].astype(np.float32)/255; o=a.copy()
    o[...,:3]=np.clip(np.round(a[...,:3]*al),0,255).astype(np.uint8); return o
def face(L,kind,col):
    a=unpre(L).astype(np.float32); h,w,_=a.shape
    ys,xs=np.mgrid[0:h,0:w]; r=np.hypot(xs-63.5,ys-63.5)
    # inner dark colour sampled on a circle at r=44 (skipping the letter's colour)
    pts=[a[int(63.5+44*math.sin(t)),int(63.5+44*math.cos(t))] for t in np.linspace(0,6.28,40)]
    pts=[p for p in pts if max(p[:3])-min(p[:3])<20]; dark=np.median(pts,axis=0)[:3]
    sat=(a[...,:3].max(-1)-a[...,:3].min(-1))>60
    ring=sat&(r>50)
    a[ring,:3]=col
    a[(r<=50)&(a[...,3]>0),:3]=dark
    im=Image.fromarray(a.astype(np.uint8),'RGBA')
    S=4; g=Image.new('RGBA',(128*S,128*S),(0,0,0,0)); d=ImageDraw.Draw(g); c=64*S; wd=9*S
    colt=tuple(int(x) for x in col)+(255,)
    if kind=='cross':
        k=21*S; d.line([(c-k,c-k),(c+k,c+k)],fill=colt,width=wd); d.line([(c-k,c+k),(c+k,c-k)],fill=colt,width=wd)
        for p in [(c-k,c-k),(c+k,c+k),(c-k,c+k),(c+k,c-k)]: d.ellipse([p[0]-wd/2,p[1]-wd/2,p[0]+wd/2,p[1]+wd/2],fill=colt)
    elif kind=='circle':
        k=25*S; d.ellipse([c-k,c-k,c+k,c+k],outline=colt,width=wd)
    elif kind=='square':
        k=22*S; d.rounded_rectangle([c-k,c-k,c+k,c+k],radius=3*S,outline=colt,width=wd)
    else:
        R=30*S; pts=[(c,c-R+2*S),(c+R*0.866,c+R*0.5+2*S),(c-R*0.866,c+R*0.5+2*S)]
        d.line(pts+[pts[0],pts[1]],fill=colt,width=wd,joint='curve')
    g=g.resize((128,128),Image.LANCZOS); im.alpha_composite(g)
    return np.array(im)
def pill(L,text):
    a=unpre(L).astype(np.float32); h,w,_=a.shape
    ys,xs=np.where(a[...,3]>128); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    fill=a[(y0+y1)//2,x0+10] if False else a[y0+16,(x0+x1)//2]
    ins=15
    a[y0+ins:y1-ins+1,x0+ins:x1-ins+1,:3]=fill[:3]; a[y0+ins:y1-ins+1,x0+ins:x1-ins+1,3]=255
    im=Image.fromarray(a.astype(np.uint8),'RGBA'); S=4
    g=Image.new('RGBA',(128*S,128*S),(0,0,0,0)); d=ImageDraw.Draw(g)
    f=ImageFont.truetype(FONT,int((44 if x1-x0>100 else 40)*S))
    cx,cy=(x0+x1+1)/2*S,(y0+y1+1)/2*S
    d.text((cx,cy),text,font=f,fill=(232,232,232,255),anchor='mm')
    g=g.resize((128,128),Image.LANCZOS); im.alpha_composite(g)
    return np.array(im)
EDITS={'Controller_A':('face','cross',(104,160,232)),'Controller_B':('face','circle',(255,92,100)),
'Controller_X':('face','square',(232,140,200)),'Controller_Y':('face','triangle',(64,214,170)),
'Controller_LB':('pill','L1'),'Controller_RB':('pill','R1'),'Controller_LT':('pill','L2'),'Controller_RT':('pill','R2')}
IDX=morton_idx(32,32)
def enc_large(hdr,rgba_pre):
    blocks=np.frombuffer(encode(rgba_pre),np.uint8).reshape(32,32,16)
    out=np.zeros((1024,16),np.uint8)
    for by in range(32):
        for bx in range(32): out[IDX[by,bx]]=blocks[by,bx]
    return out.tobytes()
def enc_small(rgba_pre):
    out=np.zeros((1024,4),np.uint8); out[IDX.reshape(-1)]=rgba_pre.reshape(-1,4); return out.tobytes()
blob=bytearray(); n=0; files={}
for nm,ed in EDITS.items():
    Lf=zf.read('Large/%s.swatchbin'%nm); Sf=zf.read(nm+'.swatchbin')
    Lo=large_decode(Lf)
    new=face(Lo,ed[1],ed[2]) if ed[0]=='face' else pill(Lo,ed[1])
    newp=pre(new)
    Image.fromarray(new,'RGBA').save('ps_%s.png'%nm)
    small=np.array(Image.fromarray(newp,'RGBA').resize((32,32),Image.BOX))
    for kind,hdr,xb,pb,paths in [('L',Lf[:87],Lf[87:],enc_large(Lf[:87],newp),['Large/'+nm+'.swatchbin']),
                               ('S',Sf[:87],Sf[87:],enc_small(small),[nm+'.swatchbin','Medium/'+nm+'.swatchbin'])]:
        assert len(pb)==len(xb),(len(pb),len(xb))
        blob+=struct.pack('<II',len(xb),len(paths))
        for p in paths: blob+=bytes([len(p)])+p.encode()
        blob+=hdr+xb+pb; n+=1
open('icons.bin','wb').write(struct.pack('<I',n)+bytes(blob)); print(n,len(blob))
# preview
sheet=Image.new('RGBA',(8*130,130),(60,60,70,255))
for k,nm in enumerate(EDITS): sheet.alpha_composite(Image.open('ps_%s.png'%nm),(k*130+1,1))
sheet.save('ps_sheet.png')
