document.addEventListener('DOMContentLoaded', function () {
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
  let recorder;
  let recordedBlob;

  startButton.addEventListener('click', function () {
    if (!navigator.mediaDevices) {
      console.error('getUserMedia not supported.');
      return;
    }

    // const constraints = { video: true, audio: true, };
    navigator.mediaDevices.getDisplayMedia(
      {
        video: true,
        audio: true

      })
      .then(function (stream) {
        const mime = MediaRecorder.isTypeSupported('video/webm; codecs=h264')
          ? 'video/webm; codecs=h264'
          : 'video/webm';

        recorder = new MediaRecorder(stream, {
          mimeType: mime
        });

        chunks = [];
        recorder.addEventListener('dataavailable', function (e) {
          chunks.push(e.data);
        });

        recorder.addEventListener('stop', function () {
          console.log('Recording stopped.');

          recordedBlob = new Blob(chunks, { type: 'video/webm' });
          recordedVideoModal.src = URL.createObjectURL(recordedBlob);

          // Open the Bootstrap Modal
          $('#videoModal').modal('show');
        });

        recorder.onstart = event => {
          console.log('Recording started.');
          startButton.disabled = true;
        };

        recorder.start();
      })
      .catch(function (err) {
        console.error('getUserMedia error:', err);
      });
  });

  stopButton.onclick = () => {
    if (recorder && recorder.state === 'recording') {
      recorder.stop();
      console.log('Recorder stopped manually.');
    }
  };

  uploadButtonModal.addEventListener('click', function () {
    if (!recordedBlob) {
      console.error('No recorded video to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('video_file', recordedBlob);
    formData.append('title', titleModal.value);
    formData.append('description', descriptionModal.value);

    console.log('Uploading...');
    console.log('Title:', titleModal.value);
    console.log('Description:', descriptionModal.value);
    console.log('Recorded Blob:', recordedBlob);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(resp => resp.json()) // Parse the JSON response
      .then(data => {
        console.log('Upload response:', data);
        if (data.status === 'success') {
          alert('File successfully uploaded!');
          window.location.reload(true);
          $('#videoModal').modal('hide');
        } else {
          alert('Error uploading File!');
          console.error('Error:', data.message);
        }
      })
      .catch(err => {
        console.error('Upload error:', err);
      });
  });
});
