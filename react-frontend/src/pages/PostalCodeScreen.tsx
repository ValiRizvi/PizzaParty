import React, { useState } from 'react';
import axios from 'axios';
import '../styles/PostalCodeScreen.css';

import PostalCodeInput from '../components/PostalCodeInput';

const PostalCodeScreen: React.FC = () => {
    const [postalCode, setPostalCode] = useState<string>('');
    const [error, setError] = useState<string>(''); // error for incorrect postal code format
    const [validSubmission, setValidSubmission] = useState<boolean>(false);

    const handleSubmit = async () => {
        // check postal code format
        const regex = /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/;

        if (!regex.test(postalCode)) {
            setError('Invalid postal code. Format must be A1A 1A1.');
            setPostalCode(''); // clear input
            return;
        };

        try {
            const response = await axios.post('http://127.0.0.1:5000/validate_postal_code', { postalCode });

            if (response.data.valid) {
                setValidSubmission(true);
                console.log('Postal code is valid:', postalCode);
                setError('');
            } else {
                setValidSubmission(false);
                setError(response.data.error);
            };
        } catch (err: unknown) {
            console.error('Error: ', err);
            setValidSubmission(false);

            if (err instanceof Error) {
                setError(err.message || 'An unexpected error occurred.');
            } else {
                setError('An unexpected error occurred.');
            };
        };
    };

    return (
        <div className='container'>
            {validSubmission ? (
                <div className="success-message">
                    <h2>Postal Code Accepted! 🎉</h2>
                    <p>more to come.</p>
                </div>
            ) : (
                <>
                    <h1>Enter your postal code :)</h1>
                    <PostalCodeInput
                        postalCode={postalCode}
                        setPostalCode={setPostalCode}
                        setError={setError}
                        handleSubmit={handleSubmit}
                    />

                    <button onClick={handleSubmit}>Submit</button>

                    {/* if error state is truthy make error message visible*/}
                    <p className={`error-message ${error ? 'show' : ''}`}>{error}</p>
                </>
            )}
        </div>
    );
};

export default PostalCodeScreen;