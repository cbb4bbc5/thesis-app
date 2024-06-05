$(document).ready(function() {
    var formIdx = 1; // hardcoded for now, might pass extra later

    var totalForms = $("#id_form-TOTAL_FORMS");
    totalForms.val(1);
    var firstRow = $(".form-row:last");

    function updateFormRows() {
        $(document).find('.form-row').each(function(index) {
            splitFor = $(this).find('label').attr('for').split('-');
            splitFor[1] = String(index);
            newFor = splitFor.join('-');
            $(this).find('label').attr('for', newFor);
            $(this).find('input, text').attr('id', newFor);
            splitName = $(this).find('input, text').attr('name').split('-');
            splitName[1] = String(index);
            newName = splitName.join('-');
            $(this).find('input, text').attr('name', newName);
        });
    }

    $("#add-more").click(function() {
    newRow = $(".form-row:last").clone();
    if ($(".form-row").length === 0) {
        newRow = firstRow;
    }
        var splitFor = newRow.find('label').attr('for').split('-');
        splitFor[1] = String(formIdx);
        newFor = splitFor.join('-');
        newRow.find('label').attr('for', newFor);
        newRow.find('input, text').attr('id', newFor);
        splitName = newRow.find('input, text').attr('name').split('-');
        splitName[1] = String(formIdx);
        newName = splitName.join('-');
        newRow.find('input, text').attr('name', newName);
        newRow.find('input, text').val('');
    newRow.appendTo("#formset-container");

    var totalForms = $("#id_form-TOTAL_FORMS");
    totalForms.val(parseInt(totalForms.val()) + 1);

    formIdx++;
    });

    $(document).on("click", ".delete-form-row", function() {
    $(this).closest('.form-row').remove();
    var totalForms = $("#id_form-TOTAL_FORMS");
    totalForms.val(parseInt(totalForms.val()) - 1);
    formIdx--;
        updateFormRows();
    });
});
