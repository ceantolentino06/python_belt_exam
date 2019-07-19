from django.db import models
from django.contrib import messages
import re
from datetime import datetime, date
from multiselectfield import MultiSelectField

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        onlyLetters_REGEX = re.compile("^[a-zA-Z]+$")
        email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        result = User.objects.filter(email=postData['email'])
        
        ############# FIRST NAME VALIDATIONS #############
        if len(postData['fname']) > 2:
            if not onlyLetters_REGEX.match(postData['fname']):
                errors['fname'] = 'First name should contain letters only'
        else:
            errors['fname'] = 'First name should be at least 2 characters'

        ############# LAST NAME VALIDATIONS #############
        if len(postData['lname']) > 2:
            if not onlyLetters_REGEX.match(postData['lname']):
                errors['lname'] = 'Last name should contain letters only'
        else:
            errors['lname'] = 'Last name should be at least 2 characters'

        ############# BIRTHDAY VALIDATIONS ############# 
        if datetime.strptime(postData['bday'], '%Y-%m-%d') > datetime.today():
            errors['bday'] = "Birthday must be a valid date"
        else:
            today = date.today().year
            bday = datetime.strptime(postData['bday'], '%Y-%m-%d').year
            if (today-bday) < 13:
                errors['bday'] = "Must be at least 13 years old to be eligible to register"
        ############# EMAIL VALIDATIONS #############
        if len(postData['email']) > 2:
            if not email_REGEX.match(postData['email']):
                errors['email'] = 'Please enter a valid email'
            else:
                if len(result) > 0:
                    errors['email'] = 'This email is already registered'
        else:
            errors['email'] = 'Email should be at least 2 characters'

        ############# PASSWORD VALIDATIONS #############
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        ############# CONFIRM PASSWORD VALIDATIONS #############
        if postData['password'] != postData['confirmpw']:
            errors['confirmpw'] = 'Password does not match'

        return errors


class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}

        if len(postData['title']) < 3:
            errors['title'] = 'Title should be at least 3 characters'
        if len(postData['desc']) < 3:
            errors['desc'] = 'Description should be at least 3 characters'
        if len(postData['location']) < 3:
            errors['location'] = 'Location should be at least 3 characters'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="jobs_created")
    users_who_added = models.ManyToManyField(User, related_name="my_jobs")
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

