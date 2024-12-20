import React from 'react'; 
import { BestDeal } from './BestValueButton';
import { Paper, Typography } from '@mui/material';

interface BestDealDisplayProps {
    coupon: BestDeal | null;
};


const BestDealDisplay: React.FC<BestDealDisplayProps> = ({ coupon }) => {
    
    if(!coupon) {
        return <p style={{ color: 'red', marginTop: '10px' }}>Something went wrong.. I have no deal for you :(</p>
    }

    return (
        <Paper
            sx={{
                padding: '20px',
                marginTop: '20px',
                borderRadius: 2,
                boxShadow: 4,
                display: 'flex',
                flexDirection: 'column',
                bgcolor: 'rgb(64, 68, 80)',
                border: '2px solid rgb(128, 228, 211)' 
            }}
        >
            <Typography variant="h6" gutterBottom sx={{ color: 'white' }}>
                Best Value Coupon:
            </Typography>

            <Typography variant="body1" sx={{ color: 'white' }}>
                <strong>Store:</strong> {coupon.chain}
                <br />
                <strong>Price:</strong> ${coupon.coupon.price}
                <br />
                <strong>Code:</strong> {coupon.coupon.code}
                <br />
                <br />
                <strong>Description:</strong> {coupon.coupon.description}
                <br />
                <br />
                <strong>Value:</strong> {coupon.value.toFixed(2)} square inches per dollar.
                
            </Typography>
        </Paper>
    );
};

export default BestDealDisplay;