# CSC418 DevOps Lab Midterm — Roll 26

Student registration example: `FA23-BSE-026`. Update the prefix if your actual registration number differs.

Repository suggestion: `CSC418-DevOps-Midterm-26`.

## Important
Run this project in its own directory and create a separate GitHub repository and self-hosted runner for the classmate.


## Requirements
Python 3.11+, Git, GitHub account, GitHub self-hosted runner.

## Run portal
```bash
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run tests
```bash
python -m pytest tests/ -v --junitxml=results.xml
python make_report.py
```

## Start local report receiver
In a separate terminal:
```bash
set REPORT_TOKEN=lab-local-token
python receiver.py
```
On macOS/Linux use `export REPORT_TOKEN=lab-local-token` instead of `set`.

## CI setup
1. Push repository to GitHub.
2. GitHub repository > Settings > Actions > Runners > New self-hosted runner; follow GitHub's Windows/Linux installation commands on your computer and start the runner.
3. Repository Settings > Secrets and variables > Actions > New repository secret: REPORT_TOKEN = lab-local-token (or choose a stronger matching value).
4. Keep `python receiver.py` running in a terminal, with the matching REPORT_TOKEN environment variable.
5. Every push executes the 3 pytest cases, creates JSON and POSTs it to http://127.0.0.1:5001/report on the same computer.
6. Inspect `test-report.json` in the receiver's working directory. A failing test marks the CI job failed after the report is delivered.

## Demo pass/fail/fix
- Push the original code: all 3 tests pass.
- Temporarily change the URL validation condition in `valid_url` to `return True`; commit and push: invalid URL test fails, report is still delivered.
- Restore the original function, commit and push: tests pass again.
- Take screenshots of Actions runs, portal, and both report versions.

Note: The runner and receiver must be running on the same computer for localhost delivery. Do not expose the receiver publicly. This project uses a local demo secret, not production authentication.
