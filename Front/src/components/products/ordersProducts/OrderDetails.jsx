import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import styles from '../../../styles/styles';

const OrderDetails = ({ order }) => {
    return (
        <Paper sx={styles.paperContainer}>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Order Details
            </Typography>
            <Grid container spacing={2}>
                {order.product_lines.map((item, index) => (
                    <Grid item xs={12} key={index}>
                        <Typography variant="body1">Product name: {item.name}</Typography>
                        <Typography variant="body1">Quantity: {item.quantity}</Typography>
                        <Typography variant="body1">Subtotal: ${item.subtotal}</Typography>
                    </Grid>
                ))}
            </Grid>
        </Paper>
    );
};

export default OrderDetails;
