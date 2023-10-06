from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from .models import Forum, ForumComment
from .forms import ForumForm, ForumCommentForm

from comments.views import AddComment, EditComment, DeleteComment, SetCommentStar


def forums(request):
    '''Forums page.'''
    return render(request, "forums/forums.html", {'forums': Forum.objects.all()})


def forum(request, forum):
    '''Forum article page.'''
    try:
        forum = Forum.objects.get(pk=forum)
        main_comments = forum.comments.filter(parent=None)
        paginator = Paginator(main_comments, 10)
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
def answer_forum_comment(request, forum, parent):
    '''Answer forum comment in a thread.'''
    try:
        forum = Forum.objects.get(pk=forum)
        parent = ForumComment.objects.get(pk=parent)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'forum': forum,
            'content': request.POST.get('content'),
            'parent': parent,
            'author': request.user
        }
        form = ForumCommentForm(data)
        if form.is_valid():
            comment = form.save()
            return redirect(f"/forum/{forum.pk}?page={request.POST.get('page')}#comment{comment.pk}")
        else:
            return render(request, "forums/answer_forum_comment.html", {'forum': forum,
                                                                        'parent': parent,
                                                                        'errors': form.errors})
    else:
        return render(request, "forums/answer_forum_comment.html", {'forum': forum, 'parent': parent})


class AddForumComment(AddComment):
    HOST = Forum
    FORM = ForumCommentForm
    HOST_KEY = 'forum'


class EditForumComment(EditComment):
    HOST = Forum
    FORM = ForumCommentForm
    HOST_KEY = 'forum'
    COMMENT_MODEL = ForumComment
    TEMPLATE = 'forums/edit_forum_comment.html'


class DeleteForumComment(DeleteComment):
    HOST_KEY = 'forum'
    COMMENT_MODEL = ForumComment


class AddForumCommentStar(SetCommentStar):
    HOST_KEY = 'forum'
    COMMENT_MODEL = ForumComment
    STATUS = True


class RemoveForumCommentStar(SetCommentStar):
    HOST_KEY = 'forum'
    COMMENT_MODEL = ForumComment
    STATUS = False
