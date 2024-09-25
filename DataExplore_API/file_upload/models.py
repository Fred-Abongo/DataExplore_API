from django.db import models

class UploadedFile(models.Model):
    data_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name
