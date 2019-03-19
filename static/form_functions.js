var initial;
var loaded = false;

$(document).ready( function(){
    initial = $("#id_sottocategoria option:selected").val();
    $('#id_categoria').trigger('change');
});

// AJAX for categories and subcategories
$('#id_categoria').on("change", function() {
    var url = $("#id_form").attr("ajax_subcat_url");
    var cat_id = $(this).val();

    $.ajax({
        url: url,
        data: {
            'categoria': cat_id
        },
        success: function (data) {
            $("#id_sottocategoria").html(data);
            if(initial && !loaded) {
                loaded = true;
                $("#id_sottocategoria").val(initial).prop("selected", true);
            }
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
