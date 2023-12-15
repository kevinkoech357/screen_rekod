document.addEventListener('DOMContentLoaded', async function () {
  // Get references to HTML elements
  const startButton = document.getElementById('startRecording');
  const stopButton = document.getElementById('stopRecording');
  const recordedVideoModal = document.getElementById('recordedVideoModal');
  const titleModal = document.getElementById('titleModal');
  const descriptionModal = document.getElementById('descriptionModal');
  const uploadButtonModal = document.getElementById('uploadButtonModal');

  // Check if all required elements are present
  if (!startButton || !stopButton || !recordedVideoModal || !titleModal || !descriptionModal || !uploadButtonModal) {
    console.error('Required elements not found.');
    return;
  }

  // Variables for recording functionality
  let chunks = [];
  let recorder = null;
  let recordedBlob = null;
  let screenStream = null;
  let audioStream = null;

  // Get browser and OS information using the 'platform' library
  const browserName = platform.name;
  const browserVersion = platform.version;
  const browserLayout = platform.layout;
  const operatingSystem = platform.os;

  // Async function to start recording
  async function startRecording () {
    try {
      // Get audio and screen streams
      audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false
        }
      });

      screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true
      });

      // Create a mixed stream from audio and screen streams
      const mixedStream = new MediaStream([...screenStream.getTracks(), ...audioStream.getTracks()]);

      // Initialize MediaRecorder with mixed stream
      recorder = new MediaRecorder(mixedStream, {
        mimeType: 'video/webm'
      });

      // Event listeners for dataavailable and stop events
      chunks = [];
      recorder.addEventListener('dataavailable', function (e) {
        chunks.push(e.data);
      });

      recorder.addEventListener('stop', function () {
        recorder.stop();
        console.log('Recording stopped.');

        // Create Blob from chunks and set source for modal
        recordedBlob = new Blob(chunks, {
          type: 'video/mp4'
        });
        recordedVideoModal.src = URL.createObjectURL(recordedBlob);

        // Open the Bootstrap Modal
        $('#videoModal').modal('show');
      });

      // Event handler when recording starts
      recorder.onstart = event => {
        console.log('Recording started.');
        startButton.disabled = true;
      };

      // Listen for the 'ended' event on the video track
      const videoTrack = screenStream.getVideoTracks()[0];
      videoTrack.addEventListener('ended', () => {
        console.log('Screen sharing ended. Stopping recording...');
        stopRecording();
      });

      // Start recording
      recorder.start();
    } catch (err) {
      console.log('Error starting recording:', err);
    }
  }

  // Function to stop recording
  function stopRecording () {
    if (recorder && recorder.state === 'recording') {
      recorder.stop();
      console.log('Recorder stopped manually.');
    }
  }

  // Event listener for upload button click
  uploadButtonModal.addEventListener('click', function () {
    if (!recordedBlob) {
      console.error('No recorded video to upload.');
      return;
    }

    // Create FormData object and append data
    const formData = new FormData();
    formData.append('video_file', recordedBlob);
    formData.append('title', titleModal.value);
    formData.append('description', descriptionModal.value);
    formData.append('browserName', browserName);
    formData.append('browserVersion', browserVersion);
    formData.append('browserLayout', browserLayout);
    formData.append('operatingSystem', operatingSystem);

    // Disable the upload button and show an alert
    uploadButtonModal.disabled = true;
    alert('File upload in progress...');

    // Log information and initiate fetch request
    console.log('Uploading...');
    console.log('Title:', titleModal.value);
    console.log('Description:', descriptionModal.value);
    console.log('browserName:', browserName);
    console.log('browserVersion:', browserVersion);
    console.log('browserLayout:', browserLayout);
    console.log('Operating System:', operatingSystem);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(resp => resp.json())
      .then(data => {
        console.log('Upload response:', data);

        // Handle the response and enable the upload button
        if (data.status === 'success') {
          alert('File successfully uploaded!');
          window.location.reload(true);
          $('#videoModal').modal('hide');
        } else {
          alert('Error uploading File!');
          console.log('Error:', data.message);
        }

        uploadButtonModal.disabled = false;
      })
      .catch(err => {
        console.log('Upload error:', err);
        // Enable the upload button in case of an error
        uploadButtonModal.disabled = false;
      });
  });

  // Event listeners for start and stop buttons
  startButton.addEventListener('click', startRecording);
  stopButton.onclick = () => stopRecording();
});
