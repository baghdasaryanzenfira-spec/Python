class Validators:

    @staticmethod
    def is_non_empty_string(value):
        return isinstance(value, str) and value.strip() != ""

    @staticmethod
    def is_valid_grade(value):
        try:
            grade = float(value)
        except (TypeError, ValueError):
            return False
        return 0.0 <= grade <= 4.0

    @staticmethod
    def is_valid_credits(value):
        try:
            credits = int(value)
        except (TypeError, ValueError):
            return False
        return 1 <= credits <= 12

    @staticmethod
    def is_valid_age(value):
        try:
            age = int(value)
        except (TypeError, ValueError):
            return False
        return 5 <= age <= 120

    @staticmethod
    def is_valid_course_code(value):
        if not Validators.is_non_empty_string(value):
            return False
        stripped = value.strip()
        has_alpha = any(ch.isalpha() for ch in stripped)
        has_digit = any(ch.isdigit() for ch in stripped)
        return has_alpha and has_digit

    @staticmethod
    def normalize_name(value):
        if not Validators.is_non_empty_string(value):
            raise ValueError("Name must be a non-empty string.")
        return value.strip().title()
