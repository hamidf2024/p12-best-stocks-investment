# Changelog

## 2026-10-29
- Automatic website publishing: `website/project-12.html` is now the source of the live page; the new workflow
  `.github/workflows/sync-website.yml` copies it to hamidf2024/hamidf2024.github.io on every push (needs the one-time
  `SITE_TOKEN` secret). `pages.yml` changed to manual-only.
- Live page: added a Downloads section and menu link (report, charter, results summary, repository); Sources now links
  the public project repository.
- Stand-alone summary page (website/index.html): added a section menu under the title, with smooth
  scrolling, and changed the header date to "Last updated". First test of the standing workflow rule.
- Added the standing workflow rule (local folder -> GitHub -> website) to the charter and `WORKFLOW_RULES.md`;
  added the `website/` folder.
- v2.1 report: 117 holdings in 12 categories scored by a trained ML model blended with the rules model.
