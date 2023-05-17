$(document).ready(function(){

    // Confirmation dialogs for deletion and submitting
    function confirmDeleteSubmit(trigger, modal){
        trigger.click(function(e){
            modal.modal('show');
            e.preventDefault();
        })
        modal.find('.btn-no').bind('click', function(){
            modal.modal('hide');
        })
        modal.find('.btn-yes').bind('click', function(){
            modal.modal('hide');
            var delete_input = $('<input>').attr({
                'type': 'hidden',
                'name': 'delete'
            });
            trigger.parents('form').append(delete_input)
            trigger.parents('form').submit();
        })
    }
    confirmDeleteSubmit($('.confirm-delete-user'), $('#confirm_delete_user_modal'));
    confirmDeleteSubmit($('.confirm-delete-lecture'), $('#confirm_delete_lecture_modal'));


    // Confirmation dialogs for deletion and redirecting
    function confirmDeleteLink(trigger, modal){
        $(trigger).click(function(e){
            $(modal).modal('show');
            e.preventDefault();
        })
        $(modal).find('.btn-no').bind('click', function(){
            $(modal).modal('hide');
        })
        $(modal).find('.btn-yes').bind('click', function(){
            $(modal).modal('hide');
            window.location = $(trigger).attr('href');
        })
    }

    confirmDeleteLink($('.confirm-delete-news-article'), $('#confirm_delete_news_article_modal'));
    confirmDeleteLink($('.confirm-delete-forum'), $('#confirm_delete_forum_modal'));
    confirmDeleteLink($('.confirm-delete-forum-comment'), $('#confirm_delete_forum_comment_modal'));
})