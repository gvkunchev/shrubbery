$(document).ready(function(){

    function enableCompareSymbols(text) {
        console.log(text)
        return text.replace(/&amp;amp;lt;/g, '&lt;').replace(/&amp;amp;gt;/g, '&gt;').replace(/ &amp;gt; /g, ' > ').replace(/ &amp;lt;= /g, ' <= ').replace(/ &amp;gt;= /g, ' >= ').replace(/ -&amp;gt; /g, ' -> ');
    }

    var showDownConverter = new showdown.Converter();
    showDownConverter.setOption('emoji', true);
    showDownConverter.setOption('simplifiedAutoLink', true);
    showDownConverter.setOption('strikethrough', true);

    // Inline text
    $('.showdown-trigger').each(function(){
        $(this).html(enableCompareSymbols(showDownConverter.makeHtml($(this).html())));
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
        var escaped_val = $("<div>").text(source.val()).html()
        $('#showdown-modal').find('.modal-body').html(enableCompareSymbols(showDownConverter.makeHtml(escaped_val)));
        // Add syntax highlighting
        $('#showdown-modal').find('.modal-body').find('code').each(function(i, e){
            var parsed = hljs.highlightAuto($(e).html());
            $(e).html(parsed.value);
        })
        $('#showdown-modal').modal('show');
        e.preventDefault();
    })
    $('#showdown-modal').find('button').bind('click', function(){
        $('#showdown-modal').modal('hide');
    })

})
