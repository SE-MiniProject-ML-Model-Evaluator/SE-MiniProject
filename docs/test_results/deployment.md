# Deployment test results (TC-22, TC-23)

## TC-23 Portability: fresh deployment (NFR-08, target ≤ 15 minutes)

| Step | Command / action | Result | Time |
|---|---|---|---|
| 1 | Install Docker Desktop (if needed) and start it |Pass |2 min 43 sec|
| 2 | `git clone https://github.com/SE-MiniProject-ML-Model-Evaluator/SE-MiniProject.git` |Pass |2 sec |
| 3 | `cd SE-MiniProject` then `docker compose up --build` |Pass |2 sec |
| 4 | Open https://localhost, register and log in (TC-03) |Pass |1 minute |
| | **Total time from step 2 to step 4** | | **_64_ sec** |

Pass if TC-03 succeeds within 15 minutes: Pass

## TC-22 Transport security (SR-04)

| Check | How | Expected | Observed |
|---|---|---|---|
| HTTP redirects to HTTPS | Open http://localhost | Address changes to https://localhost |Pass |
| TLS version | Browser padlock → Connection is secure → Certificate / Security tab (or `curl -vk https://localhost 2>&1 \| findstr TLS`) | TLS 1.2 or 1.3 |Pass |
| HSTS header | DevTools → Network → any request → Response headers | `Strict-Transport-Security: max-age=31536000` |Pass |
| Secure cookies | DevTools → Application → Cookies | `sessionid` and `csrftoken` marked **Secure** and (sessionid) **HttpOnly** |Pass |
| No mixed content | DevTools → Console | No mixed-content warnings |Pass |

Pass

(**Note:** the certificate is self-signed for the local demo, so the browser shows a warning; this is expected and documented in the deviations log.)
