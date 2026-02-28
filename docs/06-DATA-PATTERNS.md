# Data patterns

Rules for loading, transforming, caching, and passing data into charts and callbacks. Follow these so data flow stays predictable and efficient.

---

## 1. Data sources

| Source | How to access | When to use |
|--------|----------------|-------------|
| **API** | `requests.get()` or `httpx.get()`; parse JSON. Use env/config for base URL. | Live or near-live data; external service. |
| **File (CSV, Parquet, etc.)** | `pd.read_csv()`, `pd.read_parquet()` from path (config or known location). | Static or batch data; local/served files. |
| **Database** | SQL driver or ORM (e.g. `sqlalchemy`, `psycopg2`); use connection from config. | Structured data; queries with filters. |

Document each source and its config (URL, path, credentials) in this doc or in [11-DEPLOYMENT.md](11-DEPLOYMENT.md). Do not hardcode URLs or secrets.

---

## 2. Loading

| Rule | Action |
|------|--------|
| **Where** | Load in callbacks when data depends on user input (e.g. filters, date range). Load at module level only when data is static and small (e.g. reference list). |
| **Sync** | Use `requests` or `httpx` (sync) in callbacks unless the app uses async; keep callbacks simple. For long-running fetches, use caching or background jobs. |
| **Error handling** | Wrap fetch in try/except; on failure return a user-visible message (e.g. error div) and log the exception. Use timeouts (e.g. `requests.get(..., timeout=30)`). Do not let uncaught errors break the callback. |

---

## 3. Transformation

| Rule | Action |
|------|--------|
| **Where** | Transform in the callback that needs the data, or in a shared function in `data/` (e.g. `data/loaders.py`). Prefer one place per source so logic is reusable. |
| **Steps** | Use pandas: filter (e.g. `df[df.region == region]`), aggregate (`.groupby().agg()`), pivot if needed. Keep transforms in a clear order: load → filter → aggregate → plot. |
| **Consistency** | Same source and filters should use the same transform logic. If a transform is used in more than one callback, put it in `data/` and call it from both. Document non-obvious transforms in this doc. |

---

## 4. Caching

| Rule | Action |
|------|--------|
| **Mechanism** | Use in-memory caching for single-process apps (e.g. `functools.lru_cache` or a simple `@cache` decorator with a TTL). For multi-worker, use a shared store (e.g. Redis) or document that cache is per process. |
| **Cache key** | Key by inputs that affect the result: e.g. `(source_id, param1, param2)` or hash of query params. Do not key only by source if params change the result. |
| **Invalidation** | Set a TTL (e.g. 5–60 minutes) or invalidate on known events. Document TTL and invalidation in the cache helper or this doc. |
| **Example** | `@lru_cache(maxsize=128)` on a loader that takes hashable args; or `cache.get(key)` / `cache.set(key, value, ttl=300)`. |

Do not cache raw responses that contain secrets. Do not cache indefinitely without a TTL unless data is static.

---

## 5. Data refresh configuration

| Rule | Action |
|------|--------|
| **When to refetch** | Choose one or combine: (1) on load only, (2) on a timer (auto-refresh), (3) only when the user clicks refresh, (4) on navigation. Document the choice per view or dataset. |
| **Auto-refresh** | Use `dcc.Interval(id="refresh-interval", interval=interval_ms, n_intervals=0)` and a callback with `Input("refresh-interval", "n_intervals")` to re-fetch and update. Set interval via config or env (e.g. `DATA_REFRESH_INTERVAL_SEC`); use 60s or more to avoid overloading the source. |
| **TTL vs refresh** | Short TTL = “fresh enough” without a button. Manual-only refresh = no interval; user clicks to reload. For critical freshness, prefer a refresh button or short TTL over long intervals. |
| **Where to configure** | Keep refresh interval (and “manual only” vs “interval”) in app config or env. Do not hardcode intervals. Document in [11-DEPLOYMENT.md](11-DEPLOYMENT.md) or this doc. |

### User-triggered refresh (button)

| Rule | Action |
|------|--------|
| **Pattern** | Add a button (e.g. `dbc.Button("Refresh", id="refresh-btn")`). Callback: `Input("refresh-btn", "n_clicks")` → re-fetch (and optionally invalidate cache for that key) → update `dcc.Store` and/or figure outputs. |
| **Loading state** | Wrap the content that updates (e.g. graph or container) in `dcc.Loading` so the user sees a spinner while the callback runs. |
| **Feedback** | Optionally show brief feedback: e.g. “Data updated” in a div or toast, or disable the button during load. Do not leave the user unsure whether the click did anything. |

---

## 6. Passing data to callbacks

| Rule | Action |
|------|--------|
| **dcc.Store** | Use Store for data that multiple callbacks need (e.g. filtered DataFrame as JSON) or to avoid re-fetching when the user changes another control. Recompute in the callback when data is small or fetch is cheap. |
| **Payload size** | Do not put huge JSON in Store (e.g. 100k+ rows). Prefer aggregated or sampled data, or re-fetch in the callback and return the figure only. Keep Store payloads under a few MB. |
| **Serialization** | Store and callback props are JSON-serializable only. Use ISO strings for dates (`df["date"].astype(str)` or `.dt.isoformat()`); no `datetime` or NumPy types in Store. |

---

## 7. Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| **Stale data** | Use a TTL on caches; or invalidate when the user explicitly refreshes. If data must be fresh, avoid caching or use a short TTL. Document refresh behavior. |
| **Memory** | Do not hold large DataFrames in global variables or in Store. Prefer load → transform → build figure → discard; cache only aggregated or small results. |
| **Concurrency** | With multiple workers, in-memory cache is per process; use Redis or similar for shared cache. Avoid file-based state that multiple processes write to. |

---

Load in callbacks when data depends on user input; transform in one place; cache with a clear key and TTL. Use refresh configuration (interval or manual button) and give loading/feedback for user-triggered refresh. Keep Store payloads small and JSON-serializable.
