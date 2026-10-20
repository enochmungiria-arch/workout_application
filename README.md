# workout_application

# Workout Application Backend

A REST API built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.
It allows users to manage workouts, exercises, and the exercises assigned to
each workout.

## Features

- Create, list, retrieve, and delete workouts.
- Create, list, retrieve, and delete exercises.
- Assign exercises to workouts.
- Store repetitions, sets, and exercise duration.
- Validate request data with Marshmallow.
- Enforce database constraints with SQLAlchemy.
- Manage database schema changes with Flask-Migrate.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- pytest

## Project structure

```text
workout_application/
├── migrations/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── tests/
│   └── test_api.py
├── Pipfile
├── README.md
└── .gitignore
```

## Installation

Install Python and Pipenv first. From the project root, install the dependencies:

```bash
pipenv install
```

If you are adding the packages to an existing environment, you can instead run:

```bash
pipenv install Flask==2.2.2 Flask-Migrate==3.1.0 Flask-SQLAlchemy==3.0.3 Werkzeug==2.2.2 importlib-metadata==6.0.0 importlib-resources==5.10.0 ipdb==0.13.9 marshmallow==3.20.1
pipenv install --dev pytest
```

## Database migrations

Run these commands from the project root.

Initialize migrations once:

```bash
pipenv run flask --app server.app db init
```

Generate the first migration:

```bash
pipenv run flask --app server.app db migrate -m "Create workout and exercise tables"
```

Apply the migration:

```bash
pipenv run flask --app server.app db upgrade
```

Do not run `db init` again if the `migrations` directory already exists.
Whenever you change your models, generate a new migration and upgrade the database.

## Seed sample data

```bash
pipenv run python -m server.seed
```

Warning: the seed script drops and recreates the application tables before
inserting sample records.

## Start the API

```bash
pipenv run flask --app server.app run
```

The API will normally be available at:

http://127.0.0.1:5000

Visit the root URL to see the list of available endpoints.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | Retrieve a workout and its exercise details |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List exercises |
| GET | `/exercises/<id>` | Retrieve an exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Assign an exercise to a workout |

## Example requests

Create a workout:

```json
{
  "duration_minutes": 45,
  "notes": "Full body session"
}
```

Create an exercise:

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

Assign an exercise to a workout:

```json
{
  "reps": 12,
  "sets": 3
}
```

An exercise assignment may provide repetitions, sets, duration in seconds,
or a combination of these values. At least one must be provided.

## Run tests

```bash
pipenv run pytest -v
```

## Error responses

- `400 Bad Request`: invalid input or a database constraint violation.
- `404 Not Found`: the requested workout or exercise does not exist.
- `405 Method Not Allowed`: the HTTP method is unsupported for that endpoint.

## Notes

- Dates use the ISO format `YYYY-MM-DD`.
- Workout duration is measured in minutes.
- Exercise duration is measured in seconds.
- Database constraints protect the data even if invalid data bypasses request
  validation.
