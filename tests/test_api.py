

import pytest

from server.app import app
from server.models import db, Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        workout = Workout(
            duration_minutes=30,
            notes="Test workout",
        )
        exercise = Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False,
        )

        db.session.add_all([workout, exercise])
        db.session.commit()

        workout_id = workout.id
        exercise_id = exercise.id

    with app.test_client() as test_client:
        yield test_client, workout_id, exercise_id

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home(client):
    test_client, _, _ = client

    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Workout Application API"


def test_get_workouts(client):
    test_client, _, _ = client

    response = test_client.get("/workouts")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["duration_minutes"] == 30


def test_get_one_workout(client):
    test_client, workout_id, _ = client

    response = test_client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.json["id"] == workout_id


def test_create_workout(client):
    test_client, _, _ = client

    response = test_client.post(
        "/workouts",
        json={
            "duration_minutes": 45,
            "notes": "Evening workout",
        },
    )

    assert response.status_code == 201
    assert response.json["duration_minutes"] == 45


def test_reject_invalid_workout(client):
    test_client, _, _ = client

    response = test_client.post(
        "/workouts",
        json={
            "duration_minutes": 0,
        },
    )

    assert response.status_code == 400


def test_delete_workout(client):
    test_client, workout_id, _ = client

    response = test_client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert test_client.get(f"/workouts/{workout_id}").status_code == 404


def test_get_exercises(client):
    test_client, _, _ = client

    response = test_client.get("/exercises")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Push-ups"


def test_get_one_exercise(client):
    test_client, _, exercise_id = client

    response = test_client.get(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.json["id"] == exercise_id


def test_create_exercise(client):
    test_client, _, _ = client

    response = test_client.post(
        "/exercises",
        json={
            "name": "Plank",
            "category": "Core",
            "equipment_needed": False,
        },
    )

    assert response.status_code == 201
    assert response.json["name"] == "Plank"


def test_reject_empty_exercise_name(client):
    test_client, _, _ = client

    response = test_client.post(
        "/exercises",
        json={
            "name": "   ",
            "category": "Strength",
        },
    )

    assert response.status_code == 400


def test_delete_exercise(client):
    test_client, _, exercise_id = client

    response = test_client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert test_client.get(f"/exercises/{exercise_id}").status_code == 404


def test_assign_exercise_to_workout(client):
    test_client, workout_id, exercise_id = client

    response = test_client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={
            "reps": 12,
            "sets": 3,
        },
    )

    assert response.status_code == 201
    assert response.json["reps"] == 12
    assert response.json["sets"] == 3
    assert response.json["exercise"]["name"] == "Push-ups"


def test_reject_assignment_without_training_details(client):
    test_client, workout_id, exercise_id = client

    response = test_client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={},
    )

    assert response.status_code == 400


def test_workout_not_found(client):
    test_client, _, _ = client

    response = test_client.get("/workouts/99999")

    assert response.status_code == 404


def test_exercise_not_found(client):
    test_client, _, _ = client

    response = test_client.get("/exercises/99999")

    assert response.status_code == 404
