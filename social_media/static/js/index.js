// Javascript for showing the filename after select the photo/video for posting
function selectFile(input, fileType) {

    // Showing file name after selecting
    var fileName = input.files[0].name;
    var fileNameElement = document.getElementById(fileType + "-file-name");
    fileNameElement.textContent = fileName;
    
    // Limiting to select only one file type
    if (fileType == 'photo'){
        $('#post-video').parents('label').hide();
        $('#photo-remove-btn').show()
    } else if (fileType == 'video'){
        $('#post-photo').parents('label').hide();
        $('#video-remove-btn').show()
    }

}

// Javascript for removing the selected files
function removeFile(button, fileType) {
    if (fileType == 'photo') {
        var input = $('#post-photo');

        $('#post-video').parents('label').show();

    } else if (fileType == 'video') {
        var input = $('#post-video');

        $('#post-photo').parents('label').show();
    }

    input[0].value = null;
    var fileNameElement = document.getElementById(fileType + "-file-name");
    fileNameElement.textContent = null;
    $(button).hide();
}