import React from 'react';
import { TextField } from '@mui/material';

interface MostSimilarTextFieldProps {
    userInput: string;
    setUserInput: React.Dispatch<React.SetStateAction<string>>;
};

const MostSimilarTextBox: React.FC<MostSimilarTextFieldProps> = ({ userInput, setUserInput }) => {

    return (
        <TextField
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder=' Find me a coupon for ... '
            multiline
            rows={4}
            variant='outlined'
            fullWidth
            sx={{
                marginBottom: '10px',
                bgcolor: 'rgb(64, 68, 80)', 
                borderRadius: 4, 
                '& .MuiOutlinedInput-root': {
                borderRadius: 4, 
                '& fieldset': {
                    borderWidth: '3px', 
                    borderColor: 'rgb(128, 228, 211)', 
                },
                '&:hover fieldset': {
                    borderColor: 'rgb(129, 212, 250)', 
                },
                '&.Mui-focused fieldset': {
                    borderColor: 'rgb(3, 169, 244)', 
                    borderWidth: '3px', 
                },
                },
            }}
        />
    )
};

export default MostSimilarTextBox;