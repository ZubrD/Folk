$('#btnradio1, #btnradio2, #btnradio3').click(function (){
    $('#button-send-vote').removeAttr('disabled')
})

$('#button-send-vote').click(function (){
    $(this).hide()
})

$('#delete-voting').click(function (){
    let name = $(this).attr('name')
    let rule_number = $(this).attr('rule-number')
    $.ajax({
        type: "GET",
        url: "/delete_populi_voting",
        data: {
            name: name,
            rule_number: rule_number
        },
        success: function (data){
            location.reload()
        }
    });
})