# File → Markdown (powered by MarkItDown)

A tiny, free web tool that converts PDFs, Word docs, PowerPoint, Excel, and more into clean Markdown, built on Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library.

- `index.html` — the upload page (static, no build step)
- `api/convert.py` — a Python serverless function that runs MarkItDown
- `requirements.txt` — Python dependencies for the function
- `vercel.json` — Vercel config

## Deploy to Vercel (free)

Vercel is used here (not Netlify) because it runs Python serverless functions natively — Netlify's free tier doesn't support this out of the box.

1. Create a free account at https://vercel.com (you can sign in with GitHub).
2. Push this folder to a new GitHub repo:
   ```
   cd markitdown-app
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
3. In Vercel: **Add New → Project**, import that GitHub repo, and click **Deploy**. No configuration needed — `vercel.json` and `requirements.txt` are picked up automatically.
4. Once deployed, you'll get a URL like `https://your-project.vercel.app`. That's it — share it with anyone.

Alternatively, deploy straight from your machine with the Vercel CLI:
```
npm i -g vercel
cd markitdown-app
vercel
```

## Notes & limits (free tier)

- Vercel's free (Hobby) plan gives generous usage for personal projects, but serverless functions have a **request body limit (~4.5MB)** and a max execution time — this project caps uploads around 4MB accordingly (see `MAX_BYTES` in `api/convert.py`).
- `requirements.txt` installs MarkItDown with `pdf`, `docx`, `pptx`, and `xlsx` extras only, to keep the deployment small and within Vercel's function size limits. If you want audio transcription, YouTube, or OCR support, you can add extras (e.g. `markitdown[all]`), but this may push you over Vercel's free-tier function size cap (250MB unzipped).
- Files are processed in memory/temp storage per-request and are not persisted anywhere.
- This is a public tool by default — anyone with the URL can use it. If you want to restrict it to yourself, the simplest options are Vercel's built-in password protection (Pro plan) or adding basic auth in `api/convert.py`.

## Local testing

```
npm i -g vercel
cd markitdown-app
vercel dev
```
Then open http://localhost:3000
