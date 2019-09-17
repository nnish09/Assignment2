from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from .validators import validate_file_extension,validate_file_extension1
from .signals import *
from datetime import datetime,timedelta   
from django.utils import timezone

class User(AbstractUser):


    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
    )

    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=1)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    profimg = models.ImageField(upload_to='images/',default='images/about.jpg',validators=[validate_file_extension])
    address = models.CharField(max_length=30, blank=True)

    # role = models.ForeignKey(Role, on_delete=models.CASCADE,default='student')

    def __str__(self):
        return self.username



def get_deadline():
    return datetime.today() + timedelta(days=5)

class Assignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='student')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='teacher')
    assignment = models.FileField(upload_to='documents/',null=True,validators=[validate_file_extension1])
    title=models.CharField(max_length=300)
    submission_date = models.DateTimeField(default=get_deadline, blank=True)
    uploaded_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.title



class Submission(models.Model):
    sub_student = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='sub_student')
    sub_teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='sub_teacher')
    tea_assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE,null=True)
    submitted_assignment = models.FileField(upload_to='documents/',null=True,validators=[validate_file_extension1])
    sub_title=models.CharField(max_length=300)
    submitted_at = models.DateTimeField(default=datetime.now(), blank=True)
    def __str__(self):
        return self.title


class AssignRequest(models.Model):
  req_student = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='req_student')
  req_teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='req_teacher')
  requested=models.BooleanField(default=True)


class Review(models.Model):
  REVIEW_TYPE_CHOICES = (
      ('1 star', '1 star'),
      ('1.5 star', '1.5 star'),
      ('2 star', '2 star'),
      ('2.5 star', '2.5 star'),
      ('3 star', '3 star'),
      ('3.5 star', '3.5 star'),
      ('4 star', '4 star'),
      ('4.5 star', '4.5 star'),
      ('5 star', '5 star'),
    )
  review_student = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='review_student')
  review_teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='review_teacher')
  review_assignment=models.ForeignKey(Submission,on_delete=models.CASCADE,null=True)
  review_stars=models.CharField(choices=REVIEW_TYPE_CHOICES,default='3 star',max_length=20)
  def __str__(self):
      return self.review_student


