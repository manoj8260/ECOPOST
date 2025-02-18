from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    phno=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to='profile_pic/')
    bio=models.TextField(max_length=500,null=True,blank=True)
    gender=models.CharField(max_length=20,null=True,blank=True)
    website=models.CharField(max_length=250,default='https://www.linkedin.com/in/manoj-nayak-0222b1229/')

    def __str__(self) :
        return self.username.username
class Tweet(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True, blank=True,default=None)
    text=models.TextField()
    photo=models.ImageField(upload_to='tweet_photo/')
    created_at=models.DateField(auto_now_add=True)
    like=models.IntegerField(default=0)
    created_at=models.DateTimeField(null=True,auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    save_comment=models.IntegerField(default=0)

    def __str__(self) :
        return f' {self.username.username} {self.text[:10]}'

class Saved(models.Model):
     username=models.ForeignKey(User,on_delete=models.CASCADE)
     tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE)

     def __str__(self) -> str:
         return f"user '{self.username.username}' saved the tweet of '{self.tweet.username.username}' "
class Liked(models.Model):
     username=models.ForeignKey(User,on_delete=models.CASCADE)
     tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE)

     def __str__(self) :
         return f"user '{self.username.username}' liked the tweet of '{self.tweet.username.username}' "
     
class Comment(models.Model):
      username=models.ForeignKey(User,on_delete=models.CASCADE)
      tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name='comments')
      comment_text=models.TextField()
      comment_time=models.DateTimeField(auto_now_add=True)

      def __str__(self) -> str:
          return f"user '{self.username.username}' comment the tweet of '{self.tweet.username.username} {self.comment_text}' "



class Story(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile')
    video = models.FileField(upload_to='storyvideos/')  
    uploaded_at = models.DateTimeField(default=timezone.now) 

     
    def __str__(self):
        return f"{self.username} - {self.uploaded_at}"

class Explore(models.Model):
    photo=models.ImageField(upload_to='Explore/photo/',blank=True, null=True,default='Explore/photo/default_image.jpg')
    photo_desc=models.CharField(max_length=250,blank=True, null=True)
    video=models.FileField(upload_to='Explore/video/',blank=True, null=True,default='Explore/video/default_video2.mp4')  
    video_desc=models.CharField(max_length=250,blank=True, null=True)
   

    def __str__(self):
        return self.photo_desc


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]
        db_table='user_follow_table'

    def __str__(self):
        return f"{self.follower} follows {self.following}"

