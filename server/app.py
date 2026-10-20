


from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import db, Workout, Exercise, WorkoutExercise
from .schemas import (
    WorkoutSchema,
    ExerciseSchema,
    WorkoutExerciseSchema,
    WorkoutExerciseCreateSchema,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"errors": error.messages}), 400


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found."}), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return jsonify({"error": "Method not allowed."}), 405


@app.get("/")
def index():
    return jsonify({
        "message": "Workout Application API",
        "endpoints": [
            "GET /workouts",
            "GET /workouts/<id>",
            "POST /workouts",
            "DELETE /workouts/<id>",
            "GET /exercises",
            "GET /exercises/<id>",
            "POST /exercises",
            "DELETE /exercises/<id>",
            "POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises",
        ],
    })


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    validated_data = workout_schema.load(data)
    workout = Workout(**validated_data)

    db.session.add(workout)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Could not create workout."}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted successfully."}), 200


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    validated_data = exercise_schema.load(data)
    exercise = Exercise(**validated_data)

    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "An exercise with this name and category may already exist."
        }), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted successfully."}), 200


@app.post(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises"
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    details = workout_exercise_create_schema.load(data)

    association = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        **details,
    )

    db.session.add(association)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "This exercise may already be assigned to this workout."
        }), 400
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify(workout_exercise_schema.dump(association)), 201


if __name__ == "__main__":
    app.run()
