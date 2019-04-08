from django.db import models
from django.utils import timezone
from django.db.models import signals
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.

DEFAULT = datetime.strptime('Jun 1 2030  1:33PM', '%b %d %Y %I:%M%p')

#DEFAULT = '2150-10-25'
class Post(models.Model):
	id_post = models.IntegerField()
	#time_create = models.DateTimeField(auto_now_add = True)
	time_create = models.DateTimeField()
	time_death = models.DateTimeField(default = DEFAULT)
	row1  = models.CharField(max_length = 50)
	row2 = models.TextField()
	deleted = models.BooleanField(default = False)
	def __str__(self):
		return self.row1
	
	

class Journal(models.Model):
	id_jp = models.IntegerField() 
	#OPS = (('INSERT', 'INSERT'), ('UPDATE', 'UPDATE'), ('DELETE','DELETE'))
	time = models.DateTimeField()
	operation = models.CharField(default = "INSERT", max_length = 50)
	deleted = models.BooleanField(default = False)
	def __str__(self):
		return self.operation


