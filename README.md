# Marginalia
### Good search leaves a paper trail.

An interactive, local-first information retrieval lab. Search a collection of original field notes, compare BM25 with TF-IDF, and inspect the exact term-level evidence behind every result. A quiet editorial interface makes the algorithm tangible instead of hiding it behind a search box.

## Run the demo

Requires Node.js 24 and npm. No API keys, backend, Redis, database, or accounts are needed.

```sh
cd frontend
npm ci
npm run dev
```

Open the Vite URL shown in the terminal. `npm run build` produces a static `frontend/dist` deployment; `npm run preview` serves it. For a repository GitHub Pages deployment, build with `GITHUB_PAGES=true npm run build` (base path `/search-engine/`). The workflow verifies every push/PR. Repository-specific deployment is disabled unless the `ENABLE_PAGES` repository variable is explicitly set to `true` and Pages is already configured for GitHub Actions; it then deploys **only main**.

The demo is hosted as the `search-engine/` subfolder of the existing portfolio site, rather than enabling a second Pages site. To refresh that copy, run `GITHUB_PAGES=true npm run build` in `frontend`, then copy the contents of `frontend/dist/` into the portfolio repository’s `search-engine/` folder and publish through its existing Pages process. Keep `/search-engine/` as the base path. Do not overwrite unrelated portfolio files.

## Try it

- Search **document length**, then switch BM25 ↔ TF-IDF. Compare ordering, not raw score magnitudes.
- Select a result to inspect term frequency, document frequency, IDF, and each contribution to the exact total.
- Adjust BM25 saturation (`k₁`) and length correction (`b`) live.
- Search **document neverindexedword** with AND to see why a missing term must yield no matches.
- Browse the reading room, download the sample corpus, or replace it with your own JSON collection.

Imports are validated atomically: 1–500 records, a 2 MB file limit, nonempty `title` and `text`, optional unique string `id` and `category`. Titles are limited to 300 characters and document bodies to 100,000. Imported content stays in memory in this browser tab and is cleared on refresh. No document data is sent anywhere. The UI uses optional Google Fonts with system-font fallbacks; search itself works offline after the assets load.

```json
[
  { "id": "note-1", "title": "A useful observation", "category": "Notes", "text": "The full text to search." }
]
```

## Retrieval semantics

`frontend/src/lib/retrieval.ts` is a small, dependency-free TypeScript retrieval engine. Title and body tokens have equal weight. Unicode letters and numbers are lowercased, punctuation splits words, and a fixed set of English stopwords is removed. There is no stemming, fuzzy matching, semantic retrieval, or query-term boosting. Repeated query terms are deduplicated.

- **BM25:** `Σ ln(1 + (N − df + .5)/(df + .5)) × tf(k₁+1)/(tf + k₁(1−b+b×dl/avgdl))`
- **TF-IDF:** `Σ (1+ln(tf)) × (ln((N+1)/(df+1))+1)` for present terms. This is additive log-TF weighting, not cosine similarity.
- **DF:** number of distinct documents containing a term, never token occurrences.
- **AND / OR:** all unique query terms / any unique query term. Unknown terms correctly prevent AND matches.
- **Ties:** document ID order. Subject filtering is applied after corpus-wide scoring.

Collection size, vocabulary, lengths, matched terms, alternate ranks, and scores are calculated from actual data. The 12 original teaching documents are intentionally small. This is a retrieval demonstration, **not a benchmark**, and scores are not confidence probabilities. Search rebuilds the in-memory index per calculation, appropriate for this bounded demo, not large-scale production retrieval.

## Verification

```sh
cd frontend
npm test                  # Node's built-in runner: deterministic retrieval regressions
npm run build             # Vue/TypeScript check + Vite production build
npx playwright install chromium
npm run test:e2e           # Desktop/mobile flows and screenshots
```

Dependency hygiene: unused Tailwind/Vue-devtools packages were removed, runtime/build dependencies were refreshed within their existing major versions, and ESLint uses explicit Vue/TypeScript parsers instead of a glob-heavy convenience preset. `npm audit` reported zero known advisories on 2026-10-15; CI rejects high/critical advisories. This is a point-in-time check, not a security guarantee.

The Playwright suite covers model switching, explanations, AND unknown terms, empty/repeated searches, import validation, restore, overflow, and runtime exceptions. CI uploads HTML reports, failure traces, and screenshots as the `browser-qa` artifact.

## Original Python backend

The original FastAPI / SQLAlchemy / Celery / Redis crawler remains under `backend/`, along with the Docker files. It is **separate from the self-contained browser demo**. Its index service has regressions for two corrected bugs: document frequency was counting occurrences, and AND queries silently ignored unknown terms. Ties are now deterministic. The tokenizer no longer downloads NLTK data or writes directories at import time; it uses deterministic offline tokenization.

Run isolated database/tokenizer tests without PostgreSQL or Redis:

```sh
python -m venv .venv
. .venv/bin/activate
pip install sqlalchemy pydantic-settings pytest
cd backend
PYTHONPATH=. pytest tests -q
```

The historical live-web crawler integration test is deliberately opt-in (`RUN_CRAWLER_INTEGRATION=1`) and needs the full backend dependencies, reachable target, and configured database. The crawler stack and Docker deployment have not been end-to-end validated by these unit tests. The backend retains its original raw-TF/unsmoothed-IDF formula; it is not the demo's ranking API. No production-readiness claim is made.

## Structure

- `frontend/src/App.vue` — accessible search, inspection, reading, and import UI
- `frontend/src/lib/retrieval.ts` — tokenization, indexing, models, import schema
- `frontend/src/lib/corpus.ts` — original bundled collection
- `frontend/tests` — deterministic unit tests
- `frontend/e2e` — desktop/mobile browser coverage
- `backend/app/services/index_service.py` — original persisted index service
- `.github/workflows/pages.yml` — verification, screenshot artifacts, main-only Pages deployment
