import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager 
from datetime import datetime, timedelta

class User(AbstractBaseUser, PermissionsMixin):
    school_name = models.CharField(blank=False, max_length=100)
    school_code = models.CharField(blank=False, max_length=50, primary_key=True, unique=True)
    principal = models.CharField(max_length=100, blank=False)
    phone = models.CharField(db_index=True, max_length=15, unique=True, blank=False)
    email = models.EmailField(db_index=True, unique=True, blank=False)
    teacher_count = models.IntegerField(blank=False)
    affiliated_board = models.CharField(blank=False, max_length=100)
    address = models.CharField(blank=False, max_length=500)
    sub_district = models.CharField(blank=False, max_length=50)
    district = models.CharField(blank=False, max_length=50)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'school_code'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['school_name', 'principal', 'teacher_count', 'affiliated_board', 'sub_district', 'district', 'address', 'phone', 'email']

    def __str__(self):
        return self.school_code
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
