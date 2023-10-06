$(document).ready(function(){

    var showDownConverter = new showdown.Converter();
    showDownConverter.setOption('emoji', true);
    showDownConverter.setOption('simplifiedAutoLink', true);

    // Inline text
    $('.showdown-trigger').each(function(){
        $(this).html(showDownConverter.makeHtml($(this).text()));
    })

    
    // Add syntax highlighting
    $('code').each(function(i, e){
        var parsed = hljs.highlightAuto($(e).html());
        $(e).html(parsed.value);
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
