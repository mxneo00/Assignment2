from datetime import datetime
from enum import Enum
import uuid
from passlib.hash import bcrypt
from tortoise import models, fields

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(models.Model):
    user_id = fields.IntField(pk=True, unique=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    digest = fields.CharField(max_length=128)
    #role = fields.CharEnumField()
    fname = fields.CharField(max_length=50)
    lname = fields.CharField(max_length=50)
    activated_at = fields.DatetimeField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def set_password(self, raw_password: str):
        self.digest = bcrypt.hash(raw_password)

    def verify_password(self, raw_password: str):
        return bcrypt.verify(raw_password, self.digest)
    
    class Meta:
        table = "users"

    def __str__(self):
        return f"<User {self.username}"

