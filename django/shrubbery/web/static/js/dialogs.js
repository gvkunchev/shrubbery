$(document).ready(function(){

    // Confirm deleting a student
    $('.confirm-delete-student').click(function(e){
        $('#confirm_delete_student_modal').modal('show');
        e.preventDefault();
    })
    $('#confirm_delete_student_modal').find('.btn-no').bind('click', function(){
        $('#confirm_delete_student_modal').modal('hide');
    })
    $('#confirm_delete_student_modal').find('.btn-yes').bind('click', function(){
        $('#confirm_delete_student_modal').modal('hide');
        $('.confirm-delete-student').parents('form').submit();
    })

})
