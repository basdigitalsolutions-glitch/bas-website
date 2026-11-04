# BAS Digital Solutions website

Live site: https://basdigitalsolutions.ca (GitHub Pages, custom domain in `CNAME`).

Plain static files, no build step. Whatever is on the `main` branch is what GitHub Pages serves, so **merging into `main` publishes**. Make changes on a separate branch and open a pull request to review them first.

- Pages: English and French pairs (`index.html` / `fr.html`, `salons.html` / `salons-fr.html`, `rfq.html` / `rfq-fr.html`, and so on).
- Styles: `agency.css`, `experience.css`, `industrial.css`, `assistant.css`. Script: `experience.js`.
- Videos, images and PDFs: `media/`.
- Extensionless URLs such as `/rfq` are served from `rfq.html` automatically by GitHub Pages.
- The salon pages load the chat widget from the salon-assistant service on Render. That service only allows this domain (see `allowed_origins` in `salons/lumiere.json` there).
- External services: Tally form `rDybZX`, Render salon assistant.

Imported on Nov 4, 2026 from the published ChatGPT Sites project `bas-content-studio` (version 18), byte-identical to what was live.
