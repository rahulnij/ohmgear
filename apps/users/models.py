from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password

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
        #user.set_password(make_password(password))
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name,user_type, password=None,**extra_fields):
        return self._create_user(email,first_name,user_type, password,**extra_fields)

    def create_superuser(self, email,first_name,user_type, password=None,**extra_fields):
        return self._create_user(email,first_name,user_type, password,**extra_fields)

USER_TYPE =      (('1', 'admin'),
                  ('2', 'user'),
                  ('3', 'corporate user'),                  
                 )

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
    user_type = models.CharField(max_length=45,choices=USER_TYPE)
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
        return '{"id":"%s","email":"%s","user_type":"%s","status":"%s","password":"%s"}' %(self.id,self.email,self.user_type,self.status,self.password)

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
    

class Profile(AbstractBaseUser):
    class Meta:
        db_table = 'users_profile'
    user = models.OneToOneField(User)
    businesstype = models.OneToOneField(businesstype)
    incomegroup = models.OneToOneField(incomegroup)    
    DOB = models.DateField(help_text="Please use MM/DD/YYYY format.")
    address = models.CharField(max_length=80)
    mobilenumber =models.IntegerField(max_length=10,null =True)   
    status = models.IntegerField(max_length=45,null=True)    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now_add=True)
    


    def __unicode__(self):
        return '{"id":"%s","email":"%s","user_type":"%s","status":"%s","password":"%s"}' %(self.id,self.email,self.user_type,self.status,self.password)

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
    
    
    