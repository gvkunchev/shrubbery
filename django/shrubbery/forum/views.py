from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from .models import Forum, ForumComment
from .forms import ForumForm, ForumCommentForm


def forums(request):
    '''Forums page.'''
    return render(request, "forums/forums.html", {'forums': Forum.objects.all()})


def forum(request, forum):
    '''Forum article page.'''
    try:
        forum = Forum.objects.get(pk=forum)
        paginator = Paginator(forum.comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "forums/forum.html", {'forum': forum, 'comments': page_obj})


@login_required
def add_forum(request):
    '''Add new forum.'''
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = ForumForm(data)
        if form.is_valid():
            forum = form.save()
            return redirect(f'/forum/{forum.pk}')
        else:
            context = {
                'errors': form.errors
            }
            return render(request, "forums/add_forum.html", context)
    else:
        return render(request, "forums/add_forum.html")


@is_teacher
def delete_forum(request, forum):
    '''Delete forum.'''
    try:
        forum = Forum.objects.get(pk=forum)
    except ObjectDoesNotExist:
        return redirect('missing')
    forum.delete()
    return redirect('forum:forums')


@is_teacher
def edit_forum(request, forum):
    '''Edit forum.'''
    try:
        forum = Forum.objects.get(pk=forum)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = ForumForm(data, instance=forum)
        if form.is_valid():
            form.save()
            return redirect(f'/forum/{forum.pk}')
        else:
            context = {
                'forum': forum,
                'errors': form.errors
            }
            return render(request, "forums/edit_forum.html", context)
    else:
        return render(request, "forums/edit_forum.html", {'forum': forum})


@login_required
def add_forum_comment(request):
    '''Add forum comment.'''
    if request.method != 'POST':
            return redirect('missing')
    try:
        forum = Forum.objects.get(pk=request.POST.get('forum'))
    except ObjectDoesNotExist:
            return redirect('missing')
    data = {
        'content': request.POST.get('content'),
        'forum': request.POST.get('forum'),
        'author': request.user
    }
    form = ForumCommentForm(data)
    if form.is_valid():
        comment = form.save()
    return redirect(f'/forum/{forum.pk}#comment{comment.pk}')


@login_required
def edit_forum_comment(request, comment):
    '''Edit forum comment.'''
    try:
        comment = ForumComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    if not (request.user.is_teacher or comment.author.pk == request.user.pk):
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'forum': comment.forum,
            'content': request.POST.get('content'),
            'author': comment.author
        }
        form = ForumCommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            page = request.POST.get('page', '')
            return redirect(f'/forum/{comment.forum.pk}?page={page}#comment{comment.pk}')
        else:
            context = {
                'comment': comment,
                'errors': form.errors
            }
            return render(request, "forums/edit_forum_comment.html", context)
    else:
        return render(request, "forums/edit_forum_comment.html", {'comment': comment})


@is_teacher
def delete_forum_comment(request, comment):
    '''Delete forum.'''
    try:
        comment = ForumComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    forum = comment.forum
    comment.delete()
    return redirect(f'/forum/{forum.pk}')


# Helper for the below two
@is_teacher
def set_forum_comment_star(request, comment, status):
    '''Set a star to a forum comment.'''
    try:
        comment = ForumComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    comment.starred = status
    comment.save()
    page = request.GET.get('page', '')
    return redirect(f'/forum/{comment.forum.pk}?page={page}#comment{comment.pk}')

@is_teacher
def add_forum_comment_star(request, comment):
    '''Add star to a forum comment.'''
    return set_forum_comment_star(request, comment, True)

@is_teacher
def remove_forum_comment_star(request, comment):
    '''Remove a star from a forum comment.'''
    return set_forum_comment_star(request, comment, False)
