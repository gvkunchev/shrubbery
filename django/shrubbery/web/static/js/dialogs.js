$(document).ready(function(){

    // Confirmation dialogs for deletion
    function confirmDelete(trigger, modal){
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
    confirmDelete($('.confirm-delete-user'), $('#confirm_delete_user_modal'));
    confirmDelete($('.confirm-delete-news-article'), $('#confirm_delete_news_article_modal'));
    confirmDelete($('.confirm-delete-lecture'), $('#confirm_delete_lecture_modal'));

})
