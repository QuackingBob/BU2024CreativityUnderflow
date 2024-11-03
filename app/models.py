from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField() # if rendered latex
    img_content = models.ImageField(default=None, upload_to='media/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.title