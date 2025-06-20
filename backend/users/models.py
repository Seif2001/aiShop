from django.db import models
import hashlib
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# create a user
class UserManager(BaseUserManager):

    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError("users must have an email")
        
        if not username:
            raise ValueError("users must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
            )
        
        user.set_password(password)
        user.save(using = self._db)

        return user
        

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(('password'), max_length=128)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add= True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now = True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    



