$('#set-likes').click(function (){
    like_status = $(this).attr('liked')
    var rule_number, username;
    rule_number = $(this).attr("rule-number");
    username = $(this).attr('username');
    if (like_status == 'not-liked') {
        $(this).attr({liked: 'liked'}).removeAttr('class').addClass('button-liked');
        $('#set-dislikes').attr({disabled: 'disabled'});   /*Дезактивирую баттон дизлайков*/
        $.ajax({
            type: "GET",
            url: "/add_url_prefer",
            data: {
                rule_number: rule_number,
                person: username
            },
            success: function (data){
                $('#span-likes').html(data)
                location.reload()
            }
        });
    }
    if (like_status == 'liked') {
        $(this).attr({liked: 'not-liked'}).removeAttr('class').addClass('button-not-liked');
        $('#set-dislikes').removeAttr('disabled');  /*Снимаю дезактивацию*/
        $.ajax({
            type: "GET",
            url: "/delete_url_prefer",
            data: {
                rule_number: rule_number,
                person: username
            },
            success: function (data){
                $('#span-likes').html(data)
                location.reload()
            }
        });
    }
})

$('#set-dislikes').click(function (){
    dislike_status = $(this).attr('disliked')
    var rule_number, username;
    rule_number = $(this).attr("rule-number");
    username = $(this).attr('username');
    if (dislike_status == 'not-disliked') {
        $(this).attr({disliked: 'disliked'}).removeAttr('class').addClass('button-disliked');
        $('#set-likes').attr({disabled: 'disabled'});   /*Дезактивирую баттон лайков*/
        $.ajax({
            type: "GET",
            url: "/add_url_dislike",
            data: {
                rule_number: rule_number,
                person: username
            },
            success: function (data){
                $('#span-dislikes').html(data)
            }
        });
    }
    if (dislike_status == 'disliked') {
        $(this).attr({disliked: 'not-disliked'}).removeAttr('class').addClass('button-not-disliked');
        $('#set-likes').removeAttr('disabled');
        $.ajax({
            type: "GET",
            url: "/delete_url_dislike",
            data: {
                rule_number: rule_number,
                person: username
            },
            success: function (data){
                $('#span-dislikes').html(data)
            }
        });
    }
})