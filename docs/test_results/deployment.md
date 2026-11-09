# Deployment test results (TC-22, TC-23)

Fill in after running the steps on a machine with Docker Desktop. Record what you actually observe.

**Tester:** ______ · **Date:** ______ · **Machine / OS:** ______ · **Docker version:** ______

## TC-23 Portability: fresh deployment (NFR-08, target ≤ 15 minutes)

| Step | Command / action | Result | Time |
|---|---|---|---|
| 1 | Install Docker Desktop (if needed) and start it | | |
| 2 | `git clone https://github.com/SE-MiniProject-ML-Model-Evaluator/SE-MiniProject.git` | | |
| 3 | `cd SE-MiniProject` then `docker compose up --build` | | |
| 4 | Open https://localhost, register and log in (TC-03) | | |
| | **Total time from step 2 to step 4** | | **__ min** |

Pass if TC-03 succeeds within 15 minutes: ☐ Pass ☐ Fail

## TC-22 Transport security (SR-04)

| Check | How | Expected | Observed |
|---|---|---|---|
| HTTP redirects to HTTPS | Open http://localhost | Address changes to https://localhost | |
| TLS version | Browser padlock → Connection is secure → Certificate / Security tab (or `curl -vk https://localhost 2>&1 \| findstr TLS`) | TLS 1.2 or 1.3 | |
| HSTS header | DevTools → Network → any request → Response headers | `Strict-Transport-Security: max-age=31536000` | |
| Secure cookies | DevTools → Application → Cookies | `sessionid` and `csrftoken` marked **Secure** and (sessionid) **HttpOnly** | |
| No mixed content | DevTools → Console | No mixed-content warnings | |

Pass: ☐ Pass ☐ Fail

**Note:** the certificate is self-signed for the local demo, so the browser shows a warning; this is expected and documented in the deviations log.
