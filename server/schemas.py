



from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )

    exercise = fields.Nested(
        "ExerciseSchema",
        only=("id", "name", "category", "equipment_needed"),
        dump_only=True,
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120),
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=80),
    )
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
    )

    @validates_schema
    def validate_text_fields(self, data, **kwargs):
        errors = {}

        for field_name in ("name", "category"):
            value = data.get(field_name)
            if value is not None and not value.strip():
                errors[field_name] = [
                    f"{field_name} cannot contain only whitespace."
                ]

        if errors:
            raise ValidationError(errors)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=False)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )

    notes = fields.Str(
        allow_none=True,
        validate=validate.Length(max=2000),
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
    )


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    duration_seconds = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1),
    )

    @validates_schema
    def validate_training_details(self, data, **kwargs):
        allowed_fields = ("reps", "sets", "duration_seconds")

        if not any(data.get(name) is not None for name in allowed_fields):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )
