# BlueTrace — Operating Systems (Topic 2)

A **seven-page, responsive technical report starter (v4, CSS fallback fix)** for the instructor's *CPU and Memory Resource Analysis in Real Computing Systems* topic. The source and publication structure follow the class project brief. This is a **Week 1 site framework**, not a completed data analysis.

## Open locally

Unzip the whole archive and open `index.html` in Chrome, Edge, or Safari. Each HTML file now **embeds a backup copy of the CSS and mobile navigation**. This fixes the unstyled-text issue when just one HTML page is opened or CSS loading fails. For all seven pages, analysis charts, and editable shared styling, **keep the whole unzipped folder together**.

- Desktop: permanent left navigation.
- Tablet and mobile (900px and below): **☰ hamburger menu** in the top bar, with overlay and close × button.
- The seven report sections are seven **separate pages** so you do not need to scroll through the entire report.

## Report pages

| Page | File | Purpose |
|---|---|---|
| Introduction | index.html | Topic motivation, research questions, roadmap |
| Dataset | dataset.html | Original source, schema, missingness and subset selection |
| Methodology | methodology.html | Tools, data cleaning, metrics, comparisons |
| Results | results.html | Seven chart slots, optional interactive CSV explorer |
| Discussion | discussion.html | Connection to OS concepts, uncertainty, limitations |
| Conclusion | conclusion.html | Final evidence-grounded findings (pending) |
| References & Code | references.html | Sources, reproducibility and contributions |

## Publish with GitHub Pages

1. Create a new public GitHub repository.
2. Upload **all extracted files** at the repository root (including `.nojekyll`, `assets`, and `analysis`).
3. Settings → Pages → Deploy from a branch → `main` → `/(root)` → Save.
4. Wait for the Pages publishing workflow to complete; open its public URL.
5. Test the same site on desktop and phone. Page navigation uses normal relative `.html` links so it works on project-name URLs too.

## Reproducible analysis

The project Python script remains in `analysis/analyze.py`. After Team A obtains the official 2017 `server_usage.csv` and agrees on subset selection, from repository root:

```bash
pip install -r requirements.txt
python analysis/analyze.py --input path/to/server_usage.csv
```

The script writes figures to `assets/results/` and creates `assets/results/results.js`. Do not place example/mock data into final deliverables as if measured. The results page automatically displays actual figures when the generated metadata file is present.

### Optional interactive preview

On `results.html`, import a **small local subset** of `server_usage.csv` (up to 6 MB). The browser-only preview offers CPU/Memory switching and machine selection. The file is not uploaded, and the preview is **not** a substitute for validated final analysis.

## What teammates should supply

- **A**: downloadable and documented source/subset; preprocessing code and cleaned data.
- **B**: schema, sample records, completeness and data-quality report.
- **C**: CPU distributions, time-series, machine comparisons and interpretations.
- **D**: Memory distributions, CPU–memory relationship and interpretations.
- **E**: Resource utilization categories, heatmap, OS allocation/scheduling discussion and limitations.
- **F**: website design, multi-page integration, publishing and report presentation.

## Original project requirements

The teacher requires at least two testable research questions, three meaningful analyses/comparisons, at least five informative charts/tables with captions, evidence-based OS explanation, reproducibility steps, a public website and repository, an 8–10 minute group presentation, and individual contributions. **Do not treat page placeholders as finished work.**

## v4 repair (November 2026)

- The reported screenshot showed the browser's default serif fonts and blue underlined links: the relative `assets/style.css` file was not loaded.
- All seven HTML pages now contain **embedded fallback CSS** and a **built-in mobile hamburger menu script** so they remain styled and usable if an individual HTML file is moved out of its folder.
- Shared `assets/style.css` is still included and is loaded after the fallback, so edits to the shared stylesheet take priority for deployed sites.
- The analysis script and chart files still require the `assets` directory and should be uploaded together.
- **Best practice:** unzip the entire ZIP, then open the `index.html` inside the extracted folder. Do not open the HTML preview directly inside the compressed ZIP.

## V5 · Mist-blue color refresh

- Updated from bright sky blue to a low-saturation mist-blue and blue-gray palette.
- Kept seven independent pages, responsive layout, desktop sidebar, mobile hamburger menu, data import, and analysis/reproducibility files.
- Each HTML page includes fallback CSS and navigation scripts; for complete navigation and figures, keep the extracted folder together.
- To update GitHub Pages, replace the files in the repository while retaining the original folder hierarchy.



## V6 visual update
Replaced all green-rendering ✳ symbols with monochrome outline sparkles (✧) across all seven pages. No changes to page structure, scripts, or navigation.


### V7 · iOS / mobile icon fix

The decorative sparkle symbols were replaced by inline, monochrome SVGs across
all seven HTML pages. On older iPhones, the former Unicode symbol could be
rendered as a colored emoji. Vector icons now inherit the site’s blue color.
External CSS/JS and internal page links include `?v=7` for cache invalidation.
A subtle `v7` appears in the footer so the deployed revision is easy to verify.

**To update GitHub Pages**: extract the ZIP, upload and commit the full contents
(including all seven HTML files and `assets/`) to the publishing branch.
Check the published site at `https://YOUR-SITE/?v=7`; if the footer doesn't say
`v7`, the updated files are not yet being displayed (or the deployment is pending).
