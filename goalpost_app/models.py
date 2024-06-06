from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# USER
class GoalpostUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, first name
        and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email, first name
        and password.
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
    first_name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    level = models.PositiveBigIntegerField(default=0)
    experience = models.PositiveBigIntegerField(default=0)
    
    REQUIRED_FIELDS=["first_name"]
    USERNAME_FIELD = "email"
    objects = GoalpostUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

# GOAL
class Goal(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    #time_period = models.Field
    begin_date = models.BigIntegerField()
    completion_date = models.BigIntegerField()
    accomplished_goal = models.BooleanField()
    user = models.ForeignKey(GoalpostUser, on_delete=models.CASCADE, related_name="goals")

class GoalReflection(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    is_completed = models.BooleanField()
    made_progress = models.FloatField(null=True)
    made_progress_reflection = models.CharField(max_length=10000, null=True)
    could_do_better = models.FloatField(null=True)
    could_do_better_reflection = models.CharField(max_length=10000, null=True)
    steps_to_improve = models.CharField(max_length=10000, null=True)

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="reflections")
