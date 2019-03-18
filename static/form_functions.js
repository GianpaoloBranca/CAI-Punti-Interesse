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

// "Visitabile2" validation
$(document).ready(function() {
    var visitabile = $('#id_visitabile');
    var visitabile2 = $('#id_visitabile2');

    if(!visitabile.is(":checked")) {
        visitabile2.prop('checked', false);
        visitabile2.prop('disabled', true);
    }
});

$('#id_visitabile').change(function() {
    var visitabile2 = $('#id_visitabile2');
    if (!this.checked) {
        visitabile2.prop('checked', false);
        visitabile2.prop('disabled', true);
    } else {
        visitabile2.prop('disabled', false);
    }
});

// all textarea with countable attribute
$("[countable]").on("input", function() {
    var len = this.value.length;
    var maxlen = $(this).attr("maxlength");

    if(len > maxlen*0.9) {
        // show remaining characters
        $(this).next().text((maxlen - len) + " Caratteri rimanenti");
    } else {
        // hide remaining characters
        $(this).next().text("");
    }
})
