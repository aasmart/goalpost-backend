from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class GoalpostUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class GoalpostUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS=["first_name"]

    objects = GoalpostUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
