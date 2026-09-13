import json
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "harshithavardineedi-lgtm"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def fetch_contributions():

    print("Fetching GitHub contributions...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    days = []

    for cell in soup.select(
        "td.ContributionCalendar-day"
    ):

        date = cell.get("data-date")

        level = cell.get(
            "data-level",
            "0"
        )

        if date:

            days.append({
                "date": date,
                "level": int(level)
            })

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "username": USERNAME,
        "updated": datetime.utcnow().isoformat(),
        "days": days
    }

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )

    print(
        f"Saved {len(days)} contribution days."
    )


if __name__ == "__main__":
    fetch_contributions()
