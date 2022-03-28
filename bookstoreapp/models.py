from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    pdf = models.FileField(upload_to='media',null=True)
    def __str__(self):
        return self.name