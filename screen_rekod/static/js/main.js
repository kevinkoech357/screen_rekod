document.addEventListener('DOMContentLoaded', async function () {
  const startButton = document.getElementById('startRecording');
  const stopButton = document.getElementById('stopRecording');
  const recordedVideoModal = document.getElementById('recordedVideoModal');
  const titleModal = document.getElementById('titleModal');
  const descriptionModal = document.getElementById('descriptionModal');
  const uploadButtonModal = document.getElementById('uploadButtonModal');

  if (!startButton || !stopButton || !recordedVideoModal || !titleModal || !descriptionModal || !uploadButtonModal) {
    console.error('Required elements not found.');
    return;
  }

  let chunks = [];
  let recorder = null;
  let recordedBlob = null;
  let screenStream = null;
  let audioStream = null;

  // Get browser and OS information
  const browserName = platform.name;
  const browserVersion = platform.version;
  const browserLayout = platform.layout;
  const operatingSystem = platform.os;

  async function startRecording () {
    try {
      audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false
        }
      });

      screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true
      });

      const mixedStream = new MediaStream([...screenStream.getTracks(), ...audioStream.getTracks()]);

      recorder = new MediaRecorder(mixedStream, {
        mimeType: 'video/webm'
      });

      chunks = [];
      recorder.addEventListener('dataavailable', function (e) {
        chunks.push(e.data);
      });

      recorder.addEventListener('stop', function () {
        recorder.stop();
        console.log('Recording stopped.');

        recordedBlob = new Blob(chunks, {
          type: 'video/mp4'
        });
        recordedVideoModal.src = URL.createObjectURL(recordedBlob);

        // Open the Bootstrap Modal
        $('#videoModal').modal('show');
      });

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

      recorder.start();
    } catch (err) {
      console.log('Error starting recording:', err);
    }
  }

  function stopRecording () {
    if (recorder && recorder.state === 'recording') {
      recorder.stop();
      console.log('Recorder stopped manually.');
    }
  }

  uploadButtonModal.addEventListener('click', function () {
    if (!recordedBlob) {
      console.error('No recorded video to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('video_file', recordedBlob);
    formData.append('title', titleModal.value);
    formData.append('description', descriptionModal.value);
    formData.append('browserName', browserName);
    formData.append('browserVersion', browserVersion);
    formData.append('browserLayout', browserLayout);
    formData.append('operatingSystem', operatingSystem);

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
        if (data.status === 'success') {
          alert('File successfully uploaded!');
          window.location.reload(true);
          $('#videoModal').modal('hide');
        } else {
          alert('Error uploading File!');
          console.log('Error:', data.message);
        }
      })
      .catch(err => {
        console.log('Upload error:', err);
      });
  });

  startButton.addEventListener('click', startRecording);
  stopButton.onclick = () => stopRecording();
});
