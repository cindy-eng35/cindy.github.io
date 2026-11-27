# BlueTrace V9 — Updated Task 1 + Member E original figures

## Included in this revision
- Updated Task 1 tables 1–3, the exact provided English technical interpretation, and 300-second sampling-gap findings.
- Original Task 1 notebook and **three unchanged screenshots** preserved.
- **`data/cleaned_server_usage.csv`: 187,963 rows retained**; one incomplete row is kept with its missing values; 187,962 valid CPU–memory paired observations.
- Member E **original `fig6.png` and `fig7.png` copied byte-for-byte** to `assets/results/fig06_imbalance_heatmap.png` and `fig07_utilization_categories.png`. The original `Analysis.ipynb` is `analysis/04_resource_imbalance.ipynb`.
- Member D uploaded README only: `analysis/03_memory_README.md`. It describes full statistics and an Excel workbook, but the Excel file and original charts were not uploaded; no substitute figures are fabricated.
- The seven responsive mist-blue website pages, mobile hamburger and offline CSS fallback remain intact. The footer version is v9.

## Reproduce Task 1 checks
```bash
pip install -r requirements.txt
python analysis/prepare_server_usage.py --input cleaned_server_usage.csv --output data/cleaned_server_usage.csv
```
The validator retains all rows. Input and output paths must be different. The provided `data/cleaned_server_usage.csv` is already a copy of the team's uploaded normalized data.

## Charts and methods
- E Figure 6 groups per-machine mean CPU by `timestamp // 3600`; the heatmap's vertical axis is a sorted row index, not machine ID. The original figure is unmodified.
- E Figure 7 groups CPU into **Low <20%; Mid 20–<40%; High ≥40%** and uses machines with data per hour as denominator. At hour 22, only part of the hour is observed. These are not official thresholds.
- D README uses a **different** <30% and ≥70% definition for extreme CPU–Memory mismatch. Its 187,962 paired observations and the correlation numbers refer to the supplied Member D documentation; review with D when the workbook arrives.
- The supplied Member E notebook expects its author's local `MemberA_Handover_Package/data/processed/cleaned_server_usage.csv` path. Update this path in your own working copy to run from this site repository.

## Outstanding materials for final submission
- Team C: CPU distribution / time series / selected machines (Figures 1–3) and interpretation.
- Team D: original memory histogram and CPU–Memory scatter (Figures 4–5), workbook or script package to reproduce them. Only README currently included.
- Team E: final review of Figure 6–7 assumptions, category thresholds, reported time labels and OS-level limitations; add machine-level comparison or transitions if required by your group's final analysis design.
- Final overall discussion and conclusion, reproducibility instructions checked end-to-end, contributor names/statement, 8–10 minute presentation.

## Publish
Unzip the archive and upload the entire *contents* to the GitHub Pages repository root. Do not upload only the ZIP. Maintain the `assets/`, `analysis/` and `data/` folders with `index.html` in the root. The 187,963-row CSV is approximately 17MB; hosting it is optional if a reproducible download link and preprocessing instructions are provided.

**Important:** `analysis/analyze.py` now defaults to `assets/draft_results/`, not `assets/results/`. This protects Member E’s submitted Figure 6 and Figure 7 from being overwritten by a generic sample-based analysis. The draft script is not a replacement for teammates’ figures.
