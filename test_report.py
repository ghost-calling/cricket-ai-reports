from src.report_generator import generate_report

test_match = {
    "team1": "India", "team2": "Australia",
    "team1_score": "287/6", "team2_score": "241/9",
    "venue": "MCG", "match_date": "2026-01-15",
    "result": "India won by 46 runs",
    "key_stats": "Kohli 89(76), Bumrah 4/32"
}

report = generate_report(test_match)
print(report)