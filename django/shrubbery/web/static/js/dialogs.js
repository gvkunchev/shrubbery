$(document).ready(function(){

    // Confirm deleting a user
    $('.confirm-delete-user').click(function(e){
        $('#confirm_delete_user_modal').modal('show');
        e.preventDefault();
    })
    $('#confirm_delete_user_modal').find('.btn-no').bind('click', function(){
        $('#confirm_delete_user_modal').modal('hide');
    })
    $('#confirm_delete_user_modal').find('.btn-yes').bind('click', function(){
        $('#confirm_delete_user_modal').modal('hide');
        var delete_input = $('<input>').attr({
            'type': 'hidden',
            'name': 'delete'
        });
        $('.confirm-delete-user').parents('form').append(delete_input)
        $('.confirm-delete-user').parents('form').submit();
    })

    // Confirm deleting a news article
    $('.confirm-delete-news-article').click(function(e){
        $('#confirm_delete_news_article_modal').modal('show');
        e.preventDefault();
    })
    $('#confirm_delete_news_article_modal').find('.btn-no').bind('click', function(){
        $('#confirm_delete_news_article_modal').modal('hide');
    })
    $('#confirm_delete_news_article_modal').find('.btn-yes').bind('click', function(){
        $('#confirm_delete_news_article_modal').modal('hide');
        window.location = $('.confirm-delete-news-article').attr('href');
    })

})
