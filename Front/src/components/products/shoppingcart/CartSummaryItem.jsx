import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const CartSummaryItem = ({ item }) => {
    const { seller_product: product } = item;

    const calculateSubtotal = () => {
        const subtotal = (product.price + product.shipping_costs) * item.quantity;
        return subtotal.toFixed(2);
    };

    return (
        <Card sx={{ display: 'flex', alignItems: 'center', mb: 2, p: 2 }}>
            <Box sx={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '20%' }}>
                    <img src={item.seller_product.images} alt="Product image" style={{ maxWidth: '100%', height: 'auto' }} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', width: '60%' }}>
                    <CardContent sx={{ flex: '1 0 auto' }}>
                        <Typography component="div" variant="h5">
                            {product.name}
                        </Typography>
                        <Typography variant="subtitle1" color="text.secondary" component="div">
                            {product.description || 'No description available'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" component="div">
                            Seller: {product.seller?.name || 'Unknown seller'}
                        </Typography>
                    </CardContent>
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', justifyContent: 'space-between', width: '20%' }}>
                    <Typography variant="body2" color="text.secondary" component="div">
                        Quantity: {item.quantity}
                    </Typography>
                    <Typography variant="subtitle1" component="div">
                        Subtotal: ${calculateSubtotal()}
                    </Typography>
                </Box>
            </Box>
        </Card>
    );
};

export default CartSummaryItem;
