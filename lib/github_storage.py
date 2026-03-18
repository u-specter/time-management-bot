import os
import json
import base64

import httpx

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]   # e.g. "umidjon/time-managment"
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _url(date: str) -> str:
    return f"{BASE_URL}/repos/{GITHUB_REPO}/contents/data/{date}.json"


def read_day_data(date: str) -> dict:
    """Return day JSON dict. Returns {} if file not found."""
    r = httpx.get(_url(date), headers=HEADERS, timeout=10)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    raw = base64.b64decode(r.json()["content"]).decode("utf-8")
    return json.loads(raw)


def write_day_data(date: str, data: dict) -> None:
    """Create or update data/{date}.json in the repo."""
    encoded = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    sha = None
    r = httpx.get(_url(date), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        sha = r.json()["sha"]

    payload: dict = {"message": f"data: update {date}", "content": encoded}
    if sha:
        payload["sha"] = sha

    r = httpx.put(_url(date), headers=HEADERS, json=payload, timeout=15)
    r.raise_for_status()


def count_done(date: str) -> tuple:
    """Returns (done, total) schedule tasks for date."""
    data = read_day_data(date)
    schedule_map = data.get("schedule", {})
    from lib.schedule_data import get_today_schedule
    total = len(get_today_schedule())
    done = sum(1 for v in schedule_map.values() if v is True)
    return done, total
