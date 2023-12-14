from django.db import models

# Create your models here. DONE:

class Route(models.Model):
    dep = models.CharField(max_length=200)
    dest = models.CharField(max_length=200)

    def __str__(self):
        return self.dep + '-' + self.dest
