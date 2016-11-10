$function(){
    $('#search').keyup(function() {
        $.ajax({
            type: "GET",
            url: "{% url 'sell' %}",
            data:{
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'datatType': 'html'
        });
        $('#search-resul')
    });
}

function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data);
}
