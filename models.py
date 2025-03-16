from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tweet(models.Model):
    user =models.ForeignKey( User , on_delete=models.CASCADE) 
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/' , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="tweet_likes", blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:30]}'


class comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    photo = models.ImageField(upload_to='comment_photos/', blank=True, null=True)  # Add image field
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Comment by {self.user.username} on Tweet {self.tweet.id}"




   
