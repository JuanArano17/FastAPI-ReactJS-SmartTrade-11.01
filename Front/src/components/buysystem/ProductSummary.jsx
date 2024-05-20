import React from 'react';
import { Grid, Typography, Button, Paper, Box } from '@mui/material';
import styles from '../../styles/styles';

const ProductSummary = ({ cartItems, selectedCard, selectedAddress, onConfirm, onBack }) => {
    const calculateTotal = () => {
        return cartItems.reduce((acc, item) => {
            return acc + (item.seller_product.price + item.seller_product.shipping_costs) * item.quantity;
        }, 0);
    };

    return (
        <Paper sx={styles.paperContainer}>
            <Typography variant="h4" sx={{ color: '#629C44', mb: 4, fontWeight: 'bold', textAlign: 'center' }}>
                Product Summary
            </Typography>
            <Grid container spacing={2}>
                {cartItems.map((item) => (
                    <Grid item xs={12} key={item.seller_product.id}>
                        <Paper elevation={1} sx={{ p: 2, mb: 2, borderRadius: '10px' }}>
                            <Grid container spacing={2}>
                                <Grid item xs={4}>
                                    <Box sx={{ width: 50, height: 50, backgroundColor: 'grey.300' }} />
                                </Grid>
                                <Grid item xs={8}>
                                    <Typography variant="h6">{item.seller_product.name}</Typography>
                                    <Typography variant="body2">Seller name and info</Typography>
                                    <Typography variant="body2">Quantity: {item.quantity}</Typography>
                                    <Typography variant="body2">Subtotal: ${item.seller_product.price * item.quantity}</Typography>
                                </Grid>
                            </Grid>
                        </Paper>
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
        </Paper>
    );
};

export default ProductSummary;
