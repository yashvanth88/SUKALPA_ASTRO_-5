import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import ErrorMessage from './ErrorMessage'; // Import the ErrorMessage component
import { serverUrl } from '../server-url';

export default function VerifyEmail() {
    const [verificationCode, setVerificationCode] = useState('');
    const [email, setEmail] = useState(''); // State for email input
    const [errorMessage, setErrorMessage] = useState('');
    const [verificationStatus, setVerificationStatus] = useState('');
    const navigate = useNavigate();

    const handleVerificationSubmit = async (e) => {
        e.preventDefault();

        try {
            // Send email and verification code to backend for validation
            const response = await axios.post('http://localhost:5174/api/verify-email', {
                email: email,
                code: verificationCode
            });

            if (response.status === 200) {
                setVerificationStatus('Verification successful!');
                navigate('/dashboard'); // Redirect to dashboard or another page upon successful verification
            } else {
                setErrorMessage('Verification failed. Please try again.');
            }
        } catch (error) {
            console.error(error);
            setErrorMessage('An error occurred. Please try again.');
        }
    };

    const handleCodeChange = (e) => {
        setVerificationCode(e.target.value);
    };

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    return (
        <div className="max-w-md mx-auto my-8">
            <h2 className="text-2xl font-semibold mb-4">Verify Email</h2>
            <form onSubmit={handleVerificationSubmit} className="space-y-4">
                <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={handleEmailChange}
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        placeholder="Enter your email"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="verificationCode" className="block text-sm font-medium text-gray-700">Verification Code</label>
                    <input
                        id="verificationCode"
                        type="text"
                        value={verificationCode}
                        onChange={handleCodeChange}
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        placeholder="Enter verification code"
                        required
                    />
                </div>
                <div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Verify
                    </button>
                </div>
                {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}
                {verificationStatus && <p className="text-green-500 text-sm">{verificationStatus}</p>}
            </form>
        </div>
    );
}
