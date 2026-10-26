import cv2, numpy as np, csv, glob, os
from pathlib import Path

BASE=Path(os.environ.get('ANALYSIS_DATA_DIR', Path(__file__).resolve().parent))
files4=sorted(glob.glob(str(BASE/'seq4k'/'*.png')))
files1=sorted(glob.glob(str(BASE/'seq1080'/'*.png')))
files2=sorted(glob.glob(str(BASE/'seq1440'/'*.png')))
assert len(files4)==len(files1)==len(files2), (len(files4),len(files1),len(files2))

def gray(p):
    im=cv2.imread(p,cv2.IMREAD_COLOR)
    return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)

def psnr(a,b,m=64):
    h,w=a.shape
    mse=np.mean((a[m:h-m,m:w-m]-b[m:h-m,m:w-m])**2)
    return 10*np.log10(255**2/mse) if mse>0 else 99

def rad_psd(img):
    h,w=img.shape
    win=np.outer(np.hanning(h),np.hanning(w)).astype(np.float32)
    f=np.fft.fftshift(np.fft.fft2((img-img.mean())*win))
    p=(np.abs(f)**2).astype(np.float64)
    yy,xx=np.indices((h,w)); cy,cx=h//2,w//2
    r=np.sqrt(((yy-cy)/h)**2+((xx-cx)/w)**2)
    nb=120; bins=np.linspace(0,0.5,nb+1)
    idx=np.digitize(r.ravel(),bins)-1
    ps=np.bincount(idx,weights=p.ravel(),minlength=nb)[:nb]
    pc=np.bincount(idx,minlength=nb)[:nb]
    prof=ps/np.maximum(pc,1); centers=(bins[:-1]+bins[1:])/2
    return centers,prof

rows=[]
for i,(p4,p1,p2) in enumerate(zip(files4,files1,files2),1):
    g4=gray(p4); g1=gray(p1); g2=gray(p2)
    h,w=g4.shape
    # roundtrip 4K through 1080 and 1440
    s1=cv2.resize(g4,(1920,1080),interpolation=cv2.INTER_AREA)
    u1=cv2.resize(s1,(w,h),interpolation=cv2.INTER_LANCZOS4)
    s2=cv2.resize(g4,(2560,1440),interpolation=cv2.INTER_AREA)
    u2=cv2.resize(s2,(w,h),interpolation=cv2.INTER_LANCZOS4)
    # actual lower renditions upscaled
    a1=cv2.resize(g1,(w,h),interpolation=cv2.INTER_LANCZOS4)
    a2=cv2.resize(g2,(w,h),interpolation=cv2.INTER_LANCZOS4)
    # spectrum on central 1024 crop of 4K
    cy,cx=h//2,w//2; hs=512
    c4=g4[cy-hs:cy+hs,cx-hs:cx+hs]
    centers,prof=rad_psd(c4)
    lo=prof[(centers>0.03)&(centers<0.10)].mean()
    hi=prof[(centers>0.28)&(centers<0.45)].mean()
    mid=prof[(centers>0.12)&(centers<0.22)].mean()
    # 1080 own spectrum, central 512 crop
    cy1,cx1=g1.shape[0]//2,g1.shape[1]//2; hs1=256
    c1=g1[cy1-hs1:cy1+hs1,cx1-hs1:cx1+hs1]
    cen1,pr1=rad_psd(c1)
    lo1=pr1[(cen1>0.03)&(cen1<0.10)].mean()
    hi1=pr1[(cen1>0.28)&(cen1<0.45)].mean()
    # brightness / detail
    var4=float(np.var(c4)); lap4=float(cv2.Laplacian(c4,cv2.CV_32F).var())
    rows.append(dict(i=i,t=(i-1)*10+5,psnr_rt1080=psnr(g4,u1),psnr_rt1440=psnr(g4,u2),
                     psnr_up1080=psnr(g4,a1),psnr_up1440=psnr(g4,a2),
                     hf_ratio=float(hi/lo),hf_mid=float(hi/mid),hf1080=float(hi1/lo1),
                     var4=var4,lap4=lap4))
    if i%10==0: print('done',i)

with open(BASE/'timeseries.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('wrote',BASE/'timeseries.csv')
import statistics
for k in ['psnr_rt1080','psnr_rt1440','psnr_up1080','psnr_up1440','hf_ratio','hf1080']:
    v=[r[k] for r in rows]
    print(k,'min',round(min(v),2),'median',round(statistics.median(v),2),'max',round(max(v),2))
