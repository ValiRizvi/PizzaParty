import React, { useState } from 'react';
import axios from 'axios';

import PostalCodeInput from './PostalCodeInput';
import '../../styles/PostalCodeForm.css';
import '../../styles/Card.css';
import { Typography } from '@mui/material';

interface PostalCodeFormProps {
    onValidSubmission: (valid: boolean, localStores?: any, allCoupons?: any) => void;
};


const PostalCodeForm: React.FC<PostalCodeFormProps> = ({ onValidSubmission }) => {
    const [postalCode, setPostalCode] = useState<string>('');
    const [error, setError] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async () => {

        // submit without entering any text
        if (!postalCode.trim()) {
            setError('I need a postal code to find you a deal, comrade.');
            setPostalCode(''); // clear input
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
                onValidSubmission(true, response.data.local_stores, response.data.allCoupons)

            } else {

                setError(response.data.error);
                onValidSubmission(false);

            };
            
        } catch (err: unknown) {
            
            onValidSubmission(false);

            console.error('Error: ', err);

            if (err instanceof Error) {
                setError(err.message || 'An unexpected error occurred.');
            } else {
                setError('An unexpected error occurred.');
            };

        } finally {
            setLoading(false);
        };
        
    };


    return (
        <div className='container'>
            {loading ? (
                
                <div className='spinner'></div>  
                
            ) : (
                <div className='card'>
                    <Typography variant='h1'>
                        Enter your postal code:
                    </Typography>
                    <Typography>
                        let's find you a deal :)
                    </Typography>
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