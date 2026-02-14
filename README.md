# Capstone CrewAI – Intelligent User Feedback Analysis System

A Streamlit + CrewAI based system that ingests mock user feedback (CSV), classifies and analyzes it with multiple agents, and generates Jira-style tickets. The UI also supports manual review/editing of generated tickets and basic analytics.

## Features
- **Data ingestion** from mock CSV files (App Store reviews + Support emails)
- **Multi-agent processing** using CrewAI (classification, bug analysis, feature extraction, ticket creation, quality review)
- **Ticket generation** into a structured CSV
- **Manual override UI** (edit ticket fields directly)
- **Logging & error handling** with tracebacks (for debugging + submission requirement)

## Project Structure (key files)
- `app.py` – Streamlit entrypoint
- `src/main.py` – agent pipeline kickoff (`build_crew().kickoff()`)
- `src/crew/app_review_crew.py` – defines CrewAI agents + tasks
- `src/tasks/tasks.py` – task definitions
- `src/tools/FileUtils.py` – CSV read/write tools used by agents
- `src/ui/processing.py` – Manual Override page + processing trigger
- `src/ui/dashboard.py` – Dashboard + recent logs/metrics
- `src/logging_utils.py` – application logging setup

## Input Data
- `app_store_reviews.csv`
- `support_emails.csv`

## Output Files
- `expected_classifications.csv` – final generated tickets (ticket CSV)
- `processing_log.csv` – UI processing events / error tracebacks
- `metrics.csv` – snapshot metrics captured when saving tickets
- `run.log` – Python logs (including stack traces)

## Setup
> Requires Python and a virtual environment.

```bash
cd capstone-crewai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure API Key
CrewAI requires an OpenAI key.

Create `capstone-crewai/.env`:
```bash
OPENAI_API_KEY=sk-...your_key...
```

## Run
### Start Streamlit UI
```bash
cd capstone-crewai
source .venv/bin/activate
streamlit run app.py
```

### Run the agent pipeline (CLI)
```bash
cd capstone-crewai
source .venv/bin/activate
python -c "from src.main import main; main()"
```

## Using the UI
1. Open the Streamlit URL shown in terminal.
2. Go to **Manual Override** tab.
3. Click **Start Processing** to run the agent pipeline.
4. Review/edit the generated tickets in the table.

## Error Handling & Logging
- If processing fails, the UI shows a friendly error and stores the full traceback in:
  - `processing_log.csv`
  - `run.log`

To watch logs live:
```bash
tail -f capstone-crewai/run.log
```

## Notes / Troubleshooting
- If you see: `OPENAI_API_KEY is required` → verify `.env` exists and restart Streamlit.
- If a button appears greyed out → Streamlit may still be running a task; wait or restart the server.

---

## Submission Checklist (quick)
- [x] CSV ingestion
- [x] Agent-based processing
- [x] Ticket CSV generated
- [x] Manual override UI
- [x] Robust logging + error handling
