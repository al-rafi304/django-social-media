from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Post

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        posts = Post.objects.all().order_by('-posted_at')

        if request.method == 'POST':
            post_text = request.POST['post-text']
            post = Post()
            post.text = post_text
            post.account = request.user
            post.save()

            messages.success(request, 'Your post has been submitted!')

        return render(request, 'core/home.html', {
            'posts': posts,
        })
