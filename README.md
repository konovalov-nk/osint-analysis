# OSINT Analysis — case files

Live site: **https://konovalov-nk.github.io/osint-analysis/**

Pixel-level audits of synthetic media, platform metadata and persona infrastructure. Every case is reproducible from public files.

## Cases

### 001 — [House of El: The 4K Is a Lie](house-of-el/)

A 4K YouTube video that is actually a 1080p upscale — proven by spectral analysis, a 4K→1080p→4K round-trip, chroma comparison and native 4K calibration. The persona behind it is real: **Elena Markoska**, PhD in Engineering Science (University of Southern Denmark, 2019), Senior Data Scientist at the Bank of England. The synthetic part is the production: pseudonym, AI-enhanced face, AI clones, AI b-roll and a 1080p→4K upscale. The “am I AI?” panic is a top-of-funnel product for the book/course.

- **Read the case:** [house-of-el/](house-of-el/)
- **Key numbers:** 4K→1080p→4K face PSNR 52.6–54.3 dB; native 4K refs 26.6–33.8 dB; 84% of sampled frames >45 dB; 4K file 5.2× larger for no additional picture.
- **Correction:** “There is no real person behind the character” is false. “The character is a synthetic brand” is true. “The 4K is real” is false. “The AI panic is organic” is false.

## Method

Each case is built from public files and public records:

1. **Spectral fingerprint** — radial FFT of the luma plane. Native 4K keeps declining past 0.25 cycles/px; an upscale hits a wall and becomes a noise floor.
2. **1080p round-trip** — downscale the 4K frame to 1080p and back. If it reconstructs at 50+ dB, the 4K had no information above 1080p.
3. **Native calibration** — encode native 4K references at the same bitrate/codec and run the identical test.
4. **Chroma and high-pass** — 4:2:0 chroma planes and amplified detail residuals.
5. **Archive & records** — Web Archive snapshots, public thesis/working-paper records, public professional profiles.

## Structure

```
/
├── index.html                  # case index
├── house-of-el/
│   ├── index.html              # the report
│   ├── assets/                 # figures, spectra, high-pass, archived thumbnails
│   ├── refs/                   # full-resolution native 4K reference frames
│   ├── README.md               # report summary (English)
│   ├── README.ru.md            # report summary (Russian)
│   ├── spectral.py             # radial FFT / high-pass
│   ├── roundtrip.py            # 4K→1080/1440/720→4K PSNR/SSIM
│   ├── timeseries.py           # 68-frame sample
│   ├── timeseries.csv          # raw per-frame metrics
│   └── dl.sh                   # exact yt-dlp download ladder
└── .nojekyll
```

## Privacy & fair use

This is a journalistic/technical analysis of public material. It names a public professional whose PhD thesis, Bank of England working papers and a 2019 local-news profile are public records. It does **not** publish private contact details, addresses, family information or private social accounts. The LinkedIn profile is referenced as a matching professional record; the direct URL is not linked in the public report.

Third-party images — YouTube thumbnails, archived channel art and Unsplash references — are used for criticism, commentary and analysis. Rights remain with their owners. If you are the subject and want a correction or removal, open an issue.

## Reproduce

The report includes the exact commands and scripts. The frame sequences (`frames*`, `seq*`) are generated from the public YouTube files and are not checked in. Set `ANALYSIS_DATA_DIR` to the folder containing them when running the scripts.

## Credits

Analysis, writing and charts: Nikolay Konovalov. Built with `yt-dlp`, `ffmpeg`, Python, NumPy, OpenCV, scikit-image and matplotlib.
