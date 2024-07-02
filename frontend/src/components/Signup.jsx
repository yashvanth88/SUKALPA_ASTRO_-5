import React, { useState } from 'react';
import { signupFields } from "../constants/formFields";
import FormAction from "./FormAction";
import Input from "./Input";
import WebcamCapture from "./WebcamCapture"; 
import axios from "axios";
import { useNavigate } from "react-router-dom";
import CryptoJS from 'crypto-js';
import { secretKey } from './secret-key';
import { serverUrl } from '../server-url';

const fields = signupFields;
let fieldsState = {};
fields.forEach(field => fieldsState[field.id] = '');

const Signup = () => {
    const navigate = useNavigate();
    const [signupState, setSignupState] = useState(fieldsState);
    const [imageData, setImageData] = useState(null); 
    const [errorMessage, setErrorMessage] = useState('');

    const handleChange = (e) => {
        setSignupState({ ...signupState, [e.target.id]: e.target.value });
    };

    const handleCapture = (imageSrc) => {
        setImageData(imageSrc);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Encrypt the password before sending it to the backend

        const encryptedPassword = CryptoJS.AES.encrypt(signupState.password, secretKey, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }).toString();

        try {
            console.log(encryptedPassword)
            const response = await axios.post(serverUrl+"/signup", {
                username: signupState['email-address'],
                firstName: signupState.firstname,
                lastName: signupState.lastname,
                password: encryptedPassword,
                image: imageData
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.status >= 200 && response.status < 300) {
                localStorage.setItem("token", response.data.token);
                navigate('/dashboard');
            } else {
                setErrorMessage(response.data.message); // Display the error message from the backend
            }
        } catch (error) {
            console.error(error);
            setErrorMessage('An error occurred. Please try again. ' + error.message); // Display the error message received
        }
    };

    return (
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="">
                {fields.map(field => (
                    <Input
                        key={field.id}
                        handleChange={handleChange}
                        value={signupState[field.id]}
                        labelText={field.labelText}
                        labelFor={field.labelFor}
                        id={field.id}
                        name={field.name}
                        type={field.type}
                        isRequired={field.isRequired}
                        placeholder={field.placeholder}
                    />
                ))}
                <WebcamCapture onCapture={handleCapture} /> {/* Include WebcamCapture component */}
                <FormAction handleSubmit={handleSubmit} text="Signup" />
                {errorMessage && <p>{errorMessage}</p>}
            </div>
        </form>
    );
};

export default Signup;
