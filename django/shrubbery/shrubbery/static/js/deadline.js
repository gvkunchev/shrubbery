$(document).ready(function(){
    $('.deadline').each(function(i, e){
        var countDownDate = new Date($(e).text()).getTime();
        function updateTime(){
            var now = new Date().getTime();
            var distance = countDownDate - now;
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            var text = '';
            if (days > 0) text += days + 'д ';
            if (hours > 0) text += hours + 'ч ';
            if (minutes > 0) text += minutes + 'м ';
            if (seconds > 0) text += seconds + 'с ';
            $(e).text(text);
            if (distance < 0) {
                $(e).addClass('hidden');
                return false
            }
            return true;
        }

        updateTime();
        $(e).removeClass('hidden');
        var counter = setInterval(function() {
            if (!updateTime()){ 
                clearInterval(counter);
            }
        }, 1000);
    })
})

