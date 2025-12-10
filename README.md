# IMLEM Team Manager

Django web application for middle-school math-league coaches to build and optimize meet line-ups.

## Features
- CRUD for **Teams** and **Meets** (generic class-based views)
- Custom lineup editor with automatic validation of IMLEM rules:
  - ≤ 6 competitors per category (A–E)
  - Each student competes in ≤ 3 rounds and is alternate in ≥ 2
- Category-strength tracking per student
- Simple report view: total points per category for any meet
- Minimal, clean UI with basic CSS; ready for further styling

## Quick start (development)
```bash
# create & activate virtualenv (optional)
python -m venv .venv
source .venv/bin/activate

# install deps – Pipfile provided, or use pip
pip install -r requirements.txt  # or `pipenv install`

python manage.py migrate
python manage.py createsuperuser  # follow prompts
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/imlem/` for the app or `/admin/` for the Django admin.

## Directory layout
```
cs412/           – Django project settings & root URLs
project/         – IMLEM app (models, views, templates, forms)
static/          – global CSS
```

## Meeting the course rubric
| Criterion | Implementation |
|-----------|----------------|
| ≥ 4 related models | Team, Student, CategoryStrength, Meet, RoundAssignment |
| CRUD | Teams & Meets show create/list/detail/update/delete |
| Generic + function views | Generic CBVs for CRUD, custom View for lineup editing |
| URL mapping & templates | `project/urls.py` + multiple templates per view |
| Search / filter / report | Meet Category Summary (`/meets/<id>/summary/`) |
| UI aesthetics | Clean layout with `static/styles.css` |
| Documentation | Docstrings in code + this README |

Project built for **CS 412 Final Project (Fall 2025)**. Feel free to extend! 