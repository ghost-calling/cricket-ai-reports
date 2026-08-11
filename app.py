from flask import Flask, jsonify
from src.database import init_db, get_match
from src.report_generator import generate_report

app = Flask(__name__)
init_db()

@app.route("/report/<int:match_id>")
def match_report(match_id):
    match = get_match(match_id)
    if not match:
        return jsonify({"error": "match not found"}), 404
    report = generate_report(match)
    return jsonify({"match_id": match_id, "report": report})

if __name__ == "__main__":
    app.run(debug=True)