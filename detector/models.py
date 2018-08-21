from datetime import datetime

from django.db import models

# Create your models here.


class FaceDetectionHistory(models.Model):
    name = models.CharField(null=True, max_length=100)
    face_id = models.CharField(null=True, max_length=100)
    created = models.TimeField(default=datetime.now())

    class Meta:
        app_label = 'detector'
