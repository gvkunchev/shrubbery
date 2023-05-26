$(document).ready(function(){

    // Move existing comments in place
    $('.existing-inline-comment').each(function(i, e){
        var line_number = $(e).data('line');
        var line = $('.code #code-line-' + line_number);
        $(e).insertAfter(line);
    })

    // Show/hide comment content
    $('.inline-comment-hide-trigger').bind('click', function(){
        $(this).parents('.inline-comment').toggleClass('hidden-comment');
    })

    // Add new comment
    $('.linenos').bind('click', function(){
        var form = $('.add-inline-comment');
        var line = $(this).parents('[id*=code-line]');
        var line_number = line.attr('id').replace('code-line-', '');
        form.insertAfter(line);
        form.find('input[name=line]').val(line_number);
    })

    // Cancel adding inline comment
    $('.inline-comment-cancel').bind('click', function(){
        var form = $('.add-inline-comment');
        $('.add-inline-comment-wrapper').append(form);
    })

    // Comments are added later so scroll to the element once it is added
    if ($(window.location.hash).length){
        $(window.location.hash)[0].scrollIntoView();
    }

    // Hide/show all comments
    $('.toggle-inline-comments').bind('click', function(){
        if ($(this).find('.toggle-inline-comments-show').hasClass('hidden')){
            $('.toggle-inline-comments-show').removeClass('hidden');
            $('.toggle-inline-comments-hide').addClass('hidden');
            $('.inline-comment').addClass('hidden-comment');
        }
        else{
            $('.toggle-inline-comments-show').addClass('hidden');
            $('.toggle-inline-comments-hide').removeClass('hidden');
            $('.inline-comment').removeClass('hidden-comment');
        }
    })
});