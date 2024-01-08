$(document).ready(function(){
    $('.clipboard-trigger').each(function(i, e){
        $(e).bind('click', function(){
            var input = $(e).find('input');
            $(input).removeClass('hidden');
            if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
              input.contenteditable = true;
              input.readonly = false;
              var range = document.createRange();
              range.selectNodeContents(input);
              var selection = window.getSelection();
              selection.removeAllRanges();
              selection.addRange(range);
              input.setSelectionRange(0, 999999);
            } else {
              input.select();
            }
            document.execCommand('copy');
            $(input).addClass('hidden');
        })
    })
})