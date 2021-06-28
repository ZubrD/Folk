// Поиск депутата из выпадающего списка (не используется, вместо него deputy_search_bis.js)

$('body').on('change', '#select-region', function (event){
    $.ajax({
     type:"GET",
     url: "/search_deputy_in_region",      //Это путь из url.py
     data: {
       search_region: $(event.target).val()
     },
     success: function( data ) {        // data - это json-список депутатов
         $('#search-deputy-result').empty()
         $.each(data, function (){
             $('#search-deputy-result').append('<p><a href="/deputy/'+this.name+'" target="_blank">'+this.name+'</a></p>')
         })

     }
    })
})