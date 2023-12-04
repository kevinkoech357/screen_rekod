document.addEventListener('DOMContentLoaded', function () {
  // Function to manually trigger the modal
  document.getElementById('editButton').addEventListener('click', function () {
    $('#editModal').modal('show');
  });

  // Event listener for update button
  document.getElementById('saveChangesButton').addEventListener('click', function (event) {
    // Prevent the form from submitting (to control the submission using your updateVideoDetails function)
    event.preventDefault();

    // Call function to update video details
    updateVideoDetails();
  });

  // Event listener for delete button
  document.getElementById('deleteButton').addEventListener('click', function () {
    const deleteUrl = this.getAttribute('data-delete-url');
    deleteVideo(deleteUrl);
  });

  // Event listener for share button
  document.getElementById('shareButton').addEventListener('click', function () {
    // Show the share link modal and generate shareable link
    $('#shareLinkModal').modal('show');
    const videoId = this.getAttribute('data-video-id');
    generateShareLink(videoId);
  });

  // Event listener for copy button
  document.getElementById('copyLinkButton').addEventListener('click', function () {
    // Call the copyToClipboard function
    copyToClipboard();
  });

  function updateVideoDetails () {
    // Fetch values from the form
    const updatedTitle = document.getElementById('editTitle').value;
    const updatedDescription = document.getElementById('editDescription').value;

    // Create a FormData object
    const formData = new FormData();
    formData.append('title', updatedTitle);
    formData.append('description', updatedDescription);

    // Get the update URL from the data attribute
    const updateUrl = document.getElementById('saveChangesButton').getAttribute('data-update-url');

    // Make a fetch request to Flask route
    fetch(updateUrl, {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
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

          // Redirect to the dashboard
          window.location.href = window.location.origin + '/dashboard';

          console.log(data.message);
        })
        .catch(error => {
          // Handle errors, if any
          console.error(error);
        });
    }
  }

  function generateShareLink (videoId) {
    fetch(`/generate_share_link/${videoId}`)
      .then(response => response.json())
      .then(data => {
      // Display the shareable link in the shareLink input element
        const shareLinkInput = document.getElementById('shareLink');
        shareLinkInput.value = data.shareable_link;
        $('#shareLinkModal').modal('show');
      })
      .catch(error => console.error('Error:', error));
  }

  function copyToClipboard () {
    // Copy the shareable link to the clipboard
    const shareableLink = document.getElementById('shareLink');
    shareableLink.select();
    document.execCommand('copy');

    // Close the modal after copying
    $('#shareLinkModal').modal('hide');
  }
});
