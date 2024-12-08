from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model): 

    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name= "owner")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)  # Number of likes, default is 0

    def __str__(self):
        return f"{self.owner.username}'s post on {self.created_date}"
     