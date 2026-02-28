# Deployment

Rules for running dashboards in development vs staging and production. Follow these so run commands, env, and production setup stay consistent.

---

## 1. Development

| Item | Value | Rule |
|------|--------|------|
| **Run** | `python app.py` or `dash run app:app` | Use the same command as in [README](../README.md) Quick start. For an app in `apps/<name>/`: `python apps/<name>/app.py`. |
| **Host/port** | `http://127.0.0.1:8050` (default Dash port) | Set `host` and `port` in `app.run_server()` if you need a different port. |
| **Debug** | `debug=True` in `app.run_server(debug=True)` | Enables hot reload and tracebacks. Use only in development. |
| **Env** | `.env` or `.env.local` for API keys and config | Do not commit `.env`. Load with `python-dotenv` or equivalent. Document required vars in this doc. |

### Docker-based local development

Run the app in Docker on your machine with the same stack as production, plus hot reload and local `.env`.

| Step | Command / value | Rule |
|------|------------------|------|
| **Build** | `docker build -t plotly-factory:dev .` | Use a dev Dockerfile or build arg (e.g. `--target dev`) that installs deps and sets the app as entrypoint. |
| **Run** | `docker run -p 8050:8050 --env-file .env -v $(pwd):/app plotly-factory:dev` | Map port 8050; load env from `.env`; mount repo so code changes are visible (hot reload if the app supports it). |
| **Hot reload** | Mount source: `-v $(pwd):/app` and run with `debug=True` inside the container (e.g. `dash run` or `python app.py` with reload). | Restart the container after adding new system deps; code-only changes can reload if the process watches the mount. |
| **Env** | `--env-file .env` or `-e VAR=value` | Same vars as §2 Required env vars; use `.env` for local secrets. Do not commit `.env`. |
| **Compose (optional)** | `docker-compose up` with a `docker-compose.yml` that builds the dev image, maps 8050, mounts `.:/app`, and uses `env_file: .env`. | Use when you have multiple services (e.g. app + DB) or want a one-command dev startup. |

**Example one-off run:**  
`docker run -p 8050:8050 --env-file .env -v $(pwd):/app plotly-factory:dev`  
Then open `http://127.0.0.1:8050`.

---

## 2. Staging / production

| Item | Value | Rule |
|------|--------|------|
| **Server** | Gunicorn with a WSGI entry point (e.g. `app:server` or `app:app`) | Run with multiple workers (e.g. `gunicorn -w 4 app:server`). Do not use `debug=True`. |
| **Process manager** | systemd, Docker, or Kubernetes | Use one; document the chosen option and how to start/stop the app. |
| **Reverse proxy** | nginx or similar | Proxy to the app; set timeouts and static file handling as needed. |
| **Env vars** | Set all required vars in the environment | No defaults for secrets. Document below. |

### Required env vars (document per app)

| Var | Purpose | Example |
|-----|--------|---------|
| **API_BASE_URL** | Backend or API base URL | `https://api.example.com` |
| **SECRET_KEY** | App secret (e.g. for sessions) | Random string; do not commit. |
| **DATA_REFRESH_INTERVAL_SEC** | Optional; auto-refresh interval in seconds | `60` or unset for manual only. See [06-DATA-PATTERNS.md](06-DATA-PATTERNS.md) §5. |

Add or remove rows per app. Do not hardcode these in code.

---

## 3. Docker (if used)

| Step | Command / value | Rule |
|------|------------------|------|
| **Build** | `docker build -t plotly-factory .` (or `-t plotly-factory:<app-name>` for apps in `apps/`) | Dockerfile at repo root or in `apps/<name>/`. |
| **Run** | `docker run -p 8050:8050 -e API_BASE_URL=... -e SECRET_KEY=... plotly-factory` | Pass required env vars via `-e` or `--env-file`. Do not bake secrets into the image. |
| **Volumes** | Mount `assets/` or data dirs if needed: `-v $(pwd)/assets:/app/assets` | Use only when the app reads from the filesystem at runtime. |

---

## 4. Dash Enterprise (if used)

| Item | Action |
|------|--------|
| **Config** | Follow Dash Enterprise app configuration (e.g. `Procfile`, config in platform). |
| **Auth / URL** | Use platform auth and URL structure; document the app URL and any env vars the platform requires. |
| **Pipeline** | Document deploy steps (e.g. git push, CI job) in this doc or in the team runbook. |

---

## 5. Checklist

Before considering deployment done:

- [ ] Required env vars listed in this doc; none hardcoded
- [ ] `debug=False` (or omitted) in production
- [ ] Static assets and favicon served (via app or reverse proxy)
- [ ] Run command and port documented in README and this doc

---

Document run commands and env vars here. Use one source of truth for each app; keep README Quick start and this doc in sync.
