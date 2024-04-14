import React, { useState } from 'react';
import { Box, Container, Typography, Grid, Button } from '@mui/material';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import CartItem from '../components/shoppingcart/CartItem';
import CartTotal from '../components/shoppingcart/CartTotal';
import styles from '../styles/styles';
import imageplaceholder from '../images/img_mundo.png'

const ShoppingCartPage = () => {
    const [cartItems, setCartItems] = useState([
        { id: 1, name: 'Product 1', price: 255, quantity: 1, imageUrl: imageplaceholder },
        { id: 2, name: 'Product 2', price: 255, quantity: 1, imageUrl: imageplaceholder },
        { id: 3, name: 'Product 3', price: 290, quantity: 1, imageUrl: imageplaceholder },
        // ... más productos
    ]);

    const calculateTotal = () => cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);

    // Función para eliminar un item del carrito
    const handleRemoveItem = (itemId) => {
        setCartItems(cartItems.filter(item => item.id !== itemId));
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showLogoutButton={true} />
            <Container component="main" maxWidth="md" sx={styles.mainContainer}>
                <Typography variant="h4" sx={{ my: 2 }}>
                    Shopping Cart
                </Typography>
                <Grid container spacing={2}>
                    {cartItems.map((item) => (
                        <CartItem key={item.id} item={item} setCartItems={setCartItems} onRemove={handleRemoveItem} />
                    ))}
                    <Grid item xs={12}>
                        <CartTotal total={calculateTotal()} />
                    </Grid>
                    <Grid item xs={12}>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <Button variant="contained" sx={{...styles.greenRoundedButton, width:'auto'}}>
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
