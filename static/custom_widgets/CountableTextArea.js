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
