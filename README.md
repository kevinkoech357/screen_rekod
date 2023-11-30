
Screenrekod is a web application that allows users to record their screens, capture audio, and securely upload and share their recordings. It's designed to be user-friendly, privacy-conscious, and flexible. Whether you're an educator, content creator, or someone who needs to share screen recordings, Screenrekod has you covered.

## Features
* Screen Recording: Record your screen activities with ease, whether it's for tutorials, presentations, or gaming.

* Audio Capture: Simultaneously capture audio to provide narration or commentary for your recordings.

* Upload and Share: Upload your recordings to the secure server and share them with others via unique links.

* User-Private Video Management: Manage your uploaded videos with privacy and access control. You can only see what you've uploaded.

* Subtitle Generation: Optionally generate subtitles for your videos to make them more accessible to a wider audience.

## Technologies Used
* Programming Languages: Python (server-side), HTML/CSS (frontend), JavaScript (screen capture).

* Web Framework: Flask for handling HTTP requests and user authentication.

* Multimedia Processing: Python-ffmpeg for audio generation and Openai-whisper for transcription.

* Subtitles:

* Task Scheduling: Celery for managing background tasks.

* Message Broker: Redis for efficient task queuing.

## Getting Started
* Clone the repository to your local machine.
* Set up a virtual environment for the project.
* Install the required dependencies using pip install -r requirements.txt.
* Configure your database settings and other environment variables.
* Run the application using python run.py.

## Usage
* Sign up for an account or log in if you're an existing user.
* Start recording your screen and capturing audio using the on-screen controls.
* Once your recording is complete, choose to save and upload it.
* Manage your uploaded videos and set access controls as needed.
* Optionally generate subtitles and translate them into different languages for viewers.
* Share your video links with others.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
We welcome contributions from the open-source community. Please see our Contribution Guidelines for more information.

## Contact
For questions or support, contact the project owner, kevinkoech@proton.me.

## Acknowledgments
I'd like to acknowledge the open-source community and the developers of the libraries and tools that made this project possible.
