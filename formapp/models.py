from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField()
    juman = models.TextField()  
    knp = models.TextField()  
    answer = models.TextField()  
    match  = models.TextField()  
