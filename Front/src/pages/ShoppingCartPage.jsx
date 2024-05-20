import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Button } from '@mui/material';
import { useHistory } from 'react-router-dom';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import CartItem from '../components/products/shoppingcart/CartItem';
import CartTotal from '../components/products/shoppingcart/CartTotal';
import styles from '../styles/styles';
import { getCartItems } from '../api/services/products/ShoppingCartService';

const ShoppingCartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const history = useHistory();
    const fetchCartData = async () => {
        try {
            const cartItems = await getCartItems();
            console.log("Items recibidos del backend:", cartItems);
            cartItems.sort((a, b) => a.seller_product.id - b.seller_product.id);
            setCartItems(cartItems);
        } catch (error) {
            console.error('Error al cargar los datos del carrito:', error);
        }
    };
    useEffect(() => {
        fetchCartData();
    }, []);

    const handleContinue = () => {
        history.push('/buying-process');
    };

    const calculateTotal = () => {
        return cartItems.reduce((acc, item) => {
            return acc + (item.seller_product.price + item.seller_product.shipping_costs) * item.quantity;
        }, 0);
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{ color: '#629C44', my: 2, fontWeight: 'bold' }}>
                    Shopping Cart
                </Typography>
                <Grid container spacing={2}>
                    {cartItems.map((item) => (
                        <CartItem key={item.seller_product.id} item={item} quantity={item.quantity} size={item.size} setCartItems={fetchCartData} />
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
                            onClick={handleContinue}
                        >
                            Continue
                        </Button>
                    </Grid>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};
export default ShoppingCartPage;