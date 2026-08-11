def build_match_report_prompt(match: dict) -> str:
    return f"""You are a sharp, knowledgeable cricket analyst writing for readers who already understand the sport — no need to explain basic rules.

Match data:
- {match['team1']} vs {match['team2']}
- Scores: {match['team1_score']} / {match['team2_score']}
- Venue: {match['venue']}
- Date: {match['match_date']}
- Result: {match['result']}
- Key stats: {match['key_stats']}

Write a 150-200 word match report. Rules:
- Lead with the moment that decided the match, not a generic recap
- Reference specific numbers from the key stats provided — do not invent any stat not given above
- Write like a human analyst with an opinion, not a neutral encyclopedia entry
- No clichés like "a match to remember" or "fans were treated to"
- End with one sharp tactical observation, not a summary sentence

Output only the report text, nothing else."""