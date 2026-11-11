import os
import json
from pathlib import Path

from flask import Flask, jsonify
from src.database import init_db, get_match, insert_match
from src.report_generator import generate_report
from src.scraper import fetch_live_matches_with_scores

app = Flask(__name__)
init_db()

SAMPLE_PATH = Path(__file__).parent / "sample_report.json"


@app.route("/")
def home():
    return """
    <html>
      <head><title>Cricket AI Reports</title></head>
      <body style="font-family: sans-serif; max-width: 600px; margin: 60px auto;">
        <h1>Cricket AI Reports</h1>
        <p>Scrapes live cricket match data and generates match reports with an LLM
        (Flask, SQLite, Gemini API).</p>
        <ul>
          <li><a href="/demo">/demo</a> - saved sample report (real output, no API call)</li>
          <li><code>/scrape</code> - fetches and stores current matches</li>
          <li><code>/report/&lt;match_id&gt;</code> - generates a fresh AI report for a stored match</li>
          <li><a href="https://github.com/ghost-calling/cricket-ai-reports">Source code and README</a></li>
        </ul>
        <p><small>Hosted on a free tier: the first load after idle can take up to a minute.</small></p>
      </body>
    </html>
    """


@app.route("/demo")
def demo():
    with open(SAMPLE_PATH) as f:
        return jsonify(json.load(f))


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
        return jsonify({"error": "match not found. Run /scrape first, or see /demo"}), 404
    try:
        report = generate_report(match)
    except Exception:
        app.logger.exception("Report generation failed")
        return jsonify({"error": "report generation is unavailable right now. See /demo"}), 503
    return jsonify({"match_id": match_id, "report": report})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)