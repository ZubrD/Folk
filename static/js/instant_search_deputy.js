// Моментальный вывод результатов поиска закона на главной странице

$('#search-deputy-input').on('keyup',instantSearchDeputy)


function instantSearchDeputy(){
    count = $(this).val().length
    if (count > 2){         /*Минимальное количество знаков в запросе*/
        searched = $(this).val()
        $.ajax({
            type: "GET",
            url: "/isearch_deputy",
            data: {
                searched_val: searched
            },
            success: function (data){
                $('#instant-search-deputy-result').empty().css({"height": ""})
                let counter = 0
                $.each(data, function (){
                    counter = counter + 1
                    if (counter > 0){      // для прокрутки
                        $('#instant-search-deputy-result').css({"height": "200px"});
                    }
                    $('#instant-search-deputy-result').append('<p deputy-name="'+this.name+'" class="position-relative"><a href="deputy/'+this.name+'" target="_blank" class="stretched-link" style="text-decoration: none">'+this.name+'</a></p>')
                    $('#instant-search-deputy-result p:even').css({"backgroundColor": "#d1cbcb"});
                })

            $('#instant-search-deputy-result p').click(function (){
                $(this).css({'backgroundColor': '#fffb85'});
            })

            }
        });
    } else {
        $('#instant-search-deputy-result').empty().empty().css({"height": ""}) /*Если запрос меньше 5 знаков - очищаю div вывода результатов*/
    }
}

$(document).mouseup(function (e) {                  // Если клик не на
    let container5 = $("#div-search-deputy");         // div поля поиска закона или
    let container6 = $("#div-instant-search-deputy-result")        // div вывода результатов
    if (container5.has(e.target).length === 0 && container6.has(e.target).length === 0){
        $('#search-deputy-input').val('');           // то очищается поле поиска и
        $('#instant-search-deputy-result').empty().css({"height": "0"});                // и div вывода результатов
    }

});
