$(document).ready(function(){
    $('.code pre').each(function(){
        if ($(this).text().indexOf('\t') != -1){
            $('pre').prepend($('<div class="text-danger">').html('Учителю, в това решение има табулации!'))
        }
    })
})
