$(document).ready(function() {
    function updateFormIndices() {
        $('#formset-container .form-row').each(function(index) {
            $(this).find('input, select, textarea').each(function() {
                let name = $(this).attr('name').replace(/-\d+-/, '-' + index + '-');
                let id = $(this).attr('id').replace(/-\d+-/, '-' + index + '-');
                $(this).attr({'name': name, 'id': id});
            });
        });
        let totalForms = $('#formset-container .form-row').length;
        $('#id_note-TOTAL_FORMS').val(totalForms);
    }

    let formIdx = parseInt($("#id_note-TOTAL_FORMS").val());

    $('#addConnection').click(function() {
        let newForm = $('#formset-container .form-row:first').clone(false);
        newForm.find('input, select, textarea').each(function() {
            let name = $(this).attr('name').replace(/-\d+-/, '-' + formIdx + '-');
            let id = $(this).attr('id').replace(/-\d+-/, '-' + formIdx + '-');
            $(this).attr({'name': name, 'id': id}).val('');
        });
        newForm.find('input:hidden[name$="-id"]').remove();
        newForm.find('.select2-container').remove();
        newForm.find('select').removeAttr('data-select2-id').removeClass('select2-hidden-accessible').next('.select2').remove();
        newForm.find('select').attr('data-select2-id', formIdx).select2();
        newForm.appendTo('#formset-container');
        formIdx++;
        $('#id_note-TOTAL_FORMS').val(formIdx);
        updateFormIndices();
    });

    $('#formset-container').on('click', '.delete-connection', function() {
        let row = $(this).closest('.form-row');
        if (row.find('input:hidden[name$="-id"]').length) {
            row.hide();
            row.find('input:hidden[name$="-DELETE"]').val('on');
        } else {
            row.remove();
        }
        updateFormIndices();
    });

    $('#formset-container select').select2();
});