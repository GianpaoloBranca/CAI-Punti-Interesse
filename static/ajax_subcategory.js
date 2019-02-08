function load_subcategories() {
    var url = $("#id_form").attr("ajax_subcat_url");  // get the url of the `load_cities` view
    var cat_id = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request 
        data: {
            'categoria': cat_id       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
            $("#id_sottocategoria").html(data);  // replace the contents of the city input with the data that came from the server
        }
    });
}

$('#id_categoria').change(load_subcategories);