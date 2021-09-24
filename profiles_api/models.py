from django.db import models
# Base classes that we need to use when customizing django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Custom manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        # The email field becomes case insensitive
        email = self.normalize_email(email)
        # We create a ner user based on our custom manager
        user = self.model(email=email, name=name)
        # We use this method to ensure the password will be hashed/encrypted
        user.set_password(password)
        # We use this methos to ensure we will bring support to multiple databases in the future
        user.save(using=self._db)
        # We return the created user object
        return user

    def create_superuser(self, email, name, password):
        """
        Create and save a new superuser with given parameters
        This time we ask for a password because a superuser must own one
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True # defined by PermissionMixin by default
        user.is_staff = True # defined by ourselves in our clase UserProfile
        # We use this method to ensure we will bring support to multiple databases in the future
        user.save(using=self._db)
        # We return the created user object
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    """We override username field asking for the email and password to authenticate the user"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
