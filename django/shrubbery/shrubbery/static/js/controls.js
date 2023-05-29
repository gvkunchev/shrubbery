$(document).ready(function(){
    $('.select-all-trigger').bind('click', function(){
        var inputs = $(this).parents('form').find('input[type=checkbox');
        inputs.click()
    })

    $('[data-trigger="word-wrap"]').bind('change', function(){
        if($(this).is(':checked')){
            $(this).parents('.code-diff-container, .code').addClass('word-wrap-diff');
        }
        else{
            $(this).parents('.code-diff-container, .code').removeClass('word-wrap-diff');
        }
    })
})