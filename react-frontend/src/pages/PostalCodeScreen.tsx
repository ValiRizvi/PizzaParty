import React, { useState } from 'react';
import '../styles/PostalCodeScreen.css';

const PostalCodeScreen: React.FC = () => {
    const [postalCode, setPostalCode] = useState<string>('');
    const [error, setError] = useState<string>(''); // error for incorrect postal code format
    const [validSubmission, setValidSubmission] = useState<boolean>(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPostalCode(e.target.value);
        setError(''); // error message disappears when typing
        console.log("Postal Code updated:", e.target.value);
    };

    const handleSubmit = () => {
        // check postal code format
        const regex = /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/;

        if (!regex.test(postalCode)) {
            setError('Invalid postal code. Format must be A1A 1A1.');
            setPostalCode(''); // clear input
            return;
        }

        console.log('Postal code is valid:', postalCode);
        setError(''); 
        setValidSubmission(true);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') { handleSubmit() };
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
                    <input 
                        type='text' 
                        placeholder='Postal Code' 
                        value={postalCode} 
                        maxLength={7}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyPress} // listen for enter key press
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