"""
data objects
"""

from dataclasses import dataclass
from uuid import UUID

from base import enums


@dataclass
class Account:
    id: int
    username: str
    role: enums.RoleType
    real_name: str
    student_id: str


@dataclass
class S3File:
    uuid: UUID
    key: str
    bucket: str

