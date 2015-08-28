from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django_pgjson.fields import JsonField

class CustomUserManager(BaseUserManager):

    def _create_user(self, email,first_name, password=None,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        if not first_name:
            raise ValueError('first_name required')        
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name, user_type=1, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name, password=None,**extra_fields):
        return self._create_user(email,first_name, password,**extra_fields)

    def create_superuser(self, email,first_name, password=None,**extra_fields):
        return self._create_user(email,first_name, password,**extra_fields)

USER_TYPE =      (('1', 'admin'),
                  ('2', 'individual'),
                  ('3', 'corporate user'),                  
                 )

class User(AbstractBaseUser):
    class Meta:
        db_table = 'ohmgear_users'
    account_number = models.CharField(_("Account Number"),max_length=45,null=True)
    first_name = models.CharField(_("First Name"),max_length=45)
    last_name = models.CharField(_("Last Name"),max_length=45,null=True)    
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
   
    emai_verification_code = models.CharField(_("Email Verification"),max_length=45,null=True)
    user_type = models.IntegerField(_("User Type"),choices=USER_TYPE,default=2)
    pin_number = models.IntegerField(_("Pin Number"),default=0)
    status = models.IntegerField(_("Status"),default=1)    
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return '{"id":"%s","email":"%s","user_type":"%s","status":"%s"}' %(self.id,self.email,self.user_type,self.status)

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
        return True

BUSINESS_TYPE = (('1', 'option1'),
                  ('2', 'option2'),
                  ('3', 'option3'),                  
                 )
                 
INCOME_GROUP = (('1', '1000'),
                  ('2','2000'),
                  ('3','5000'),
               )               

SOCIAL_TYPE = (('1','FB'),
                ('2','QQ'),
                )  
    
               
class Profile(models.Model):
    class Meta:
        db_table = 'ohmgear_profile'
    dob = models.DateField(_("DOB"),null=True)
    gender = models.CharField(_("Gender"),null =True,max_length= 10) 
    address = models.CharField(_("Address"),max_length=80,null=True)
    mobile_number = models.CharField(_("Mobile Number"),max_length=10,null=True)   
    custom_data = JsonField(null=True)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=True)    
    user = models.OneToOneField(User,null=True)
    income_group = models.CharField(_("Income Group"),max_length=45,choices=INCOME_GROUP,default=1)
    business_type = models.CharField(_("Business Type"),max_length=45,choices=BUSINESS_TYPE,default=1)

    def __unicode__(self):
        return '{"id":"%s","dob":"%s","gender":"%s","address":"%s","mobile_number":"%s","user":"%s","income_group":"%s","business_type":"%s"}' %(self.id,self.dob,self.gender,self.address,self.mobile_number,self.user,self.income_group,self.business_type)



class SocialLogin(models.Model):
    class Meta:
        db_table = 'ohmgear_socialprofile'
    social_media_login_id = models.CharField(_("Social Media Login Id"),null=True,max_length=50)
    social_type = models.CharField(_("Social Type"),max_length=45,choices=SOCIAL_TYPE,default=1)
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True)
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return'{"id:"%s","social_media_login_id":"%s","social_type":"%s","status":""}'%(self.id,self.social_media_login_id,self.social_type)
    
    
        
    

    
    
    