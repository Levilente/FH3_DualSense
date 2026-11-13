import sys,struct,math;sys.path.insert(0,'/tmp/ic')
src=open('scripts/gen_icons_base.py').read(); exec(src[:src.index("EDITS={")])
SS=4
_g=open('scripts/gen_icons_base.py').read(); exec(_g[_g.index('IDX='):_g.index('blob=bytearray()')])
def keycap_img(text,fs,w=116,h=116,cx=64,cy=64,arrow=None):
    g=Image.new('RGBA',(128*SS,128*SS),(0,0,0,0)); d=ImageDraw.Draw(g)
    x0,y0,x1,y1=(cx-w/2)*SS,(cy-h/2)*SS,(cx+w/2)*SS,(cy+h/2)*SS
    d.rounded_rectangle([x0,y0,x1,y1],radius=16*SS,fill=(225,225,225,255))
    d.rounded_rectangle([x0+6*SS,y0+6*SS,x1-6*SS,y1-6*SS],radius=11*SS,fill=(32,32,32,255))
    if arrow:
        R=24*SS; c=(cx*SS,cy*SS)
        pts={'u':[(c[0],c[1]-R),(c[0]+R,c[1]+R*0.7),(c[0]-R,c[1]+R*0.7)],'d':[(c[0],c[1]+R),(c[0]+R,c[1]-R*0.7),(c[0]-R,c[1]-R*0.7)],
             'l':[(c[0]-R,c[1]),(c[0]+R*0.7,c[1]-R),(c[0]+R*0.7,c[1]+R)],'r':[(c[0]+R,c[1]),(c[0]-R*0.7,c[1]-R),(c[0]-R*0.7,c[1]+R)]}[arrow]
        d.polygon(pts,fill=(232,232,232,255))
    else:
        f=ImageFont.truetype(FONT,fs*SS); d.text((cx*SS,cy*SS),text,font=f,fill=(232,232,232,255),anchor='mm')
    return g
def to_arr(g): return np.array(g.resize((128,128),Image.LANCZOS))
def keycap(text,fs): return to_arr(keycap_img(text,fs))
def arrowcap(a): return to_arr(keycap_img('',0,arrow=a))
def two(a,b):
    g=Image.new('RGBA',(128*SS,128*SS),(0,0,0,0))
    for (cx,arr) in ((33,a),(95,b)):
        t=keycap_img('',0,w=56,h=56,cx=cx,cy=64,arrow=arr)
        g.alpha_composite(t)
    return to_arr(g)
def pillkey(L,text,fs):
    a=unpre(L).astype(np.float32)
    ys,xs=np.where(a[...,3]>128); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    fill=a[y0+16,(x0+x1)//2]; ins=15
    a[y0+ins:y1-ins+1,x0+ins:x1-ins+1,:3]=fill[:3]; a[y0+ins:y1-ins+1,x0+ins:x1-ins+1,3]=255
    im=Image.fromarray(a.astype(np.uint8),'RGBA')
    g=Image.new('RGBA',(128*SS,128*SS),(0,0,0,0)); d=ImageDraw.Draw(g)
    d.text(((x0+x1+1)/2*SS,(y0+y1+1)/2*SS),text,font=ImageFont.truetype(FONT,fs*SS),fill=(232,232,232,255),anchor='mm')
    im.alpha_composite(g.resize((128,128),Image.LANCZOS)); return np.array(im)
PS={'Controller_A':('face','cross',(104,160,232)),'Controller_B':('face','circle',(255,92,100)),
'Controller_X':('face','square',(232,140,200)),'Controller_Y':('face','triangle',(64,214,170)),
'Controller_LB':('pill','L1'),'Controller_RB':('pill','R1'),'Controller_LT':('pill','L2'),'Controller_RT':('pill','R2')}
KEYS={'Controller_A':lambda L:keycap('Space',30),'Controller_B':lambda L:keycap('E',64),'Controller_X':lambda L:keycap('Q',64),'Controller_Y':lambda L:keycap('R',64),
'Controller_LB':lambda L:pillkey(L,'Shift',30),'Controller_RB':lambda L:pillkey(L,'C',50),'Controller_LT':lambda L:pillkey(L,'S',50),'Controller_RT':lambda L:pillkey(L,'W',50),
'Controller_Menu':lambda L:keycap('Esc',40),'Controller_View':lambda L:keycap('Tab',40),
'Controller_DPadUp':lambda L:arrowcap('u'),'Controller_DPadDown':lambda L:arrowcap('d'),'Controller_DPadLeft':lambda L:arrowcap('l'),'Controller_DPadRight':lambda L:arrowcap('r'),
'Controller_DPadLeftRight':lambda L:two('l','r'),'Controller_DPadUpDown':lambda L:two('u','d')}
names=sorted(set(PS)|set(KEYS))
low={i.filename.lower():i.filename for i in zf.infolist()}
blob=bytearray(); n=0; prev=[]
for nm in names:
    Lf=zf.read('Large/%s.swatchbin'%nm); Lo=large_decode(Lf)
    looks=[None,None,None]
    if nm in PS:
        e=PS[nm]; looks[1]=face(Lo,e[1],e[2]) if e[0]=='face' else pill(Lo,e[1])
    if nm in KEYS: looks[2]=KEYS[nm](Lo)
    rootname=low[(nm+'.swatchbin').lower()]; medname=low[('medium/'+nm+'.swatchbin').lower()]
    Sf=zf.read(rootname)
    for kind,hdr,xb,paths in [('L',Lf[:87],Lf[87:],['Large/'+nm+'.swatchbin']),('S',Sf[:87],Sf[87:],[rootname,medname])]:
        datas=[xb]
        for lk in (1,2):
            if looks[lk] is None: datas.append(xb); continue
            p=pre(looks[lk])
            if kind=='L': datas.append(enc_large(hdr,p))
            else: datas.append(enc_small(np.array(Image.fromarray(p,'RGBA').resize((32,32),Image.BOX))))
        assert all(len(d)==len(xb) for d in datas)
        blob+=struct.pack('<II',len(xb),len(paths))
        for pth in paths: blob+=bytes([len(pth)])+pth.encode()
        blob+=hdr+b''.join(datas); n+=1
    for lk in (1,2):
        if looks[lk] is not None: Image.fromarray(looks[lk],'RGBA').save('look%d_%s.png'%(lk,nm))
open('icons3.bin','wb').write(struct.pack('<I',n)+bytes(blob)); print(n,len(blob),names)
sheet=Image.new('RGBA',(8*130,2*130),(60,60,70,255))
for k,nm in enumerate(names):
    try: sheet.alpha_composite(Image.open('look2_%s.png'%nm),((k%8)*130+1,(k//8)*130+1))
    except Exception: pass
sheet.save('keys_sheet.png')
