from django.db import models

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    data_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
