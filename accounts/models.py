from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.html import format_html
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

# Create your models here.

#this models is for super admin
class MyAccountManager(BaseUserManager):
    #this is for creating a normal user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email), #if the letter is capital it will be small or normalized
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #this is for creating superuser
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        #setting permission as superuser
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


#and this is the account data
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone           = models.CharField(max_length=50)
    profession      = models.CharField(max_length=210, blank=True)
    profile_pic     = models.ImageField(default='userprofile/bugambilaya.jpg', null=True, blank=True, upload_to='userprofile/')
    image_thumbnail = ImageSpecField(source='profile_pic', processors=[ResizeToFill(150, 150)], format = 'JPEG', options = {'quality':60})

    address_line_1 = models.CharField(max_length=51, blank=True)
    address_line_2 = models.CharField(max_length=51, blank=True)
    country = models.CharField(max_length=54, blank=True, default="Philippines")
    state = models.CharField(max_length=54, blank=True)
    city = models.CharField(max_length=54, blank=True)
    zip = models.IntegerField(null=True, blank=True)



    #required when making custom usermodels
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def address(self):
        return f'{self.address_line_1} {self.address_line_2} {self.city} {self.state} {self.country}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
