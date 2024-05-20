import React from 'react';
import { Grid, Typography, Button } from '@mui/material';
import styles from '../../styles/styles';
import CartTotal from '../products/shoppingcart/CartTotal';
import CartItem from '../products/shoppingcart/CartItem';

const CartSummary = ({ cartItems, onContinue }) => {
    const calculateTotal = () => {
        return cartItems.reduce((acc, item) => {
            return acc + (item.seller_product.price + item.seller_product.shipping_costs) * item.quantity;
        }, 0);
    };

    return (
        <div>
            <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                Shopping Cart
            </Typography>
            <Grid container spacing={2}>
                {cartItems.map((item) => (
                    <CartItem key={item.seller_product.id} item={item} quantity={item.quantity} size={item.size} />
                ))}
                <Grid item xs={12}>
                    <CartTotal total={calculateTotal()} />
                </Grid>
                <Grid item xs={12}>
                    <Button
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{ ...styles.greenRoundedButton, mt: 2 }}
                        onClick={onContinue}
                    >
                        Continue
                    </Button>
                </Grid>
            </Grid>
        </div>
    );
};

export default CartSummary;
