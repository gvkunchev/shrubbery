$(document).ready(function(){
    $('.select-all-trigger').bind('click', function(){
        var inputs = $(this).parents('form').find('input[type=checkbox');
        inputs.click()
    })
})