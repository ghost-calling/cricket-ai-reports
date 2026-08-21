from src.prompts import build_match_report_prompt

def test_prompt_includes_match_data():
    match = {
        "team1": "India", "team2": "Australia",
        "team1_score": "287/6", "team2_score": "241/9",
        "venue": "MCG", "match_date": "2026-01-15",
        "result": "India won by 46 runs",
        "key_stats": "Kohli 89(76), Bumrah 4/32"
    }
    prompt = build_match_report_prompt(match)
    assert "India" in prompt
    assert "Kohli 89(76)" in prompt
    assert "150-200 word" in prompt

def test_prompt_handles_different_teams():
    match = {
        "team1": "Pakistan", "team2": "England",
        "team1_score": "310/5", "team2_score": "298/8",
        "venue": "Lord's", "match_date": "2026-03-10",
        "result": "Pakistan won by 12 runs",
        "key_stats": "Babar Azam 102(89)"
    }
    prompt = build_match_report_prompt(match)
    assert "Pakistan" in prompt
    assert "England" in prompt
    assert "Babar Azam 102(89)" in prompt