$(document).ready(function(){
    $('.code pre').each(function(){
        if ($(this).text().indexOf('\t') != -1){
            alert('Учителю, в това решение има табулации!')
        }
    })
})
