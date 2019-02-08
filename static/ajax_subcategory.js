function load_subcategories() {
    var url = $("#id_form").attr("ajax_subcat_url");
    var cat_id = $(this).val();

    $.ajax({
        url: url,
        data: {
            'categoria': cat_id
        },
        success: function (data) {
            $("#id_sottocategoria").html(data);
        }
    });
}

$('#id_categoria').change(load_subcategories);