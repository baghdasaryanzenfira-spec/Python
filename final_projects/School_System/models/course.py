from ..utils.validators import Validators


class Course:

    def __init__(self, course_code, name, credits):
        if not Validators.is_valid_course_code(course_code):
            raise ValueError(f"Invalid course code: {course_code!r}")
        if not Validators.is_non_empty_string(name):
            raise ValueError(f"Invalid course name: {name!r}")
        if not Validators.is_valid_credits(credits):
            raise ValueError(f"Invalid credits (expected 1-12): {credits!r}")

        self.course_code = course_code.strip().upper()
        self.name = name.strip()
        self.credits = int(credits)

    def to_dict(self):
        return {
            "course_code": self.course_code,
            "name": self.name,
            "credits": self.credits,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            course_code=data["course_code"],
            name=data["name"],
            credits=data["credits"],
        )

    def __eq__(self, other):
        return isinstance(other, Course) and other.course_code == self.course_code

    def __hash__(self):
        return hash(self.course_code)

    def __repr__(self):
        return f"Course(code={self.course_code!r}, name={self.name!r}, credits={self.credits})"

    def __str__(self):
        return f"{self.course_code} - {self.name} ({self.credits} cr)"
