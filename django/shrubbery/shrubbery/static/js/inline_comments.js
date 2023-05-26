$(document).ready(function(){

    // Move existing comments in place
    $('.inline-comment').each(function(i, e){
        var line_number = $(e).data('line');
        var line = $('.code #code-line-' + line_number);
        $(e).insertAfter(line);
    })

    $('.inline-comment-hide-trigger').bind('click', function(){
        $(this).parents('.inline-comment').toggleClass('hidden-comment');
    })
})