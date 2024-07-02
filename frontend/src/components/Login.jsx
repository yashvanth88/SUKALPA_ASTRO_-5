import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import CryptoJS from 'crypto-js';
import WebcamCapture from './WebcamCapture'; // Import your WebcamCapture component
import { secretKey } from './secret-key';
import ErrorMessage from './ErrorMessage'; // Import the ErrorMessage component
import { serverUrl } from '../server-url';

export default function Login() {
    const [loginState, setLoginState] = useState({ email: '', password: '' });
    const [imageData, setImageData] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setLoginState({ ...loginState, [e.target.id]: e.target.value });
    };

    const handleCapture = (imageSrc) => {
        setImageData(imageSrc);
    };

    const handleLogin = async (e) => {
        e.preventDefault();

        // Encrypt the password before sending it to the backend
        const encryptedPassword = CryptoJS.AES.encrypt(loginState.password, secretKey, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }).toString();

        try {
            console.log(encryptedPassword);
            const response = await axios.post(serverUrl+"/signin", {
                username: loginState.email,
                password: encryptedPassword,
                image: imageData // Send captured image data for facial recognition
            });

            if (response.status === 200 && response.data.status === "pass") {
                console.log(response.data.message);
                navigate('/dashboard');
            } else {
                setErrorMessage(response.data.message);
            }
        } catch (error) {
            console.error(error);
            setErrorMessage(error.response?.data?.message || 'An error occurred. Please try again.');
        }
    };

    const handleTryAnotherWay = async () => {
        try {
            const response = await axios.post(serverUrl+"/verifyEmail",{
                username: loginState.email,
                type:"send-otp"
            });

            if (response.status === 200) {
                navigate('/verify-email');
            } else {
                setErrorMessage('Unable to send verification email. Please try again.');
            }
        } catch (error) {
            console.error(error);
            setErrorMessage(error.response?.data?.message || 'An error occurred. Please try again.');
        }
    };

    return (
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
            <div className="space-y-4">
                {errorMessage && <ErrorMessage message={errorMessage} />} {/* Display error message */}
                <div>
                    <label htmlFor="email" className="sr-only">Email address</label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        required
                        onChange={handleChange}
                        value={loginState.email}
                        className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                        placeholder="Email address"
                    />
                </div>
                <div>
                    <label htmlFor="password" className="sr-only">Password</label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        autoComplete="current-password"
                        required
                        onChange={handleChange}
                        value={loginState.password}
                        className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                        placeholder="Password"
                    />
                </div>
                <WebcamCapture onCapture={handleCapture} /> {/* Component for webcam capture */}
            </div>
            <div className="text-sm mt-4">
                <button
                    type="button"
                    onClick={handleTryAnotherWay}
                    className="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    Try Another Way (Verify via Email)
                </button>
            </div>
            <div className="mt-6">
                <button
                    type="submit"
                    className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                    Sign in
                </button>
            </div>
        </form>
    );
}
