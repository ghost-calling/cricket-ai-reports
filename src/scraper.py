import requests
import re
from datetime import datetime

def fetch_live_matches_with_scores(limit: int = 10) -> list[dict]:
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    content = response.text.replace('\\"', '"')

    # Split into one chunk per match using "matchId" as the boundary marker
    chunks = content.split('"matchInfo":{"matchId"')

    matches = []
    seen = set()

    for chunk in chunks:
        status_m = re.search(r'"status":"([^"]+)"', chunk)
        team1_m = re.search(r'"team1":\{"teamId":\d+,"teamName":"([^"]+)"', chunk)
        team2_m = re.search(r'"team2":\{"teamId":\d+,"teamName":"([^"]+)"', chunk)
        ground_m = re.search(r'"venueInfo":\{"id":\d+,"ground":"([^"]+)"',chunk)
        start_date_m = re.search(r'"startDate":"([^"]+)"',chunk)

        if not (status_m and team1_m and team2_m and ground_m and start_date_m):
            continue  # this chunk isn't a full match block, skip it

        key = (team1_m.group(1), team2_m.group(1), status_m.group(1), ground_m.group(1), start_date_m.group(1))
        if key in seen:
            continue
        seen.add(key)

        t1_score_m = re.search(r'"team1Score":\{"inngs1":\{"inningsId":\d+,"runs":(\d+),"wickets":(\d+),"overs":([\d.]+)', chunk)
        t2_score_m = re.search(r'"team2Score":\{"inngs1":\{"inningsId":\d+,"runs":(\d+),"wickets":(\d+),"overs":([\d.]+)', chunk)

        team1_score = f"{t1_score_m.group(1)}/{t1_score_m.group(2)} ({t1_score_m.group(3)} ov)" if t1_score_m else "Yet to bat"
        team2_score = f"{t2_score_m.group(1)}/{t2_score_m.group(2)} ({t2_score_m.group(3)} ov)" if t2_score_m else "Yet to bat"

        if start_date_m:
            timestamp_ms = int(start_date_m.group(1))
            match_date = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")
        else:
            match_date = "Unknown"

        matches.append({
            "team1": team1_m.group(1),
            "team2": team2_m.group(1),
            "status": status_m.group(1),
            "team1_score": team1_score,
            "team2_score": team2_score,
            "venue": ground_m.group(1),  # remove leading and trailing quotes
            "match_date": match_date
        })
        if len(matches) >= limit:
            break

    return matches

if __name__ == "__main__":
    for match in fetch_live_matches_with_scores():
        print(f"{match['team1']} {match['team1_score']} vs {match['team2']} {match['team2_score']} — {match['status']} {match['venue']} {match['match_date']}")