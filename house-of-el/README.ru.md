# «4K — это ложь»: отчёт по House of El

Открывать **`index.html`** в браузере. Картинки лежат в **`assets/`**, полноразмерные 4K-референсы — в **`refs/`**.

## Коротко

- **4K — апскейл.** VP9 2160p — это 4K-контейнер примерно с 1080p информации. Говорящая голова реально **720–1080p**; b-roll максимум **~1440p**; ни одна сцена не выглядит как настоящий 4K.
- **Лицо — главное доказательство.** Round-trip 4K → 1080p → 4K: **52.6–54.3 dB**, SSIM **0.986–0.997**. Нативные 4K-референсы, сжатые тем же 6 Mbps: **26.6–33.8 dB**. Спектр 4K-лица выше **0.25 cycles/px** — плоский шумовой пол.
- **720p ≈ 1080p для лица.** Апскейл 720p → 4K даёт **42.01 dB**, 1080p → 4K — **42.07 dB**. Разница 0.06 dB. 4K не добавляет к лицу ничего сверх 720p.
- **84% из 68 кадров** выше 45 dB; **63%** выше 50 dB. Файл 4K в **5.2×** больше, потому что YouTube даёт 4K **5.8×** битрейта на 4× пикселей — не потому, что там больше картинки.
- **Человек реальный.** «El» — это **Elena Markoska**: PhD in Engineering Science, University of Southern Denmark (2016–2019); Senior Data Scientist в Bank of England; соавтор BoE Staff Working Papers 924 и 943. Канал «Walk the walk» (2020–21) — её собственный старый канал. Человек не фейк. Синтетическая — **постановка**.
- **Апрель 2026 — не доказательство.** `lmt` — это время последнего перекодирования на YouTube, а не дата загрузки. YouTube перекодирует старые видео. 4K-апскейл доказывается пикселями, а не метаданными.

## Что поправить в треде

Если уже написал «I don't believe this character is real», раздели утверждения:

| Утверждение | Вердикт |
|---|---|
| «За персонажем нет реального человека» | **Ложь.** Елена Маркоска реальна: PhD, Bank of England. |
| «Персонаж — синтетический бренд» | **Правда.** Псевдоним, AI-усиленное лицо, AI-клоны, AI-b-roll, 1080p→4K апскейл. |
| «4K настоящий» | **Ложь.** Это 1080p-апскейл. |
| «AI-паника органическая» | **Ложь.** Видео «am I AI?» — верх воронки книги/курса. |

Сильная версия истории: **реальная PhD/data scientist перезапустила свой старый канал как безликий AI/geopolitics-бизнес, использует AI-клонов и 1080p→4K апскейл и продаёт курс о том, как распознавать AI, пока интернет спорит, не AI ли она сама.**

## Цифры

| Метрика | Значение |
|---|---|
| 720p video bitrate | 0.677 Mbps |
| 1080p video bitrate | 1.061 Mbps |
| 1440p video bitrate | 3.214 Mbps |
| 2160p VP9 video bitrate | 6.123 Mbps |
| 2160p AV1 video bitrate | 4.402 Mbps |
| 4K / 1080p file ratio | 5.21× |
| 4K / 1080p video bitrate ratio | 5.77× |
| 4K→1080→4K face PSNR | 52.6–54.3 dB |
| Native 4K city ref | 26.6 dB |
| Native 4K portrait ref | 33.8 dB |
| Face high/low above 0.25 cyc/px | 4.8e−5 |
| Native ref high/low | 3.97e−2 |
| Frames > 45 dB | 84% (57/68) |
| Frames > 50 dB | 63% (43/68) |

## Файлы

- `index.html` — отчёт.
- `assets/` — графики, спектры, high-pass, архивные превью, чарты.
- `refs/` — полноразмерные нативные 4K-референсы.
- `spectral.py` — радиальный FFT, high-pass, спектры.
- `roundtrip.py` — 4K→1080/1440/720→4K и PSNR/SSIM.
- `timeseries.py` / `timeseries.csv` — 68 кадров и сырые метрики.
- `exa_search.py` / `exa_linkedin.py` — точечный поиск по персонажу.
- `dl.sh` — точная лестница `yt-dlp`.

Последовательности кадров (`frames*`, `seq*`) генерируются командами из отчёта и не включены. Для запуска скриптов задай `ANALYSIS_DATA_DIR`.

## Источники

- Видео: https://www.youtube.com/watch?v=rDKzAml5nn8
- Основной канал: https://www.youtube.com/@HouseofEl
- AI-канал: https://www.youtube.com/@houseofel-ai
- «You're Right — I'm AI generated (Here's The Proof)»: https://www.youtube.com/watch?v=K3SD34vHPe4
- Сайт: https://houseofel.net
- Книга: https://houseofell.gumroad.com/l/isdum
- PhD-диссертация SDU: https://portal.findresearcher.sdu.dk/en/publications/a-framework-for-automated-real-time-performance-evaluation-of-sma/ · DOI 10.21996/5hay-tm27
- BoE Staff Working Paper 924: https://www.bankofengland.co.uk/working-paper/2021/impacts-of-the-covid-19-crisis-evidence-from-2-million-uk-smes
- OTown (5 Nov 2019), архив: https://web.archive.org/web/20191113021521/https://otown.dk/som-5-arig-ville-elena-have-en-ph-d-grad-nu-vil-hun-redde-verden/
- Wayback, «Walk the walk» 2021: https://web.archive.org/web/20210117055850/https://www.youtube.com/c/walkthewalk007
- LinkedIn (login-walled; direct profile not linked here) — the public education/experience record matches the SDU and Bank of England sources above.

## Оговорки

- Одно видео. Вывод про 4K относится к `rDKzAml5nn8`.
- AI-контент мягкий. Нативный 4K-рендер гладкого аватара тоже мог бы хорошо проходить round-trip; но плоский шумовой пол выше 0.25 cyc/px и равенство 720≈1080 делают версию «мягкий нативный 4K» маловероятной.
- Нативный референс — фото, не видео. Он калибрует кодек/битрейт, а не контент. Crowd b-roll — единственная неоднозначная сцена.
- PSNR зависит от контента. Приведены консервативные цифры без subpixel-shift; выравнивание может добавить 1–2 dB.
- Форматы YouTube и `lmt` — на 26 октября 2026.
