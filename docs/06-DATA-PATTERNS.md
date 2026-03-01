# Data patterns

Rules for loading, transforming, caching, and passing data into charts and callbacks. Follow these so data flow stays predictable and efficient.

---

## 1. Data sources

| Source | How to access | When to use |
|--------|----------------|-------------|
| **API** | `requests.get()` or `httpx.get()`; parse JSON. Use env/config for base URL. | Live or near-live data; external service. |
| **File (CSV, Parquet, etc.)** | `pd.read_csv()`, `pd.read_parquet()` from path (config or known location). | Static or batch data; local/served files. |
| **Database** | SQL driver or ORM (e.g. `sqlalchemy`, `psycopg2`); use connection from config. | Structured data; queries with filters. |
| **Google Sheets** | `gspread` with service account auth; open by sheet ID/URL, read range or `get_all_records()` → DataFrame. | Tabular data in a sheet; lightweight or shared inputs. See §1.1. |

Document each source and its config (URL, path, credentials) in this doc or in [11-DEPLOYMENT.md](11-DEPLOYMENT.md). Do not hardcode URLs or secrets.

### 1.1 Connecting to data sources

Use a single place for connection config (e.g. `utils/config.py` or env vars); create connections per request or use a connection pool where the driver supports it. Never hardcode credentials.

| Source | Library / driver | Connection pattern | Config (env) | Notes |
|--------|------------------|--------------------|-------------|--------|
| **MySQL** | `mysql-connector-python`, `pymysql`, or SQLAlchemy `mysql+pymysql://` | Connection string from env; use context manager or pool. | `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` | Prefer parameterized queries; set `connect_timeout`. |
| **PostgreSQL** | `psycopg2` or SQLAlchemy `postgresql://` | Same as above; connection string or separate host/port/user/password/dbname. | `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` (or `DATABASE_URL`) | Use server-side cursors for large result sets. |
| **ClickHouse** | `clickhouse-connect` or `clickhouse-driver` | Client from config; execute queries, return results as list/dict or pandas. | `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, `CLICKHOUSE_DATABASE` | Good for analytics; keep queries selective and use aggregations. |
| **Snowflake** | `snowflake-connector-python` or SQLAlchemy `snowflake://` | Connector with account, user, password, role, warehouse, database, schema from config. | `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA` | Use warehouse and schema; avoid huge unbounded SELECTs. |
| **Redis** | `redis` (pyredis) | `redis.Redis(host=..., port=..., password=..., decode_responses=True)` from config. | `REDIS_URL` or `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` | Use for caching (get/set with TTL) or as shared state; not as primary query store for dashboards. |
| **Elasticsearch** | `elasticsearch` (official client) | `Elasticsearch(hosts=[...], basic_auth=...)` from config. | `ES_HOST`, `ES_PORT`, `ES_USER`, `ES_PASSWORD` (or `ELASTICSEARCH_URL`) | Use for search/aggregations; map response to DataFrame for charts; set request timeouts. |
| **Google Sheets** | `gspread` + `google-auth` | Authenticate with service account JSON (path or env); `gc.open_by_key(sheet_id)` or `open_by_url()`; `worksheet.get_all_records()` → DataFrame. | `GOOGLE_SHEETS_CREDENTIALS_JSON` (or `GOOGLE_APPLICATION_CREDENTIALS` path), `GOOGLE_SHEET_ID` (or sheet URL in config) | Share the sheet with the service account email. Cache sheet data with TTL; avoid per-request reads for large sheets. |

**Rules for all sources:**

- **Config** — Read host, port, credentials, and DB name from environment or a config module. Document required env vars in this doc or [11-DEPLOYMENT.md](11-DEPLOYMENT.md).
- **Lifecycle** — Create the client/connection inside the callback or in a loader that’s called per request; or use a pool (e.g. SQLAlchemy pool) and reuse. Close connections or use context managers; do not leave long-lived connections open in global scope without a pool.
- **Errors** — Wrap connect and query in try/except; log the error and return a user-visible message or `no_update`; use timeouts to avoid hanging.
- **Secrets** — Never commit credentials. Use env vars or a secrets manager; reference in deployment docs only by variable name.

### 1.2 Environment file and credential configuration

Use an environment file so the dashboard can load credentials and config securely without hardcoding. Follow these so the app works the same locally and in deployment while keeping secrets out of the repo.

| Rule | Action |
|------|--------|
| **File location** | Use `.env` at the project root (or `apps/<name>/.env` for an app in `apps/`). Optionally use `.env.local` for overrides; load it after `.env` if present. |
| **Load in app** | At app startup, call `load_dotenv()` from `python-dotenv` (e.g. in `app.py` or in `utils/config.py` before any connection is made). Use `load_dotenv(".env")` or `load_dotenv(Path(__file__).parent.parent / ".env")` so the path is explicit. |
| **Single config module** | Read all env vars in one place (e.g. `utils/config.py`): `os.getenv("VAR_NAME")` or `os.environ.get("VAR_NAME", "default")`. Export a small set of variables or a config object so the rest of the app does not call `os.getenv` everywhere. |
| **No secrets in code** | Never put passwords, API keys, or connection strings in source. Only variable names (e.g. `os.getenv("PGPASSWORD")`) may appear in code. |
| **.env in .gitignore** | Ensure `.env`, `.env.local`, and `.env.*.local` are in `.gitignore` so they are never committed. |
| **.env.example** | Commit a `.env.example` (or `.env.sample`) that lists every variable name with placeholder or empty values and short comments. No real secrets. New developers copy it to `.env` and fill in values. |

**Example `.env.example`:**  
The repo root contains a [`.env.example`](../.env.example) that lists env vars for **all** supported data sources (MySQL, PostgreSQL, ClickHouse, Snowflake, Redis, Elasticsearch, Google Sheets) plus app and API. Copy it to `.env` and set only the variables your dashboard uses.

**Example loading in code (`utils/config.py`):**

```python
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def get_db_url():
    return os.getenv("DATABASE_URL") or (
        f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}"
        f"@{os.getenv('PGHOST')}:{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE')}"
    )
```

For production and required vars, see [11-DEPLOYMENT.md](11-DEPLOYMENT.md) §2.1 and §2.2.

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
