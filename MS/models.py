from django.db import models

# Create your models here.
class TempFile(models.Model):
    name = models.CharField(max_length=100, null=False)
    path = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name