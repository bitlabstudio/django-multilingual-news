/*
 * Functionality usable in conjunction with Twitter Bootstrap 3
 *
 */
/* global getModalB3 */


// Opening a modal to delete an entry instead of calling the view regularly
$(document).on('click', '[data-class=toggleDeleteModal]', function(e) {
    var modal_url;

    var bootstrap_enabled = (typeof $().modal === 'function');

    if (bootstrap_enabled) {
        modal_url = $(this).attr('href');
        e.preventDefault();
        getModalB3(modal_url);
    }
});

$(document).on('click', '[data-id=entryDeleteCancel]', function(e) {
    var $modal = $(this).parents('.modal');

    e.preventDefault();
    $modal.modal('hide');
});
