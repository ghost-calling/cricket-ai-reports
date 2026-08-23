from flask import Flask, jsonify
from src.database import init_db, get_match, insert_match
from src.report_generator import generate_report
from src.scraper import fetch_live_matches_with_scores

app = Flask(__name__)
init_db()

@app.route("/scrape")
def scrape_and_store():
    matches = fetch_live_matches_with_scores(limit=10)
    stored_count = 0

    for m in matches:
        match_data = {
            "team1": m["team1"],
            "team2": m["team2"],
            "team1_score": m["team1_score"],
            "team2_score": m["team2_score"],
            "venue": m["venue"],
            "match_date": m["match_date"],
            "result": m["status"],
            "key_stats": "N/A",
        }
        insert_match(match_data)
        stored_count += 1

    return jsonify({"stored": stored_count})

@app.route("/report/<int:match_id>")
def match_report(match_id):
    match = get_match(match_id)
    if not match:
        return jsonify({"error": "match not found"}), 404
    report = generate_report(match)
    return jsonify({"match_id": match_id, "report": report})

if __name__ == "__main__":
    app.run(debug=True)