import os
import json
import base64

import httpx

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
SETTINGS_FILE = "data/settings.json"


def _url() -> str:
    return f"{BASE_URL}/repos/{GITHUB_REPO}/contents/{SETTINGS_FILE}"


def read_settings() -> dict:
    r = httpx.get(_url(), headers=HEADERS, timeout=10)
    if r.status_code == 404:
        return {"lang": "ru"}
    r.raise_for_status()
    raw = base64.b64decode(r.json()["content"]).decode("utf-8")
    return json.loads(raw)


def write_settings(data: dict) -> None:
    encoded = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")
    sha = None
    r = httpx.get(_url(), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        sha = r.json()["sha"]
    payload: dict = {"message": "settings: update lang", "content": encoded}
    if sha:
        payload["sha"] = sha
    httpx.put(_url(), headers=HEADERS, json=payload, timeout=15).raise_for_status()


def get_lang() -> str:
    return read_settings().get("lang", "ru")


def set_lang(lang: str) -> None:
    settings = read_settings()
    settings["lang"] = lang
    write_settings(settings)
