# Operations

These notes capture the practical work needed to run, maintain, or modernize the repository from its current state.

## Local Operation

- Create a Python virtual environment
- Install dependencies with pip install -r requirements.txt
- Configure a safe local Django settings environment
- Run python manage.py migrate
- Run python manage.py runserver

## Validation

- Run python manage.py check
- Run Django tests if present
- Smoke-test candidate and recruiter flows locally

## Maintenance Notes

- Pin and review Python dependencies
- Keep synthetic demo data separate from real candidate data
- Document algorithm assumptions and limitations

## Operational Risks

- Scoring workflows need fairness, explainability, and validation before real hiring use
- Candidate data handling must be reviewed carefully
- Model or heuristic outputs should support human decisions, not replace them


