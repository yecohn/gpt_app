import { useState, useRef, useEffect } from "react";
const mimeType = "audio/webm";

const AudioRecorder = (props) => {
    const [permission, setPermission] = useState(false);
    const mediaRecorder = useRef(null);
    const [recordingStatus, setRecordingStatus] = useState("inactive");
    const [stream, setStream] = useState(null);
    const [audioChunks, setAudioChunks] = useState([]);

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const streamData = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false,
                });
                setPermission(true);
                setStream(streamData);
            } catch (err) {
                alert(err.message);
            }
        } else {
            alert("The MediaRecorder API is not supported in your browser.");
        }
    };

    const sendAudioToBackend = (fd) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Accept': 'application/json' },
            body: fd
        };
        fetch('http://localhost:8000/chat', requestOptions
            // Add parameters here
        ).then((response) => {
            return response.json()
        }).then((data) => {
            console.log(data.transcript);
            console.log(data.answer);
            props.setGpt(data.answer);
            props.setUser(data.transcript);
        }).catch((error) => {
            console.log(error);
        });
        console.log("Audio sent to backend")
    };




    const startRecording = async () => {
        setRecordingStatus("recording");
        //create new Media recorder instance using the stream
        const media = new MediaRecorder(stream, { type: mimeType });
        //set the MediaRecorder instance to the mediaRecorder ref
        mediaRecorder.current = media;
        //invokes the start method to start the recording process
        mediaRecorder.current.start();
        let localAudioChunks = [];
        mediaRecorder.current.ondataavailable = (event) => {
            if (typeof event.data === "undefined") return;
            if (event.data.size === 0) return;
            localAudioChunks.push(event.data);
        };
        setAudioChunks(localAudioChunks);
    };
    const stopRecording = () => {
        setRecordingStatus("inactive");
        //stops the recording instance
        mediaRecorder.current.stop();
        mediaRecorder.current.onstop = () => {
            //creates a blob file from the audiochunks data
            const audioBlob = new Blob(audioChunks, { type: mimeType });
            //creates a playable URL from the blob file.
            const audioUrl = URL.createObjectURL(audioBlob);
            setAudioChunks([]);
            var fd = new FormData();
            fd.append('audio', audioBlob);
            console.log(fd.getAll('audio'))
            sendAudioToBackend(fd);
        };
    };

    return (
        <div className="text-blue-500  font-cursive flex justify-center hover:font-bold">
            {!permission ? (
                <button className="bg-sky-500 text-white rounded p-2" onClick={getMicrophonePermission} type="button">
                    Start Chat
                </button>
            ) : null}
            {permission && recordingStatus === "inactive" ? (
                <button className="bg-sky-500 text-white rounded p-2" onClick={startRecording} type="button">
                    Start Recording
                </button>
            ) : null}
            {recordingStatus === "recording" ? (
                <button className="bg-sky-500 text-white rounded p-2" onClick={stopRecording} type="button">
                    Stop Recording
                </button>
            ) : null}
        </div>
    );
};

export default AudioRecorder;