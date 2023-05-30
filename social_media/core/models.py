from django.db import models

from accounts.models import Account

# Like/comment of a deleted account will also be counted even though they don't exist

class Follow(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followed_accounts')
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followers')

    """  
    ---------------------------ChatGPT-------------------------------
    the related_name argument specifies the reverse relation names for
    the foreign key relationships. The related_name='followed_accounts'
    sets the reverse relation name for the account field,
    while related_name='followers' sets it for the follower field.
    These unique related_name values prevent the clash
    and allow you to access the relationships without conflicts.
    """

    followed_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    
    text = models.TextField()
    likeCount = models.IntegerField(default = 0)
    commentCount = models.IntegerField(default = 0)
    shareCount = models.IntegerField(default=0)

    photo = models.ImageField(upload_to='post_pics/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    shared_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)       # Recursive relation

    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.text[:50]}..."

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)

    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"'{self.post.text[:15]}...' liked by {self.account.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    
    comment = models.TextField()
    likeCount = models.IntegerField(default = 0)

    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"'{self.comment[:50]}...' commented by '{self.account.username}' on '{self.post.text[:15]}..'"
    
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)

    liked_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f"'{self.comment.comment[:15]}...' liked by {self.account.username}"



