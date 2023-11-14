document.addEventListener('DOMContentLoaded', function () {
        var flashMessages = document.querySelectorAll('.flash');

        flashMessages.forEach(function (flashMessage) {
            setTimeout(function () {
                flashMessage.style.opacity = '0';
                setTimeout(function () {
                    flashMessage.remove();
                }, 500); // Remove after fading out
            }, 2000); // Disappear after 2 seconds
    });
});
