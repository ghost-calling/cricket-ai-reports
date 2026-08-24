
# Cricket AI Match Reports

This is a simple AI assisted scraper project that scrapes live cricket data.

## What it does 

This project scrapes live match data from Cricbuzz. It takes match datas like both team's scores , match status with ground and date informations and generated a AI report on the match.

## Architecture
Cricbuzz → scraper.py → SQLite database → Gemini API → Flask API

## Tech stack
- Python, Flask
- SQLite
- Google Gemini API (gemini-flash-lite-latest)
- BeautifulSoup/regex for scraping
- pytest

## How to run locally
1. Clone the repo
2. Create venv, install requirements.txt
3. Add your own GEMINI_API_KEY to a .env file
4. Run `python app.py`
5. Visit /scrape to fetch live matches, then /report/<id> for a report

## Key design decisions

While testing the AI report generation, I found the model would invent specific 
match details (fake in-progress scores, fictional tactical moments) when given 
incomplete stats. I fixed this by adding explicit constraints to the prompt: 
don't invent details not present in the data, and clearly state when detailed 
stats aren't available rather than filling the gap with plausible-sounding fiction.

Separately, I traced a related issue to stale test data still sitting in the 
database from earlier development — a good reminder that when AI output looks 
wrong, the data feeding it needs to be verified just as carefully as the prompt 
or the model itself.

## What I'd improve with more time

I might add individual player stats, deployment, duplicate-scrape protection etc. 

## Note on AI assistance

This project was built with AI assistance (Claude) for debugging, code review and learning - I
designed the architecture, wrote and tested the code and understand every part of it.