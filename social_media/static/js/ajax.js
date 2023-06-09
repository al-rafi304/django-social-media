$(document).ready(function() {

    // Hide the sharePrompt initially
    $('.sharePrompt').hide();
    
    // Unhide and scroll to the sharePrompt when share button is clicked
    $(document).on('click', '.shareBtn', function() {
        var sharePrompt = $(this).parents('.postContainer').siblings('.sharePrompt');

        sharePrompt.fadeIn(500);
        
        // Scroll to the sharePrompt div
        var scrollPos = sharePrompt.offset().top - $(window).height() / 2
        $('html, body').animate({
            scrollTop: scrollPos
        }, 'fast');
    });

    // Hide the sharePrompt when cancel button is clicked
    //$('.cancel-share').click(function() {
    ///    $(this).closest('.sharePrompt').fadeOut('fast')
    //});

    $(document).on('click', '.cancel-share', function() {
        $(this).closest('.sharePrompt').fadeOut('fast')
    });

    // Restricts blank posts
    $('#post-input').on('input', function(e) {
        input = $(this);
        submitButton = $('#submit-button');

        if (input.val() == '') {
            submitButton.prop("disabled", true);
        } else {
            submitButton.prop('disabled', false);
        }
    });

    // Restricts blank comments
    $(document).on('input', '.comment-input', function(e) {
        input = $(this);
        submitButton = $(input).siblings('.comment-button');

        if (input.val() == '') {
            submitButton.prop("disabled", true);
        } else {
            submitButton.prop('disabled', false);
        }
    });

    // Comment posting with AJAX
    $(document).on('submit', '.comment-form', function(e) {

        // Prevents default behavior
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = new FormData(form[0]);

        var commentCountSpan = form.siblings('.interaction-btn-container').find('.comment-count-span');
        
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var commentContainer = form.siblings('.comment-container');
                var newCommentHTML = $(response.comment_HTML)
                var commentCount = response.commentCount

                newCommentHTML.hide()
                // prepend adds the new item at the top, append adds the item at the bottom
                commentContainer.prepend(newCommentHTML);
                newCommentHTML.slideDown();

                // Setting comment count
                if (commentCount > 0) {
                    commentCountSpan.text(numberFormat(commentCount))
                } else if (commentCount == 0) {
                    commentCountSpan.text('')
                } 

                form[0].reset();
            }
        });

    });

    // Posting with AJAX
    $('#post-form').submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = new FormData(form[0]);

        var submitButton = $('#submit-button');

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var postContainer = $('#all-post-container');
                var postHTML = $(response.post_HTML);

                // Resetting the post prompt
                $('#post-photo').value = null;
                $('#post-video').value = null;
                var photoNameElement = document.getElementById('photo' + "-file-name");
                var videoNameElement = document.getElementById('video' + "-file-name");
                photoNameElement.textContent = null;
                videoNameElement.textContent = null;
                $("#photo-remove-btn").hide();
                $("#video-remove-btn").hide();
                $('#post-video').parents('label').show();
                $('#post-photo').parents('label').show();
                submitButton.prop("disabled", true);
                form[0].reset();

                // Animation for newly added post
                postHTML.hide();
                postContainer.prepend(postHTML);
                postHTML.slideDown();

            }
        });
    });

    //Sharing with AJAX
    $(document).on('submit', '.share-form', function(e){
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = new FormData(form[0]);
        
        var shareCountSpan = form.parents('.sharePrompt').siblings('.postContainer').find('.share-count-span');
        console.log(shareCountSpan)
        // Hiding sharePrompt
        sharePrompt = form.parents('.sharePrompt');
        sharePrompt.slideUp();

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var postContainer = $('#all-post-container');
                var postHTML = $(response.post_HTML);
                var shareCount = response.shareCount;

                // Resetting the post prompt
                form[0].reset();

                // Animation for newly added post
                postHTML.hide();
                postContainer.prepend(postHTML);
                postHTML.slideDown();

                if (shareCount > 0) {
                    shareCountSpan.text(numberFormat(shareCount));
                } else if (shareCount == 0) {
                    shareCountSpan.text('');
                }

            }
        });
    });

    //Liking with AJAX
    $(document).on('submit', '.like-form', function(e){
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = new FormData(form[0]);

        var buttonIcon = form.children('button').children('i');
        var likeCountSpan = form.children('button').children('span');
        console.log(buttonIcon);

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                
                liked = response.liked
                likeCount = response.likeCount
                if (liked) {
                    buttonIcon.replaceWith('<i class="bi bi-heart-fill"></i>')
                } else {
                    buttonIcon.replaceWith('<i class="bi bi-heart"></i>')
                }

                if (likeCount > 0) {
                    likeCountSpan.text(numberFormat(likeCount))
                } else if (likeCount == 0) {
                    likeCountSpan.text('')
                }

                form[0].reset();

            }
        });
    });

    //Liking comments with AJAX
    $(document).on('submit', '.comment-like-form', function(e){
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = new FormData(form[0]);

        var buttonIcon = form.children('button').children('i');
        var likeCountSpan = form.children('button').children('span');

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var liked = response.liked
                var likeCount = response.likeCount

                if (liked) {
                    buttonIcon.replaceWith('<i class="bi bi-heart-fill"></i>')
                } else {
                    buttonIcon.replaceWith('<i class="bi bi-heart"></i>')
                }

                if (likeCount > 0) {
                    likeCountSpan.text(numberFormat(likeCount))
                } else if (likeCount == 0) {
                    likeCountSpan.text('')
                }

                form[0].reset();

            }
        });
    });
    
    // For formating like count numbers, just like the template tag
    function numberFormat(num) {
        let newNum = String(num);
        if (num > 999) {
            newNum = (num / 1000).toFixed(1) + 'K';
        }
        if (num > 999999) {
            newNum = (num / 1000000).toFixed(1) + 'M';
        }
        if (num > 999999999) {
            newNum = (num / 1000000000).toFixed(1) + 'B';
        }
        
        return newNum;
    }
});
