/* https://github.com/select2/select2/issues/3106 */
/* sorting is not worth it */
/* https://stackoverflow.com/questions/76773528/creating-a-search-bar-using-javascript-and-an-unordered-list-how-to-hide-the-li */
$(document).ready(function() {
    $('#search-bar').select2({
        placeholder: 'Search for notes by tags',
        allowClear: true,

    });

    function removeItem(item) {
        $('#selected-item-' + item).remove();
        var newOption = new Option(item, item, false, false);
        $('#search-bar').append(newOption).trigger('change.select2');
        filterNotes();
    }

    $('#search-bar').on('select2:select', function (e) {
        var item = e.params.data.id;
        var itemText = e.params.data.text;

        $('#selected-items').append(
            '<span class="selected-item" id="selected-item-' + item + '">' +
            itemText +
            '<span class="remove-item" onclick="removeItem(\'' + item + '\')">x</span>' +
            '</span>'
        );

        filterNotes();
    });

    $('#search-bar').on('select2:unselect', function (e) {
        var item = e.params.data.id;
        $('#selected-item-' + item).remove();
        filterNotes();
    });

    function filterNotes() {
        var selectedTags = $('#search-bar').val() || [];

        $('.note').each(function() {
            var note = $(this);
            var noteTags = note.data('tags').split(',');

            var showNote = selectedTags.every(tag => noteTags.includes(tag));

            if (showNote) {
                note.show();
            } else {
                note.hide();
            }
        });
    }
});
