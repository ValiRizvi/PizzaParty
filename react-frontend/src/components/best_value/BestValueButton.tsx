import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Container, Typography } from '@mui/material';

import BestDealDisplay from './BestValueDisplay';

interface BestValueButtonProps {
    local_stores: any;
    allCoupons: any;
};

export interface BestDeal {
    chain: string;
    code: string;
    value: number;
    store_id: string;
    coupon: {
        price: string;
        description: string;
        code: string;
    };
};


const BestValueButton: React.FC<BestValueButtonProps> = ({ local_stores, allCoupons }) => {

    const [bestDeal, setBestDeal] = useState<BestDeal | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        console.log(bestDeal);
    }, [bestDeal]);

    const getBestDeal = async () => {

        setLoading(true);
        setError('');

        try {
            const response = await axios.post('http://127.0.0.1:5000/best_value', { local_stores, allCoupons});

            if (response.data && response.data.coupon) {
                setBestDeal(response.data.coupon);
            } else {
                throw new Error('Unexpected response from server. Please try again later.');
            }
                      
        } catch (err: unknown) {
            console.error('Error fetching best deal:', err);
            setError(`Error: ${err}`);
        } finally {
            setLoading(false);
        }
    }

    return (
        <Container>
            <Typography variant='h4' sx={{ color: 'white'}}>
                Best Value
            </Typography>
            <Button onClick={getBestDeal} 
                    disabled={loading} 
                    variant='contained' 
                    sx={{
                        bgcolor: 'rgb(128, 228, 211)', 
                        '&:hover': {
                            bgcolor: 'rgb(102, 198, 183)', 
                        },
                    }}>

                {loading ? 'Loading...' : 'Find Best Deal'}
            </Button>

            {bestDeal && <BestDealDisplay coupon={bestDeal}/>}
            
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </Container>
    );
};

export default BestValueButton;