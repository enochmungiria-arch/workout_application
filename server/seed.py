
 
from datetime import date, timedelta

from .app import app
from .models import db, Workout, Exercise, WorkoutExercise


def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        pushups = Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False,
        )
        squats = Exercise(
            name="Squats",
            category="Strength",
            equipment_needed=False,
        )
        treadmill = Exercise(
            name="Treadmill Running",
            category="Cardio",
            equipment_needed=True,
        )

        db.session.add_all([pushups, squats, treadmill])
        db.session.flush()

        workout_one = Workout(
            date=date.today(),
            duration_minutes=30,
            notes="Upper body and legs",
        )
        workout_two = Workout(
            date=date.today() - timedelta(days=1),
            duration_minutes=25,
            notes="Cardio session",
        )

        db.session.add_all([workout_one, workout_two])
        db.session.flush()

        db.session.add_all([
            WorkoutExercise(
                workout_id=workout_one.id,
                exercise_id=pushups.id,
                reps=12,
                sets=3,
            ),
            WorkoutExercise(
                workout_id=workout_one.id,
                exercise_id=squats.id,
                reps=15,
                sets=3,
            ),
            WorkoutExercise(
                workout_id=workout_two.id,
                exercise_id=treadmill.id,
                duration_seconds=1200,
            ),
        ])

        db.session.commit()
        print("Database successfully seeded.")


if __name__ == "__main__":
    seed_database()
