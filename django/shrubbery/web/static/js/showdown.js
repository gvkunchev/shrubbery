$(document).ready(function(){
    var showDownConverter = new showdown.Converter();
    showDownConverter.setOption('emoji', true);
    
    // Inline text
    $('.showdown-trigger').each(function(){
        $(this).html(showDownConverter.makeHtml($(this).html()));
    })

    // Dynamic preview
    $('.showdown-preview').bind('click', function(e){
        var source_id = $(this).data('showdown-source');
        var source = $('#' + source_id);
        $('#showdown-modal').find('.modal-body').html(showDownConverter.makeHtml(source.val()));
        $('#showdown-modal').modal('show');
        e.preventDefault();
    })
    $('#showdown-modal').find('button').bind('click', function(){
        $('#showdown-modal').modal('hide');
    })
})
