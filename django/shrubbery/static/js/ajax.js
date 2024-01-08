$(document).ready(function(){

    $('.ajax-toggle-trigger').each(function(i, e){
        $(e).bind('click', function(event){
            $.ajax({
                url: $(e).attr('href'),
                success: function(result){
                    var active = $(e).parents('.ajax-toggle').find('.ajax-toggle-trigger.active');
                    var passive = $(e).parents('.ajax-toggle').find('.ajax-toggle-trigger').not('.active');
                    active.removeClass('active');
                    passive.addClass('active');
                    $(e).parents('.ajax-toggle-container').first().find('.ajax-toggle-target').toggleClass('hidden');
                },
                error: function(){
                    window.location = $(e).attr('href');
                }
            });
            event.preventDefault();
        })
    })

})
