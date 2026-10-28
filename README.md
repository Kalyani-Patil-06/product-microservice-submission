# Product Microservice – CRUD Operations and Product Search

Python/Flask reference-aligned project containing the Product model, factory, model and route tests, BDD scenarios, and step definitions.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```powershell
python run.py
```
Open http://127.0.0.1:5000/

## Run unit tests
```powershell
python -m unittest discover -s tests -v
```

## Run browser BDD tests
Keep the app running, then in another terminal run `behave`. Chrome and a compatible ChromeDriver are required.

This is a standalone implementation based on the assignment rubric's Python reference patterns. If your course supplied a starter repository with different conventions, compare before replacing files.
