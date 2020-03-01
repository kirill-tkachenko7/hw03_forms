from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    """ display latest posts """
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # display 10 posts per page

    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) # retreive posts with correct offset
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    """ display latest posts in the group """

    # get group object using a slug passed in the URL
    group = get_object_or_404(Group, slug=slug)

    # show 10 posts per page
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'group.html', {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    """display a form for adding a new post to authenticated users"""
    if request.method == 'POST':
        # if we got a POST request, validate form
        form = PostForm(request.POST)
        if form.is_valid():
            # if form is valid, populate missing data and save a post
            # all validation is done at the model level
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # redirect user to the home page
            return redirect('index')
        # if form is not valid, display the same form and show validation errors
        return render(request, 'new_post.html', {'form': form})
    # if this is not a POST request, display a blank PostForm
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    """ profile information and user's latest posts """
    profile_user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author__username=username).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # display 10 posts per page

    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) # retreive posts with correct offset
    context_dict =  {
        'profile_user': profile_user,
        'post_count': post_list.count(),
        'page': page, 
        'paginator': paginator
    }
    return render(request, 'profile.html', context_dict)


def post_view(request, username, post_id):
    # тут тело функции
    return render(request, "post.html", {})

@login_required
def post_edit(request, username, post_id):
    # return 404 if User with username does not exist, if Post with 
    # post_id does not exist or if username is not the author of the Post.
    post_object = get_object_or_404(Post, id=post_id, author__username=username)

    # only post author can edit post
    if request.user.username != username:
        raise PermissionDenied("Редактировать публикацию может только ее автор")
    
    # TODO the rest of the function
    # тут тело функции. Не забудьте проверить, 
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    return render(request, "new_post.html", {})