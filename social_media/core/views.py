from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Post, Comment, Follow, Like, CommentLike

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        posts = Post.objects.all().order_by('-posted_at')
        post_element = []

        for post in posts:
            comments = Comment.objects.filter(post = post).order_by('-commented_at')
            liked = True if Like.objects.filter(post=post, account=request.user).exists() else False

            comment_element = []
            for comment in comments:
                temp = {
                    'comment': comment,
                    'liked': True if CommentLike.objects.filter(comment=comment, account=request.user).exists() else False
                }
                comment_element.append(temp)

            temp = {
                'post': post,
                'comment_element': comment_element if len(comment_element) > 0 else None,
                'liked': liked
            }
            post_element.append(temp)

        return render(request, 'core/home.html', {
            'post_element': post_element,
        })

def post(request):
        if request.method == 'POST':
            post_text = request.POST['post-text']
            post_photo = request.FILES.get('post-photo')
            post_video = request.FILES.get('post-video')
            post = Post()
            post.text = post_text
            post.account = request.user
            post.photo = post_photo
            post.video = post_video
            post.save()
            messages.success(request, 'Your post has been submitted!')

        return redirect('home')

def comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)

        comment_text = request.POST['comment-text']

        comment = Comment()
        comment.account = request.user
        comment.post = post
        comment.comment = comment_text
        comment.save()

        post.commentCount += 1
        post.save()
    return redirect('home')

def like(request, post_id):
    post = Post.objects.get(id=post_id)
    if Like.objects.filter(post=post_id, account=request.user).exists() == False:       # Have to use filter instead of get to use exists()
        like = Like()
        like.account = request.user
        like.post = post
        like.save()

        post.likeCount += 1
    else:
        like = Like.objects.get(post=post_id, account=request.user)
        like.delete()
        post.likeCount -= 1
    
    post.save()
    return redirect('home')

def commentLike(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if CommentLike.objects.filter(comment=comment, account=request.user).exists() == False:
        like = CommentLike()
        like.comment = comment
        like.account = request.user
        like.save()
        comment.likeCount += 1
    else:
        like = CommentLike.objects.get(comment=comment, account=request.user)
        like.delete()
        comment.likeCount -= 1
    
    comment.save()
    return redirect('home')