

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class EncryptedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    file = models.FileField(upload_to="encrypted_files/")
    
    encrypted_key = models.BinaryField()
    iv = models.BinaryField()
   
    
    original_filename = models.CharField(max_length=255)
    size = models.BigIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_filename} ({self.user.username}) {self.id}"
