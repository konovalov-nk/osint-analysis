import os, cv2, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

RES = ['1080','1440','2160']
DIR = Path(os.environ.get('ANALYSIS_DATA_DIR', Path(__file__).resolve().parent))

def load_gray(t, n):
    im = cv2.imread(str(DIR/f'frames{n}'/f'f{t}.png'), cv2.IMREAD_COLOR)
    if im is None: raise FileNotFoundError(f'frames{n}/f{t}.png')
    # BT.709 luma
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return g

def crop_resize(g, box, out_size, n):
    """box normalized (x0,x1,y0,y1) -> crop and resize to out_size."""
    h,w = g.shape
    x0,x1,y0,y1 = box
    c = g[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
    interp = cv2.INTER_AREA if c.shape[0] > out_size else cv2.INTER_LANCZOS4
    return cv2.resize(c, (out_size,out_size), interpolation=interp)

def rad_psd(img):
    h,w = img.shape
    win = np.outer(np.hanning(h), np.hanning(w)).astype(np.float32)
    f = np.fft.fftshift(np.fft.fft2((img-img.mean())*win))
    p = (np.abs(f)**2).astype(np.float64)
    yy,xx = np.indices((h,w))
    cy,cx = h//2, w//2
    r = np.sqrt(((yy-cy)/h)**2 + ((xx-cx)/w)**2)  # cycles/pixel
    nb = 120
    bins = np.linspace(0, 0.5, nb+1)
    idx = np.digitize(r.ravel(), bins)-1
    psum = np.bincount(idx, weights=p.ravel(), minlength=nb)[:nb]
    pcnt = np.bincount(idx, minlength=nb)[:nb]
    with np.errstate(invalid='ignore'):
        prof = psum/np.maximum(pcnt,1)
    centers = (bins[:-1]+bins[1:])/2
    return centers, prof

def highpass_vis(g, sigma=2.0):
    lo = cv2.GaussianBlur(g, (0,0), sigma)
    hp = g-lo
    v = np.clip(128 + hp*6, 0, 255).astype(np.uint8)
    return v

scenes = {
    'face_360': dict(t=360, box=(0.27,0.80,0.00,0.95), size=2048),
    'city_240': dict(t=240, box=(0.23,0.77,0.02,0.97), size=2048),
}
# text crop smaller
scenes_text = dict(t=120, box=(0.12,0.30,0.22,0.31), size=1024)

plt.figure(figsize=(9,6))
colors = {'1080':'tab:blue','1440':'tab:orange','2160':'tab:green'}
stats = {}
for name, cfg in scenes.items():
    print('=== scene', name)
    plt.figure(figsize=(9,6))
    for n in RES:
        g = load_gray(cfg['t'], n)
        c = crop_resize(g, cfg['box'], cfg['size'], n)
        centers, prof = rad_psd(c.astype(np.float32))
        # normalize by low band
        low = prof[(centers>0.03)&(centers<0.10)].mean()
        pn = prof/low
        plt.semilogy(centers, pn, label=n, color=colors[n], lw=1.4)
        def band(a,b):
            m=(centers>=a)&(centers<b)
            return prof[m].mean()
        hi = band(0.28,0.45); mid=band(0.12,0.22); lo=band(0.03,0.10)
        stats[(name,n)] = (hi/lo, hi/mid, lo)
        print(f'{n}: high/low={hi/lo:.5g} high/mid={hi/mid:.5g} low={lo:.3g}')
        hp = highpass_vis(c)
        cv2.imwrite(str(DIR/f'hp_{name}_{n}.png'), hp)
    plt.axvline(0.25, color='k', ls='--', lw=1, alpha=.6)
    plt.text(0.252, plt.ylim()[1]*0.5, '1080p Nyquist', rotation=90, fontsize=8, va='center')
    plt.xlabel('spatial frequency, cycles/pixel at 4K')
    plt.ylabel('normalized power (low band = 1)')
    plt.title(f'Radial luma power spectrum — {name}')
    plt.grid(alpha=.25); plt.legend(); plt.tight_layout()
    plt.savefig(str(DIR/f'spectrum_{name}.png'), dpi=140)
    plt.close()

# text scene
print('=== scene text_120')
plt.figure(figsize=(9,6))
for n in RES:
    g = load_gray(scenes_text['t'], n)
    c = crop_resize(g, scenes_text['box'], scenes_text['size'], n)
    centers, prof = rad_psd(c.astype(np.float32))
    low = prof[(centers>0.03)&(centers<0.10)].mean()
    pn = prof/low
    plt.semilogy(centers, pn, label=n, color=colors[n], lw=1.4)
    def band(a,b):
        m=(centers>=a)&(centers<b); return prof[m].mean()
    hi=band(0.28,0.45); mid=band(0.12,0.22); lo=band(0.03,0.10)
    stats[('text_120',n)] = (hi/lo, hi/mid, lo)
    print(f'{n}: high/low={hi/lo:.5g} high/mid={hi/mid:.5g} low={lo:.3g}')
    cv2.imwrite(str(DIR/f'hp_text_120_{n}.png'), highpass_vis(c))
plt.axvline(0.25, color='k', ls='--', lw=1, alpha=.6)
plt.xlabel('spatial frequency, cycles/pixel at 4K')
plt.ylabel('normalized power (low band = 1)')
plt.title('Radial luma power spectrum — text_120')
plt.grid(alpha=.25); plt.legend(); plt.tight_layout()
plt.savefig(str(DIR/'spectrum_text_120.png'), dpi=140)
plt.close()
