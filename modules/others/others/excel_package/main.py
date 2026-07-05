#!/usr/bin/env python3
import argparse
import sys

from reader import read_student_data, filter_students
from writer import create_excel_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a formatted Excel report from a student data text file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input text file (e.g. data.txt).",
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to the output Excel file (e.g. students.xlsx).",
    )

    parser.add_argument(
        "--faculty",
        help="Filter by faculty name (case-insensitive).",
    )
    parser.add_argument(
        "--age",
        type=int,
        help="Filter by age (integer comparison).",
    )
    parser.add_argument(
        "--gender",
        help="Filter by gender (case-insensitive).",
    )

    return parser.parse_args(argv)


def filters_provided(args):
    return args.faculty is not None or args.age is not None or args.gender is not None


def main(argv=None):
    args = parse_args(argv)

    all_students = read_student_data(args.input)

    is_filtered = filters_provided(args)
    filtered_students = []
    if is_filtered:
        filtered_students = filter_students(
            all_students,
            faculty=args.faculty,
            age=args.age,
            gender=args.gender,
        )
        print(
            f"Filter matched {len(filtered_students)} of {len(all_students)} students.",
            file=sys.stderr,
        )

    sheet_titles = create_excel_report(
        all_students,
        filtered_students,
        args.output,
        is_filtered,
    )

    print(
        f"Success: wrote {len(all_students)} students to '{args.output}' "
        f"(sheets: {', '.join(sheet_titles)})."
    )


if __name__ == "__main__":
    main()
