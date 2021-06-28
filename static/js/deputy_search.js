$('#region-list p').click(function (){
    $('#search-deputy-result').css('display', 'block')

    let search_data = $(this).attr('id')

    $.ajax({
     type:"GET",
     url: "/search_deputy_in_region",      //Это путь из url.py
     data: {
       search_region: search_data
     },
     success: function( data ) {        // data - это json-список депутатов
         $('#search-deputy-result').empty()
         $.each(data, function (){
             $('#search-deputy-result').append('<p class="position-relative"><a href="/deputy/'+this.name+'" class="stretched-link" style="text-decoration: none" target="_blank">'+this.name+'</a></p>')
             $('#search-deputy-result p:even').css({"backgroundColor": "#eeedd2"});
         })
     }
    })

})