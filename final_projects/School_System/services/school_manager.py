import os

from ..models.student import Student


class School:

    def __init__(self, name="My School"):
        self.name = str(name).strip() or "My School"
        self._students = {}


    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("add_student() expects a Student instance.")
        if student.student_id in self._students:
            raise ValueError(f"Duplicate student_id: {student.student_id}")
        self._students[student.student_id] = student

    def remove_student(self, student_id):
        return self._students.pop(str(student_id).strip(), None)

    def get_student(self, student_id):
        return self._students.get(str(student_id).strip())

    @property
    def students(self):
        return list(self._students.values())


    def total_students(self):
        return len(self._students)

    def overall_average(self):
        students = self.students
        if not students:
            return 0.0
        return round(sum(s.calculate_gpa() for s in students) / len(students), 2)

    def top_students(self, n=3):
        return sorted(
            self.students, key=lambda s: s.calculate_gpa(), reverse=True
        )[:n]


    def filter_by_level(self, level):
        target = str(level).strip().lower()
        return [s for s in self.students if s.level.lower() == target]

    def filter_by_min_gpa(self, min_gpa):
        threshold = float(min_gpa)
        return [s for s in self.students if s.calculate_gpa() >= threshold]

    def filter_by_course(self, course_code):
        code = str(course_code).strip().upper()
        return [s for s in self.students if code in s.courses]


    def build_report(self):
        lines = []
        lines.append("=" * 60)
        lines.append(f"SCHOOL REPORT: {self.name}")
        lines.append("=" * 60)
        lines.append(f"Total students : {self.total_students()}")
        lines.append(f"Overall avg GPA: {self.overall_average():.2f}")
        lines.append("")
        lines.append("Top 3 Students")
        lines.append("-" * 60)
        top = self.top_students(3)
        if top:
            for rank, student in enumerate(top, start=1):
                lines.append(
                    f"{rank}. {student.name} "
                    f"(GPA {student.calculate_gpa():.2f}) [{student.level}]"
                )
        else:
            lines.append("(no students)")
        lines.append("")
        lines.append("Full Roster")
        lines.append("-" * 60)
        if self.students:
            for student in sorted(
                self.students, key=lambda s: s.calculate_gpa(), reverse=True
            ):
                lines.append(student.summary())
        else:
            lines.append("(no students)")
        lines.append("=" * 60)
        return "\n".join(lines)

    def export_report(self, filepath="school_report.txt"):
        path = os.path.abspath(filepath)
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.build_report())
            fh.write("\n")
        return path

    def __len__(self):
        return self.total_students()

    def __repr__(self):
        return f"School(name={self.name!r}, students={self.total_students()})"
