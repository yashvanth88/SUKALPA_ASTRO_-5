// WebcamCapture.jsx
import React, { useState } from 'react';
import Webcam from "react-webcam";

const WebcamCapture = ({ onCapture }) => {
    const webcamRef = React.useRef(null);

    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        onCapture(imageSrc);
    }, [webcamRef, onCapture]);

    return (
        <div>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
            />
            <button onClick={capture}>Capture</button>
        </div>
    );
};

export default WebcamCapture;