from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        (1,'ADMIN'),
        (2,'AGENCY'),
        (3,'GROWER'),
    )

    user_type = models.CharField(choices= USER, max_length=50,default=1)
    profile_pic = models.ImageField( upload_to="media/profile_pic", height_field=None, width_field=None, max_length=None)

class Country(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class State(models.Model):
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class City(models.Model):
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    # state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    

class Variety(models.Model):
    name = models.CharField(max_length=50)
    yield_per_acre = models.CharField(max_length=50)
    maturity_duration = models.CharField(max_length=50)  #add this
    description = models.TextField()
    variety_image = models.ImageField(null=True,blank=True, upload_to="images/")

    def __str__(self):
        return self.name
    
class Season(models.Model):
    name = models.CharField(max_length=50)
    from_date = models.CharField(max_length=150)
    to_date = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name 

class Crop(models.Model):
    name = models.CharField(max_length=50)
    plant_type = models.CharField(max_length=50)
    soil_type = models.CharField(max_length=50)
    cultivation_type = models.CharField(max_length=50)
    description = models.TextField()
    crop_image = models.ImageField(null=True,blank=True, upload_to="images/")
    maturity_date = models.CharField(max_length=50)
    sowing_date = models.CharField(max_length=50)
    area =  models.CharField(max_length=50)
    variety_id = models.ForeignKey(Variety, on_delete=models.DO_NOTHING)
    season_id = models.ForeignKey(Season, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Grower(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12)
    pan_number = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10)
    address = models.TextField()
    # country = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    state_id = models.ForeignKey(State, on_delete=models.DO_NOTHING, null=True)
    city_id = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    crop_id =models.ForeignKey(Crop, on_delete=models.DO_NOTHING, null=True)

    examination_image =  models.ImageField( upload_to="media/examinationimage", height_field=None, width_field=None, max_length=None)
     
    def __str__(self):
        return self.admin.first_name + " " +self.admin.last_name
    

class Agency(models.Model):
     name = models.CharField(max_length=50)
     address = models.TextField()
     pin = models.CharField(max_length=50)
     establishment = models.CharField(max_length=50)
     gst = models.CharField(max_length=50)
     contact_person = models.CharField(max_length=50)
     tan = models.TextField()
     website = models.CharField(max_length=50)
     mobile_number = models.CharField(max_length=10)
     email =  models.CharField(max_length=50)
     country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
     state_id = models.ForeignKey(State, on_delete=models.DO_NOTHING)
     city_id = models.ForeignKey(City, on_delete=models.DO_NOTHING)
     
     def __str__(self):
         return self.name


class Branch(models.Model):
    # admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.TextField()
    pin = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    state_id = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city_id = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    agency_id =models.ForeignKey(Agency, on_delete=models.DO_NOTHING)
    # grower_id =models.ForeignKey(Grower, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class Field_worker(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    gender = models.TextField()
    dob = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    agency_id = models.ForeignKey(Agency, on_delete=models.DO_NOTHING)
    branch_id = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    grower = models.CharField(max_length=50)

    # grower_id =models.ForeignKey(Grower, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.admin.first_name + " " +self.admin.last_name
    

# from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username





