// AJAX for categories and subcategories
$('#id_categoria').change(function() {
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
});

// Max file size validation
$(':file').change(function() {
    var file = this.files[0];
    if (file.size > 1024 * 1024) {
        alert('La massima dimensione consentita è 1 MB');
        this.value = null;
    }
});