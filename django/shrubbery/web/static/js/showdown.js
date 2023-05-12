$(document).ready(function(){
    var showDownConverter = new showdown.Converter();
    showDownConverter.setOption('emoji', true);
    
    $('.showdown-trigger').each(function(){
        $(this).html(showDownConverter.makeHtml($(this).html()));
    })
})
