import React, { useState } from 'react';
import axios from 'axios';
import '../styles/PostalCodeScreen.css';
import '../styles/Card.css';

import PostalCodeInput from '../components/PostalCodeInput';

const PostalCodeScreen: React.FC = () => {
    const [postalCode, setPostalCode] = useState<string>('');
    const [error, setError] = useState<string>(''); // error for incorrect postal code format
    const [validSubmission, setValidSubmission] = useState<boolean>(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        // submit without entering any text
        if (postalCode === '') {
            setError('I need a postal code to find you a deal comrade.');
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
            setLoading(true);

            const response = await axios.post('http://127.0.0.1:5000/process_postal_code', { postalCode });

            if (response.data.valid) {
                setValidSubmission(true);
                console.log('Postal code is valid:', postalCode);
                setError('');
            } else {
                setValidSubmission(false);
                setLoading(false)
                setError(response.data.error);
            };
        } catch (err: unknown) {
            setLoading(false);

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

                    {/* show error is error has a truthy value */}
                    <p className={`error-message ${error ? 'show' : ''}`}>{error}</p>
                </div>
            )}
        </div>
    );
};

export default PostalCodeScreen;