from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth import get_user_model


def index(request):
    """ get 10 latest posts and display them using the index.html template """
    # pylint: disable=no-member
    latest = Post.objects.order_by('-pub_date')[:10]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    """ show 12 latest posts in the group """

    # get group object using a slug passed in the URL
    # pylint: disable=no-member
    group = get_object_or_404(Group, slug=slug)

    # get 12 latest posts in the group
    latest = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, 'group.html', {'group': group, 'posts': latest})


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

