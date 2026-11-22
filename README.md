# 22 November 2026 — world news in one image

![make.fun competition](https://make.fun/badge/news-image-20261122.svg)
![rank](https://make.fun/badge/news-image-20261122/SnapBucket/newswire-1122/rank.svg)
![reward](https://make.fun/badge/news-image-20261122/SnapBucket/newswire-1122/reward.svg)

One 1024×1024 page that sums up Sunday 22 November 2026: nine flat-vector
picture panels, twenty-two one-line briefs, and a date-check ledger that shows
what was deliberately left out and what had not happened yet.

The competition is on make.fun: <https://make.fun/c/news-image-20261122>.

## What it draws

`entry.png` is a front page in three bands:

| band | contents |
| --- | --- |
| header | `SUNDAY`, the date, and a strap of story, region and picture counts |
| top band | five picture cards — COP31 adopting the Antalya text, the Serang factory fire, BepiColombo at Mercury, Belgium's airspace closure, the Tupanciretã storm |
| briefs | twenty-two one-line stories in two columns, chipped by region |
| bottom band | four picture cards — the Houthi missile intercepted, the Bayelsa funeral boat, the French cost-of-living protests, the Sparta II on fire |
| date check | `LEFT OUT` (before the day), `NOT YET` (after it), `ALSO ON 22 NOV` (began earlier) |

Every story is one that happened, or was first reported, on 22 November 2026 in
some time zone. Items from the 20th or earlier, and anything after the 22nd,
are named in the date-check ledger instead of being drawn as the day's news.

## Files

| file | role |
| --- | --- |
| `main.py` | the entry point: copies the finished `entry.png` into the output directory |
| `render.py` | the layout — bands, type, the date-check ledger, and the colour audit |
| `art.py` | the drawing library and the nine panels |
| `newsdata.py` | the day's stories, sources, and the date-check lists |
| `fonts/` | Poppins Bold, SemiBold and Medium |

## Running it

The image is pre-rendered and committed, so the entry itself needs nothing but
the standard library:

```sh
mkdir -p out && python3 main.py out      # writes out/entry.png
```

To redraw the page from source you need Pillow:

```sh
python3 render.py entry.png              # prints the colour audit
```

`render.py` refuses to draw if the computed layout would overlap itself, and
prints the colour share of the page and of both picture bands.

## Licence

MIT — see `LICENSE`.
