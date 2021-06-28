// Моментальный вывод результатов поиска закона на главной странице

// $('#search-input').keyup(instantSearchRule)
$('#search-input').on('keyup',instantSearchRule)

function instantSearchRule(){
    count = $(this).val().length
    if (count > 4){         /*Минимальное количество знаков в запросе*/
        searched = $(this).val()
        $.ajax({
            type: "GET",
            url: "/isearch",
            data: {
                searched_val: searched
            },
            success: function (data){
                $('#search-result').empty().css({"height": ""})
                let counter = 0
                $.each(data, function (){
                    counter = counter + 1
                    if (counter > 0){      // для прокрутки
                        $('#search-result').css({"height": "300px"});
                    }
                    $('#search-result').append('<p rule-number="'+this.rule_number+'" class="position-relative"><a href="rule/'+this.rule_number+'" target="_blank" class="stretched-link" style="text-decoration: none">'+this.rule_number+' '+this.title+'</a></p>')
                    $('#search-result p:even').css({"backgroundColor": "#d1cbcb"});
                })

            $('#search-result p').click(function (){
                $(this).css({'backgroundColor': '#fffb85'});
            })

            }
        });
    } else {
        $('#search-result').empty().empty().css({"height": ""}) /*Если запрос меньше 5 знаков - очищаю div вывода результатов*/
    }
}

$(document).mouseup(function (e) {                  // Если клик не на
    let container3 = $("#div-search-rule");         // div поля поиска закона или
    let container4 = $("#div-search-result")        // div вывода результатов
    if (container3.has(e.target).length === 0 && container4.has(e.target).length === 0){
        $('#search-input').val('');           // то очищается поле поиска и
        $('#search-result').empty().css({"height": "0"});                // и div вывода результатов
    }

});
