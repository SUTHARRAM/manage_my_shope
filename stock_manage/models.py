from django.db import models
from django.contrib.auth.models import User
from PIL import Image 

import os

# Create your models here.

def image_rename(instance, filename): 
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    path = os.path.join("stock_manage/static/img/userPics/"+ filename)
    if os.path.exists(path):
        os.remove(path)
    return path


class UserProfile(models.Model):
    '''It is used to customizing the user model'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=image_rename)

    def save(self, *args, **kwargs): 
        super(UserProfile, self).save(*args, **kwargs)
        imag = Image.open(self.picture.path)
        if imag.width > 40 or imag.height > 40: 
            output_size = (40, 40)
            imag.thumbnail(output_size)
            imag.save(self.picture.path)

    def __str__(self):
        return str(self.user)


class Category(models.Model): 
    name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name

class Stock(models.Model):
    ''' It contain details about stock '''
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    received_quantity = models.IntegerField(default='0', blank=True, null=True)
    received_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name + " : " + str(self.quantity)

class StockHistory(models.Model):
    ''' It maintain the history of our database '''
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    received_quantity = models.IntegerField(default='0', blank=True, null=True)
    received_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

    def __str__(self):
        return self.item_name + " : " + str(self.quantity)



