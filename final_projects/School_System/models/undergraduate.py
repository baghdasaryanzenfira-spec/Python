from .student import Student


class UndergraduateStudent(Student):

    level = "Undergraduate"
    HONOR_ROLL_THRESHOLD = 3.5

    def __init__(self, student_id, name, age, major="Undeclared", year=1):
        super().__init__(student_id, name, age)
        self.major = str(major).strip() or "Undeclared"
        try:
            self.year = max(1, min(4, int(year)))
        except (TypeError, ValueError):
            self.year = 1

    def is_honor_roll(self):
        return self.calculate_gpa() >= self.HONOR_ROLL_THRESHOLD

    @classmethod
    def from_dict(cls, data):
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            major=data.get("major", "Undeclared"),
            year=data.get("year", 1),
        )
        from .course import Course
        for course_data in data.get("courses", []):
            student.enroll(Course.from_dict(course_data))
        for code, grade in data.get("grades", {}).items():
            student.assign_grade(code, grade)
        return student

    def to_dict(self):
        data = super().to_dict()
        data.update({"major": self.major, "year": self.year,
                     "honor_roll": self.is_honor_roll()})
        return data

    def summary(self):
        base = super().summary()
        honors = "  Honor Roll" if self.is_honor_roll() else ""
        return f"{base} | major: {self.major}, year {self.year}{honors}"
