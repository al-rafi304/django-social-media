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
            temp = {
                'post': post,
                'comments': comments if len(comments) > 0 else None,
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
        comment_text = request.POST['comment-text']

        comment = Comment()
        comment.account = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.comment = comment_text
        comment.save()
    return redirect('home')