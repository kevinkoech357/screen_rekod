document.addEventListener('DOMContentLoaded', function () {
  // Function to manually trigger the modal
  document.querySelector('.btn-edit').addEventListener('click', function () {
    $('#editModal').modal('show');
  });

  function updateVideoDetails () {
    // Fetch values from the form
    const updatedTitle = document.getElementById('editTitle').value;
    const updatedDescription = document.getElementById('editDescription').value;

    // Create a FormData object
    const formData = new FormData();
    formData.append('title', updatedTitle);
    formData.append('description', updatedDescription);

    // Make a fetch request to Flask route
    fetch('{{ url_for("video.update_video", video_id=video.id) }}', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the server, if needed
        console.log(data);

        // Update the video details on the page
        document.getElementById('videoTitle').innerText = updatedTitle;
        document.getElementById('videoDescription').innerText = updatedDescription;

        // Close the modal
        $('#editModal').modal('hide');
      })
      .catch(error => {
        // Handle errors, if any
        console.log(error);
      });
  }

  function deleteVideo (deleteUrl) {
    // Confirm with the user before proceeding with the deletion
    if (confirm('Are you sure you want to delete this video?')) {
      // Make a fetch request to delete the video
      fetch(deleteUrl, {
        method: 'DELETE'
      })
        .then(response => response.json())
        .then(data => {
          alert('Video successfully deleted!');

          // Remove the video element from the DOM
          const videoContainer = document.querySelector('.video-container');
          if (videoContainer) {
            videoContainer.parentNode.removeChild(videoContainer);
          }

          // Redirect to the dashboard
          window.location.href = '{{ url_for("user.dashboard") }}';

          console.log(data.message);
        })
        .catch(error => {
          // Handle errors, if any
          console.error(error);
        });
    }
  }
});
