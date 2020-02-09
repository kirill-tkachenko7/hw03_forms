from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Group


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

