import React from 'react';
import { Grid, Typography, Button } from '@mui/material';
import styles from '../../styles/styles';

const ProductSummary = ({ cartItems, selectedCard, selectedAddress, onConfirm, onBack }) => {
    const calculateTotal = () => {
        return cartItems.reduce((acc, item) => {
            return acc + (item.seller_product.price + item.seller_product.shipping_costs) * item.quantity;
        }, 0);
    };

    return (
        <div>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Product Summary
            </Typography>
            <Grid container spacing={2}>
                {cartItems.map((item) => (
                    <Grid item xs={12} key={item.seller_product.id}>
                        <Typography variant="h6">{item.seller_product.name}</Typography>
                        <Typography>Quantity: {item.quantity}</Typography>
                        <Typography>Price: ${item.seller_product.price}</Typography>
                    </Grid>
                ))}
                <Grid item xs={12}>
                    <Typography variant="h6">Selected Card</Typography>
                    <Typography>{selectedCard}</Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="h6">Shipping Address</Typography>
                    <Typography>{selectedAddress}</Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="h6">Total: ${calculateTotal()}</Typography>
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                        onClick={onConfirm}
                    >
                        Confirm Buy
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                        onClick={onBack}
                    >
                        Back
                    </Button>
                </Grid>
            </Grid>
        </div>
    );
};

export default ProductSummary;
