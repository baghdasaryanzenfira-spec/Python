from .student import Student


class GraduateStudent(Student):

    level = "Graduate"
    GOOD_STANDING_THRESHOLD = 3.0

    def __init__(self, student_id, name, age, research_area="General",
                 advisor="Unassigned"):
        super().__init__(student_id, name, age)
        self.research_area = str(research_area).strip() or "General"
        self.advisor = str(advisor).strip() or "Unassigned"

    def in_good_standing(self):
        return self.calculate_gpa() >= self.GOOD_STANDING_THRESHOLD

    @classmethod
    def from_dict(cls, data):
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            research_area=data.get("research_area", "General"),
            advisor=data.get("advisor", "Unassigned"),
        )
        from .course import Course
        for course_data in data.get("courses", []):
            student.enroll(Course.from_dict(course_data))
        for code, grade in data.get("grades", {}).items():
            student.assign_grade(code, grade)
        return student

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "research_area": self.research_area,
            "advisor": self.advisor,
            "good_standing": self.in_good_standing(),
        })
        return data

    def summary(self):
        base = super().summary()
        standing = "good standing" if self.in_good_standing() else "review needed"
        return (f"{base} | research: {self.research_area}, "
                f"advisor: {self.advisor} ({standing})")
