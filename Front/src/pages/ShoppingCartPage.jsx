import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Button } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import CartItem from '../components/products/shoppingcart/CartItem';
import CartTotal from '../components/products/shoppingcart/CartTotal';
import styles from '../styles/styles';
import { getCartItems } from '../api/services/user/ShoppingCartService';

const ShoppingCartPage = () => {
    const [cartItems, setCartItems] = useState([]); 

    useEffect(() => {
        const fetchCartItems = async () => {
            try {
                const items = await getCartItems();
                console.log("Items recibidos del backend:", items);
                setCartItems(items);
            } catch (error) {
                console.error('Error al cargar los datos del carrito:', error);
            }
        };

        fetchCartItems();
    }, []);



    const calculateTotal = () => cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);

    

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{ my: 2 }}>
                    Shopping Cart
                </Typography>
                <Grid container spacing={2}>
                    {cartItems.map((item) => (
                        <CartItem key={item.id} item={item} setCartItems={setCartItems} />
                    ))}
                    <Grid item xs={12}>
                        <CartTotal total={calculateTotal()} />
                    </Grid>
                    <Grid item xs={12}>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <Button variant="contained" sx={{ ...styles.greenRoundedButton, width: 'auto' }}>
                                Continue
                            </Button>
                        </Box>
                    </Grid>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default ShoppingCartPage;
