# Question Bank Generator (browser-only)

Single HTML file. No backend. Hosted free on GitHub Pages.

- **PDF text** → PDF.js (CDN)
- **Image OCR** → Tesseract.js (CDN)
- **Generation** → OpenRouter, called directly from the browser

## Setup (one-time)

1. Open `index.html` in a text editor.
2. Find `const API_KEYS = { ... }` near the top of the JS block.
3. Replace the three placeholder keys with your OpenRouter keys for Biology, Chemistry, Physics.

```js
const API_KEYS = {
  Biology:   'sk-or-v1-...',
  Chemistry: 'sk-or-v1-...',
  Physics:   'sk-or-v1-...',
};
```

4. Commit and push:

```bash
git add index.html
git commit -m "Browser-only build with OpenRouter keys"
git push origin main
```

## Publish on GitHub Pages

1. https://github.com/farooq-coschool/question-bank → **Settings** → **Pages**.
2. **Build and deployment** → **Source**: **Deploy from a branch**.
3. **Branch**: `main`, folder: `/ (root)` → **Save**.
4. Wait ~30 s. Your site is live at:
   ```
   https://farooq-coschool.github.io/question-bank/
   ```
5. Share that URL with users.

Every `git push` to `main` redeploys automatically.

## Caveats

- **Keys are visible in the page source.** Anyone using the site can read them and spend your OpenRouter credit. Mitigations:
  - Use throwaway keys with low monthly limits per subject on OpenRouter.
  - Rotate the keys whenever you see abuse.
- **OCR runs in the browser** (Tesseract.js) — large/scanned PDFs may take a minute. First image-OCR call downloads ~2 MB of model data (cached after).
- **Free OpenRouter models** still have low rate limits (~10–20 req/min, low daily caps). Bulk generation may hit 429s.

## Updating

```bash
git add . && git commit -m "..." && git push origin main
```
GitHub Pages rebuilds in ~30 s.
