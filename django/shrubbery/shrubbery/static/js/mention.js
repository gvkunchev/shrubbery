$(document).ready(function(){
    $('.showdown-input').suggest('@', {
        data: function(q) {
        if (q) {
            return $.getJSON("/users", { q: q });
        }
        },
        map: function(user) {
        return {
            value: user.replace(' ', '_'),
            text: '@' + user
        }
        }
    })
})