from django.db import models
from django.contrib.auth.models import User
# pillow not working in django 3.9 use other version
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField()
    owner = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
