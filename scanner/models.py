from django.db import models
from django.contrib.auth.models import User

class ScanResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.CharField(max_length=255)
    port = models.IntegerField()
    service = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)