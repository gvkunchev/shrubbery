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
    def post(self, request):
        try:
            host = self.HOST.objects.get(pk=request.POST.get(self.HOST_KEY))
        except ObjectDoesNotExist:
                return redirect('missing')
        data = {
            'content': request.POST.get('content'),
            self.HOST_KEY: request.POST.get(self.HOST_KEY),
            'author': request.user
        }
        form = self.FORM(data)
        if form.is_valid():
            comment = form.save()
        return redirect(f'/{self.HOST_KEY}/{host.pk}#comment{comment.pk}')


class EditComment(View):
    # Set these when inheriting.
    HOST = 'Model of the object holding the comment - e.g. Forum, Homework'
    FORM = 'Form for the comment model in the context of the host - e.g. ForumCommentForm. HomeworkCommentForm'
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'
    TEMPLATE = 'Template for parsing the result - e.g. forums/edit_forum_comment.html'

    def get_comment_from_link(self, request, comment):
        """Validate that the host exists and user can change it and return the comment."""
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        if not (request.user.is_teacher or comment.author.pk == request.user.pk):
            return redirect('missing')
        return comment

    @method_decorator(login_required)
    def post(self, request, comment):
        comment = self.get_comment_from_link(request, comment)
        data = {
            self.HOST_KEY: getattr(comment, self.HOST_KEY),
            'content': request.POST.get('content'),
            'author': comment.author
        }
        form = self.FORM(data, instance=comment)
        if form.is_valid():
            form.save()
            page = request.POST.get('page', '')
            return redirect(f'/{self.HOST_KEY}/{getattr(comment, self.HOST_KEY).pk}?page={page}#comment{comment.pk}')
        else:
            context = {
                'comment': comment,
                'errors': form.errors
            }
            return render(request, self.TEMPLATE, context)

    @method_decorator(login_required)
    def get(self, request, comment):
        comment = self.get_comment_from_link(request, comment)
        return render(request, self.TEMPLATE, {'comment': comment})


class DeleteComment(View):
    # Set these when inheriting.
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'

    @method_decorator(is_teacher)
    def get(self, request, comment):
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        host = getattr(comment, self.HOST_KEY)
        comment.delete()
        return redirect(f'/{self.HOST_KEY}/{host.pk}')
    

class SetCommentStar(View):
    # Set these when inheriting.
    HOST_KEY = 'Key for the host that comes from the url - e.g. forum, homework'
    COMMENT_MODEL = 'Model of the comment - e.g. ForumComment'
    STATUS = 'Boolean for adding/removing the star'

    @method_decorator(is_teacher)
    def get(self, request, comment):
        try:
            comment = self.COMMENT_MODEL.objects.get(pk=comment)
        except ObjectDoesNotExist:
            return redirect('missing')
        comment.starred = self.STATUS
        comment.save()
        page = request.GET.get('page', '')
        return redirect(f'/{self.HOST_KEY}/{getattr(comment, self.HOST_KEY).pk}?page={page}#comment{comment.pk}')
