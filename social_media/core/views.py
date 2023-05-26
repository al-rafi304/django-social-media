from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Post, Comment, Follow, Like

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        posts = Post.objects.all().order_by('-posted_at')
        post_element = []

        for post in posts:
            comments = Comment.objects.filter(post = post).order_by('-commented_at')
            liked = True if Like.objects.filter(post=post, account=request.user).exists() else False
            temp = {
                'post': post,
                'comments': comments if len(comments) > 0 else None,
                'liked': liked
            }
            post_element.append(temp)
        return render(request, 'core/home.html', {
            'post_element': post_element,
        })

def post(request):
        if request.method == 'POST':
            post_text = request.POST['post-text']
            post = Post()
            post.text = post_text
            post.account = request.user
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