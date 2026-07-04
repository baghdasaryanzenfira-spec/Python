#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from School_System.models.course import Course
from School_System.models.undergraduate import UndergraduateStudent
from School_System.models.graduate import GraduateStudent
from School_System.services.school_manager import School
from School_System.utils.validators import Validators


def prompt(message):
    return input(message).strip()


def pause():
    input("\nPress Enter to continue...")


def seed_demo_data(school):
    cs101 = Course("CS101", "Intro to Programming", 3)
    math200 = Course("MATH200", "Linear Algebra", 4)
    phd500 = Course("RES500", "Research Methods", 3)

    alice = UndergraduateStudent("S001", "alice smith", 19,
                                 major="Computer Science", year=2)
    alice.enroll(cs101)
    alice.enroll(math200)
    alice.assign_grade("CS101", 4.0)
    alice.assign_grade("MATH200", 3.5)

    bob = UndergraduateStudent("S002", "bob jones", 20,
                               major="Mathematics", year=3)
    bob.enroll(math200)
    bob.assign_grade("MATH200", 3.0)

    carol = GraduateStudent("G001", "carol white", 26,
                            research_area="Machine Learning",
                            advisor="Dr. Lee")
    carol.enroll(phd500)
    carol.enroll(cs101)
    carol.assign_grade("RES500", 3.9)
    carol.assign_grade("CS101", 3.8)

    for student in (alice, bob, carol):
        school.add_student(student)
    print("Demo data loaded (3 students, 3 courses).")


def add_student(school):
    print("\nStudent type:  1) Undergraduate   2) Graduate")
    choice = prompt("Choose (1/2): ")

    student_id = prompt("Student ID: ")
    name = prompt("Name: ")
    age = prompt("Age: ")

    if not Validators.is_valid_age(age):
        print("! Invalid age. Aborting.")
        return

    try:
        if choice == "2":
            research = prompt("Research area: ") or "General"
            advisor = prompt("Advisor: ") or "Unassigned"
            student = GraduateStudent(student_id, name, age,
                                      research_area=research, advisor=advisor)
        else:
            major = prompt("Major: ") or "Undeclared"
            year = prompt("Year (1-4): ") or "1"
            student = UndergraduateStudent(student_id, name, age,
                                           major=major, year=year)
        school.add_student(student)
        print(f"Added: {student.summary()}")
    except (ValueError, TypeError) as exc:
        print(f"! Could not add student: {exc}")


def enroll_and_grade(school):
    student_id = prompt("Student ID: ")
    student = school.get_student(student_id)
    if student is None:
        print("! No such student.")
        return

    code = prompt("Course code (e.g. CS101): ")
    name = prompt("Course name: ")
    credits = prompt("Credits (1-12): ")
    try:
        course = Course(code, name, credits)
        student.enroll(course)
        print(f"Enrolled {student.name} in {course}.")
    except (ValueError, TypeError) as exc:
        print(f"! Could not enroll: {exc}")
        return

    grade = prompt(f"Grade for {course.course_code} (0.0-4.0, blank to skip): ")
    if grade:
        try:
            student.assign_grade(course.course_code, grade)
            print(f"Grade recorded. New GPA: {student.calculate_gpa():.2f}")
        except (ValueError, KeyError) as exc:
            print(f"! Could not record grade: {exc}")


def list_students(school):
    if not school.students:
        print("(no students)")
        return
    for student in school.students:
        print(" ", student.summary())


def show_statistics(school):
    print(f"\nTotal students : {school.total_students()}")
    print(f"Overall avg GPA: {school.overall_average():.2f}")
    print("\nTop 3 students:")
    top = school.top_students(3)
    if not top:
        print("  (none)")
    for rank, student in enumerate(top, start=1):
        print(f"  {rank}. {student.name} — GPA {student.calculate_gpa():.2f} "
              f"[{student.level}]")


def filter_students(school):
    print("\nFilter by:  1) Level   2) Minimum GPA   3) Course code")
    choice = prompt("Choose (1/2/3): ")
    results = []
    if choice == "1":
        level = prompt("Level (Undergraduate/Graduate): ")
        results = school.filter_by_level(level)
    elif choice == "2":
        value = prompt("Minimum GPA: ")
        if not Validators.is_valid_grade(value):
            print("! Invalid GPA value.")
            return
        results = school.filter_by_min_gpa(value)
    elif choice == "3":
        code = prompt("Course code: ")
        results = school.filter_by_course(code)
    else:
        print("! Unknown option.")
        return

    if not results:
        print("(no matching students)")
    for student in results:
        print(" ", student.summary())


def export_report(school):
    default = "school_report.txt"
    filepath = prompt(f"Output file [{default}]: ") or default
    try:
        path = school.export_report(filepath)
        print(f"Report written to: {path}")
    except OSError as exc:
        print(f"! Could not write report: {exc}")


MENU = """
========= SCHOOL MANAGEMENT SYSTEM =========
1) Add student
2) Enroll student in a course + grade
3) List all students
4) Show statistics (total, average, top 3)
5) Filter students
6) Export report to .txt
7) Load demo data
0) Exit
============================================"""


def run():
    school = School("Central High")
    print("Welcome to the School Management System!")

    while True:
        print(MENU)
        choice = prompt("Select an option: ")

        if choice == "1":
            add_student(school)
        elif choice == "2":
            enroll_and_grade(school)
        elif choice == "3":
            list_students(school)
        elif choice == "4":
            show_statistics(school)
        elif choice == "5":
            filter_students(school)
        elif choice == "6":
            export_report(school)
        elif choice == "7":
            seed_demo_data(school)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("! Invalid option, please try again.")

        pause()


if __name__ == "__main__":
    run()
