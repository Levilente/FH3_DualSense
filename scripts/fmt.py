import sys,zipfile,glob,numpy as np
sys.path.insert(0,'/home/claude/fh3_launchcontrol/scripts/icontools')
from PIL import Image
from bc import decode
from bc7enc import encode
Z=glob.glob('/mnt/user-data/uploads/**/ControllerIcons.zip',recursive=True)[0]
zf=zipfile.ZipFile(Z)
def morton_idx(bw,bh,tile=8):
    ys,xs=np.mgrid[0:bh,0:bw]; lx,ly=xs&7,ys&7
    m=(lx&1)|((ly&1)<<1)|(((lx>>1)&1)<<2)|(((ly>>1)&1)<<3)|(((lx>>2)&1)<<4)|(((ly>>2)&1)<<5)
    return ((ys>>3)*(bw>>3)+(xs>>3))*64+m
def large_decode(d):
    blocks=np.frombuffer(d[87:],dtype=np.uint8).reshape(-1,16)
    idx=morton_idx(32,32)
    b=blocks[idx.reshape(-1)]
    return np.array(Image.open(__import__('io').BytesIO(decode(b.tobytes(),128,128,98))) if False else decode(b.tobytes(),128,128,98))
