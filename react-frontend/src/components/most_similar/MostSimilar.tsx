import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, Button, Paper } from '@mui/material';

import MostSimilarTextBox from './MostSimilarTextField';

interface MostSimilarProps {
    local_stores: any;
    allCoupons: any;
};

interface MostSimilarCoupon {
    chain: string;
    store_id: string;
    code: string;
    price: string;
    description: string;
    similarity: number;
};

const MostSimilar: React.FC<MostSimilarProps> = ({ local_stores, allCoupons }) => {

    const [mostSimilar, setMostSimilar] = useState<MostSimilarCoupon | null>(null);
    const [userInput, setUserInput] = useState<string>('');
    const [error, setError] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    
    const handleUserInput = async () => {

        if (!userInput.trim()) {
            setError('Please enter a description.');
            setTimeout(() => setError(''), 5000);
            return;
        }

        try {
            setLoading(true)
            setError('');
            setMostSimilar(null);  // clear previous result 

            const response = await axios.post('http://127.0.0.1:5000/most_similar', { 
                                                                                        local_stores, 
                                                                                        allCoupons,
                                                                                        userInput  
                                                                                    });

            if (response.data && response.data.mostSimilar) {
                setMostSimilar(response.data.mostSimilar);
            } else {
                throw new Error ('Unexpected response from server. Please try again later.');
            }

        } catch (err: unknown) {
            console.error('Error fetching most similar coupon:', err);
            setError(`Error: ${err}`);
        } finally {
            setLoading(false);
        }

    }

    return (
        <Container sx={{ maxWidth: 'md', marginTop: '20px' }}>
            <Typography variant="h4" gutterBottom color='white'>
                Most Similar Coupon
            </Typography>
           
            <MostSimilarTextBox userInput={userInput} setUserInput={setUserInput}/>

            <Button
                onClick={handleUserInput}
                disabled={loading}
                sx={{
                    backgroundColor: loading ? '#ddd' : '#007bff',
                    color: '#fff',
                    padding: '10px 15px',
                    fontSize: '14px',
                    borderRadius: '5px',
                    border: 'none',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    '&:hover': {
                        backgroundColor: '#0056b3',
                    },
                }}
            >
                {loading ? 'Searching...' : 'Find Coupon'}
            </Button>

            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

            {mostSimilar && (
                <Paper
                    sx={{
                        marginTop: '20px',
                        padding: '20px',
                        borderRadius: 2,
                        boxShadow: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        bgcolor: 'rgb(64, 68, 80)'
                    }}
                >
                    <Typography variant="h6" gutterBottom sx={{ color: 'white' }}>
                        Best Match
                    </Typography>
                    
                    <Typography variant="body1" sx={{ color: 'white' }}>
                        <strong>Chain:</strong> {mostSimilar.chain}
                        <br />
                        <strong>Store ID:</strong> {mostSimilar.store_id}
                        <br />
                        <strong>Coupon Code:</strong> {mostSimilar.code}
                        <br />
                        {mostSimilar.price && (
                            <>
                                <strong>Price:</strong> {mostSimilar.price}
                            </>
                        )}
                        <br />
                        <strong>Description:</strong> {mostSimilar.description}
                        <br />
                        <br />
                        <strong>Similarity Score:</strong> {mostSimilar.similarity.toFixed(2)}
                    </Typography>
                </Paper>
            )}
        </Container>

    );
};

export default MostSimilar;