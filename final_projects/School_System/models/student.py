from ..utils.validators import Validators
from .course import Course


class Student:


    level = "General"

    def __init__(self, student_id, name, age):
        if not Validators.is_non_empty_string(str(student_id)):
            raise ValueError("student_id must be non-empty.")
        if not Validators.is_valid_age(age):
            raise ValueError(f"Invalid age: {age!r}")

        self.student_id = str(student_id).strip()
        self.name = Validators.normalize_name(name)
        self.age = int(age)
        self.courses = {}
        self.grades = {}


    def enroll(self, course):
        if not isinstance(course, Course):
            raise TypeError("enroll() expects a Course instance.")
        self.courses[course.course_code] = course

    def assign_grade(self, course_code, grade):
        code = str(course_code).strip().upper()
        if code not in self.courses:
            raise KeyError(f"Student is not enrolled in {code}.")
        if not Validators.is_valid_grade(grade):
            raise ValueError(f"Invalid grade (expected 0.0-4.0): {grade!r}")
        self.grades[code] = float(grade)


    def calculate_gpa(self):
        total_points = 0.0
        total_credits = 0
        for code, grade in self.grades.items():
            course = self.courses.get(code)
            if course is None:
                continue
            total_points += grade * course.credits
            total_credits += course.credits
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)

    @property
    def gpa(self):
        return self.calculate_gpa()


    @classmethod
    def from_dict(cls, data):
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
        )
        for course_data in data.get("courses", []):
            student.enroll(Course.from_dict(course_data))
        for code, grade in data.get("grades", {}).items():
            student.assign_grade(code, grade)
        return student

    @classmethod
    def from_string(cls, text, sep=","):
        parts = [p.strip() for p in str(text).split(sep)]
        if len(parts) < 3:
            raise ValueError(
                f"Expected 'id{sep}name{sep}age', got {text!r}"
            )
        student_id, name, age = parts[0], parts[1], parts[2]
        return cls(student_id=student_id, name=name, age=age)


    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "level": self.level,
            "courses": [c.to_dict() for c in self.courses.values()],
            "grades": dict(self.grades),
            "gpa": self.calculate_gpa(),
        }

    def summary(self):
        return (
            f"[{self.level}] {self.student_id} | {self.name} | "
            f"age {self.age} | GPA {self.calculate_gpa():.2f} | "
            f"{len(self.courses)} course(s)"
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(id={self.student_id!r}, "
            f"name={self.name!r}, age={self.age})"
        )

    def __str__(self):
        return self.summary()
