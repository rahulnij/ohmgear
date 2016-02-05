from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django_pgjson.fields import JsonField
import datetime
from datetime import timedelta
from django.utils.html import format_html


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
#        if not first_name:
#            raise ValueError('first_name required')        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.user_type = UserType.objects.get(id=1)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None,**extra_fields):
        return self._create_user(email, password,**extra_fields)

    def create_superuser(self, email, password=None,**extra_fields):
        return self._create_user(email, password,**extra_fields)

#------------------ Look up Table -------------------#          

class BusinessType(models.Model):
    class Meta:
        db_table = 'ohmgear_users_businesstype'
    business_type_id = models.AutoField(primary_key=True)
    business_type   = models.CharField(_('Business Type'),max_length=50,null=True)
    
    def __unicode__(self):
        return'{"business_type_id":"%s","business_type":"%s"}'%(self.business_type_id,self.business_type)
    
    
    
class IncomeGroup(models.Model):
    class Meta:
        db_table = 'ohmgear_users_incomegroup'
    income_group_id = models.AutoField(primary_key=True)
    income_group    = models.CharField(_('Income Group'),max_length=50,null =True)
    
    def __unicode__(self):
        return'{"income_group_id":"%s","income_group":"%s"}'%(self.income_group_id,self.income_group)
    
    
class SocialType(models.Model):
    class Meta:
         db_table = 'ohmgear_users_socialtype'
    social_type    = models.CharField(_('Social Type'), max_length=50,null=True)
    
    def __unicode__(self):
        return'{"id":"%s","social_type":"%s"}'%(self.id,self.social_type)
    
class UserType(models.Model):
    class Meta:
        db_table = 'ohmgear_users_usertype'
        app_label = 'users'
    user_type = models.CharField(_('User Type'),max_length =50)
    
    def __unicode__(self):
       # return '{"id":"%s","user_type":"%s"}'%(self.id,self.user_type)
       return (self.user_type)

#----------------------- End -----------------------------------------------------------------#    

class User(AbstractBaseUser):

    class Meta:
        db_table = 'ohmgear_users_user'
        unique_together = ('email', 'user_type',)
    account_number = models.CharField(_("Account Number"),max_length=45,null=True)
#    first_name = models.CharField(_("First Name"),max_length=45)
#    last_name = models.CharField(_("Last Name"),max_length=45,null=True)    
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
   
    email_verification_code = models.CharField(_("Email Verification"),max_length=45,null=True)
    user_type = models.ForeignKey(UserType,null= True)
    pin_number = models.IntegerField(_("Pin Number"),default=0)
    status = models.IntegerField(_("Status"),default=0)    
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    objects = CustomUserManager()

    update_password =  True
    update_email = True
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return '{"id":"%s","email":"%s","user_type":"%s","status":"%s","pin_number":"%s"}' %(self.id,self.email,self.user_type,self.status,self.pin_number)

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
    
    @property
    def _disable_signals(self):
        return self.status
    
    #Overriding
    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        if self.password and self.update_password:
           self.set_password(self.password)           
        super(User, self).save(*args, **kwargs)    
    


    
               
class Profile(models.Model):
    class Meta:
        db_table = 'ohmgear_users_profile'
    
    first_name = models.CharField(_("First Name"),max_length=45)
    last_name = models.CharField(_("Last Name"),max_length=45,null=True)
    nick_name = models.CharField(_("Nick Name"),max_length=45,null=True)
    headline  = models.CharField(_("Headline"),max_length=80,null=True)
    dob = models.DateField(_("DOB"),null=True)
    gender = models.CharField(_("Gender"),null =True,max_length= 10) 
    address = models.CharField(_("Address"),max_length=80,null=True)
    mobile_number = models.CharField(_("Mobile Number"),max_length=10,null=True)   
    custom_data = JsonField(null=True)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)    
    user = models.OneToOneField(User,null=True,related_name="user_profile")
    income_group = models.ForeignKey(IncomeGroup, null=True, blank=True)
    business_type = models.ForeignKey(BusinessType,null= True)
    profile_image = models.ImageField(_("Profile Image"),upload_to='uploads/profile_img/', max_length=254,blank=True,null=True)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now_add=True)
    #------------ field for forgot passoword ---------------------#
    reset_password_key = models.CharField(max_length=40,null= True)
    #------------ field for first time login ---------------------#
    first_time_login  = models.BooleanField(default=True)
    #------------- End -------------------------------------------#
    def __unicode__(self):
        return '{"id":"%s","dob":"%s","gender":"%s","address":"%s","mobile_number":"%s","user":"%s","income_group":"%s","business_type":"%s","first_time_login":"%s","first_name":"%s","last_name":"%s","nick_name":"%s","headline":"%s","profile_image":"%s"}' %(self.id,self.dob,self.gender,self.address,self.mobile_number,self.user,self.income_group,self.business_type,self.first_time_login,self.first_name,self.last_name,self.nick_name,self.headline,self.profile_image)



class SocialLogin(models.Model):
    class Meta:
        db_table = 'ohmgear_users_socialprofile'
    social_media_login_id = models.CharField(_("Social Media Login Id"),null=True,max_length=50)
    social_type = models.ForeignKey(SocialType,null=True)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    user = models.OneToOneField(User,null=True)
    
    def __unicode__(self):
        return '{"id":"%s","social_media_login_id":"%s","social_type":"%s"}' %(self.id,self.social_media_login_id,self.social_type)
    
    
    
class ConnectedAccount(models.Model):
    class Meta:
        
        db_table    =   "ohmgear_users_connectedaccount"
        unique_together = ('user_id', 'social_type_id',)
    user_id            = models.ForeignKey(User,db_column ="user_id")
    social_type_id     =   models.ForeignKey(SocialType,db_column ="social_type_id",related_name="social_type_id")
    created_date    =   models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date    =   models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return '{"id":"%s","social_type_id":"%r", "user_id":"%r"}' %(self.id,self.social_type_id, self.user_id)
    

class UserEmail(models.Model):
    class Meta:
        db_table    =   'ohmgear_users_useremail'
    
    user_id = models.ForeignKey(User,db_column ="user_id")
    email = models.EmailField()
    # default=0, email not verified
    isVerified = models.BooleanField(_("Email Verified"), default=False)
    verification_code = models.CharField(_("Verification Code"),max_length=40,blank=True, null=True)
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date = models.DateTimeField(_("Updated Date"),auto_now=True)

    def __unicode__(self):
        import json
        userEmail = {'user_id': self.user_id.id, "email":self.email,"isVerified":self.isVerified,"request_for_default":self.request_for_default,"verification_code":self.verification_code}
        #"created_date":self.created_date,"updated_date":self.updated_date
        return json.dumps(userEmail)
        #'{"id":"%s","email":"%r"}' %(self.id, self.e_mail)
    
    
    

    

    
    
    
