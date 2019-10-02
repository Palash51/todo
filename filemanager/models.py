import random

from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    """
    Model holding the details of users
    """
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    mobile = models.CharField(max_length=13, verbose_name="Mobile Number", null=True, unique=True)
    address = models.CharField(max_length=400, verbose_name="Address", null=True, blank=True)
    city = models.CharField(max_length=30, verbose_name="City", null=True, blank=True)
    zipcode = models.CharField(max_length=30, verbose_name="Zipcode", null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name="Country", null=True, blank=True)
    profile_image = models.CharField(null=True, blank=True, max_length=500)
    gender = models.CharField(
        max_length=1,
        choices=(('M', "Male"), ('F', "Female"), ('B', "Non-Binary")),
        verbose_name="Gender", null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)

    def __str__(self):
        return self.email



class ToDoList(models.Model):
    """
    Model to have user's todolist details.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, max_length=200)
    unique_url = models.CharField(unique=True, null=True, blank=True, max_length=2000)
    description = models.CharField(null=True, blank=True, max_length=1000)
    make_public = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8, null=True, blank=True
    )

    def get_unique_url(self):
        code_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        url = ''
        for i in range(0, 12):
            slice_start = random.randint(0, len(code_chars) - 1)
            url += code_chars[slice_start: slice_start + 1]

        url = 'todolist.'  + url + '.shareit'

        check_code = ToDoList.objects.filter(unique_url=url)
        if check_code:
            self.get_unique_url()

        return url



class Item(models.Model):
    """
    List of itmes or subtask's
    """
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=250)
    task = models.CharField(null=True, blank=True, max_length=2500)
    mark_done = models.BooleanField(default=False)