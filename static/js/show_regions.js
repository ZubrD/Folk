$('#show-regions').click(function (){
    $('#region-list').css('display', 'block')
    $('#region-list p:even').css({"backgroundColor": "#d1cbcb"});
})

$('#region-list p').click(function (){
    $('#show-regions').html($(this).attr('id'))
    $('#region-list').css('display', 'none')
})

$(document).mouseup(function (e) {              // Клик в любом месте экрана скрывает список регионов
    let container = $("#region-list");
    if (container.has(e.target).length === 0){
        container.hide();
    }
});

$(document).mouseup(function (e) {              // Клик в любом месте экрана скрывает список депутатов
    let container = $("#search-deputy-result");
    if (container.has(e.target).length === 0){
        container.hide();
    }
});

$(document).mouseup(function (e) {                  // Если клик не на div списка регионов или списка депутатов,
    let container1 = $("#search-deputy-result");    // то возвращается надпись на баттоне 'Выберите регион'
    let container2 = $('#region-list');
    if (container1.has(e.target).length === 0 && container2.has(e.target).length === 0){
        $('#show-regions').html('Выберите регион');
    }
});
