import requests
import re

def fetch_live_matches(limit: int = 10) -> list[dict]:
    """
    Scrapes Cricbuzz's live-scores page by extracting embedded JSON
    data from the page's script tags, rather than parsing visible HTML.
    Returns a list of dicts with team1, team2, and status.
    """
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    content = response.text.replace('\\"', '"')

    pattern = re.compile(
        r'"status":"(?P<status>[^"]+)".*?'
        r'"team1":\{"teamId":\d+,"teamName":"(?P<team1>[^"]+)".*?'
        r'"team2":\{"teamId":\d+,"teamName":"(?P<team2>[^"]+)"'
    )

    matches = []
    for m in pattern.finditer(content):
        matches.append({
            "team1": m.group("team1"),
            "team2": m.group("team2"),
            "status": m.group("status"),
        })
        if len(matches) >= limit:
            break

    return matches


if __name__ == "__main__":
    for match in fetch_live_matches():
        print(f"{match['team1']} vs {match['team2']} — {match['status']}")