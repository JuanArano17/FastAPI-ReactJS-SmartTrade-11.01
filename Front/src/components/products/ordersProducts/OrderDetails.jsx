import React from 'react';
import { Box, Typography, Grid, Paper, Stepper, Step, StepLabel, Divider } from '@mui/material';
import styles from '../../../styles/styles';

const OrderDetails = ({ order }) => {
    const steps = ['CONFIRMED', 'SHIPPED', 'DELIVERED'];

    const getActiveStep = (state) => {
        switch (state) {
            case 'CONFIRMED':
                return 0;
            case 'SHIPPED':
                return 1;
            case 'DELIVERED':
                return 2;
            default:
                return 0;
        }
    };

    return (
        <Paper sx={{ ...styles.paperContainer, width: '600px' }}>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Order Details
            </Typography>
            <Stepper activeStep={getActiveStep(order.state)} alternativeLabel>
                {steps.map((label) => (
                    <Step key={label}>
                        <StepLabel>{label}</StepLabel>
                    </Step>
                ))}
            </Stepper>
            <Box sx={{ mt: 4 }}>
                <Typography variant="h6" sx={{ color: '#629C44', mb: 2 }}>
                    Order ID: {order.id}
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                    Order Date: {new Date(order.order_date).toLocaleDateString()}
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                    Total: ${order.total}
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                    Estimated Arrival: {order.estimated_date ? new Date(order.estimated_date).toLocaleDateString() : 'Pending'}
                </Typography>
                <Grid container spacing={2}>
                    {order.product_lines.map((item, index) => (
                        <Grid item xs={12} key={index}>
                            <Paper sx={{ p: 2, mb: 2 }}>
                                <Typography variant="body1">Product name: {item.name}</Typography>
                                <Typography variant="body1">Quantity: {item.quantity}</Typography>
                                <Typography variant="body1">Subtotal: ${item.subtotal}</Typography>
                                <Typography variant="body2" color="textSecondary">{item.description}</Typography>
                            </Paper>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Paper>
    );
};

export default OrderDetails;