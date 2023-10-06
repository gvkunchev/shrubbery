##
## These views are abstract. Inherit them and
## set the class properties as needed.
##

from django.views import View
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher


class AddComment(View):
    # Set these when inheriting.
    HOST = 'Model of the object holding the comment - e.g. Forum, Homework'
    FORM = 'Form for the comment model in the context of the host - e.g. ForumCommentForm. HomeworkCommentForm'
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        try:
            self.HOST.objects.get(pk=kwargs.get(self.HOST_KEY))
        except ObjectDoesNotExist:
            return redirect('missing')
        data = {
            'content': request.POST.get('content'),
            'line': request.POST.get('line'),
            'author': request.user
        }
        data.update(kwargs)
        form = self.FORM(data)
        if form.is_valid():
            comment = form.save()
        if 'inlinecomment' in request.path:
            redirect_path = request.path.replace('/inlinecomment/add', '')
            return redirect(f'{redirect_path}#inlinecomment{comment.pk}')
        else:
            redirect_path = request.path.replace('/comment/add', '')
            return redirect(f'{redirect_path}#comment{comment.pk}')


class EditComment(View):
    # Set these when inheriting.
    HOST = 'Model of the object holding the comment - e.g. Forum, Homework'
    FORM = 'Form for the comment model in the context of the host - e.g. ForumCommentForm. HomeworkCommentForm'
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'
    TEMPLATE = 'Template for parsing the result - e.g. forums/edit_forum_comment.html'

    def get_comment_from_link(self, request, comment, **kwargs):
        """Validate that the host exists and user can change it and return the comment."""
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        if not (request.user.is_teacher or comment.author.pk == request.user.pk):
            return redirect('missing')
        return comment

    @method_decorator(login_required)
    def post(self, request, comment, **kwargs):
        comment = self.get_comment_from_link(request, comment)
        data = {
            'content': request.POST.get('content'),
            'line': request.POST.get('line'),
            'parent': request.POST.get('parent'),
            'author': comment.author
        }
        data.update(kwargs)
        form = self.FORM(data, instance=comment)
        if form.is_valid():
            form.save()
            page = request.POST.get('page', '')
            if 'inlinecomment' in request.path:
                redirect_path = request.path.replace(f'/inlinecomment/{comment.pk}/edit', '')
                return redirect(f'{redirect_path}?page={page}#inlinecomment{comment.pk}')
            else:
                redirect_path = request.path.replace(f'/comment/{comment.pk}/edit', '')
                return redirect(f'{redirect_path}?page={page}#comment{comment.pk}')
        else:
            context = {
                'comment': comment,
                'errors': form.errors
            }
            return render(request, self.TEMPLATE, context)

    @method_decorator(login_required)
    def get(self, request, comment, **kwargs):
        comment = self.get_comment_from_link(request, comment)
        return render(request, self.TEMPLATE, {'comment': comment})


class DeleteComment(View):
    # Set these when inheriting.
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'

    @method_decorator(is_teacher)
    def get(self, request, comment, **kwargs):
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        comment_pk = comment.pk
        comment.delete()
        if 'inlinecomment' in request.path:
            redirect_path = request.path.replace(f'/inlinecomment/{comment_pk}/delete', '')
        else:
            redirect_path = request.path.replace(f'/comment/{comment_pk}/delete', '')
        return redirect(redirect_path)


class SetCommentStar(View):
    # Set these when inheriting.
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'
    STATUS = 'Boolean for adding/removing the star'

    @method_decorator(is_teacher)
    def get(self, request, comment, **kwargs):
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        comment.starred = self.STATUS
        comment.save()
        page = request.GET.get('page', '')
        redirect_path = request.path.replace(f'/comment/{comment.pk}/star/add', '')
        redirect_path = redirect_path.replace(f'/comment/{comment.pk}/star/remove', '')
        return redirect(f'{redirect_path}?page={page}#comment{comment.pk}')
