import React from 'react';

interface PostalCodeInputProps {
    postalCode: string;
    setPostalCode: React.Dispatch<React.SetStateAction<string>>;
    setError: React.Dispatch<React.SetStateAction<string>>;
    handleSubmit: () => void; 
};


const PostalCodeInput: React.FC<PostalCodeInputProps> = ({ postalCode, setPostalCode, setError, handleSubmit }) => {
    
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPostalCode(e.target.value);
        setError('');
        console.log(`Postal Code updated: ${postalCode}`);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') { 
            handleSubmit(); 
        };
        
        if (postalCode.length === 7) {
            setError('Max character limit reached.');
            setTimeout(() => setError(''), 1750);  // clear error after a second
        };
    };
    

    return (
        <input
            type='text'
            value={postalCode}
            maxLength={7}
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
        />
    );
};

export default PostalCodeInput;