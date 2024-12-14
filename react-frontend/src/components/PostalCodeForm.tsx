import React, { useState, useEffect } from 'react';
import axios from 'axios';

import PostalCodeInput from './PostalCodeInput.tsx';
import '../styles/PostalCodeForm.css';
import '../styles/Card.css';

interface PostalCodeFormProps {
    onValidSubmission: (validSubmission: boolean) => void;
};

const PostalCodeForm: React.FC<PostalCodeFormProps> = ({ onValidSubmission }) => {
    const [postalCode, setPostalCode] = useState<string>('');
    const [validSubmission, setValidSubmission] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        onValidSubmission(validSubmission)
    }, [validSubmission]);


    const handleSubmit = async () => {

        // submit without entering any text
        if (postalCode === '') {
            setError('I need a postal code to find you a deal, comrade.');
            return;
        };

        // check postal code format
        const regex = /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/;

        if (!regex.test(postalCode)) {
            setError('Invalid postal code. Format must be A1A 1A1.');
            setPostalCode(''); // clear input
            return;
        };

        try {
            setLoading(true); // show the spinner 

            const response = await axios.post('http://127.0.0.1:5000/process_postal_code', { postalCode });

            if (response.data.valid) {
                console.log('Postal code is valid:', postalCode);
                setError('');
                setValidSubmission(true)
            } else {
                setLoading(false)
                setError(response.data.error);
                setValidSubmission(false)
            };
        } catch (err: unknown) {
            setLoading(false);
            setValidSubmission(false)

            console.error('Error: ', err);

            if (err instanceof Error) {
                setError(err.message || 'An unexpected error occurred.');
            } else {
                setError('An unexpected error occurred.');
            };
        };
        
    };


    return (
        <div className='container'>
            {loading ? (
                <div>
                    {validSubmission ? (
                        <div className="success-message">
                            <h2>Postal Code Accepted! 🎉</h2>
                        </div>
                    ) : ( <div className='spinner'></div> )} 
                </div>
            ) : (
                <div className='card'>
                    <h1>Enter your postal code :)</h1>
                    <PostalCodeInput
                        postalCode={postalCode}
                        setPostalCode={setPostalCode}
                        setError={setError}
                        handleSubmit={handleSubmit}
                    />

                    <button onClick={handleSubmit} disabled={loading}>🍕</button>

                    {/* show error if error has a truthy value */}
                    <p className={`error-message ${error ? 'show' : ''}`}>{error}</p>
                </div>
            )}
        </div>
    );
};

export default PostalCodeForm;