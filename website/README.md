# Project 12 website

`index.html` is a single self-contained page (no external scripts or fonts) summarizing the project:
doubling leaderboard, the 12 categories, model test results and download links.

## Update it
```
python website/build_site.py data/model/model_results_final.json model/ml_results.json
```
Re-run after every project update (standing rule: local GitHub folder -> GitHub -> website).

## Publish it
- **GitHub Pages:** the workflow `.github/workflows/pages.yml` deploys this folder on every push to `main`
  that changes `website/`. One-time setup: repo Settings -> Pages -> Source: **GitHub Actions**.
  The site will then be at https://hamidf2024.github.io/p12-best-stocks-investment/
- **Any other host:** upload `index.html` as is.
