import csv
import os
import sys


EXPECTED_HEADERS = ["name", "surname", "age", "faculty", "gender", "average_grade"]

INT_COLUMNS = {"age"}

FLOAT_COLUMNS = {"average_grade"}


def convert_value(header, raw_value):
    value = raw_value.strip()

    if header in INT_COLUMNS:
        return int(value)

    if header in FLOAT_COLUMNS:
        number = float(value)
        return int(number) if number.is_integer() else number

    return value


def read_student_data(file_path):
    if not os.path.exists(file_path):
        sys.exit(f"Error: input file not found: '{file_path}'")

    if not os.path.isfile(file_path):
        sys.exit(f"Error: input path is not a file: '{file_path}'")

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh)
            rows = [row for row in reader if any(cell.strip() for cell in row)]
    except OSError as exc:
        sys.exit(f"Error: could not read input file '{file_path}': {exc}")

    if not rows:
        sys.exit(f"Error: input file '{file_path}' is empty.")

    headers = [h.strip().lower() for h in rows[0]]
    if headers != EXPECTED_HEADERS:
        sys.exit(
            "Error: unexpected header line.\n"
            f"  Expected: {','.join(EXPECTED_HEADERS)}\n"
            f"  Found:    {','.join(headers)}"
        )

    data_rows = rows[1:]
    if not data_rows:
        sys.exit(f"Error: input file '{file_path}' contains headers but no data rows.")

    students = []
    for line_number, raw_row in enumerate(data_rows, start=2):
        if len(raw_row) != len(EXPECTED_HEADERS):
            print(
                f"Warning: skipping malformed row on line {line_number} "
                f"(expected {len(EXPECTED_HEADERS)} columns, got {len(raw_row)}): "
                f"{raw_row}",
                file=sys.stderr,
            )
            continue

        try:
            student = {
                header: convert_value(header, cell)
                for header, cell in zip(EXPECTED_HEADERS, raw_row)
            }
        except ValueError as exc:
            print(
                f"Warning: skipping invalid row on line {line_number} "
                f"(could not parse numeric field: {exc}): {raw_row}",
                file=sys.stderr,
            )
            continue

        students.append(student)

    if not students:
        sys.exit(f"Error: no valid data rows found in '{file_path}'.")

    return students


def filter_students(students, faculty=None, age=None, gender=None):
    matched = []
    for student in students:
        if faculty is not None:
            if str(student["faculty"]).strip().lower() != faculty.strip().lower():
                continue

        if age is not None:
            if student["age"] != age:
                continue

        if gender is not None:
            if str(student["gender"]).strip().lower() != gender.strip().lower():
                continue

        matched.append(student)

    return matched
