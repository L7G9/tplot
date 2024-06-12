function ShowImageModal(image_src, image_alt) {
    $('#modalTitle').html(image_alt);
    let modalImage = document.getElementById('modalImage');
    modalImage.src = image_src;
    modalImage.alt = image_alt;
    $('#imageModal').modal('show');
}
