from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def _create_user(self, email,first_name,user_type, password=None,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name,user_type, password=None,**extra_fields):
        return self._create_user(email,first_name,user_type, password=None,**extra_fields)

    def create_superuser(self, email,first_name,user_type, password=None,**extra_fields):
        return self._create_user(email,first_name,user_type, password=None,**extra_fields)


class User(AbstractBaseUser):
    class Meta:
        db_table = 'users_user'
    account_number = models.CharField(max_length=45,null=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45,null=True)    
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
   
    emai_verification_code = models.CharField(max_length=45,null=True)
    user_type = models.CharField(max_length=45)
    pin_number = models.IntegerField(default=0)
    status = models.IntegerField(default=0)    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','user_type']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
    