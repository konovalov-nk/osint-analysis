import os, cv2, numpy as np
from skimage.metrics import structural_similarity as ssim
from pathlib import Path

DIR=Path(os.environ.get('ANALYSIS_DATA_DIR', Path(__file__).resolve().parent))

def load(t,n):
    im=cv2.imread(str(DIR/f'frames{n}'/f'f{t}.png'),cv2.IMREAD_COLOR)
    if im is None: raise FileNotFoundError(f'{n} {t}')
    return im

def to_gray(im): return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)

def best_shift(ref, mov, rng=2):
    # both same size; search integer shifts, return best psnr and shifted mov
    h,w=ref.shape
    m=40
    rc=ref[m:h-m,m:w-m]
    best=(-1,0,0,None)
    for dy in range(-rng,rng+1):
        for dx in range(-rng,rng+1):
            M=np.float32([[1,0,dx],[0,1,dy]])
            sm=cv2.warpAffine(mov,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
            sc=sm[m:h-m,m:w-m]
            mse=np.mean((rc-sc)**2)
            ps=10*np.log10(255**2/mse) if mse>0 else 99
            if ps>best[0]: best=(ps,dx,dy,sm)
    return best

def metrics(ref,mov,rng=2):
    ps,dx,dy,sm=best_shift(ref,mov,rng)
    h,w=ref.shape; m=60
    rc=ref[m:h-m,m:w-m].astype(np.uint8); sc=sm[m:h-m,m:w-m].astype(np.uint8)
    s=ssim(rc,sc,data_range=255)
    return ps,s,dx,dy

def roundtrip(im, target_w, target_h, out_w, out_h):
    small=cv2.resize(im,(target_w,target_h),interpolation=cv2.INTER_AREA)
    return cv2.resize(small,(out_w,out_h),interpolation=cv2.INTER_LANCZOS4)

print('round-trip self-consistency (4K -> lower -> 4K)')
for t in [240,360,480,600]:
    f4=load(t,'2160'); g4=to_gray(f4)
    for src in ['1080','1440','720']:
        n=src
        w={'720':1280,'1080':1920,'1440':2560}[n]
        h={'720':720,'1080':1080,'1440':1440}[n]
        u=roundtrip(f4,w,h,3840,2160)
        ps,s,dx,dy=metrics(g4,to_gray(u))
        print(f't={t} 4K->{src}->4K: PSNR={ps:.2f} SSIM={s:.4f} shift=({dx},{dy})')
    # baseline: 1080 roundtrip
    f1=load(t,'1080'); g1=to_gray(f1)
    u=roundtrip(f1,960,540,1920,1080)
    ps,s,dx,dy=metrics(g1,to_gray(u))
    print(f't={t} 1080->540->1080: PSNR={ps:.2f} SSIM={s:.4f} shift=({dx},{dy})')
    print()

print('actual cross-resolution prediction: upscale lower rendition to 4K')
for t in [240,360,480,600]:
    g4=to_gray(load(t,'2160'))
    for src in ['720','1080','1440']:
        g=to_gray(load(t,src))
        u=cv2.resize(g,(3840,2160),interpolation=cv2.INTER_LANCZOS4)
        ps,s,dx,dy=metrics(g4,u)
        print(f't={t} {src}->4K vs actual 4K: PSNR={ps:.2f} SSIM={s:.4f} shift=({dx},{dy})')
    print()

print('actual downscale: 4K -> lower vs native lower')
for t in [240,360,480,600]:
    g4=to_gray(load(t,'2160'))
    for dst in ['720','1080','1440']:
        w={'720':1280,'1080':1920,'1440':2560}[dst]
        h={'720':720,'1080':1080,'1440':1440}[dst]
        d=cv2.resize(g4,(w,h),interpolation=cv2.INTER_AREA)
        gn=to_gray(load(t,dst))
        ps,s,dx,dy=metrics(gn,d)
        print(f't={t} 4K->{dst} vs native {dst}: PSNR={ps:.2f} SSIM={s:.4f} shift=({dx},{dy})')
    print()
