from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField()
    juman = models.TextField()  
    knp = models.TextField()  
<<<<<<< HEAD
    answer = models.TextField()  
    match  = models.TextField()  
=======
>>>>>>> 0b7709c2468b7a7dc0871da89016190f7722dd34
