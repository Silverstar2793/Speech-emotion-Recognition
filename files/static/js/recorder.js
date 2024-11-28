let mediaRecorder;
let audioChunks = [];

// Start recording
function startRecording() {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                sendAudioData(audioBlob);
            };

            mediaRecorder.start();
            document.getElementById('start-recording').disabled = true;
            document.getElementById('stop-recording').disabled = false;
            console.log("Recording started...");
        })
        .catch(error => {
            console.error("Error starting the recording:", error);
        });
}

// Stop recording
function stopRecording() {
    mediaRecorder.stop();
    document.getElementById('start-recording').disabled = false;
    document.getElementById('stop-recording').disabled = true;
    console.log("Recording stopped...");
}

// Send the recorded audio to the server for prediction
function sendAudioData(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');

    fetch('/audio', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const emotion = data.emotion || "Unknown";
        document.getElementById('emotion-result').innerText = `Predicted Emotion: ${emotion}`;
    })
    .catch(error => {
        console.error('Error sending audio:', error);
    });
}
