from .models.course import Course
from .models.student import Student
from .models.undergraduate import UndergraduateStudent
from .models.graduate import GraduateStudent
from .services.school_manager import School
from .utils.validators import Validators

__version__ = "1.0.0"

__all__ = [
    "Course",
    "Student",
    "UndergraduateStudent",
    "GraduateStudent",
    "School",
    "Validators",
]
