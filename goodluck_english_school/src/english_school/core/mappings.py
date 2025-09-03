from .models import User

from profiles.models import TeacherProfile, StudentProfile
from payments.constants import (
    STUDENT_START_BALANCE_WALLET,
    TEACHER_START_BALANCE_WALLET,
)

PROFILE_MAPPING = {
    'models': {
        User.Role.TEACHER: TeacherProfile,
        User.Role.STUDENT: StudentProfile,
    },
}

WALLET_BALANCE_MAPPING = {
    User.Role.TEACHER: TEACHER_START_BALANCE_WALLET,
    User.Role.STUDENT: STUDENT_START_BALANCE_WALLET,
}
