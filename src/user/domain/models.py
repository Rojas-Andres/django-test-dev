from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class User:
    email: str
    id: Optional[int] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    document: Optional[str] = None
    code_phone: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    is_superuser: Optional[bool] = False
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    locked_until: Optional[datetime] = None
    failed_attempts: Optional[int] = None
