#!/usr/bin/env python
"""NFR-01 / NFR-03 / TC-13: page load times and error rate with concurrent users.

Start the app in one PowerShell window:      py manage.py runserver
Then in a second window (venv active):       py scripts/load_test.py
Options: --users 20  --duration 300  --base http://127.0.0.1:8000

Each simulated user registers, logs in, and keeps opening pages (and a few API calls) with
0.5-1.5 s pauses, staying under the 100 API requests/minute limit (SR-06).
Writes docs/test_results/performance_load.md
"""
import argparse
import http.cookiejar
import pathlib
import platform
import random
import re
import statistics
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["/datasets/", "/evaluations/", "/datasets/upload/", "/"]
APIS = ["/api/datasets", "/api/evaluations", "/api/models"]
P95_LIMIT_S, ERROR_LIMIT = 3.0, 0.01


class Client:
    def __init__(self, base):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def csrf(self):
        return next((c.value for c in self.jar if c.name == "csrftoken"), "")

    def request(self, path, data=None, headers=None):
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        req = urllib.request.Request(self.base + path, data=body, headers=headers or {})
        if data is not None:
            req.add_header("Referer", self.base + path)
            req.add_header("X-CSRFToken", self.csrf())
        started = time.perf_counter()
        try:
            with self.opener.open(req, timeout=30) as resp:
                resp.read()
                status = resp.status
        except urllib.error.HTTPError as err:
            status = err.code
        except Exception:
            status = 0
        return status, time.perf_counter() - started

    def form_post(self, path, fields):
        self.request(path)                                  # get the CSRF cookie
        fields = dict(fields, csrfmiddlewaretoken=self.csrf())
        return self.request(path, fields)


def user_session(base, idx, run_id, stop_at, records, lock):
    client = Client(base)
    email, password = f"load{run_id}u{idx}@test.com", "LoadTest123!"
    client.form_post("/accounts/register/", {"email": email, "password": password, "confirm_password": password})
    status, _ = client.form_post("/accounts/login/", {"email": email, "password": password})
    if status != 200:
        with lock:
            records.append(("login", status, 0.0))
        return
    while time.time() < stop_at:
        path = random.choice(APIS) if random.random() < 0.2 else random.choice(PAGES)
        headers = {"Accept": "application/json"} if path.startswith("/api/") else {}
        status, seconds = client.request(path, headers=headers)
        with lock:
            records.append((path, status, seconds))
        time.sleep(random.uniform(0.5, 1.5))


def pct(values, p):
    values = sorted(values)
    if not values:
        return 0.0
    k = max(0, min(len(values) - 1, int(round(p / 100 * len(values) + 0.5)) - 1))
    return values[k]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    ap.add_argument("--users", type=int, default=20)
    ap.add_argument("--duration", type=int, default=300, help="seconds (TC-13 says 5 minutes = 300)")
    args = ap.parse_args()
    base = args.base.rstrip("/")

    probe, _ = Client(base).request("/api/health")
    if probe != 200:
        sys.exit(f"Cannot reach {base}/api/health - start the app first with: py manage.py runserver")

    run_id = re.sub(r"\D", "", str(time.time()))[-8:]
    records, lock = [], threading.Lock()
    stop_at = time.time() + args.duration
    print(f"{args.users} users for {args.duration} s against {base} ...", flush=True)
    threads = [threading.Thread(target=user_session, args=(base, i, run_id, stop_at, records, lock), daemon=True)
               for i in range(args.users)]
    for t in threads:
        t.start()
        time.sleep(0.1)
    for t in threads:
        t.join()

    page = [s for p, st, s in records if not p.startswith("/api/") and p != "login"]
    errors = [r for r in records if r[1] < 200 or r[1] >= 400]
    error_rate = len(errors) / max(1, len(records))
    p95 = pct(page, 95)
    passed = p95 <= P95_LIMIT_S and error_rate <= ERROR_LIMIT and records

    rows = []
    for path in PAGES + APIS:
        times = [s for p, st, s in records if p == path]
        if times:
            rows.append(f"| `{path}` | {len(times)} | {statistics.median(times) * 1000:.0f} | "
                        f"{pct(times, 95) * 1000:.0f} | {max(times) * 1000:.0f} |")
    report = "\n".join([
        "# NFR-01 / NFR-03 load test (TC-13 steps 1 and 3)", "",
        f"Generated by `scripts/load_test.py` on {time.strftime('%d %b %Y %H:%M')}.", "",
        f"- Target: {base} (Django `runserver`)",
        f"- Machine: {platform.platform()}, Python {platform.python_version()}",
        f"- Load: **{args.users} concurrent logged-in users** for **{args.duration} s**, 0.5-1.5 s think time",
        f"- Total requests: {len(records)} · errors: {len(errors)} (**{error_rate:.2%}**, limit 1%)",
        f"- Page load 95th percentile: **{p95:.3f} s** (limit {P95_LIMIT_S:.0f} s)", "",
        "| Endpoint | Requests | Median (ms) | p95 (ms) | Max (ms) |", "|---|---|---|---|---|",
        *rows, "",
        f"**Overall: {'PASS' if passed else 'FAIL'}**", "",
    ])
    out = ROOT / "docs" / "test_results" / "performance_load.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {out.relative_to(ROOT)}")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
