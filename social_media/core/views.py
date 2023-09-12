from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string
from django.http import JsonResponse


from .models import Post, Comment, Follow, Like, CommentLike, Account

def getPostElement(request, given_posts=None, account_id=None):
    following = Follow.objects.filter(follower = request.user).values('account').values_list('account', flat=True)
    if account_id == None:
        posts = Post.objects.filter(
            # Public Posts | Following only post and user is following | Post are of users
            Q(privacy=Post.EVERYONE) | (Q(privacy=Post.FOLLOWERS) & Q(account__in = following)) | Q(account=request.user)
            ).order_by('-posted_at')
    else:
        posts = Post.objects.filter(
            # All Posts of account_id & (Public Posts | Following only post and user is following | Posts are of users)
            Q(account=Account.objects.get(id=account_id)) & (Q(privacy=Post.EVERYONE) | (Q(privacy=Post.FOLLOWERS) & Q(account__in = following)) | Q(account=request.user))
            ).order_by('-posted_at')
        
    # If a list of posts has been provided, it will only return those posts with correct filtering
    if given_posts != None:
        posts = [post for post in posts if post in given_posts]
    

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

    return post_element

def homePage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        post_element = getPostElement(request)

        return render(request, 'core/home.html', {
            'post_element': post_element,
            'privacy_options': {'everyone': Post.EVERYONE, 'followers': Post.FOLLOWERS}
        })

def profilePage(request, account_id):

    post_element = getPostElement(request, account_id=account_id)
    # print(post_element)

    return render(request, 'core/profile.html', {
        'account': Account.objects.get(id=account_id),
        'post_element': post_element,
        'privacy_options': {'everyone': Post.EVERYONE, 'followers': Post.FOLLOWERS},
        'following_info': Follow.objects.filter(follower=request.user, account = Account.objects.get(id=account_id))
    })

@login_required
def post(request):
        if request.method == 'POST':
            post_text = request.POST['post-text']
            post_photo = request.FILES.get('post-photo')
            post_video = request.FILES.get('post-video')
            post_privacy = request.POST['post-privacy']
            post = Post()
            post.text = post_text
            post.account = request.user
            post.privacy = post_privacy
            post.photo = post_photo
            post.video = post_video
            post.save()
            messages.success(request, 'Your post has been submitted!')

            print(post_privacy, post.privacy)

            # YOU NEED TO PASS 'request', otherwise csrf_token won't be present
            post_HTML = render_to_string('core/elements/postContainer.html', {
                    'element': {
                        'post': post,
                        'comment_element': None,
                        'liked': False
                    },
                },
                request=request
            )

        return JsonResponse({
            'post_HTML': post_HTML
        })

@login_required
def removePost(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.delete()

        return JsonResponse({})

@login_required
def sharePost(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        
        new_post = Post()
        new_post.account = request.user
        new_post.text = request.POST['share-text']
        
        # If 'post' is an original post
        if post.shared_post == None:
            new_post.shared_post = post

        # If 'post' is already sharing a post
        else:
            original_post = Post.objects.get(id=post.shared_post.id)
            new_post.shared_post = original_post
            original_post.shareCount += 1
            original_post.save()
        
        post.shareCount += 1

        post.save()
        new_post.save()
        messages.success(request, 'You have shared a post')
        
        post_HTML = render_to_string('core/elements/postContainer.html', {
                    'element': {
                        'post': new_post,
                        'comment_element': None,
                        'liked': False
                    },
                },
                request=request
            )

    return JsonResponse({
        'post_HTML': post_HTML,
        'shareCount': post.shareCount
    })

@login_required
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

        # Works like render() but render_to_string() returns it in a string format instead of an http response
        comment_HTML = render_to_string('core/elements/commentElement.html', {
                'comment_element': {
                    'comment': comment,
                    'liked': False
                }
            },
            request=request
        )

    # Using jsonResponse for accessing the comment_HTML in jQuery
    return JsonResponse({
        'comment_HTML': comment_HTML,
        'commentCount': post.commentCount
    })

@login_required
def like(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if Like.objects.filter(post=post_id, account=request.user).exists() == False:       # Have to use filter instead of get to use exists()
            like = Like()
            like.account = request.user
            like.post = post
            like.save()

            post.likeCount += 1
            liked = True
        else:
            like = Like.objects.get(post=post_id, account=request.user)
            like.delete()
            post.likeCount -= 1
            liked = False
        post.save()
    return JsonResponse({
        'liked': liked,
        'likeCount': post.likeCount
    })

@login_required
def commentLike(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if CommentLike.objects.filter(comment=comment, account=request.user).exists() == False:
            like = CommentLike()
            like.comment = comment
            like.account = request.user
            like.save()
            comment.likeCount += 1
            liked = True

        else:
            like = CommentLike.objects.get(comment=comment, account=request.user)
            like.delete()
            comment.likeCount -= 1
            liked = False

        comment.save()
    return JsonResponse({
        'liked': liked,
        'likeCount': comment.likeCount
    })

@login_required
def followButton(request):
    if request.method == "POST":
        following = Account.objects.get(id=request.POST['account-id'])
        user = Account.objects.get(id=request.user.id)

        # Unfollow
        if Follow.objects.filter(follower=request.user, account=following).exists():
            followObj = Follow.objects.get(follower=request.user, account=following)
            followObj.delete()

            user.followingCount -= 1
            following.followerCount -= 1

        # Follow
        else:
            followObj = Follow()
            followObj.follower = request.user
            followObj.account = following
            followObj.save()

            user.followingCount += 1
            following.followerCount += 1

        user.save()
        following.save()

    return redirect('profile', account_id=request.POST['account-id'])

def search(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            query = request.GET.get('search')

            if query == None:
                raise Http404("You didn't search anything dummy !")
            
            posts = Post.objects.filter(text__contains = query)
            accounts = Account.objects.filter(
                Q(first_name__contains = query) | Q(username__contains = query)
            )
            
            account_element = []
            for account in accounts:
                temp = {
                    'account': account,
                    'isFollowing': Follow.objects.filter(account=account, follower=request.user).exists()
                }
                account_element.append(temp)

    return render(request, 'core/searchPage.html', {
        'account_elements': account_element,
        'post_element': getPostElement(request, posts),
    })

def postPage(request, post_id):
    post = Post.objects.filter(id=post_id)
    element = getPostElement(request, given_posts=post)
    print(element)
    return render(request, 'core/postPage.html', {
        'elements': element
    })