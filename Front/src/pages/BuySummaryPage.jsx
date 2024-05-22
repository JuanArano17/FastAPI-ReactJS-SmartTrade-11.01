import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Button, Paper, Divider } from '@mui/material';
import { useLocation, useHistory } from 'react-router-dom';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import CartSummaryItem from '../components/products/shoppingcart/CartSummaryItem';
import styles from '../styles/styles';
import { getCartItems } from '../api/services/products/ShoppingCartService';

const BuySummaryPage = () => {
    const { state } = useLocation();
    const { selectedCard, selectedAddress } = state;
    const [cartItems, setCartItems] = useState([]);
    const history = useHistory();

    const fetchCartData = async () => {
        const cartData = await getCartItems();
        setCartItems(cartData);
    };

    useEffect(() => {
        fetchCartData();
    }, []);

    const calculateTotal = () => {
        const total = cartItems.reduce((acc, item) => {
            return acc + (item.seller_product.price + item.seller_product.shipping_costs) * item.quantity;
        }, 0);
        return total.toFixed(2);
    };

    const handleConfirmPurchase = () => {
        history.push('/review-product');
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Paper sx={styles.paperContainer}>
                    <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                        Product Summary
                    </Typography>
                    <Grid container spacing={2}>
                        {cartItems.map((item) => (
                            <Grid item xs={12} key={item.seller_product.id}>
                                <CartSummaryItem item={item} />
                            </Grid>
                        ))}
                        <Grid item xs={12}>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="h6">Selected card:{selectedCard}</Typography>
                            <Typography variant="h6" sx={{ mt: 2 }}>Shipping address: {selectedAddress}</Typography>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>Total bill: ${calculateTotal()}</Typography>
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                fullWidth
                                variant="contained"
                                color="primary"
                                sx={{ ...styles.greenRoundedButton, mt: 2 }}
                                onClick={handleConfirmPurchase}
                            >
                                Confirm Purchase
                            </Button>
                        </Grid>
                    </Grid>
                </Paper>
            </Container>
            <Footer />
        </Box>
    );
};

export default BuySummaryPage;
