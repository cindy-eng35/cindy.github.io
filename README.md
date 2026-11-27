# BlueTrace V13 — instructor-format review edition

## Instructor alignment
Follows **seven required PDF report areas**, organized into **ten instructor-example navigation topics** across seven responsive HTML pages:
1 Overview; 2 Research questions; 3 Dataset; 4 Methodology; 5 Results & figures; 6 Discussion; 7 What we learned; 8 Conclusion; 9 Reproduce; 10 References.

## Key fixes after V12 review
- Removed collapsed `<details>` so **all seven numbered figures display directly**, without any clicks.
- Removed stale text claiming CPU/Memory handoffs were missing.
- Added **Table 4** showing actual 300-second same-machine utilization-category transitions, with reproducible script and CSV. This addresses Topic 2 Task 4 transitions explicitly.
- Reordered What we learned before Conclusion; Reproduce before References.
- Added direct repo URL, documented reproduction caveats for team C/E source paths.
- All images are original PNG files or source-derived images; embedded in HTML for mobile reliability.

## Dataset and units
- Alibaba Cluster Trace 2017; 187,963 records, 1,310 machines, 11.92 hours.
- One CPU missing; all records retained. Valid CPU-memory pairs: 187,962.
- Task 4 thresholds: Low <20%, Mid 20–<40%, High ≥40%. This differs from Task 3 mismatch cutoffs.
- 185,982 same-machine 300-second adjacent valid pairs; 34,165 (18.37%) changed categories, 151,817 stable.
- E's figure 7 uses hourly-mean values; Table 4 uses individual consecutive observations. Do not confuse their units.

## Deployment
Upload the **contents of this folder** to the existing GitHub repository root, including all root HTML pages, `assets/`, `analysis/`, `data/`, `requirements.txt`, `.nojekyll`. Do not upload the ZIP by itself.

## Quick reproduction
```bash
python -m pip install -r requirements.txt
python analysis/member_e/compute_transitions.py --input data/cleaned_server_usage.csv --output analysis/member_e/transition_counts_300s.csv
python analysis/member_d/scripts/analyze_memory.py --input data/cleaned_server_usage.csv --output analysis/member_d/analysis_data.json
```
For source C and source E, inspect the path adjustments in References/Reproduce on the website. A requires official raw files to reconstruct preprocessing.

## Final human review still needed
Verify the official dataset source/version, check analysis outputs on teammate systems, replace A–F roles with real member names, confirm accessible live URLs after deployment, and rehearse the 8–10 minute group talk. Do not claim every script was rerun unless the group actually reruns it.
